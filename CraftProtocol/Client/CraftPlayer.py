#!/usr/bin/env python

import Queue
import errno
import json
import socket
import threading
import time
import traceback
from cStringIO import StringIO

import Event
from ..ChatMode import ChatMode
from ..ChatSerializer import ChatSerializer
from ..Hand import Hand
from ..Inventory import Inventory
from ..ClientStatus import ClientStatus
from ..Packet import *
from ..StreamIO import StreamIO
from ..VersionConstants import VersionConstants


class CraftPlayerReaderThread(threading.Thread):

    def __init__(self, player):
        threading.Thread.__init__(self)
        self._player = player
        self._stopped = False

    def stop(self):
        self._stopped = True

    def run(self):
        while not self._stopped:
            try:
                packet = self._player._serializer.read(self._player._sock)
            except socket.timeout:
                self._player.disconnect("Timed out")
            except socket.error as ex:
                if ex.errno == errno.EINTR:
                    continue
                raise
            except EOFError:
                self._player.disconnect("Connection closed by remote host")

            self._player.fire(Event.PacketInEvent(self._player, packet))


class CraftPlayerWriterThread(threading.Thread):

    def __init__(self, player):
        threading.Thread.__init__(self)
        self._player = player
        self._queue = Queue.Queue()
        self._stopped = False

    def send_packet(self, packet):
        self._queue.put_nowait(packet)

    def stop(self):
        self._stopped = True

    def run(self):
        while not self._stopped:
            packet = None

            try:
                packet = self._queue.get_nowait()
            except Queue.Empty:
                time.sleep(0.1)
                continue

            event = Event.PacketOutEvent(self._player, packet)
            self._player.fire(event)
            if event.is_cancelled():
                continue

            self._player._serializer.write(self._player._sock, event.get_packet())


class CraftPlayerEventBus(object):

    def __init__(self, player):
        self._player = player
        self._listeners = {}

    def register_listener(self, event, handler):
        if not hasattr(handler, "_CraftProtocol"):
            raise ValueError("Handler must be decorated by CraftProtocol.Client.Event.Handler")

        if event not in self._listeners:
            self._listeners[event] = []

        self._listeners[event].append(handler)
        self._sort_listeners()

    def _sort_listeners(self):
        for event in self._listeners:
            self._listeners[event] = sorted(self._listeners[event], key=lambda x: x._CraftProtocol["priority"],
                                            reverse=True)

    def fire(self, event):
        if event.__class__ not in self._listeners:
            return

        for handler in self._listeners[event.__class__]:
            if event.is_cancelled() and handler._CraftProtocol["ignore_cancelled"] != True:
                continue

            try:
                handler.__call__(event)
            except:
                traceback.print_exc()


