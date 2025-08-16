from trainer import Trainer
from room import Room
from pokemon_registry import *

class Egg:
    egg_id = {}
    egg_num = 1
    def __init__(self, species, room, mother=None, father=None, days_remaining=100, egg_id=None):
        self.species = species  # e.g. Bulbasaur
        self.name = "Egg"
        self.mother = mother if isinstance(mother, str) or mother == None else mother.pkmn_id
        self.father = father if isinstance(father, str) or father == None else father.pkmn_id
        self.days_remaining = days_remaining
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

    def hatch(self):
        species_cls = pokemon_registry.get(self.species)
        if not species_cls:
            raise ValueError(f"Species '{self.species}' is not registered.")
        if list(Trainer.trainer_id.values())[0].room == self.room:
            print(f"You watch in amazement as a {self.species} hatches from an egg right before your very eyes!")
        return(species_cls(sex="r",pattern="parents",mother=self.mother,father=self.father,hatched_from_egg=True))

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
            "room": self.room if isinstance(self.room, str) or self.room == None else self.room.room_id,
            "desc": self.description,
        })

    @staticmethod
    def from_dict(data):
        loaded_egg = Egg(data["species"], data["room"], mother=data["mother"], father=data["father"], egg_id=data["egg_id"])
        loaded_egg.set_held(data["holder"])
        return(loaded_egg)
