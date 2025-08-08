from room import Room
from item import Item
from indiv import *

def generate_world():
	generate_stages()
	master_bedroom = Room("Master bedroom in a quaint house")
	master_bedroom.set_verbose("A cozy room bearing no hints of profession, there isn't much space to move around. A bed covered in maroon blankets sits against the wall, underneath the lone window in the room. Next to it is a small wooden night table, leaving just enough room to climb into bed. The floor is soft cream-colored carpet, and the walls, a faint baby blue.")
	starting_backpack = Item("A worndown leather backpack", "Misc.", master_bedroom, 50, container=True)
	starting_backpack.set_desc("Leather makes up the majority of this dark brown backpack. It features one large main pocket with a flap and snap for closure, and another smaller pocket on the front with another snap for closure. Two straps that have begun to fray allow for easy wear.")

	main_hallway = Room("A narrow hallway")
	main_hallway.set_verbose("There is little room to maneuver through this hallway. Getting around requires walking sideways and even then the average person or Pokemon is prone to bumping into the wall or passing doorknob. Against all wisdom, a painting is hung here - a testament to the intelligence of its hanger as it requires ducking to get past.")
	hallway_painting = Item("A juvenile watercolor painting", "Art", main_hallway, 200)
	hallway_painting.set_desc("Blotches and spots of watercolor mark a warped piece of lined paper. Whether the depicted shapes were meant to be abstract art or a more defined form is up for interpretation by the viewer. The paper, taped to cardboard, sits inside a dusty, ornate wooden frame. The artist's shaky, pencil-written initials reside in the lower right corner of the cardboard.")

	master_bedroom.set_exits({"east": main_hallway})
	main_hallway.set_exits({"west": master_bedroom})
	return(master_bedroom)

def generate_stages():
	Bulbasaur.stages = [Bulbasaur, Ivysaur, Venusaur]
	Ivysaur.stages = [Bulbasaur, Ivysaur, Venusaur]
	Venusaur.stages = [Bulbasaur, Ivysaur, Venusaur]
