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

		return(self.description)
