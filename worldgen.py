from room import Room
from item import Item
from trainer import Trainer
from indiv import *
from pokemon_registry import *

def generate_world(player_type, player):
	generate_stages()
	if player_type == "new":
		starting_stage = new_world(player)
	else:
		print("How did you even get into this code block?")
		starting_stage = new_world(player)
	return(starting_stage)

def new_world(player):
	print("Welcome to the wonderful world of Pokemon!")
	print("Through some method or another to be decided later, you got a Pokemon! You're getting a Bulbasaur, to be precise.")
	print("In the future, you'll be able to choose from:")
	player_starter_pkmn = list_starters()

	starting_room = new_home(player)

	aether = Room("Aether", id_num="Aether000")
	aether.set_verbose("How did you even get in here!?")
	aether.set_exits({"out":starting_room})

	#############
	### DEBUG ###
	#############
	mom = Ivysaur("Mommy", sex="F")
	dad = Venusaur("Daddy", sex="M")
	testBulba = mom.breed(dad)
	testBulba.set_trainer(player)
	player.add_pokemon(testBulba)
	testBulba.set_room(room=starting_room)
	### end debug
	### the debug should be replaced when we make it so that you can actually pick your starter but there's a cool *253* starters to pick from so that'll be a while

	return(starting_room)

def new_home(player):
	home_master_bedroom = Room("Master bedroom in a quaint house")
	home_master_bedroom.set_verbose("A cozy room bearing no hints of profession, there isn't much space to move around. A bed covered in maroon blankets sits against the wall, underneath the lone window in the room. Next to it is a small wooden night table, leaving just enough room to climb into bed. The floor is soft cream-colored carpet, and the walls, a faint baby blue.")
	starting_backpack = Item("A worndown leather backpack", "Misc.", home_master_bedroom, 50, container=True)
	starting_backpack.set_desc("Leather makes up the majority of this dark brown backpack. It features one large main pocket with a flap and snap for closure, and another smaller pocket on the front with another snap for closure. Two straps that have begun to fray allow for easy wear.")

	home_main_hallway = Room("A narrow hallway")
	home_main_hallway.set_verbose("There is little room to maneuver through this hallway. Getting around requires walking sideways and even then the average person or Pokemon is prone to bumping into the wall or passing doorknob. Against all wisdom, a painting is hung here - a testament to the intelligence of its hanger as it requires ducking to get past. The wooden floor offers a chance for splinters.")
	hallway_painting = Item("A juvenile watercolor painting", "Art", home_main_hallway, 200)
	hallway_painting.set_desc("Blotches and spots of watercolor mark a warped piece of lined paper. Whether the depicted shapes were meant to be abstract art or a more defined form is up for interpretation by the viewer. The paper, taped to cardboard, sits inside a dusty, ornate wooden frame. The artist's shaky, pencil-written initials reside in the lower right corner of the cardboard.")

	home_upstairs_bathroom = Room("A small, uncomfortable bathroom")
	home_upstairs_bathroom.set_verbose("The stale air in this insufficiently-sized room is marked by the distinct aroma of water. Best efforts to keep this room clean and neat have been done. The lone window on the far wall is open to let some much-needed fresh air inside. The toilet-sink combination sits below a bathroom mirror, and directly adjacent to the combination is a tub that is too small for any adult to sit in comfortably.")
	home_upstairs_toilet = Item("Toilet with a sink on top", "Furniture", home_upstairs_bathroom, 26000, gettable=False, container=True)
	home_upstairs_toilet.set_desc("A porcelain throne with a wooden seat has a strange attachment: atop and connected to the toilet's tank is a simple sink. The bowl of the sink and the bowl of the toilet itself both have been kept in pristine condition. The plumbing device awaits further use.")
	home_upstairs_rubber_ducklett = Item("A periwinkle rubber Ducklett", "Misc.", None, 50)
	home_upstairs_rubber_ducklett.set_desc("Small and a lovely periwinkle color, this rubber Ducklett has all the features of its live counterpart made of industrial-grade plastic. Its stylized face with two large beady black eyes stare out vacantly, and its wings are folded against its body. On the bottom of the rubber Ducklett is an embossed mark reading PM with a Poke Ball in the loop of the P.")
	home_upstairs_tub = Item("Tiny tub for a smaller person", "Furniture", home_upstairs_bathroom, 100000, gettable=False, container=True)
	home_upstairs_tub.set_desc("Every effort has been made to try to maintain the cleanliness of a tub made for someone far smaller than the average adult human. The white interior is stained, and the metal handles and faucet, rusty. Marks are present indicating that someone tried at least once to remove the grime and age from the tub.")
	home_upstairs_tub.inventory = [home_upstairs_rubber_ducklett.item_id]
	home_upstairs_rubber_ducklett.in_somewhere = home_upstairs_tub
	
	home_stairs_top = Room("The top of the stairs")
	home_stairs_top.set_verbose("Brought on a draft, cool air makes its way up a half-turned flight of oak stairs. On one side is a bannister with chipped wood, and the other, a wall covered in floral wallpaper. Much like the bannister, the wooden floor here is chipped, waiting for the chance to lodge pieces of itself in some unsuspecting foot.")

	home_den = Room("Spacious family den")
	home_den.set_verbose("Large and spacious, this room was recently painted a deep red color that further enhances the warm feeling. A steady flow of air circulates through the room that keeps it at a slightly warm, but not hot, temperature. In the center of the room is a large in-ground sectional couch with a small set of steps descending into a small adjacent space that has room for up to eight people to sit. Towards the back of the room is an oak staircase lined with a too-old wooden bannister. The staircase turns halfway and ascends past where can be seen.")
	tempmom = Trainer(f"Your Mother", home_den) ## TEST
	tempmom.set_desc("A pleasant woman with her long black hair pulled into a side braid.") ## TEST

	home_master_bedroom.set_exits({"east": home_main_hallway})
	home_main_hallway.set_exits({"west": home_master_bedroom, "north": home_stairs_top, "east": home_upstairs_bathroom})
	home_upstairs_bathroom.set_exits({"west": home_main_hallway})
	home_stairs_top.set_exits({"south": home_main_hallway, "down": home_den})
	home_den.set_exits({"up": home_stairs_top})

	return(home_master_bedroom)

