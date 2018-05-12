#!/usr/bin/env python

import threading
import time
import json
from ..Packet import *
from ..VersionConstants import VersionConstants
from ..StreamIO import StreamIO
from ..ChatSerializer import ChatSerializer
from ..ClientStatus import ClientStatus
from ..Inventory import Inventory
from ..Hand import Hand
from ..ChatMode import ChatMode
from cStringIO import StringIO
import Event
import traceback
import Queue
import socket
import errno
import types

class CraftPlayerReaderThread(threading.Thread):

	def __init__(self, craftplayer):
		threading.Thread.__init__(self)
		self.craftplayer = craftplayer
		self.stopped = False

	def stop(self):
		self.stopped = True

	def run(self):
		while not self.stopped:
			try:
				packet = self.craftplayer.serializer.read(self.craftplayer.sock)
				self.craftplayer.event_bus.fire(Event.PacketInEvent(packet))
			except socket.timeout:
				self.craftplayer.disconnect("Timed out")
			except socket.error as ex:
				if ex.errno == errno.EINTR:
					continue
				raise
			except EOFError:
				self.craftplayer.disconnect("Connection closed by remote host")

class CraftPlayerWriterThread(threading.Thread):

	def __init__(self, craftplayer):
		threading.Thread.__init__(self)
		self.craftplayer = craftplayer
		self.queue = Queue.Queue()
		self.stopped = False

	def send_packet(self, packet):
		self.queue.put_nowait(packet)

	def stop(self):
		self.stopped = True

	def run(self):
		while not self.stopped:
			packet = None

			try:
				packet = self.queue.get_nowait()
			except Queue.Empty:
				time.sleep(0.1)
				continue

			event = Event.PacketOutEvent(packet)

			self.craftplayer.event_bus.fire(event)

			if event.is_cancelled():
				continue

			self.craftplayer.serializer.write(self.craftplayer.sock, event.get_packet())

class CraftPlayerEventBus(object):

	def __init__(self, craftplayer):
		self.craftplayer = craftplayer
		self.listeners = {}

	def register_listener(self, event, handler):
		if not hasattr(handler, "_CraftProtocol"):
			raise ValueError("Handler must be decorated by CraftProtocol.Client.Event.Handler")

		if type(handler) == types.MethodType and handler.__self__:
			handler = handler.__self__.__class__.__dict__[handler.__name__]

		if event not in self.listeners:
			self.listeners[event] = []

		self.listeners[event].append(handler)
		self._sort_listeners()

	def _sort_listeners(self):
		for event in self.listeners:
			self.listeners[event] = sorted(self.listeners[event], key = lambda x: x._CraftProtocol["priority"], reverse = True)

	def fire(self, event):
		if event.__class__ not in self.listeners:
			return

		for handler in self.listeners[event.__class__]:
			if event.is_cancelled() and handler._CraftProtocol["ignore_cancelled"] != True:
				continue

			try:
				handler.__call__(self.craftplayer, event)
			except:
				traceback.print_exc()

