import re
import random
from room import Room ## Test

class Trainer:
	trainer_id = {}
	trainer_num = 1
	def __init__(self, name, room, trainer_id=None):
		self.name = name
		self.currency = 2000
		self.pasture_size = 1
		self.pokemon = {}
		self.pokedex = []
		self.inventory = []
		self.entourage = []
		self.energy = 120
		self.room = room
		self.description = ""
		if trainer_id:
			self.trainer_id = trainer_id
		else:
			self.trainer_id = f"Trainer{name.title()}{Trainer.trainer_num:02d}"
			Trainer.trainer_num += 1
		Trainer.trainer_id[self.trainer_id] = self

	def set_desc(self, desc):
		self.description = desc

	def set_room(self, room=None):
		if not room or room == "":
			room = self.room
		if self.trainer_id[-2:] != "01":
			if isinstance(room, str):
				self.room = Room.rooms[room]
			self.room.add_inventory(self.trainer_id) if self.trainer_id not in self.room.inventory else None

	def add_pokemon(self, new_pokemon):
		self.pokemon[new_pokemon.pkmn_id] = new_pokemon
		if new_pokemon.species not in self.pokedex:
			self.pokedex.append(new_pokemon.species)

	def add_inventory(self, thing):
		if type(thing).__str__ == "Egg":
			thing = thing.egg_id
		elif type(thing).__str__ == "Item":
			thing = thing.item_id
		#thing = item if type(item) == type("") else item.item_id
		self.inventory.append(thing)

	def check_inventory(self, search_string=None):
		counts = {}
		for i in sorted(self.inventory):
			i = re.sub("\\d+$", "", i)
			if i in counts.keys():
				counts[i] += 1
			else:
				counts[i] = 1
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

	def check_energy(self):
		LIGHT_GRAY = "\x1b[38;5;240m"
		DARK_GRAY = "\x1b[38;5;236m"
		RESET = "\033[0m"
		if self.energy == -20:
			print(f"{DARK_GRAY}Your body refuses to move and begs for rest.{RESET}")
			return(False)
		elif self.energy == 0:
			print(f"{LIGHT_GRAY}You're slowing down and becoming sluggish.{RESET}")
			return(True)
		else:
			return(True)

	def display_energy(self):
		DARK_RED = "\x1b[38;5;88m"
		RED = "\x1b[38;5;124m"
		ORANGE = "\x1b[38;5;172m"
		YELLOW = "\x1b[38;5;226m"
		LIME = "\x1b[38;5;40m"
		RESET = "\033[0m"
		if self.energy >= 100:
			energy_string = f"{LIME}Energetic{RESET}"
		elif self.energy >= 80:
			energy_string = f"{YELLOW}Active{RESET}"
		elif self.energy >= 60:
			energy_string = f"{ORANGE}Decent{RESET}"
		elif self.energy > 30:
			energy_string = f"{RED}Tired{RESET}"
		else:
			energy_string = f"{DARK_RED}Struggling{RESET}"
		return(energy_string)

	def sleep(self):
		if self.room.brief == "Master bedroom in a quaint house.":
			regain = 100
			print("You crawl into bed and under your covers, pulling your bed sheet up to your chin. You close your eyes and slip off to sweet slumber.")
		elif self.room.brief == "Spacious family den.":
			regain = 75
			print("You throw yourself, sprawled out like a Staryu, onto your sectional couch. You stick the landing and wiggle this way and that until you are comfortable enough to find sleep.")
		else:
			regain = 50
			print("With little dignity, you collapse to the ground and sleep where you are. You're going to feel that in the morning.")
		self.energy += min(regain, 100)
		[pkmn.new_day() for pkmn in self.pokemon.values()]
		print("---")
		if self.energy == 100:
			print("You wake up the next morning full of energy. Let's take care of Pokemon again, today!")
		elif self.energy >= 80:
			print("After a long night's rest, your eyes snap open. You're ready for the day!")
		elif self.energy >= 60:
			print("The sun in beating down on your eyelids causes you to wake, whether or not you're ready to.")
		elif self.energy > 30:
			print("Everything in your body begs you to sleep just a bit longer. Alas, you are awake.")
		else:
			print("Your body screams for sleep that you have not permitted it. How are you supposed to take care of Pokemon if you can't take care of yourself?")

	def to_dict(self):
		"""
		#############
		### DEBUG ###
		#############
		presave_inventory = []
		for i in self.inventory:
			if isinstance(i, str):
				presave_inventory.append(i)
			else:
				print("Crap, how'd this get in there?: {i}")
		### END DEBUG ###
		"""
		return({
			"trainer_id": self.trainer_id,
			"name": self.name,
			"currency": self.currency,
			"pasture_size": self.pasture_size,
			"pokemon": list(self.pokemon.keys()),
			"pokedex": self.pokedex,
			"inventory": self.inventory,
			"entourage": [ent.to_dict() for ent in self.entourage],
			"energy": self.energy,
			"description": self.description,
			"room": self.room.room_id
		})

	@staticmethod
	def from_dict(data):
		from room import Room
		from pokemon import Pokemon

		trainer = Trainer(data["name"], data["room"], trainer_id=data["trainer_id"])
		trainer.name = data["name"]
		trainer.currency = data["currency"]
		trainer.pokemon = data["pokemon"]
		trainer.pokedex = data["pokedex"]
		trainer.inventory = data["inventory"]
		trainer.entourage = [Pokemon.from_dict(p) for p in data["entourage"]]
		trainer.energy = data["energy"]
		trainer.description = data["description"]
		trainer.room_string = data["room"]

		return(trainer)
