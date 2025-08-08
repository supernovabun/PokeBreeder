from indiv import *
from trainer import Trainer
from commands import CommandParser
from worldgen import generate_world

user = Trainer("Player", generate_world())

if __name__ == "__main__":
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
	myBulba.set_room(myBulba.trainer.room)

	parser = CommandParser(user)
	#print(myBulba.room.room_id)
	#print(type(myBulba))
	while True:
		user_input = input("> ")
		parser.parse(user_input)