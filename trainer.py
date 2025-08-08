import random
from indiv import *

class Trainer:
	trainer_id = {}
	def __init__(self, name, room):
		self.currency = 2000
		self.pasture_size = 1
		self.pokemon = {}
		self.pokedex = []
		self.inventory = []
		self.room = room
		if len(Trainer.trainer_id.keys()) == 0:
			self.trainer_id = f"Trainer{name.title()}"+"{:02d}".format(1)
		else:
			trainer_id_keys = Trainer.trainer_id.keys()
			trainer_id_keys = [re.findall("\\d{2}", k)[0] for k in trainer_id_keys]
			trainer_id_keys = sorted(trainer_id_keys)
			trainer_last = trainer_id_keys[-1]
			self.trainer_id = f"Trainer{name.title()}"+"{:02d}".format(int(trainer_last)-1)
		Trainer.trainer_id[self.trainer_id] = self

	def add_pokemon(self, new_pokemon):
		self.pokemon[new_pokemon.pkmn_id] = new_pokemon
		if new_pokemon.species not in self.pokedex:
			self.pokedex.append(new_pokemon.species)

	def add_inventory(self, item):
		self.inventory.append(item)

	def check_inventory(self, search_string=None):
		counts = {}
		for i in sorted(self.inventory):
			if i[:-4] in counts.keys():
				counts[i[:-4]] += 1
			else:
				counts[i[:-4]] = 1
		for k, v in counts.items():
			print(f"  {"{:03d}".format(v)} ... {k}")
		if len(counts.keys()) == 0:
			print(f"  Nothing")

	def remove_inventory(self, to_remove):
		if type(to_remove) == type([]):
			for i in to_remove:
				i = i if type(i) == type("string") else i.item_id
				self.inventory.pop(self.inventory.index(i))
		else:
			to_remove = to_remove if type(to_remove) == type("string") else to_remove.item_id
			self.inventory.pop(self.inventory.index(to_remove))
		return(to_remove)