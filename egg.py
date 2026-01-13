from trainer import Trainer
from room import Room
from pokemon_registry import *

class Egg:
    egg_id = {}
    egg_num = 1
    def __init__(self, species, room, mother=None, father=None, steps_remaining=100, egg_id=None):
        self.species = species  # e.g. Bulbasaur
        self.name = "Egg"
        self.mother = mother if isinstance(mother, str) or mother == None else mother.pkmn_id
        self.father = father if isinstance(father, str) or father == None else father.pkmn_id
        self.steps_remaining = steps_remaining
        self.held_by = None
        if mother and not isinstance(mother, str):
            self.trainer = mother.trainer
        elif father and not isinstance(father, str):
            self.trainer = father.trainer
        else:
            self.trainer = list(Trainer.trainer_id.values())[0]
        self.room = room if isinstance(room, Room) else Room.rooms[room]
        self.description = "This large egg has a smooth surface and is awkward to hold due to its size. It is slightly pointed at one side and at the other, it is round and slightly flat. The egg is warm, like something might be alive in there."
        if egg_id:
            self.egg_id = egg_id
        else:
            self.egg_id = f"Egg{Egg.egg_num:08d}"
            Egg.egg_num += 1
        Egg.egg_id[self.egg_id] = self
        if isinstance(room, Room):
            self.room.add_inventory(self.egg_id)

    def move_to_room(self, new_room):
        if self.room and self.egg_id in self.room.inventory:
            self.room.remove_inventory(self.egg_id)
        self.room = new_room
        if not self.held_by:
            new_room.add_inventory(self.egg_id)

    def get_desc(self):
        desc = self.description
        status = ""
        if self.steps_remaining >= 100:
            status = " It will be a while before it hatches. What could be inside?"
        elif self.steps_remaining >= 75:
            status = " It's getting closer to hatching and sometimes it moves around."
        elif self.steps_remaining >= 50:
            status = " A single crack has made itself known on the surface."
        elif self.steps_remaining >= 25:
            status = " Many small cracks splinter off from the larger cracks on its surface."
        elif self.steps_remaining >= 0:
            status = " It's covered in cracks and hints of the egg's membrane are visible within. It's going to hatch at any moment!"
        return(self.description + status)


    def hatch(self):
        species_cls = pokemon_registry.get(self.species)
        if not species_cls:
            raise ValueError(f"Species '{self.species}' is not registered.")
        if list(Trainer.trainer_id.values())[0].room == self.room:
            print(f"You watch in amazement as a {self.species} hatches from an egg right before your very eyes!")
        hatched_pokemon = species_cls(sex="r",pattern="parents",mother=self.mother,father=self.father,hatched_from_egg=True)
        hatched_pokemon.room = self.room
        self.room.add_inventory(hatched_pokemon.pkmn_id)
        hatched_pokemon.set_trainer(self.trainer)
        if self.held_by:
            self.trainer.remove_inventory(self.egg_id)
        return(hatched_pokemon)

    def set_held(self, holder):
        if not holder:
            self.held_by = None
        else:
            self.held_by = holder.trainer_id if isinstance(holder, Trainer) else holder

    def __repr__(self):
        return(f"Egg({self.species})")

    def to_dict(self):
        return({
            "egg_id": self.egg_id,
            "species": self.species,
            "mother": self.mother,
            "father": self.father,
            "holder": self.held_by,
            "steps": self.steps_remaining,
            "room": self.room if isinstance(self.room, str) or self.room == None else self.room.room_id,
            "desc": self.description
        })

    @staticmethod
    def from_dict(data):
        loaded_egg = Egg(data["species"], data["room"], mother=data["mother"], father=data["father"], steps_remaining=data["steps"], egg_id=data["egg_id"])
        loaded_egg.set_held(data["holder"])
        return(loaded_egg)
