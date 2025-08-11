import re
import sys
from pokemon import Pokemon
from trainer import Trainer
from room import Room
from item import Item
from save_manager import SaveManager ## TEST
from game_state import GameState ## TEST

class CommandParser:

	def __init__(self, player):
		self.player = player
		self.saver = SaveManager()
		self.commands = {
			"look": self.handle_look,
			"l": self.handle_look,
			"north": self.handle_move,
			"n": self.handle_move,
			"northeast": self.handle_move,
			"ne": self.handle_move,
			"east": self.handle_move,
			"e": self.handle_move,
			"southeast": self.handle_move,
			"se": self.handle_move,
			"south": self.handle_move,
			"s": self.handle_move,
			"southwest": self.handle_move,
			"sw": self.handle_move,
			"west": self.handle_move,
			"w": self.handle_move,
			"northwest": self.handle_move,
			"nw": self.handle_move,
			"in": self.handle_move,
			"out": self.handle_move,
			"up": self.handle_move,
			"down": self.handle_move,
			"pet": self.handle_affection,
			"hug": self.handle_affection,
			"cuddle": self.handle_affection,
			"snuggle": self.handle_affection,
			"say": self.handle_say,
			"yes": self.handle_yes,
			"no": self.handle_no,
			"feed": self.handle_feed,
			"exit": self.handle_quit,
			"quit": self.handle_quit,
			"qq": self.handle_quit,
			"here": self.handle_here,
			"ih": self.handle_here,
			"ii": self.handle_inventory,
			"inv": self.handle_inventory,
			"inventory": self.handle_inventory,
			"get": self.handle_get,
			"take": self.handle_get,
			"drop": self.handle_drop,
			"place": self.handle_drop,
			"put": self.handle_put,
			"stat": self.handle_status,
			"status": self.handle_status,
			"score": self.handle_status,
			"help": self.handle_help,
			"sleep": self.handle_sleep,
			"use": self.handle_use,
			"lose": self.handle_lose,
			"ent": self.handle_entourage,
			"entourage": self.handle_entourage,
			"save": self.handle_save
		}

	def parse(self, text):
		directions = [
		"n", "north", 
		"ne", "northeast", 
		"e", "east", 
		"se", "southeast", 
		"s", "south", 
		"sw", "southwest", 
		"w", "west", 
		"nw", "northwest", 
		"up", 
		"down", 
		"in", 
		"out"
		]
		affections = [
		"pet",
		"cuddle",
		"snuggle",
		"hug"
		]
		parts = text.strip().split()
		if not parts:
			print("Try that again?")
			return
		cmd = parts[0].lower()
		args = parts[1:]
		if cmd in self.commands and cmd not in directions and cmd not in affections:
			self.commands[cmd](args)
		elif cmd in directions:
			self.commands[cmd](cmd)
		elif cmd in affections:
			self.commands[cmd](cmd, args)
		else:
			print(f"What is {parts[0]}ing?")

	def handle_look(self, args):
		if not args:
			self.player.room.display()
		else:
			desc_thing = ""
			for thing in self.player.room.inventory:
				if " ".join(args).title() == thing and thing in Item.item_id.keys():
					desc_thing = Item.item_id[thing].get_desc()
					break
				elif desc_thing == "" and args[0] == re.findall("\\d+$", thing)[0]:
					if thing in Item.item_id.keys():
						desc_thing = Item.item_id[thing].get_desc()
					elif thing in Pokemon.pkmn_id.keys():
						desc_thing = Pokemon.pkmn_id[thing].description
					else:
						desc_thing = Trainer.trainer_id[thing].description
				elif desc_thing == "" and args[0].lower() == re.findall("^[a-zA-Z \\-\\']+", thing)[0].lower():
					if thing in Pokemon.pkmn_id.keys():
						desc_thing = Pokemon.pkmn_id[thing].description
					elif thing in Item.item_id.keys():
						desc_thing = Item.item_id[thing].get_desc()
					elif thing in Trainer.trainer_id.keys():
						desc_thing = Trainer.trainer_id[thing].description
					else:
						desc_thing = ""
				elif desc_thing == "" and re.findall(" ".join(args).title(), thing) != []:
					if thing in Pokemon.pkmn_id.keys():
						desc_thing = Pokemon.pkmn_id[thing].description
					elif thing in Item.item_id.keys():
						desc_thing = Item.item_id[thing].get_desc()
					elif thing in Trainer.trainer_id.keys():
						desc_thing = Trainer.trainer_id[thing].description
					else:
						desc_thing = ""
			if desc_thing == "":
				for thing in self.player.inventory:
					if " ".join(args).title() == thing:
						desc_thing = Item.item_id[thing].get_desc()
						break
					elif desc_thing == "" and args[0] == re.findall("\\d+$", thing)[0]:
						desc_thing = Item.item_id[thing].get_desc()
					elif desc_thing == "" and args[0].lower() == re.findall("^[a-zA-Z \\-\\']+", thing)[0].lower():
						desc_thing = Item.item_id[thing].get_desc()
					elif desc_thing == "" and re.findall(" ".join(args).title(), thing) != []:
						desc_thing = Item.item_id[thing].get_desc()
			desc_thing = desc_thing if desc_thing != "" else "What are you trying to look at?"
			print(desc_thing)

	def handle_move(self, user_cmd):
		if user_cmd == "n":
			cmd = "north"
		elif user_cmd == "ne":
			cmd = "northeast"
		elif user_cmd == "e":
			cmd = "east"
		elif user_cmd == "se":
			cmd = "southeast"
		elif user_cmd == "s":
			cmd = "south"
		elif user_cmd == "sw":
			cmd = "southwest"
		elif user_cmd == "w":
			cmd = "west"
		elif user_cmd == "nw":
			cmd = "northwest"
		else:
			cmd = user_cmd
		if cmd in self.player.room.exits.keys():
			if self.player.check_energy():
				self.player.energy -= 1
				self.player.room = self.player.room.exits[cmd]
				for each_item in self.player.inventory:
					each_item = Item.item_id[each_item]
					each_item.room = self.player.room
				for each_pkmn in self.player.entourage:
					each_pkmn.room.remove_inventory(each_pkmn.pkmn_id)
					each_pkmn.room = self.player.room
					self.player.room.add_inventory(each_pkmn.pkmn_id)
				self.player.room.display()
			else:
				return
		else:
			print(f"As much as you wish to head {cmd}, you cannot.")

	def handle_affection(self, user_cmd, args):
		if not args:
			print(f"What are you trying to {user_cmd}?")
		else:
			pkmn_present = [pkmn for pkmn in self.player.room.inventory if re.findall("^[a-zA-Z \\-\\']+\\d{6}$", pkmn) != []]
			for pkmn in pkmn_present:
				if args[0].title() == pkmn:
					if self.player.check_energy():
						self.player.energy -= 1
						Pokemon.pkmn_id[pkmn].receive_affection(user_cmd)
					return
				elif args[0] in re.findall("\\d{6}$", pkmn):
					if self.player.check_energy():
						self.player.energy -= 1
						Pokemon.pkmn_id[pkmn].receive_affection(user_cmd)
					return
				elif args[0].title() in re.findall("^[a-zA-Z \\-\\']+", pkmn):
					if self.player.check_energy():
						self.player.energy -= 1
						Pokemon.pkmn_id[pkmn].receive_affection(user_cmd)
					return
			print("That's not a Pokemon you're trying to pet...")

	def handle_feed(self, args):
		if len(args) == 0:
			print("What are you trying to feed what food?")
		elif len(args) == 1:
			print(f"What are you trying to feed to {args[0].title()}?")
		else:
			pkmn_present = [i for i in self.player.room.inventory if re.findall("\\d{6}$", i) != []]
			if args[0].title() in pkmn_present and args[0].title() in Pokemon.pkmn_id.keys():
				if args[1]:
					Pokemon.pkmn_id[args[0]].feed(" ".join(i.title() for i in args[1:]))
				else:
					print(f"What are you trying to feed to {args[0][:-6]}")
			elif args[0].title() in pkmn_present and args[0].title() not in Pokemon.pkmn_id.keys():
				print(f"There is no such {args[0][:-6]} that exists - is that a ghost?")
			elif [pkmn for pkmn in pkmn_present if re.findall(f"{args[0]}$", pkmn) != []] != []:
				pkmn = [pkmn for pkmn in pkmn_present if re.findall(f"{args[0]}$", pkmn) != []][0]
				if args[1]:
					food = " ".join(args[1:]).title()
					food = [f for f in self.player.inventory if re.findall(food, f) != []][0]
					if Item.item_id[food].item_type == "Food":
						Pokemon.pkmn_id[pkmn].feed(food)
					else:
						print("Why are you trying to feed Pokemon inedible objects?")
				else:
					print(f"What are you trying to feed to {pkmn[:-6]}?")
			elif [pkmn for pkmn in pkmn_present if re.findall(f"^{args[0].title()}", pkmn) != []]:
				pkmn = [pkmn for pkmn in pkmn_present if re.findall("^[a-zA-Z \\-\\']+", args[0].title()) != []][0]
				if args[1]:
					food = " ".join(args[1:]).title()
					if [f for f in self.player.inventory if re.findall(food, f) != []] != []:
						food = [f for f in self.player.inventory if re.findall(food, f) != []][0]
						if Item.item_id[food].item_type == "Food":
							Pokemon.pkmn_id[pkmn].feed(food)
						else:
							print("Why are you trying to feed Pokemon inedible objects?")
					else:
						print(f"You're not holding any {food.lower()} to feed {Pokemon.pkmn_id[pkmn].name}.")
				else:
					print(f"What are you trying to feed to {pkmn[:-6]}?")
			else:
				print(f"The Pokemon you're looking for - {args[0].title()} - is not present.")

	def handle_say(self, args):
		CYAN = "\x1b[38;5;51m"
		RESET = "\033[0m"
		if len(args) < 1:
			print("You open your mouth, but you say nothing.")
		else:
			spoken = " ".join([args[0][0].upper()+args[0][1:]] + args[1:])
			if spoken[-1] not in ["?", ".", "!"]:
				spoken += "."
			print(f'{CYAN}You say, "{spoken}"{RESET}')
			if "follow" in args or "Follow" in args:
				follow = "follow" if "follow" in args else "Follow"
				args = args[args.index(follow)+1:]
				if "me" in args or "me," in args:
					me = "me" if "me" in args else "me,"
					pkmn_to_follow = re.sub("\\.\\?\\!", "", " ".join(args[args.index(me)+1:]).title())
					pkmn_present = [Pokemon.pkmn_id[thing] for thing in self.player.room.inventory if re.findall("\\d{6}$", thing) != []]
					pkmn_present_species = {}
					for pkmn in pkmn_present:
						if pkmn.species in pkmn_present_species.keys():
							pkmn_present_species[pkmn.species] += 1
						else:
							pkmn_present_species[pkmn.species] = 1
					pkmn_present_species = [f"{v} {k}" for k, v in pkmn_present_species.items()]
					if pkmn_to_follow:
						pkmn_to_follow = [pkmn for pkmn in pkmn_present if re.findall(pkmn_to_follow, pkmn.name) and pkmn.trainer == self.player]
						if pkmn_to_follow:
							if pkmn_to_follow[0] not in self.player.entourage:
								pkmn_to_follow[0].follow(self.player)
							print(f"{pkmn_to_follow[0].name} falls in line behind you.")
						else:
							print(f"The {", ".join(pkmn_present_species)} here look at you with confused expressions.")
					else:
						pkmn_to_follow = [pkmn for pkmn in pkmn_present if pkmn.trainer == self.player]
						if pkmn_to_follow:
							for pkmn in pkmn_to_follow:
								if pkmn not in self.player.entourage:
									pkmn.follow(self.player)
							print("Your Pokemon follow closely behind you.")
						elif pkmn_present:
							print(f"The {", ".join(pkmn_present_species)} look up curiously.")
						else:
							pass
			return(spoken)

	def handle_yes(self, args):
		print("You nod your head in the affirmative.")
		return(True)

	def handle_no(self, args):
		print("You shake your head in the negative.")
		return(False)

	def handle_here(self, args):
		room_brief = self.player.room.brief
		room_article = self.get_article(room_brief.split(" "))
		print(f"The following things are in {room_article}{room_brief[:-1].lower()}:")
		for i in self.player.room.inventory:
			print(f"  {i}")

	def handle_inventory(self, args):
		print("You take a look at what you're carrying on you:")
		self.player.check_inventory()

	def handle_get(self, args):
		if len(args) == 1:
			if args[0].title() in self.player.room.inventory and args[0].title() not in Pokemon.pkmn_id.keys():
				if not Item.item_id[args[0]].gettable:
					print(f"Try as you might, you cannot pick up {Item.item_id[args[0]].get_article()}{args[0]}.")
					return
				if self.player.check_energy():
					self.player.energy -= 1
					to_remove = self.player.room.remove_inventory(args[0])
					item_article = self.get_article(to_remove)
					self.player.add_inventory(to_remove)
					print(f"You pick up {item_article}{to_remove}.")
			elif [i for i in self.player.room.inventory if re.findall(args[0].title(), i) != []] != []:
				to_remove = [i for i in self.player.room.inventory if re.findall(args[0].title(), i) != []]
				to_remove = [i for i in to_remove if i not in Pokemon.pkmn_id.keys()]
				if len(to_remove) == 0:
					print("What are you trying to take? No picking up Pokemon!")
				elif len(to_remove) > 1:
					print(f"Did you mean to get one of these? {", ".join(to_remove)}")
				else:
					if to_remove[0] in Item.item_id.keys() and not Item.item_id[to_remove[0]].gettable:
						print(f"Try as you might, you cannot pick up {Item.item_id[to_remove[0]].get_article()}{Item.item_id[to_remove[0]].name.lower()}.")
						return
					elif to_remove[0] not in Item.item_id.keys():
						print(f"You can't pick up {to_remove[0]}")
						return
					if self.player.check_energy():
						self.player.energy -= 1
						to_remove = self.player.room.remove_inventory(to_remove[0])
						item_article = self.get_article(to_remove)
						self.player.add_inventory(to_remove)
						print(f"You pick up {item_article}{to_remove[:-4].lower()}.")
		elif "from" in args:
			to_get = " ".join(args[:args.index("from")]).title()
			from_where = " ".join(args[args.index("from")+1:]).title()
			if [w for w in self.player.inventory if re.findall(from_where, w) != []] != []:
				from_where = [w for w in self.player.inventory if re.findall(from_where, w) != []][0]
				from_where_item = Item.item_id[from_where]
			elif [w for w in self.player.room.inventory if re.findall(from_where, w) != []] != []:
				from_where = [w for w in self.player.room.inventory if re.findall(from_where, w) != []][0]
				if re.findall("[a-zA-Z \\'\\,\\-]+\\d\\d$") != []:
					from_where_item = Item.item_id[from_where]
				else:
					print("You cannot take things from people, especially not without their permission!")
			else:
				print(f"There is nothing around by name of {from_where}.")
			if [i for i in from_where_item.inventory if re.findall(to_get, i) != []] != []:
				if self.player.check_energy():
					self.player.energy -= 1
					to_get = [i for i in from_where_item.inventory if re.findall(to_get, i) != []][0]
					to_get = Item.item_id[to_get]
					from_where_item.remove_inventory(to_get.item_id)
					print(f"You take out {to_get.get_article()}{to_get.name.lower()} from {from_where_item.get_article()}{from_where_item.name.lower()}.")
			else:
				print(f"{from_where_item.name[0]+from_where_item.name[1:].lower()} does not hold {self.get_article(to_get)}{to_get.lower()}.")
				return
			self.player.add_inventory(to_get)
			if len(self.player.inventory) > 10:
				self.handle_drop(to_get.item_id)
		else:
			get_string = " ".join([arg.title() for arg in args])
			if get_string in self.player.room.inventory and get_string not in Pokemon.pkmn_id.keys():
				if self.player.check_energy():
					self.player.energy -= 1
					to_remove = self.player.room.remove_inventory(get_string)
					item_article = self.get_article(to_remove)
					self.player.add_inventory(to_remove)
					print(f"You pick up {item_article}{to_remove}.")

	def handle_drop(self, args):
		if len(args) >= 1:
			if args[0] in ["all", "everything"]:
				to_drop = self.player.inventory[:]
				if len(to_drop) == 0:
					print("You throw your hands out towards the ground to no effect.")
				else:
					to_drop = self.player.remove_inventory(to_drop)
					self.player.room.add_inventory(to_drop)					
					print(f"You drop {self.get_article(to_drop[0])}{to_drop[0][:-4].lower()}." if len(to_drop) == 1 else "You throw everything you have to the floor.")
			elif " ".join(args).title() in self.player.inventory:
				to_drop = " ".join(args)
				to_drop = self.player.remove_inventory(to_drop)
				self.player.room.add_inventory(to_drop)					
				print(f"You drop {self.get_article(to_drop[0])}{to_drop[0][:-4].lower()}.")
			elif [i for i in self.player.inventory if re.findall(" ".join(args).title(), i) != []] != []:
				to_drop = " ".join(args).title()
				to_drop = [i for i in self.player.inventory if re.findall(to_drop, i) != []]
				to_drop = to_drop[0]
				to_drop = self.player.remove_inventory(to_drop)
				self.player.room.add_inventory(to_drop)					
				print(f"You drop {self.get_article(to_drop[0] if type(to_drop) != type("string") else to_drop)}{to_drop[0][:-4].lower() if type(to_drop) != type("string") else to_drop[:-4].lower()}.")
			else:
				print(f"You do not have {self.get_article(" ".join(args))}{" ".join(args)} to drop.")
		else:
			print("You make a dropping gesture with your hands, but quickly put them back together." if len(self.player.inventory) == 0 else "You nearly drop everything you're holding, but manage to catch everything in time.")

	def handle_put(self, args):
		if args[-1] in ["ground", "floor"]:
			if args[-2] in ["in", "on"]:
				self.handle_drop(args[:-2])
		else:
			if "in" in args:
				to_put = " ".join(args[:args.index("in")]).title()
				where_put = " ".join(args[args.index("in")+1:]).title()
				if [w for w in self.player.inventory if re.findall(where_put, w) != []] != []:
					where_put = [w for w in self.player.inventory if re.findall(where_put, w) != []][0]
					where_put = Item.item_id[where_put]
				elif [w for w in self.player.room.inventory if re.findall(where_put, w) != []] != []:
					where_put = [w for w in self.player.room.inventory if re.findall(where_put, w) != []][0]
					where_put = Item.item_id[where_put] if where_put in Item.item_id.keys() else Pokemon.pkmn_id[where_put]
				else:
					print(f"Where are you trying to put {to_put.lower()}?")
					return()
				if [i for i in self.player.inventory if re.findall(to_put, i) != []] != []:
					to_put = [i for i in self.player.inventory if re.findall(to_put, i) != []][0]
					to_put = Item.item_id[to_put]
					if isinstance(where_put, Item) and where_put.container:
						if self.player.check_energy():
							self.player.energy -= 1
							self.player.remove_inventory(to_put.item_id)
						else:
							return
					else:
						print(f"You can't put items into {where_put.name}!")
						return
				else:
					print(f"You are not holding {self.get_article(to_put)}{to_put.lower()}.")
					return
				where_put.add_inventory(to_put)
			elif len(args) == 2:
				to_put = args[0].title()
				where_put = args[1].title()
				if [w for w in self.player.inventory if re.findall(where_put, w) != []] != []:
					where_put = [w for w in self.player.inventory if re.findall(where_put, w) != []][0]
					where_put = Item.item_id[where_put]
				elif [w for w in self.player.room.inventory if re.findall(where_put, w) != []] != []:
					where_put = [w for w in self.player.room.inventory if re.findall(where_put, w) != []]
					where_put = Item.item_id[where_put] if where_put in Item.item_id.keys() else Pokemon.pkmn_id[where_put]
				else:
					print(f"Where are you trying to put {to_put.lower()}")
					return
				if [i for i in self.player.inventory if re.findall(to_put, i) != []] != []:
					to_put = [i for i in self.player.inventory if re.findall(to_put, i) != []][0]
					to_put = Item.item_id[to_put]
					if self.player.check_energy():
						self.player.energy -= 1
						self.player.remove_inventory(to_put.item_id)
					else:
						return
				else:
					print(f"You are not holding {self.get_article(to_put)}{to_put.lower()}.")
					return
				where_put.add_inventory(to_put)
			else:
				print(f"Where are you trying to put {self.get_article(" ".join(args))}{" ".join(args)}? Did you forget IN?")
				return

	def handle_status(self, args):
		pass

	def handle_sleep(self, args):
		self.player.sleep()

	def handle_use(self, args):
		if not args:
			print("Try as you might, you cannot use yourself.")
		else:
			to_use = " ".join(args[0:]).title()
			if [thing for thing in self.player.room.inventory if re.findall(to_use, thing) != []] != []:
				to_use = [thing for thing in self.player.room.inventory if re.findall(to_use, thing) != []][0]
				if to_use in Item.item_id.keys():
					to_use = Item.item_id[to_use]
				else:
					print("You can't use a Pokemon like that!")
					return
			elif [thing for thing in self.player.inventory if re.findall(to_use, thing) != []] != []:
				to_use = [thing for thing in self.player.inventory if re.findall(to_use, thing) != []][0]
				if to_use in Item.item_id.keys():
					to_use = Item.item_id[to_use]
				else:
					print("You can't use a Pokemon like that!")
					return
			else:
				print(f"You can't use {to_use.lower()} no matter how hard you try.")
				return
			if re.findall("[Tt]oilet", to_use.name):
				to_flush = ", ".join(to_use.inventory).lower()
				to_flush = re.sub("\\d", "", to_flush)
				[to_use.remove_inventory(item) for item in to_use.inventory]
				to_flush = to_flush if to_flush == "" else f" You watch in mild amusement as {to_flush} slowly spirals down the drain, vanishing before your very eyes into the piping through some miracle."
				print(f"You pull down on the lever to flush {to_use.get_article()}{to_use.name.lower()}.{to_flush}")

	def handle_lose(self, args):
		if not args:
			print("What are you trying to have stop following you?")
		else:
			to_lose = " ".join(args).title()
			pkmn_entourage = [i for i in self.player.entourage]
			pkmn = [p for p in pkmn_entourage if re.findall(to_lose, p.pkmn_id) != []]
			pkmn = pkmn if pkmn else [p for p in pkmn_entourage if re.findall(to_lose, p.name) != []]
			pkmn = pkmn if pkmn else None
			if pkmn:
				pkmn[0].unfollow(self.player)
				print(f"{pkmn[0].name} stops following you.")
			elif args[0] == "all":
				[p.unfollow(self.player) for p in pkmn_entourage]
				print("Everyone decides to stop following you.")
			else:
				print(f"It doesn't appear {to_lose} is following you.")

	def handle_entourage(self, args):
		print(f"The following Pokemon are following you:\n  {"\n  ".join([pkmn.pkmn_id for pkmn in self.player.entourage])}")

	def handle_help(self, args):
		GREEN = "\033[92m"
		RESET = "\033[0m"
		if not args:
			print(f"{GREEN}Need help with commands? This is the spot for you. Here's a list of all available commands:{RESET}")
			print(f"{GREEN}{", ".join(sorted(self.commands.keys()))}{RESET}")
		else:
			if args[0] in self.commands.keys():
				if args[0] in ["l", "look"]:
					print(f"{GREEN}Syntax: l, look\nTargetted: optional\nDisplays a description of whatever you're looking at.{RESET}")
				elif args[0] in ["n", "north", "ne", "northeast", "e", "east", "se", "southeast", "s", "south", "sw", "southwest", "w", "west", "nw", "northwest", "up", "down", "in", "out"]:
					print(f"{GREEN}Syntax: n, north, ne, northeast, e, east, se, southeast, s, south, sw, southwest, w, west, nw, northwest, up, down, in, out\nTargetted: No\nMoves your player in a given direction - provided there's an exit for it.{RESET}")
				elif args[0] in ["pet", "cuddle", "snuggle", "hug"]:
					print(f"{GREEN}Syntax: pet, cuddle, snuggle, hug\nTargetted: Required (pet <Pokemon>)\nDote affection on your Pokemon to build up trust and care.{RESET}")
				elif args[0] == "say":
					print(f"{GREEN}Syntax: say\nTargetted: No (say I like to talk!)\nSay whatever you like, but watch out! People might be listening!{RESET}")
				elif args[0] in ["yes", "no"]:
					print(f"{GREEN}Syntax: yes, no\nTargetted: No\nRespond to the world around you with a nod or shake of your head.{RESET}")
				elif args[0] == "feed":
					print(f"{GREEN}Syntax: feed\nTargetted: Required (feed <Pokemon> <food>)\nHow you make sure you don't starve your Pokemon every day. Remember to feed them regularly!{RESET}")
				elif args[0] in ["exit", "qq", "quit"]:
					print(f"{GREEN}Syntax: exit, qq, quit\nTargetted: No\nHow you close out of the game.{RESET}")
				elif args[0] in ["here", "ih"]:
					print(f"{GREEN}Syntax: here, ih\nTargetted: No\nSee what items are present.{RESET}")
				elif args[0] in ["inventory", "inv", "ii"]:
					print(f"{GREEN}Syntax: inventory, inv, ii\nTargetted: No\nLook at your personal inventory.{RESET}")
				elif args[0] in ["get", "take"]:
					print(f"{GREEN}Syntax: get, take\nTargetted: Yes (get <item>(from <container>))\nPick up an item from the ground or take an item out of a container.{RESET}")
				elif args[0] in ["drop", "place"]:
					print(f"{GREEN}Syntax: drop, place\nTargetted: No (drop <item>)\nLet an item fall to the ground.{RESET}")
				elif args[0] == "put":
					print(f"{GREEN}Syntax: put\nTargetted: Yes (put <item> in <container>)\nPut an item into a container.{RESET}")
				elif args[0] in ["stat", "status", "score"]:
					print(f"{GREEN}Syntax: status, stat, score\nTargetted: no\nShows some information about yourself.{RESET}")
				elif args[0] == "help":
					print(f"{GREEN}Syntax: help\nTargetted: No (help( <command>))\nYOU ARE HERE! Reveals the help system. Without a command, it'll list all the available commands.{RESET}")
				elif args[0] == "sleep":
					print(f"{GREEN}Syntax: sleep\nTargetted: No\nGets some energy back. Best to do this in a room with a bed...{RESET}")
				else:
					print(f"{GREEN}Someone forgot to program the rest of these help lines in...{RESET}")
			else:
				print(f"{GREEN}I cannot help you with the sort of help you need...{RESET}")

	def handle_save(self, args):
		if not args:
			trainer_ids = list(Trainer.trainer_id.values())[1:]
			pkmn_ids = list(Pokemon.pkmn_id.values())
			room_ids = list(Room.rooms.values())
			item_ids = list(Item.item_id.values())
			save_state = GameState(self.player, trainer_ids, pkmn_ids, room_ids, item_ids)
			self.saver.save_game(save_state)
		pass

	def handle_quit(self, args):
		self.handle_save(args)
		print("You decide it's time for a break and to tend to yourself. Your Pokemon will eagerly await your return.")
		sys.exit()

	def get_article(self, args):
		if args[0] in ["The", "A", "An"]:
			article = ""
		elif args[0][0] in ["A", "E", "I", "O", "U"]:
			article = "an "
		else:
			article = "a "
		return(article)
