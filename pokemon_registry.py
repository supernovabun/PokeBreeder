pokemon_registry = {}

def register_pokemon(cls):
    species = cls.__name__  # e.g., "Bulbasaur"
    pokemon_registry[species] = cls
    return cls