# PokeBreeder
This ~~ambitious~~ insane project is for creating a single-player text game where you breed and raise Pokemon! I don't have everything figured out yet, but it's a start.

## Running the Game

1. Download the whole thing. ALL OF IT.
2. Shove it in a folder of your choosing
3. Either open terminal or command prompt in that folder, or open terminal or command prompt and navigate to that folder
4. Enter `python main.py` (make sure you have some version of Python3)

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

### Following mechanics
**Edit:** Psych, I fixed the following mechanics at 4:34 AM EST on 14 Aug 2025. Just gotta upload it!
~~Right now you lose all your Pokemon on quitting (as in they stop following you), but honestly... fair. It's not necessarily something that I need to code.~~

### Individual Pokemon layouts

Before I make more Pokemon: do I want to move the types and base stats to the initialization of the individual species instead of the specific individuals? I think I do...

### Evolution

This needs to create a new instance of next stage of Pokemon, set the IVs the same, the nature the same, the genetics the same, and replace the new Pokemon in its place in the Pokemon list with the same id number but new Pokemon name (Bulbasaur000001 becomes Ivysaur000001).

### More Breeding Mechanics

Gotta create a dictionary called "pkmn_affection" in the Pokemon class to keep track of how different Pokemon feel about each other (gosh this is an awful idea I've started why am I still making this game) so that they don't automatically breed with each other if shoved in a room together. I do know that I want it to be that Pokemon only breed in pastures.
