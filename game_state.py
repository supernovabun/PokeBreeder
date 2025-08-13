from trainer import Trainer
from egg import Egg
from pokemon import Pokemon
from room import Room
from item import Item
from worldgen import generate_stages

class GameState:
    def __init__(self, trainer, created_trainers, created_eggs, created_pokemon, created_rooms, created_items):
        self.trainer = trainer
        self.created_trainers = created_trainers # List of Trainer instances
        self.created_eggs = created_eggs         # List of Egg instances
        self.created_pokemon = created_pokemon   # List of Pokemon instances
        self.created_rooms = created_rooms       # List of Room instances
        self.created_items = created_items       # List of Item instances

    def to_dict(self):
        return({
            "trainer": self.trainer.to_dict(),
            "created_trainers": [t.to_dict() for t in self.created_trainers],
            "created_eggs": [e.to_dict() for e in self.created_eggs],
            "created_pokemon": [p.to_dict() for p in self.created_pokemon],
            "created_rooms": [r.to_dict() for r in self.created_rooms],
            "created_items": [i.to_dict() for i in self.created_items]
        })

    @staticmethod
    def from_dict(data):
        created_rooms = [Room.from_dict(r) for r in data["created_rooms"]]
        trainer = Trainer.from_dict(data["trainer"])
        created_trainers = [Trainer.from_dict(t) for t in data["created_trainers"]]
        created_pokemon = [Pokemon.from_dict(p) for p in data["created_pokemon"]]
        created_eggs = [Egg.from_dict(e) for e in data["created_eggs"]]
        created_items = [Item.from_dict(i) for i in data["created_items"]]

        trainer.room = trainer.room if type(trainer.room) != type(" ") else Room.rooms[trainer.room]

        Trainer.trainer_id = {}
        Trainer.trainer_id[trainer.trainer_id] = trainer
        for index in range(len(created_trainers)):
            t_id = created_trainers[index].trainer_id
            Trainer.trainer_id[t_id] = created_trainers[index]
            Trainer.trainer_id[t_id].room = Room.rooms[created_trainers[index].room]

        for index in range(len(created_items)):
            created_items[index].room = created_items[index].room if created_items[index].room else None
            created_items[index].in_somewhere = Item.item_id[created_items[index].in_somewhere_string] if created_items[index].in_somewhere_string else created_items[index].in_somewhere_string

        for index in range(len(created_rooms)):
            for k, v in created_rooms[index].exits.items():
                created_rooms[index].exits[k] = Room.rooms[v]

        for pkmn in created_pokemon:
            pkmn.trainer = Trainer.trainer_id[pkmn.trainer] if pkmn.trainer != "None" else pkmn.trainer

        trainer_pkmn = {}
        for pkmn in trainer.pokemon:
            trainer_pkmn[pkmn] = Pokemon.pkmn_id[pkmn]
            trainer_pkmn[pkmn].set_room(trainer_pkmn[pkmn].room)
        trainer.pokemon = trainer_pkmn

        Item.item_id = {}
        for each_item in created_items:
            Item.item_id[each_item.item_id] = each_item

        for each_trainer in Trainer.trainer_id.values():
            each_trainer.pokemon = dict(zip(each_trainer.pokemon, [Pokemon.pkmn_id[each_pkmn] for each_pkmn in each_trainer.pokemon]))
            each_trainer.set_room()

        generate_stages()

        return(GameState(trainer, created_trainers, created_eggs, created_pokemon, created_rooms, created_items))
