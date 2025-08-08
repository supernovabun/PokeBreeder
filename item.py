import re

class Item:
	item_id = {}
	def __init__(self, name, item_type, room, value, gettable=True, container=False):
		self.name = name.title()
		self.item_type = item_type.title() if item_type.title() not in ["Food", "Held Item", "Medicine", "Painting", "Statue", "Drawing", "Misc."] else "Misc."
		self.room = room
		self.base_value = int(value)
		self.gettable = gettable
		self.container = container
		self.inventory = [] if container else None
		if len(Item.item_id.keys()) == 0:
			self.item_id = f"{name.title()}"+"{:04d}".format(1)
		else:
			item_id_keys = Item.item_id.keys()
			item_id_keys = [re.findall("\\d{4}", k)[0] for k in item_id_keys]
			item_id_keys = sorted(item_id_keys)
			item_last = item_id_keys[-1]
			self.item_id = f"{name.title()}"+"{:04d}".format(int(item_last)-1)
		Item.item_id[self.item_id] = self
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
