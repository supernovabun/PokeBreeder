from trainer import Trainer
from egg import Egg
from pokemon import Pokemon
from room import Room
from item import Item
from worldgen import generate_stages

class GameState:
    MONTHS = [
    ("January", 31),
    ("February", 28),
    ("March", 31),
    ("April", 30),
    ("May", 31),
    ("June", 30),
    ("July", 31),
    ("August", 31),
    ("September", 30),
    ("October", 31),
    ("November", 30),
    ("December", 31),
    ]
    def __init__(self, trainer, created_trainers, created_eggs, created_pokemon, created_rooms, created_items, day=1):
        self.trainer = trainer
        self.created_trainers = created_trainers # List of Trainer instances
        self.created_eggs = created_eggs         # List of Egg instances
        self.created_pokemon = created_pokemon   # List of Pokemon instances
        self.created_rooms = created_rooms       # List of Room instances
        self.created_items = created_items       # List of Item instances
        self.day = day

    def advance_day(self):
        self.day += 1

        for pokemon in Pokemon.pkmn_id.values():
            pokemon.new_day()

        for trainer in Trainer.trainer_id.values():
            trainer.on_new_day()

        return(self.get_date())

    def get_months_for_year(self, year):
        months = GameState.MONTHS[:]
        if year % 4 == 0:
            months[1] = ("February", 29)
        return(months)

    def get_date(self):
        total_days = self.day

        year = 1
        days_passed = 0

        while True:
            months = self.get_months_for_year(year)

            year_days = sum(length for name, length in months)
            if total_days <= (year_days - 90):  # -90 to start at April 1
                break

            total_days -= year_days
            year += 1

        months = months[3:] + months[:3]  # Start from April

        for month_name, days_in_month in months:
            if total_days <= days_in_month:
                return(f"{total_days:02d} {month_name} Year {year:03d}")
            total_days -= days_in_month

        # Fallback
        return(f"??? (Error in date calculation)")

    def to_dict(self):
        return({
            "trainer": self.trainer.to_dict(),
            "created_trainers": [t.to_dict() for t in self.created_trainers],
            "created_eggs": [e.to_dict() for e in self.created_eggs],
            "created_pokemon": [p.to_dict() for p in self.created_pokemon],
            "created_rooms": [r.to_dict() for r in self.created_rooms],
            "created_items": [i.to_dict() for i in self.created_items],
            "created_day": self.day
        })

    @staticmethod
    def from_dict(data):
        created_rooms = [Room.from_dict(r) for r in data["created_rooms"]]
        trainer = Trainer.from_dict(data["trainer"])
        created_trainers = [Trainer.from_dict(t) for t in data["created_trainers"]]
        created_pokemon = [Pokemon.from_dict(p) for p in data["created_pokemon"]]
        created_eggs = [Egg.from_dict(e) for e in data["created_eggs"]]
        created_items = [Item.from_dict(i) for i in data["created_items"]]
        created_day = data["created_day"]

        trainer.room = trainer.room if type(trainer.room) != type(" ") else Room.rooms[trainer.room]
        trainer.entourage = [Pokemon.pkmn_id[pkmn_id] for pkmn_id in trainer.entourage]

        Trainer.trainer_id = {}
        Trainer.trainer_id[trainer.trainer_id] = trainer
        for index in range(len(created_trainers)):
            t_id = created_trainers[index].trainer_id
            Trainer.trainer_id[t_id] = created_trainers[index]
            Trainer.trainer_id[t_id].room = Room.rooms[created_trainers[index].room]
            new_ent = []
            for pkmn_id in Trainer.trainer_id[t_id].entourage:
                new_ent.append(Pokemon.pkmn_id[pkmn_id])
            Trainer.trainer_id[t_id].entourage = new_ent

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

        return(GameState(trainer, created_trainers, created_eggs, created_pokemon, created_rooms, created_items, created_day))
