#from indiv import *
from trainer import Trainer
from pokemon import Pokemon ## TEST
from item import Item ## TEST
from room import Room ## TEST
import sys
from save_manager import SaveManager ### this is a test
from game_state import GameState ### this is a test
from commands import CommandParser
from worldgen import generate_world


def main():
	saver = SaveManager()
	first_decision = input("  [1] New Game\n  [2] Load Game\n  [3] Exit\n> ").lower()
	if first_decision in ["one", "new", "1"]:
		player_name = input("What name do you want to go by?\n> ")
		player = Trainer(player_name, None)
		player.room = generate_world("new", player)
		game_state = GameState(player, list(Trainer.trainer_id.values())[1:], list(Pokemon.pkmn_id.values()), list(Room.rooms.values()), list(Item.item_id.values()))
		return(game_state)
	elif first_decision in ["two", "load", "load game", "2"]:
		loaded = saver.load_game()
		if not loaded:
			print("Creating a new game!")
			loaded = Trainer("Player", None)
			loaded.room = generate_world("new", loaded)
			game_state = GameState(loaded, list(Trainer.trainer_id.values())[1:], list(Pokemon.pkmn_id.values()), list(Room.rooms.values()), list(Item.item_id.values()))
		return(loaded)
	else:
		sys.exit()


if __name__ == "__main__":
	game_state = main()
	user = game_state.trainer

	"""
	mom = Ivysaur("Mommy", sex="F")
	dad = Venusaur("Daddy", sex="M")
	# mom.held_item = "Power Weight"
	# dad.held_item = "Destiny Knot"
	myBulba = mom.breed(dad)
	try:
		myBulba.display_genetics()
	except:
		print("No baby made!")
	# print("Mom: %s" % (str(mom.IVs)))
	# print("Dad: %s" % (str(dad.IVs)))
	# print("Baby: %s" % (str(myBulba.IVs)))
	myBulba.get_description()
	myBulba.get_IVs()
	#user = Trainer()
	myBulba.trainer = user
	user.add_pokemon(myBulba)
	myBulba.set_room(myBulba.trainer.room)
	"""

	parser = CommandParser(user)
	#print(myBulba.room.room_id)
	#print(type(myBulba))

	parser.handle_look([])
	while True:
		user_input = input(f"{user.display_energy()} > ")
		parser.parse(user_input)
