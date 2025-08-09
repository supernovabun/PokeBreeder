from room import Room
from item import Item
from indiv import *

def generate_world():
	generate_stages()
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
	
	home_stairs_top = Room("The top of the stairs")
	home_stairs_top.set_verbose("Brought on a draft, cool air makes its way up a half-turned flight of oak stairs. On one side is a bannister with chipped wood, and the other, a wall covered in floral wallpaper. Much like the bannister, the wooden floor here is chipped, waiting for the chance to lodge pieces of itself in some unsuspecting foot.")

	home_master_bedroom.set_exits({"east": home_main_hallway})
	home_main_hallway.set_exits({"west": home_master_bedroom, "north": home_stairs_top, "east": home_upstairs_bathroom})
	home_upstairs_bathroom.set_exits({"west": home_main_hallway})
	home_stairs_top.set_exits({"south": home_main_hallway})
	return(home_master_bedroom)

def generate_stages():
	Bulbasaur.stages = [Bulbasaur, Ivysaur, Venusaur]
	Ivysaur.stages = [Bulbasaur, Ivysaur, Venusaur]
	Venusaur.stages = [Bulbasaur, Ivysaur, Venusaur]
