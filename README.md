# PokeBreeder
This ~~ambitious~~ insane project is for creating a single-player text game where you breed and raise Pokemon! I don't have everything figured out yet, but it's a start.

## Currently...

As of writing this, you can run main.py without error (unless you're creative). You can move between a few rooms I've created, you have a Bulbasaur that's just sitting in your bedroom, and there's a painting in the hallway and a secret in another room. You can also look at Bulbasaur, your debug-mom, the rooms, and any objects I've put in. You can grab the painting too, but why would you ever do that? You can also speak, but nothing really cool happens there... unless...

## Features
* [ ] Tutorials
* [ ] All the breedable Pokemon:
  * [ ] Kanto
  * [ ] Johto
  * [ ] Hoenn
  * [ ] Sinnoh
  * [ ] Unova
  * [ ] Kalos
  * [ ] Alola
  * [ ] Galar
  * [ ] Paldea
* [x] Breeding - Basic
* [ ] Breeding - Advanced
* [ ] Evolution
* [ ] Currency System
* [ ] Quests System
* [x] Energy System
* [x] Save System

## To Work On

### Egg

Gotta make eggs. Not sure how best to do this. Maybe as a subclass of Pokemon... probably as a subclass of Pokemon...

### Evolution

This needs to create a new instance of next stage of Pokemon, set the IVs the same, the nature the same, the genetics the same, and replace the new Pokemon in its place in the Pokemon list with the same id number but new Pokemon name (Bulbasaur000001 becomes Ivysaur000001).
