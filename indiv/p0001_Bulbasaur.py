from pokemon import Pokemon
from pokemon_registry import register_pokemon
import random

@register_pokemon
class Bulbasaur(Pokemon):
	species = "Bulbasaur"
	def __init__(self, name="", sex="r", nature="r", pattern="r", mother=None, father=None, **kwargs):
		Pokemon.__init__(self, "Bulbasaur", [45, 49, 49, 65, 65, 45], ["Grass", "Poison"], ["Grass", "Monster"], "Spots", **kwargs)
		self.name = name if name != "" else self.species
		if pattern == "r":
			self.random_pattern(pattern_weights=[0.2,0.6,0.2], color_placement_weights=[0.1,0.8,0.1])
		elif type(pattern) != type([]) and mother and father:
			self.mother = mother
			self.father = father
			self.pattern_inheritance(self.mother, self.father)
		else:
			self.pattern = pattern[0]
			self.color = pattern[1]
			self.color_placement = pattern[2]
			self.color_dilution = pattern[3]
			self.color_extension = pattern[4]
			self.inheritance = pattern[5]
		self.sex = random.choices(["F", "M"], weights=[0.125, 0.875], k=1)[0] if sex == "r" else sex
		self.set_pronouns()
		self.set_IVs()
		self.set_nature(nature)
		self.gen_descriptors()

	def gen_descriptors(self):
		pattern_desc = {
		"AA": "spotless murky",
		"A/": "viridian, vaguely triangular spots with",
		"/A": "viridian, vaguely triangular spots with",
		"//": "green splotches with",
		"/a": "lime, rounded spots with",
		"a/": "lime, rounded spots with",
		"aa": "spotless clear",
		"Aa": "spotless smooth",
		"aA": "spotless smooth"
		}
		self.pattern_desc = pattern_desc[self.pattern]
		color_desc = {
		"BB": "forestal",
		"Bb": "green",
		"bB": "green",
		"bb": "mint"
		}
		self.color_desc = color_desc[self.color]
		color_placement_desc = {
		"CC": "obsidian",
		"C/": "bloody-shaded",
		"/C": "bloody-shaded",
		"//": "ruby",
		"/c": "crimson",
		"c/": "crimson",
		"cc": "gold",
		"Cc": "amber",
		"cC": "amber"
		}
		self.color_placement_desc = color_placement_desc[self.color_placement]
		color_dilution_desc = {
		"DD": "vibrant",
		"Dd": "healthy",
		"dD": "healthy",
		"dd": "faded"
		}
		self.color_dilution_desc = color_dilution_desc[self.color_dilution]
		color_extension_desc = {
		"EE": "covered sporadically with small bumps",
		"Ee": "that glistens in the available light",
		"eE": "that glistens in the available light",
		"ee": "that is unmarred"
		}
		self.color_extension_desc = color_extension_desc[self.color_extension]
		inheritance_desc = {
			"None": "",
			"Spots": ""
		}
		self.inheritance_desc = inheritance_desc[self.inheritance]
		# 0 = She/He/It
		# 1 = Her/His/Its
		# 2 = Hers/His/Its
		# 3 = Her/Him/It
		self.description = f"About knee-height and froglike, this {self.species} has {self.pattern_desc} {self.color_dilution_desc} {self.color_desc} flesh {self.color_extension_desc}. {self.pronouns[0]} waddles and hops about the world on four legs that end in three small nails, each bounce making the {self.inheritance_desc}bulb on {self.pronouns[1].lower()} back wiggle. Observing the world with a {self.nature.lower()} {self.color_placement_desc} gaze, {self.pronouns[0].lower()} seems unperturbed by the ongoings of {self.pronouns[1].lower()} surroundings."
