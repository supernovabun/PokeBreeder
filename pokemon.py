import random
import re
import copy
from room import Room
from pokemon_registry import *

class Pokemon:
	pkmn_id = {}
	pkmn_num = 1
	def __init__(self, species, base_stats, types, egg_groups, descriptor, pkmn_id=None):
		if type(species) != type(""):
			raise TypeError("Invalid entry for species; you entered: %s" % (str(species)))
		if type(base_stats) != type([]):
			raise TypeError("Invalid entry for base_stats; you entered: %s" % (str(base_stats)))
		if type(types) != type([]):
			raise TypeError("Invalid entry for types; you entered: %s" % (str(types)))
		self.species = species
		self.base_stats = {
		"Health": base_stats[0],
		"Attack": base_stats[1],
		"Defense": base_stats[2],
		"Special Attack": base_stats[3],
		"Special Defense": base_stats[4],
		"Speed": base_stats[5]
		}
		self.type1 = types[0]
		self.type2 = types[1]
		self.mother = "Unknown"
		self.father = "Unknown"
		self.egg_group1 = egg_groups[0]
		self.egg_group2 = egg_groups[1]
		self.descriptor = descriptor
		self.held_item = ""
		self.sex = ""
		self.affection = 0
		self.daily_affection = []
		self.loved = 0
		self.fullness = 0
		self.daily_food = []
		self.room = "Aether000"
		self.trainer = ""
		self.following = None
		if pkmn_id:
			self.pkmn_id = pkmn_id
		else:
			self.pkmn_id = f"{self.species}{Pokemon.pkmn_num:06d}"
			Pokemon.pkmn_num += 1
		Pokemon.pkmn_id[self.pkmn_id] = self

	def set_trainer(self, trainer):
		self.trainer = trainer

	def set_room(self, room=None):
		if not room or room == "":
			room = self.room
		if isinstance(room, str):
			room = Room.rooms[room]
		self.room = room
		self.room.add_inventory(self.pkmn_id) if self.pkmn_id not in self.room.inventory else None

	def random_pattern(self, pattern_weights=[0.333, 0.333, 0.333], color_weights=[0.5, 0.5], color_placement_weights=[0.333,0.333,0.333], color_dilution_weights=[0.5, 0.5], color_extension_weights=[0.5, 0.5]):
		self.pattern = random.choices(["A", "/", "a"], weights=pattern_weights, k=1)[0] + random.choices(["A", "/", "a"], weights=pattern_weights, k=1)[0]
		self.color = random.choices(["B", "b"], weights=color_weights, k=1)[0] + random.choices(["B", "b"], weights=color_weights, k=1)[0]
		self.color_placement = random.choices(["C", "/", "c"], weights=color_placement_weights, k=1)[0] + random.choices(["C", "/", "c"], weights=color_placement_weights, k=1)[0]
		self.color_dilution = random.choices(["D", "d"], weights=color_dilution_weights, k=1)[0] + random.choices(["D", "d"], weights=color_dilution_weights, k=1)[0]
		self.color_extension = random.choices(["E", "e"], weights=color_extension_weights, k=1)[0] + random.choices(["E", "e"], weights=color_extension_weights, k=1)[0]
		self.inheritance = "None"

	def pattern_inheritance(self, mother, father):
		if mother.species == "Ditto" or father.species == "Ditto":
			self.pattern = mother.pattern if mother.species != "Ditto" else father.pattern
			self.color = mother.color if mother.species != "Ditto" else father.color
			self.color_placement = mother.color_placement if mother.species != "Ditto" else father.color_placement
			self.color_dilution = mother.color_dilution if mother.species != "Ditto" else father.color_dilution
			self.color_extension = mother.color_extension if mother.species != "Ditto" else father.color_extension
			self.inheritance = mother.inheritance if mother.species != "Ditto" else father.inheritance
		else:
			self.pattern = random.choice(mother.pattern) + random.choice(father.pattern)
			self.color = random.choice(mother.color) + random.choice(father.color)
			self.color_placement = random.choice(mother.color_placement) + random.choice(father.color_placement)
			self.color_dilution = random.choice(mother.color_dilution) + random.choice(father.color_dilution)
			self.color_extension = random.choice(mother.color_extension) + random.choice(father.color_extension)
			if mother.species == father.species:
				self.inheritance = random.choice([mother.inheritance, father.inheritance])
			else:
				self.inheritance = father.descriptor
	
	def breed(self, other_parent):
		if self.species == "Ditto" or other_parent.species == "Ditto":
			pass
		elif self.egg_group1 not in [other_parent.egg_group1, other_parent.egg_group2] and self.egg_group2 not in [other_parent.egg_group1, other_parent.egg_group2]:
			print("These Pokemon are not compatible.")
			return
		if self.sex == other_parent.sex:
			print("Two Pokemon must be opposite sexes to breed an egg!")
			return
		elif self.sex == "M" and other_parent.sex == "F":
			temp_mother = other_parent
			temp_father = self
			# baby = type(self)(self.species, sex="r", pattern="parents", mother=temp_mother, father=temp_father) ### This works, but gotta fix this
			baby = type(self).stages[0](type(self).stages[0].species, sex="r", pattern="parents", mother=temp_mother, father=temp_father)
			baby.loved = 25
			return(baby)
		else:
			temp_mother = self
			temp_father = other_parent
			# baby = type(self)(self.species, sex="r", pattern="parents", mother=temp_mother, father=temp_father) ### This works, but gotta fix this
			baby = type(self).stages[0](type(self).stages[0].species, sex="r", pattern="parents", mother=temp_mother, father=temp_father)
			baby.loved = 25
			return(baby)
	
	def set_name(self, new_name):
		self.name = new_name

	def set_IVs(self, IVs=None):
		if IVs:
			self.IVs = dict(zip(["Health", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"], IVs))
		elif self.mother != "Unknown" and self.father != "Unknown":
			IVs_to_get = []
			power_items = {
			"Power Anklet": "Speed",
			"Power Band": "Special Defense",
			"Power Belt": "Defense",
			"Power Bracer": "Attack",
			"Power Lens": "Special Attack",
			"Power Weight": "Health",
			}
			if self.mother.held_item == "Destiny Knot":
				mother_to_get = random.sample(list(self.mother.IVs.keys()), 5)
				mother_to_get = [(k, self.mother.IVs[k]) for k in mother_to_get]
				IVs_to_get += mother_to_get
			elif self.mother.held_item in ["Power Anklet", "Power Band", "Power Belt", "Power Bracer", "Power Lens", "Power Weight"]:
				IVs_to_get.append((power_items[self.mother.held_item], self.mother.IVs[power_items[self.mother.held_item]]))
			if self.father.held_item == "Destiny Knot":
				if len(IVs_to_get) == 1:
					temp_father_IVs = copy.deepcopy(self.father.IVs)
					temp_father_IVs.pop(IVs_to_get[0][0])
					IVs_to_get += list(temp_father_IVs.items())
				else:
					father_to_get = random.sample(list(self.father.IVs.keys()), 5)
					father_to_get = [(k, self.father.IVs[k]) for k in father_to_get]
					IVs_to_get += father_to_get
			elif self.father.held_item in list(power_items.keys()):
				father_to_get = (power_items[self.father.held_item], self.father.IVs[power_items[self.father.held_item]])
				if len(IVs_to_get) == 5 and father_to_get[0] in [k for k,v in IVs_to_get]:
					IVs_to_get = [father_to_get]
					temp_mother_IVs = copy.deepcopy(self.mother.IVs)
					temp_mother_IVs.pop(father_to_get[0])
					temp_mother_IVs = list(temp_mother_IVs.items())
					IVs_to_get += temp_mother_IVs
				else:
					IVs_to_get += [father_to_get]
			if len(IVs_to_get) >= 7:
				IVs_to_get = sorted(IVs_to_get, key=lambda x: x[1])
				IVs_to_get = dict(IVs_to_get)
			elif len(IVs_to_get) == 0:
				IVs_to_get = random.sample(["Health", "Attack", "Defense", "Special Attack", "Special Defense", "Speed"], 2)
				IVs_to_get = [(IVs_to_get[0], self.mother.IVs[IVs_to_get[0]]), (IVs_to_get[1], self.father.IVs[IVs_to_get[1]])]
				IVs_to_get = dict(IVs_to_get)
			IVs_to_get = dict(IVs_to_get)
			self.IVs = {
			"Health": IVs_to_get.get("Health", random.randint(0, 31)),
			"Attack": IVs_to_get.get("Attack", random.randint(0, 31)),
			"Defense": IVs_to_get.get("Defense", random.randint(0, 31)),
			"Special Attack": IVs_to_get.get("Special Attack", random.randint(0, 31)),
			"Special Defense": IVs_to_get.get("Special Defense", random.randint(0, 31)),
			"Speed": IVs_to_get.get("Speed", random.randint(0, 31)),
			}

		else:
			self.IVs = {
			"Health": random.randint(0, 31),
			"Attack": random.randint(0, 31),
			"Defense": random.randint(0, 31),
			"Special Attack": random.randint(0, 31),
			"Special Defense": random.randint(0, 31),
			"Speed": random.randint(0, 31)
			}

	def set_pronouns(self):
		if self.sex == "F":
			self.pronouns = ["She", "Her", "Hers", "Her"]
		elif self.sex == "M":
			self.pronouns = ["He", "His", "His", "Him"]
		else:
			self.pronouns = ["It", "Its", "Its", "It"]

	def set_nature(self, method="r"):
		natures = [
		"Adamant",
		"Bashful",
		"Bold",
		"Brave",
		"Calm",
		"Careful",
		"Docile",
		"Gentle",
		"Hardy",
		"Hasty",
		"Impish",
		"Jolly",
		"Lax",
		"Lonely",
		"Mild",
		"Modest",
		"Naive",
		"Naughty",
		"Quiet",
		"Quirky",
		"Rash",
		"Relaxed",
		"Sassy",
		"Serious",
		"Timid"
		]
		if method in natures:
			self.nature = method
		elif self.mother != "Unknown" and self.father != "Unknown":
			if self.mother.held_item == "Everstone" and self.father.held_item == "Everstone":
				self.nature = random.choice([self.mother.nature, self.father.nature])
			elif self.mother.held_item == "Everstone":
				self.nature = self.mother.nature
			elif self.father.held_item == "Everstone":
				self.nature = self.father.nature
			else:
				self.nature = random.choice(natures)
		else:
			self.nature = random.choice(natures)

	def receive_affection(self, affection_type):
		affection_descriptor = {
			"pet": "petting",
			"hug": "hugging",
			"snuggle": "snuggling",
			"cuddle": "cuddling"
		}
		if affection_type in self.daily_affection:
			print(f"{self.name} seems bored of your {affection_descriptor[affection_type]}.")
		else:
			self.daily_affection.append(affection_type)
			print(f"You reach over and {affection_type} {self.name} with utmost care.")
			self.affection += 1

	def feed(self, food):
		food = food.title()
		if self.fullness >= 25 and self.room == self.trainer.room:
			print(f"{self.name} rejects all offers of food. They're not hungry.")
		else:
			if food not in self.daily_food and food in self.room.inventory:
				self.daily_food.append(self.room.inventory.pop(self.room.inventory.index(food)))
				self.fullness += 10
				self.affection += 2
			elif food not in self.daily_food and self.room == self.trainer.room and food in self.trainer.inventory:
				if self.trainer.check_energy():
					self.trainer.energy -= 1
					self.daily_food.append(self.trainer.inventory.pop(self.trainer.inventory.index(food)))
					self.fullness += 10
					self.affection += 2
			elif food in self.daily_food and food in self.room.inventory:
				self.daily_food.append(self.room.inventory.pop(self.room.inventory.index(food)))
				self.fullness += 5
				self.affection += 1
			elif food in self.daily_food and self.room == self.trainer.room and food in self.trainer.inventory:
				if self.trainer.check_energy():
					self.trainer.energy -= 1
					self.daily_food.append(self.trainer.inventory.pop(self.trainer.inventory.index(food)))
					self.fullness += 5
					self.affection += 1
			else:
				if food not in self.room.inventory and self.room == self.trainer.room:
					if food not in self.trainer.inventory:
						print(f"You don't appear to have a {food.lower()} to feed {self.name}.")

	def new_day(self):
		self.update_loved()
		self.daily_affection = []
		self.daily_food = []
		self.affection = 0
		self.fullness = 0

	def update_loved(self):
		if self.fullness >= 25:
			self.loved += 1
		elif self.fullness <= 0:
			self.loved -= 5
		if self.affection > 0:
			self.loved += int(self.affection/2)
		else:
			self.loved += -5

	def display_genetics(self):
		nametag = "%s the %s" % (self.name, self.species)
		nametag_length = len(nametag)
		specdef_length = 25
		total_length = 1+nametag_length+2+1+specdef_length+2
		print("+%s+" % ("-"*(nametag_length+2)))
		print("| %s |" % (nametag))
		print("+%s+%s" % (("-"*(nametag_length+2)), "" if specdef_length+4 <= nametag_length+4 else "-"*(specdef_length+1) + "+"))
		print("| Pattern:%s%s |" % (" "*(1 if (specdef_length+4)-len("| Pattern:\t%s|" % (self.pattern)) <= 2 else total_length-len("| Pattern:\t%s|" % (self.pattern))), self.pattern))
		print("| Color:%s%s |" % (" "*(1 if (specdef_length+4)-len("| Color:\t%s|" % (self.color)) <= 2 else total_length-len("| Color:\t%s|" % (self.color))), self.color))
		print("| Color Placement:%s%s |" % (" "*(1 if total_length-len("| Color Placement:\t%s|" % (self.color_placement)) <= 2 else total_length-len("| Color Placement:\t%s|" % (self.color_placement))), self.color_placement))
		print("| Color Dilution:%s%s |" % (" "*(1 if total_length-len("| Color Dilution:\t%s|" % (self.color_dilution)) <= 2 else total_length-len("| Color Dilution:\t%s|" % (self.color_dilution))), self.color_dilution))
		print("| Color Extension:%s%s |" % (" "*(1 if total_length-len("| Color Extension:\t%s|" % (self.color_extension)) <= 2 else total_length-len("| Color Extension:\t%s|" % (self.color_extension))), self.color_extension))
		print("| Inheritance:%s%s |" % (" "*(1 if total_length-len("| Inheritance:\t%s|" % (self.inheritance)) <= 2 else total_length-len("| Inheritance:\t%s|" % (self.inheritance))), self.inheritance))
		print("+%s+" % ("-"*(total_length-2)))

	def get_IVs(self):
		nametag = "%s the %s" % (self.name, self.species)
		nametag_length = len(nametag)
		specdef_length = 25
		total_length = 1+nametag_length+2+1+(specdef_length-nametag_length)+2
		print("+%s+" % ("-"*(nametag_length+2)))
		print("| %s |" % (nametag))
		print("+%s+%s" % (("-"*(nametag_length+2)), "" if specdef_length+4 <= nametag_length+4 else "-"*(specdef_length-nametag_length+2) + "+"))
		for k, v in self.IVs.items():
			if v == 0:
				val = "No Good"
			elif v <= 15:
				val = "Decent"
			elif v <= 25:
				val = "Pretty Good"
			elif v <= 29:
				val = "Very Good"
			elif v == 30:
				val = "Fantastic"
			else:
				val = "Best"
			spaces = " "*(total_length-(2+len(k)+len(val)+2))
			print(f"| {k}:{spaces}{val} |")
		print("+"+("-"*(total_length-1))+"+")

	def get_description(self):
		print(self.description)

	def follow(self, following):
		following.entourage.append(self)
		self.following = following

	def unfollow(self, following):
		if self.following:
			following.entourage.pop(following.entourage.index(self))
			self.following = None

	def to_dict(self):
		if self.trainer:
			if type(self.trainer) == type(" "):
				pkmn_trainer = self.trainer
			else:
				pkmn_trainer = self.trainer.trainer_id
		else:
			pkmn_trainer = "None"
		return({
			"species": self.species,
			"pkmn_id": self.pkmn_id,
			"name": self.name,
			"trainer": pkmn_trainer,
			"nature": self.nature,
			"base_stats": self.base_stats,
			"type1": self.type1,
			"type2": self.type2,
			"mother": self.mother if type(self.mother) == type(" ") else self.mother.pkmn_id,
			"father": self.father if type(self.father) == type(" ") else self.father.pkmn_id,
			"egg_group1": self.egg_group1,
			"egg_group2": self.egg_group2,
			"held_item": self.held_item,
			"sex": self.sex,
			"affection": self.affection,
			"daily_affection": self.daily_affection,
			"daily_food": self.daily_food,
			"loved": self.loved,
			"room": self.room if type(self.room) == type(" ") else self.room.room_id,
			"genes": [self.pattern, self.color, self.color_placement, self.color_dilution, self.color_extension, self.inheritance],
			"ivs": list(self.IVs.values())
		})

	@staticmethod
	def from_dict(data):
		species = data["species"]
		cls = pokemon_registry.get(species)
		if cls:
			new_pkmn = cls(data["name"], data["sex"], data["nature"], data["genes"], mother=data["mother"], father=data["father"], pkmn_id=data["pkmn_id"])
			new_pkmn.set_IVs(data["ivs"])
			new_pkmn.trainer = data["trainer"]
			new_pkmn.affection = data["affection"]
			new_pkmn.daily_affection = data["daily_affection"]
			new_pkmn.daily_food = data["daily_food"]
			new_pkmn.held_item = data["held_item"]
			new_pkmn.mother_id = data["mother"]
			new_pkmn.father_id = data["father"]
			return(new_pkmn)
		else:
			print("How did you even... manage to call a non-existing species of Pokemon...")
			# I'll just... return a random Pokemon here...
			return(Pokemon(data["name"], data["sex"], data["nature"], data["genes"], mother=data["mother"], father=data["father"], pkmn_id=data["pkmn_id"]))