def generate_stages():
	Bulbasaur.stages = [Bulbasaur, Ivysaur, Venusaur]
	Ivysaur.stages = [Bulbasaur, Ivysaur, Venusaur]
	Venusaur.stages = [Bulbasaur, Ivysaur, Venusaur]

def list_starters():
	starter_list = [
		"Wishiwashi",
		"Sunkern",
		"Blipbug",
		"Snom",
		"Azurill",
		"Kricketot",
		"Caterpie",
		"Weedle",
		"Wurmple",
		"Ralts",
		"Magikarp",
		"Feebas",
		"Scatterbug",
		"Pichu",
		"Igglybuff",
		"Wooper",
		"Paldean Wooper",
		"Tyrogue",
		"Bounsweet",
		"Tarountula",
		"Nymble",
		"Sentret",
		"Cleffa",
		"Poochyena",
		"Lotad",
		"Seedot",
		"Happiny",
		"Burmy",
		"Wimpod",
		"Makuhita",
		"Bunnelby",
		"Zigzagoon",
		"Galarian Zigzagoon",
		"Whismur",
		"Rolycoly",
		"Pawmi",
		"Toxel",
		"Combee",
		"Zubat",
		"Togepi",
		"Starly",
		"Noibat",
		"Rookidee",
		"Nickit",
		"Wiglett",
		"Spinarak",
		"Hoppip",
		"Slugma",
		"Swinub",
		"Smeargle",
		"Bidoof",
		"Fomantis",
		"Gossifleur",
		"Pidgey",
		"Rattata",
		"Alolan Rattata",
		"Yungoos",
		"Lechonk",
		"Patrat",
		"Charcadet",
		"Flittle",
		"Skitty",
		"Wynaut",
		"Venipede",
		"Applin",
		"Smoliv",
		"Spearow",
		"Hoothoot",
		"Shinx",
		"Pidove",
		"Diglett",
		"Alolan Diglett",
		"Ledyba",
		"Pikipek",
		"Hatenna",
		"Impidimp",
		"Nincada",
		"Surskit",
		"Dewpider",
		"Taillow",
		"Wingull",
		"Wooloo",
		"Yamper",
		"Milcery",
		"Dreepy",
		"Rellor",
		"Tadbulb",
		"Nidoran Female",
		"Nidoran Male",
		"Cherubi",
		"Lillipup",
		"Tynamo",
		"Litwick",
		"Skwovet",
		"Bramblin",
		"Fletchling",
		"Mareep",
		"Slakoth",
		"Meditite",
		"Budew",
		"Roggenrola",
		"Cottonee",
		"Petilil",
		"Rockruff",
		"Arrokuda",
		"Nacli",
		"Wattrel",
		"Purrloin",
		"Chewtle",
		"Paras",
		"Chingling",
		"Riolu",
		"Morelull",
		"Ekans",
		"Barboach",
		"Inkay",
		"Helioptile",
		"Meowth",
		"Alolan Meowth",
		"Galarian Meowth",
		"Pineco",
		"Trapinch",
		"Spheal",
		"Bonsly",
		"Gothita",
		"Solosis",
		"Shroodle",
		"Greavard",
		"Munna",
		"Sandile",
		"Tympole",
		"Foongus",
		"Horsea",
		"Shroomish",
		"Electrike",
		"Shuppet",
		"Duskull",
		"Blitzle",
		"Tinkatink",
		"Vulpix",
		"Alolan Vulpix",
		"Sandshrew",
		"Alolan Sandshrew",
		"Poliwag",
		"Bellsprout",
		"Geodude",
		"Alolan Geodude",
		"Dratini",
		"Snubbull",
		"Remoraid",
		"Larvitar",
		"Baltoy",
		"Snorunt",
		"Bagon",
		"Beldum",
		"Bronzor",
		"Gible",
		"Croagunk",
		"Minccino",
		"Klink",
		"Deino",
		"Goomy",
		"Grubbin",
		"Jangmo-o",
		"Varoom",
		"Gimmighoul",
		"Gulpin",
		"Yamask",
		"Galarian Yamask",
		"Golett",
		"Flabebe",
		"Bergmite",
		"Cutiefly",
		"Capsakid",
		"Venonat",
		"Mankey",
		"Machop",
		"Shellder",
		"Smoochum",
		"Carvanha",
		"Numel",
		"Timburr",
		"Ducklett",
		"Vanillite",
		"Ferroseed",
		"Cubchoo",
		"Shelmet",
		"Mareanie",
		"Sizzlipede",
		"Tandemaus",
		"Binacle",
		"Fennekin",
		"Corphish",
		"Snivy",
		"Tepig",
		"Oshawott",
		"Sinistea",
		"Poltchageist",
		"Charmander",
		"Cyndaquil",
		"Chimchar",
		"Phantump",
		"Abra",
		"Doduo",
		"Gastly",
		"Treecko",
		"Torchic",
		"Mudkip",
		"Swablu",
		"Glameow",
		"Mime Jr.",
		"Sewaddle",
		"Grookey",
		"Scorbunny",
		"Sobble",
		"Clobbopus",
		"Sprigatito",
		"Fuecoco",
		"Quaxly",
		"Fidough",
		"Chespin",
		"Squirtle",
		"Totodile",
		"Piplup",
		"Froakie",
		"Slowpoke",
		"Galarian Slowpoke",
		"Darumaka",
		"Galarian Darumaka",
		"Karrablast",
		"Silicobra",
		"Finizen",
		"Pansage",
		"Pansear",
		"Panpour",
		"Bulbasaur",
		"Chikorita",
		"Turtwig",
		"Joltik",
		"Oddish",
		"Psyduck",
		"Cubone",
		"Goldeen",
		"Natu",
		"Axew",
		"Skrelp",
		"Rowlet",
		"Litten",
		"Popplio",
		"Salandit",
		"Sandygast",
		"Frigibax",
		"Woobat"
	]
	starters = []
	starter_list_split = int((len(starter_list)-1)/3) + (1 if (len(starter_list)-1)%3 > 0 else 0)
	for i, starter_pkmn in enumerate(starter_list, start=1):
		starter_string = f"[{i:03d}] {starter_pkmn}{" "*(19-len(starter_pkmn))}"
		if i-1 < starter_list_split:
			starters.append((" "*5) + starter_string)
		else:
			starters[(i-1)%starter_list_split] += starter_string
	print("\n".join(starters))
	print("Just curious, who'd you pick, though?")
	while True:
		user_input = input("> ")
		if user_input.title() in starter_list:
			return(user_input.title())
			False
		elif user_input.isdigit():
			user_input = int(user_input)
			if user_input in range(1, len(starter_list)+1):
				return(starter_list[user_input-1])
				False
			else:
				print(f"Please enter a number from 1 to {len(starter_list)} or one of the specific Pokemon mentioned.")
		else:
			print(f"Please enter a number from 1 to {len(starter_list)} or one of the specific Pokemon mentioned.")
