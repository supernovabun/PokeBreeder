import os
import json
from datetime import datetime

class SaveManager:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        os.makedirs(self.save_dir, exist_ok=True)

    def _get_today_date_str(self):
        return(datetime.now().strftime("%Y-%m-%d"))

    def _get_existing_save_numbers(self, date_prefix):
        return([
            int(f.split("_save_")[1].split(".")[0])
            for f in os.listdir(self.save_dir)
            if f.startswith(f"{date_prefix}_save_") and f.endswith(".json")
        ])

    def _generate_save_filename(self):
        date_str = self._get_today_date_str()
        existing_numbers = self._get_existing_save_numbers(date_str)
        next_number = max(existing_numbers, default=0) + 1
        filename = f"{date_str}_save_{next_number:03}.json"
        return(os.path.join(self.save_dir, filename))

    def save_game(self, game_state):
        save_path = self._generate_save_filename()
        with open(save_path, "w") as f:
            json.dump(game_state.to_dict(), f, indent=2)
        print(f"Game saved to {save_path}")

    def load_game(self):
        from game_state import GameState

        saves = sorted([
            f for f in os.listdir(self.save_dir)
            if f.endswith(".json")
        ])

        if not saves:
            print("No save files found.")
            return(None)

        print("\nAvailable save files:")
        for i, filename in enumerate(saves, start=1):
            print(f"{i}. {filename}")

        while True:
            try:
                choice = int(input("\nSelect a save file to load (number): "))
                if 1 <= choice <= len(saves):
                    break
            except ValueError:
                pass
            print("Invalid choice.")

        selected_file = saves[choice - 1]
        path = os.path.join(self.save_dir, selected_file)

        with open(path, "r") as f:
            data = json.load(f)

        return(GameState.from_dict(data))
