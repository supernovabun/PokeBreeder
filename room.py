import re
from item import Item

class Room:
	rooms = {}
	def __init__(self, brief_desc):
		self.brief = brief_desc + "."
		self.inventory = []
		self.exits = {}
		room_id = brief_desc.replace(" ", "_")
		if list(Room.rooms.keys()) == []:
			self.room_id = f"{room_id}"+"{:03d}".format(1)
		else:
			rooms_keys = Room.rooms.keys()
			rooms_keys = [re.findall("\\d{3}", k)[0] for k in rooms_keys]
			rooms_keys = sorted(rooms_keys)
			room_last = rooms_keys[-1]
			self.room_id = f"{room_id}" + "{:03d}".format(int(room_last)+1)
		Room.rooms[self.room_id] = self

	def set_verbose(self, verbose_desc):
		self.verbose = verbose_desc

	def set_exits(self, exit_dict):
		self.exits = exit_dict

	def add_exit(self, direction, exit):
		self.exits[direction] = exit

	def get_exits(self):
		self.exit_string = ", ".join(self.exits.keys()) if len(self.exits) > 0 else "None"
		self.exit_string = self.exit_string[0].upper() + self.exit_string[1:]
		return(self.exit_string)

	def add_inventory(self, to_add):
		if type(to_add) == type([]):
			self.inventory += to_add
		else:
			self.inventory.append(str(to_add))

	def remove_inventory(self, to_remove):
		if type(to_remove) == type([]):
			for i in to_remove:
				i = i if type(i) == type("string") else i.item_id
				self.inventory.pop(self.inventory.index(i))
		else:
			to_remove = to_remove if type(to_remove) == type("string") else to_remove.item_id
			self.inventory.pop(self.inventory.index(to_remove))
		return(to_remove)

	def display(self):
		print(self.brief)
		print(self.verbose)
		print(f"Exits: {self.get_exits()}.")
