import re
from room import Room

class Item:
	item_id = {}
	item_num = 1
	def __init__(self, name, item_type, room, value, item_id=None, gettable=True, container=False, held_by=None):
		self.name = name.title()
		self.item_type = item_type.title() if item_type.title() not in ["Food", "Furniture", "Held Item", "Medicine", "Painting", "Statue", "Drawing", "Misc."] else "Misc."
		self.room = room if not isinstance(room, str) else Room.rooms[room]
		self.in_somewhere = False
		self.held_by = None
		self.base_value = int(value)
		self.gettable = gettable
		self.container = container
		self.inventory = [] if container else None
		if item_id:
			self.item_id = item_id
		else:
			self.item_id = f"{name.title()}{Item.item_num:04d}"
			Item.item_num += 1
		Item.item_id[self.item_id] = self
		if isinstance(room, Room):
			self.room.add_inventory(self.item_id)

	def set_desc(self, desc):
		self.description = desc

	def get_desc(self):
		if self.container:
			counts = {}
			for i in sorted(self.inventory):
				if i[:-4] in counts.keys():
					counts[i[:-4]] += 1
				else:
					counts[i[:-4]] = 1
			counts = [f"  {"{:03d}".format(v)} ... {k}" for k, v in counts.items()]
			counts = "\n".join(counts)
			counts = counts if len(counts) > 0 else "  Nothing"
			return(self.description+"\nIt holds the following:\n"+counts)
		else:
			return(self.description)

	def get_article(self):
		if self.name.split(" ")[0] in ["The", "A", "An"]:
			article = ""
		elif self.name[0] in ["A", "E", "I", "O", "U"]:
			article = "an "
		else:
			article = "a "
		return(article)

	def add_inventory(self, to_add):
		if self.container:
			if self.inventory:
				self.inventory.append(to_add.item_id)
			else:
				self.inventory = [to_add.item_id]
			to_add.in_somewhere = self
			print(f"You carefully place {to_add.get_article()}{to_add.name.lower()} inside of {self.get_article()}{self.name.lower()}.")
		else:
			print(f"{self.name[0]+self.name[1:].lower()} will not fit {to_add.get_article()}{to_add.name.lower()}, no matter how hard you may try.")

	def remove_inventory(self, to_remove):
		if self.container:
			if self.inventory:
				self.inventory.pop(self.inventory.index(to_remove))
			else:
				print(f"{self.name} has nothing inside of it.")
		else:
			print(f"{self.name} cannot and does not hold anything inside of it.")

	def move_to_room(self, new_room):
		if self.room and self.item_id in self.room.inventory:
			self.room.remove_inventory(self.item_id)
		self.room = new_room
		if self.in_somewhere in [False, None] and self.held_by in [False, None]:
			new_room.add_inventory(self.item_id)

	def to_dict(self):
		return({
			"item_id": self.item_id,
			"name": self.name,
			"item_type": self.item_type,
			"room": self.room if type(self.room) == type(" ") or self.room == None else self.room.room_id,
			"desc": self.description,
			"in_somewhere": self.in_somewhere.item_id if self.in_somewhere else self.in_somewhere,
			"base_value": self.base_value,
			"gettable": self.gettable,
			"container": self.container,
			"inventory": [i if type(i) == type(" ") else i.item_id for i in self.inventory] if self.inventory else self.inventory,
			"held_by": self.held_by
		})

	@staticmethod
	def from_dict(data):
		loaded_item = Item(data["name"], data["item_type"], data["room"], data["base_value"], item_id=data["item_id"], gettable=data["gettable"], container=data["container"], held_by=data["held_by"])
		loaded_item.in_somewhere_string = data["in_somewhere"]
		loaded_item.inventory = data["inventory"]
		loaded_item.set_desc(data["desc"])
		return(loaded_item)
