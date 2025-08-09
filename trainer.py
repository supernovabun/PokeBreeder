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
		self.entourage = []
		self.energy = 120
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
		item = item if type(item) == type("") else item.item_id
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
		elif self.room.brief == "An oversized living room.":
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