class CraftPlayer(object):

	def __init__(self, username, uuid, sock, serializer, craftserver):
		self.username = username
		self.uuid = uuid
		self.sock = sock
		self.serializer = serializer
		self.craftserver = craftserver

		self.writer = CraftPlayerWriterThread(self)
		self.reader = CraftPlayerReaderThread(self)
		self.event_bus = CraftPlayerEventBus(self)

		self.lock = threading.Lock()

		self.spawned = False
		self.entity_id = None
		self.x = None
		self.y = None
		self.z = None
		self.main_inventory = Inventory(0, "Inventory", "minecraft:container", 46)
		self.open_inventory = None
		self.last_teleport_id = None

		self.register_listener(Event.PacketInEvent, self._process_in_packet)
		self.register_listener(Event.PacketOutEvent, self._process_out_packet)

	@Event.Handler(priority = Event.HandlerPriority.LOW, ignore_cancelled = True)
	def _process_in_packet(self, event):
		packet = event.get_packet()

		if packet.__class__ == Play.DisconnectPacket:
			self.disconnect(ChatSerializer.strip_colors(json.loads(packet.get_reason())))
		elif packet.__class__ == Play.ChatMessageClientPacket:
			if event.is_cancelled():
				return

			self.event_bus.fire(Event.ChatReceiveEvent(json.loads(packet.get_chat())))
		elif packet.__class__ == Play.PlayerPositionAndLookClientPacket:
			if event.is_cancelled():
				return

			teleport_event = Event.TeleportEvent(packet.get_x(), packet.get_y(), packet.get_z(), packet.get_teleport_id())
			self.event_bus.fire(teleport_event)

			if teleport_event.is_cancelled():
				event.cancel()
				return

			if packet.get_teleport_id() == 1 and (self.last_teleport_id == None or self.last_teleport_id >= 1):
				server_teleport_event = Event.ServerTeleportEvent(packet.get_x(), packet.get_y(), packet.get_z(), packet.get_teleport_id())
				self.event_bus.fire(server_teleport_event)

				if server_teleport_event.is_cancelled():
					event.cancel()
					return

			self.send_packet(Play.TeleportConfirmPacket(packet.get_teleport_id()))

			if not self.spawned:
				self.send_packet(Play.PlayerPositionServerPacket(packet.get_x(), packet.get_y(), packet.get_z(), True))
				self.spawned = True

			with self.lock:
				self.x = packet.get_x()
				self.y = packet.get_y()
				self.z = packet.get_z()
				self.last_teleport_id = packet.get_teleport_id()
		elif packet.__class__ == Play.JoinGamePacket:
			if event.is_cancelled():
				return

			login_event = Event.LoginEvent(packet.get_entity_id(), packet.get_gamemode(), packet.get_dimension(), packet.get_difficulty(), packet.get_max_players(), packet.get_level_type(), packet.get_debug_info())
			self.event_bus.fire(login_event)

			if login_event.is_cancelled():
				event.cancel()
				return

			self.entity_id = packet.get_entity_id()

			brand_buf = StringIO()
			StreamIO.write_string(brand_buf, "CraftProtocol/" + VersionConstants.VERSION)
			brand_message = brand_buf.getvalue()
			brand_buf.close()

			self.respawn()
			self.send_packet(Play.ClientSettingsPacket("en_US", 0, ChatMode.ENABLED, False, int("11111110", 2), Hand.RIGHT))
			self.send_packet(Play.PluginMessageServerPacket("MC|Brand", brand_message))
		elif packet.__class__ == Play.ConfirmTransactionClientPacket:
			if event.is_cancelled():
				return

			self.lock.acquire()
			if self.open_inventory == None or packet.get_window_id() != self.open_inventory.get_id():
				event.cancel()
				self.lock.release()
				self.disconnect("Received confirm transaction packet for not initialized window")
				return

			self.lock.release()
			self.send_packet(Play.ConfirmTransactionServerPacket(packet.get_window_id(), packet.get_action_number(), packet.is_accepted()))
		elif packet.__class__ == Play.OpenWindowPacket:
			if event.is_cancelled():
				return

			inventory = Inventory(packet.get_window_id(), json.loads(packet.get_window_title()), packet.get_window_type(), packet.get_slots_number(), packet.get_entity_id())

			open_inventory_event = Event.OpenInventoryEvent(inventory)
			self.event_bus.fire(open_inventory_event)

			if open_inventory_event.is_cancelled():
				event.cancel()
				return

			self.open_inventory = open_inventory_event.get_inventory()			
		elif packet.__class__ == Play.KeepAliveClientPacket:
			self.send_packet(Play.KeepAliveServerPacket(packet.get_id()))
		elif packet.__class__ == Play.WindowItemsPacket:
			if event.is_cancelled():
				return

			update_inventory_event = Event.UpdateInventoryEvent(packet.get_window_id(), packet.get_slots())
			self.event_bus.fire(update_inventory_event)

			if update_inventory_event.is_cancelled():
				event.cancel()
				return

			self.lock.acquire()

			if update_inventory_event.get_id() == self.main_inventory.get_id():
				slots = update_inventory_event.get_slots()

				if len(slots) > len(self.main_inventory):
					event.cancel()
					self.lock.release()
					self.disconnect("Received too many items")
					return

				main_inventory = self.main_inventory.copy()

				for i in range(len(slots)):
					main_inventory[i] = slots[i]

				self.main_inventory = main_inventory
				self.lock.release()
				return

			if self.open_inventory == None or packet.get_window_id() != self.open_inventory.get_id():
				event.cancel()
				self.lock.release()
				self.disconnect("Received items for not initialized window")
				return

			slots = update_inventory_event.get_slots()[:len(self.open_inventory) - 1]
			main_slots = update_inventory_event.get_slots()[len(self.open_inventory) - 1:]

			if len(main_slots) + 8 > len(self.main_inventory):
				event.cancel()
				self.lock.release()
				self.disconnect("Received too many items")
				return

			main_inventory = self.main_inventory.copy()
			open_inventory = self.open_inventory.copy()

			for i in range(len(main_slots)):
				main_inventory[i + 9] = main_slots[i]

			self.main_inventory = main_inventory

			for i in range(len(slots)):
				open_inventory[i] = slots[i]

			self.open_inventory = open_inventory
			self.lock.release()

	@Event.Handler(priority = Event.HandlerPriority.LOW, ignore_cancelled = True)
	def _process_out_packet(self, event):
		packet = event.get_packet()

		if packet.__class__ == Play.PlayerPositionServerPacket:
			if event.is_cancelled():
				return

			with self.lock:
				self.x = packet.get_x()
				self.y = packet.get_y()
				self.z = packet.get_z()
		elif packet.__class__ == Play.CloseWindowServerPacket:
			if event.is_cancelled():
				return
	
			with self.lock:
				if packet.get_window_id() == self.open_inventory.get_id():
					self.open_inventory = None
		elif packet.__class__ == Play.ChatMessageServerPacket:
			if event.is_cancelled():
				return

			chat_send_event = Event.ChatSendEvent(packet.get_text())
			self.event_bus.fire(chat_send_event)

			if chat_send_event.is_cancelled():
				event.cancel()

			event.set_packet(Play.ChatMessageServerPacket(chat_send_event.get_text()))

	def get_username(self):
		return self.username

	def get_uuid(self):
		return self.uuid

	def get_protocol(self):
		return self.craftserver.protocol

	def is_connected(self):
		return self.sock != None

	def _disconnect_async(self, reason = ""):
		if not self.is_connected():
			raise IOError("Not connected")

		self.event_bus.fire(Event.DisconnectEvent(reason))

		self.writer.stop()
		self.reader.stop()

		if threading.current_thread() != self.writer:
			self.writer.join()

		if threading.current_thread() != self.reader:
			self.reader.join()

		self.sock.close()
		self.sock = None
		self.serializer = None

	def disconnect(self, reason = ""):
		with self.lock:
			self._disconnect_async(reason)

	def send_packet(self, packet):
		with self.lock:
			if not self.is_connected():
				raise IOError("Not connected")

			self.writer.send_packet(packet)

	def chat(self, message):
		self.send_packet(Play.ChatMessageServerPacket(message))

	def use_hand(self, hand):
		self.send_packet(Play.UseItemPacket(hand))

	def click_slot(self, inventory, slot, button, mode):
		if slot < 0:
			raise ValueError("Slot is too small")

		if slot >= len(inventory):
			raise ValueError("Slot is too big")

		self.send_packet(Play.ClickWindowPacket(inventory.get_id(), slot, button, inventory.get_and_inc_action_number(), mode, inventory[slot]))

	def get_open_inventory(self):
		with self.lock:
			return self.open_inventory

	def get_main_inventory(self):
		with self.lock:
			return self.main_inventory

	def close_inventory(self):
		with self.lock:
			if self.open_inventory != None:
				self.send_packet(Play.CloseWindowServerPacket(self.open_inventory.get_id()))

	def get_x(self):
		with self.lock:
			return self.x

	def get_y(self):
		with self.lock:
			return self.y

	def get_z(self):
		with self.lock:
			return self.z

	def get_entity_id(self):
		with self.lock:
			return self.entity_id

	def respawn(self):
		self.send_packet(Play.ClientStatusPacket(ClientStatus.RESPAWN))

	def is_spawned(self):
		with self.lock:
			return self.spawned

	def register_listener(self, event_class, handler):
		self.event_bus.register_listener(event_class, handler)

	def reconnect(self):
		with self.lock:
			if self.is_connected():
				self._disconnect_async("Reconnecting...")

			new = self.craftserver.login(self.username)
			new.event_bus = self.event_bus
			self.__dict__.update(new.__dict__)

	def loop(self):
		with self.lock:
			if not self.is_connected():
				raise IOError("Not connected")

			if not (self.writer.is_alive() and self.reader.is_alive()):
				self.writer.start()
				self.reader.start()

		while self.writer.is_alive():
			time.sleep(0.1)

		while self.reader.is_alive():
			time.sleep(0.1)