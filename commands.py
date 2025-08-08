import re
import sys
from pokemon import Pokemon
from item import Item

class CommandParser:

	def __init__(self, player):
		self.player = player
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
			"score": self.handle_status
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
					else:
						desc_thing = Pokemon.pkmn_id[thing].description
				elif desc_thing == "" and args[0].lower() == re.findall("^[a-zA-Z \\-\\']+", thing)[0].lower():
					desc_thing = Pokemon.pkmn_id[thing].description if thing in Pokemon.pkmn_id.keys() else Item.item_id[thing].get_desc()
				elif desc_thing == "" and re.findall(" ".join(args).title(), thing) != []:
					desc_thing = Pokemon.pkmn_id[thing].description if thing in Pokemon.pkmn_id.keys() else Item.item_id[thing].get_desc()
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
			self.player.room = self.player.room.exits[cmd]
			for each_item in self.player.inventory:
				each_item = Item.item_id[each_item]
				each_item.room = self.player.room
			self.player.room.display()
		else:
			print(f"As much as you wish to head {cmd}, you cannot.")

	def handle_affection(self, user_cmd, args):
		if not args:
			print(f"What are you trying to {user_cmd}?")
		else:
			for thing in self.player.room.inventory:
				if args[0].title() == thing and thing in Pokemon.pkmn_id.keys():
					Pokemon.pkmn_id[thing].receive_affection(user_cmd)
					return
				elif args[0] == re.findall("\\d{6}$", thing)[0]:
					if thing in Pokemon.pkmn_id.keys():
						Pokemon.pkmn_id[thing].receive_affection(user_cmd)
						return
					else:
						print(f"That's not a Pokemon you're trying to {user_cmd}...")
						return
				elif args[0].title() == re.findall("^[a-zA-Z \\-\\']+", thing)[0]:
					if thing in Pokemon.pkmn_id.keys():
						Pokemon.pkmn_id[thing].receive_affection(user_cmd)
						return
					else:
						print("That's not a Pokemon you're trying to pet...")
						return
				else:
					print(f"Args: {args}")
					print(f"Present:{thing}")
					return

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
			elif [pkmn for pkmn in pkmn_present if re.findall("\\d{6}$", args[0])] != 0:
				pkmn = [pkmn for pkmn in pkmn_present if re.findall("\\d{6}$", pkmn) != []][0]
				if args[1]:
					food = " ".join(args[1:]).title()
					Pokemon.pkmn_id[pkmn].feed(food)
				else:
					print(f"What are you trying to feed to {pkmn[:-6]}?")
			elif args[0].title() in [pkmn for pkmn in pkmn_present if re.findall("^[a-zA-Z \\-\\']+", args[0].title())]:
				pkmn = [pkmn for pkmn in pkmn_present if re.findall("^[a-zA-Z \\-\\']+", args[0].title()) != []][0]
				if args[1]:
					food = " ".join(args[1:]).title()
					Pokemon.pkmn_id[pkmn].feed(food)
				else:
					print(f"What are you trying to feed to {pkmn[:-6]}?")
			else:
				print(f"The Pokemon you're looking for - {args[0].title()} - is not present.")

	def handle_say(self, args):
		CYAN = "\033[36m"
		RESET = "\033[0m"
		if len(args) < 1:
			print("You open your mouth, but you say nothing.")
		else:
			spoken = " ".join([args[0][0].upper()+args[0][1:]] + args[1:])
			if spoken[-1] not in ["?", ".", "!"]:
				spoken += "."
			print(f'{CYAN}You say, "{spoken}{RESET}"')
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
			if args[0] in self.player.room.inventory and args[0] not in Pokemon.pkmn_id.keys():
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
				from_where_item = Item.item_id[from_where]
			else:
				print(f"There is nothing around by name of {from_where}.")
			if [i for i in from_where_item.inventory if re.findall(to_get, i) != []] != []:
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
					where_put = [w for w in self.player.room.inventory if re.findall(where_put, w) != []]
					where_put = Item.item_id[where_put]
				else:
					print(f"Where are you trying to put {to_put.lower()}?")
					return
				if [i for i in self.player.inventory if re.findall(to_put, i) != []] != []:
					to_put = [i for i in self.player.inventory if re.findall(to_put, i) != []][0]
					to_put = Item.item_id[to_put]
					if where_put.container:
						self.player.remove_inventory(to_put.item_id)
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
					where_put = Item.item_id[where_put]
				else:
					print(f"Where are you trying to put {to_put.lower()}")
					return
				if [i for i in self.player.inventory if re.findall(to_put, i) != []] != []:
					to_put = [i for i in self.player.inventory if re.findall(to_put, i) != []][0]
					to_put = Item.item_id[to_put]
					self.player.remove_inventory(to_put.item_id)
				else:
					print(f"You are not holding {self.get_article(to_put)}{to_put.lower()}.")
					return
				where_put.add_inventory(to_put)
			else:
				print(f"Where are you trying to put {self.get_article(" ".join(args))}{" ".join(args)}? Did you forget IN?")
				return

	def handle_status(self, args):
		pass

	def handle_quit(self, args):
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
