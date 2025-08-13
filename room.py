import re

class Room:
	rooms = {}
	room_num = 1
	def __init__(self, brief_desc, id_num=None):
		self.brief = brief_desc + "."
		self.inventory = []
		self.exits = {}
		self.verbose = ""
		room_id = brief_desc
		if id_num:
			self.room_id = id_num
		else:
			self.room_id = f"{room_id}{Room.room_num:03d}"
			Room.room_num += 1
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
		if isinstance(to_remove, list):
			for i in to_remove:
				i = i if isinstance(i, str) else i.item_id
				self.inventory.pop(self.inventory.index(i))
		else:
			#to_remove = to_remove if isinstance(to_remove, str) else to_remove.item_id
			if not isinstance(to_remove, str):
				to_remove = to_remove.egg_id if to_remove.egg_id else to_remove.item_id
			self.inventory.pop(self.inventory.index(to_remove))
		return(to_remove)

	def display(self):
		DARK_GREEN = "\x1b[38;5;22m"
		LIGHT_GREEN = "\x1b[38;5;34m"
		MED_GRAY = "\x1b[38;5;248m"
		RESET = "\033[0m"
		print(f"{DARK_GREEN}{self.brief}{RESET}")
		print(f"{MED_GRAY}{self.verbose}{RESET}")
		print(f"{LIGHT_GREEN}Exits{RESET}: {self.get_exits()}.")

	def to_dict(self):
		return({
			"brief": self.brief[:-1],
			"room_id": self.room_id,
			"inventory": [i if type(i) == type(" ") else i.item_id for i in self.inventory],
			"exits": [(k, v.room_id) for k, v in self.exits.items()],
			"desc": self.verbose
		})

	@staticmethod
	def from_dict(data):
		loaded_room = Room(data["brief"], id_num=data["room_id"])
		for each_room in data["exits"]:
			loaded_room.add_exit(each_room[0], each_room[1])
		loaded_room.set_verbose(data["desc"])
		loaded_room.add_inventory(data["inventory"])
		return(loaded_room)