class CraftPlayer(object):

    def __init__(self, username, uuid, sock, serializer, server):
        self._username = username
        self._uuid = uuid
        self._sock = sock
        self._serializer = serializer
        self._server = server

        self._writer = CraftPlayerWriterThread(self)
        self._reader = CraftPlayerReaderThread(self)
        self._event_bus = CraftPlayerEventBus(self)

        self._lock = threading.Lock()

        self._spawned = False
        self._entity_id = None
        self._x = None
        self._y = None
        self._z = None
        self._main_inventory = Inventory(0, "Inventory", "minecraft:container", 46)
        self._open_inventory = None
        self._last_teleport_id = None

        self.register_listener(Event.PacketInEvent, self._process_in_packet)
        self.register_listener(Event.PacketOutEvent, self._process_out_packet)

    @Event.Handler(priority=Event.HandlerPriority.LOW, ignore_cancelled=True)
    def _process_in_packet(self, event):
        packet = event.get_packet()
        player = event.get_player()

        if packet.__class__ == Play.DisconnectPacket:
            player.disconnect(ChatSerializer.strip_colors(json.loads(packet.get_reason())))
        elif packet.__class__ == Play.ChatMessageClientPacket:
            if event.is_cancelled():
                return

            player.fire(Event.ChatReceiveEvent(player, json.loads(packet.get_chat())))
        elif packet.__class__ == Play.PlayerPositionAndLookClientPacket:
            if event.is_cancelled():
                return

            teleport_event = Event.TeleportEvent(player, packet.get_x(), packet.get_y(), packet.get_z(),
                                                 packet.get_teleport_id())
            player.fire(teleport_event)

            if teleport_event.is_cancelled():
                event.cancel()
                return

            if packet.get_teleport_id() == 1 and player._last_teleport_id >= 1:
                server_teleport_event = Event.ServerTeleportEvent(player)
                player.fire(server_teleport_event)

                if server_teleport_event.is_cancelled():
                    event.cancel()
                    return

            player.send_packet(Play.TeleportConfirmPacket(packet.get_teleport_id()))
            if not player._spawned:
                spawn_event = Event.SpawnEvent(player)
                player.fire(spawn_event)

                if spawn_event.is_cancelled():
                    event.cancel()
                    return

                player.send_packet(
                    Play.PlayerPositionServerPacket(packet.get_x(), packet.get_y(), packet.get_z(), True))
                player._spawned = True

            with player._lock:
                player._x = packet.get_x()
                player._y = packet.get_y()
                player._z = packet.get_z()
                player._last_teleport_id = packet.get_teleport_id()
        elif packet.__class__ == Play.JoinGamePacket:
            if event.is_cancelled():
                return

            login_event = Event.LoginEvent(player, packet.get_entity_id, packet.get_gamemode(),
                                           packet.get_dimension(), packet.get_difficulty(), packet.get_max_players(),
                                           packet.get_level_type(), packet.get_debug_info())
            player.fire(login_event)

            if login_event.is_cancelled():
                event.cancel()
                return

            player._entity_id = packet.get_entity_id()

            brand_buf = StringIO()
            StreamIO.write_string(brand_buf, "CraftProtocol/" + VersionConstants.VERSION)
            brand_message = brand_buf.getvalue()
            brand_buf.close()

            player.respawn()
            player.send_packet(
                Play.ClientSettingsPacket("en_US", 0, ChatMode.ENABLED, False, int("11111110", 2), Hand.RIGHT))
            player.send_packet(Play.PluginMessageServerPacket("MC|Brand", brand_message))
        elif packet.__class__ == Play.ConfirmTransactionClientPacket:
            if event.is_cancelled():
                return

            player._lock.acquire()
            if player._open_inventory == None or packet.get_window_id() != player._open_inventory.get_id():
                event.cancel()
                player._lock.release()
                player.disconnect("Received confirm transaction packet for not initialized window")
                return

            player._lock.release()
            player.send_packet(Play.ConfirmTransactionServerPacket(packet.get_window_id(), packet.get_action_number(),
                                                                   packet.is_accepted()))
        elif packet.__class__ == Play.OpenWindowPacket:
            if event.is_cancelled():
                return

            inventory = Inventory(packet.get_window_id(), json.loads(packet.get_window_title()),
                                  packet.get_window_type(), packet.get_slots_number(), packet.get_entity_id())

            open_inventory_event = Event.OpenInventoryEvent(player, inventory)
            player.fire(open_inventory_event)

            if open_inventory_event.is_cancelled():
                event.cancel()
                return

            player._open_inventory = open_inventory_event.get_inventory()
        elif packet.__class__ == Play.KeepAliveClientPacket:
            player.send_packet(Play.KeepAliveServerPacket(packet.get_id()))
        elif packet.__class__ == Play.WindowItemsPacket:
            if event.is_cancelled():
                return

            player._lock.acquire()

            if packet.get_window_id() == player._main_inventory.get_id():
                update_inventory_event = Event.UpdateInventoryEvent(player, player._main_inventory, packet.get_slots())
            elif player._open_inventory is None:
                event.cancel()
                player._try_disconnect_async("Received items for not initialized window")
                player._lock.release()
                return
            else:
                update_inventory_event = Event.UpdateInventoryEvent(player, player._open_inventory, packet.get_slots())

            player._lock.release()

            player.fire(update_inventory_event)
            if update_inventory_event.is_cancelled():
                event.cancel()
                return

            player._lock.acquire()

            if update_inventory_event.get_inventory() == player._main_inventory:
                slots = update_inventory_event.get_slots()

                if len(slots) > len(player._main_inventory):
                    event.cancel()
                    player._try_disconnect_async("Received too many items")
                    player._lock.release()
                    return

                main_inventory = player._main_inventory.copy()

                for i in range(len(slots)):
                    main_inventory[i] = slots[i]

                player._main_inventory = main_inventory
                player._lock.release()
                return

            slots = update_inventory_event.get_slots()[:len(player._open_inventory) - 1]
            main_slots = update_inventory_event.get_slots()[len(player._open_inventory) - 1:]

            if len(main_slots) + 8 > len(player._main_inventory):
                event.cancel()
                player._try_disconnect_async("Received too many items")
                player._lock.release()
                return

            main_inventory = player._main_inventory.copy()
            open_inventory = player._open_inventory.copy()

            for i in range(len(main_slots)):
                main_inventory[i + 9] = main_slots[i]
            player._main_inventory = main_inventory

            for i in range(len(slots)):
                open_inventory[i] = slots[i]
            player._open_inventory = open_inventory

            player._lock.release()

    @Event.Handler(priority=Event.HandlerPriority.LOW, ignore_cancelled=True)
    def _process_out_packet(self, event):
        packet = event.get_packet()
        player = event.get_player()

        if packet.__class__ == Play.PlayerPositionServerPacket:
            if event.is_cancelled():
                return

            with player._lock:
                player._x = packet.get_x()
                player._y = packet.get_y()
                player._z = packet.get_z()
        elif packet.__class__ == Play.CloseWindowServerPacket:
            if event.is_cancelled():
                return

            close_inventory_event = None

            with player._lock:
                if player._open_inventory is not None and packet.get_window_id() == player._open_inventory.get_id():
                    close_inventory_event = Event.CloseInventoryEvent(player, player._open_inventory)

            if close_inventory_event is None:
                return

            player.fire(close_inventory_event)
            if close_inventory_event.is_cancelled():
                event.cancel()
                return

            player._open_inventory = None
        elif packet.__class__ == Play.ChatMessageServerPacket:
            if event.is_cancelled():
                return

            chat_send_event = Event.ChatSendEvent(player, packet.get_text())
            player.fire(chat_send_event)

            if chat_send_event.is_cancelled():
                event.cancel()
                return

            event.set_packet(Play.ChatMessageServerPacket(chat_send_event.get_text()))

    def get_username(self):
        return self._username

    def get_uuid(self):
        return self._uuid

    def get_protocol(self):
        return self._server.get_protocol()

    def is_connected(self):
        return self._sock is not None

    def _try_disconnect_async(self, reason=""):
        if not self.is_connected():
            return

        self.fire(Event.DisconnectEvent(self, reason))

        self._writer.stop()
        self._reader.stop()

        if threading.current_thread() != self._writer:
            self._writer.join()

        if threading.current_thread() != self._reader:
            self._reader.join()

        self._sock.close()
        self._sock = None
        self._serializer = None

    def disconnect(self, reason=""):
        with self._lock:
            if not self.is_connected():
                raise IOError("Not connected")

            self._try_disconnect_async(reason)

    def try_disconnect(self, reason=""):
        with self._lock:
            self._try_disconnect_async(reason)

    def send_packet(self, packet):
        with self._lock:
            if not self.is_connected():
                raise IOError("Not connected")

            self._writer.send_packet(packet)

    def chat(self, message):
        self.send_packet(Play.ChatMessageServerPacket(message))

    def use_hand(self, hand):
        self.send_packet(Play.UseItemPacket(hand))

    def click_slot(self, inventory, slot, button, mode):
        if slot < 0:
            raise ValueError("Slot is too small")

        if slot >= len(inventory):
            raise ValueError("Slot is too big")

        self.send_packet(
            Play.ClickWindowPacket(inventory.get_id(), slot, button, inventory.get_and_inc_action_number(), mode,
                                   inventory[slot]))

    def get_open_inventory(self):
        with self._lock:
            return self.open_inventory

    def get_main_inventory(self):
        with self._lock:
            return self.main_inventory

    def close_inventory(self):
        with self._lock:
            if self._open_inventory is not None:
                self.send_packet(Play.CloseWindowServerPacket(self._open_inventory.get_id()))

    def get_x(self):
        with self._lock:
            return self._x

    def get_y(self):
        with self._lock:
            return self._y

    def get_z(self):
        with self._lock:
            return self._z

    def get_entity_id(self):
        with self._lock:
            return self._entity_id

    def respawn(self):
        self.send_packet(Play.ClientStatusPacket(ClientStatus.PERFORM_RESPAWN))

    def fire(self, event):
        self._event_bus.fire(event)

    def is_spawned(self):
        with self._lock:
            return self._spawned

    def register_listener(self, event_class, handler):
        self._event_bus.register_listener(event_class, handler)

    def reconnect(self):
        with self._lock:
            self._try_disconnect_async("Reconnecting...")

            new = self._server.login(self._username)
            new._event_bus = self._event_bus
            self.__dict__.update(new.__dict__)

    def loop(self):
        with self._lock:
            if not self.is_connected():
                raise IOError("Not connected")

            if not (self._writer.is_alive() and self._reader.is_alive()):
                self._writer.start()
                self._reader.start()

        while self._writer.is_alive():
            time.sleep(0.1)

        while self._reader.is_alive():
            time.sleep(0.1)
