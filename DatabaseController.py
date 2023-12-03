import json
import os
from typing import List, Tuple, Union
import Monster

import jsobject  # Import JSObject from the relevant module

class DatabaseController:
    def __init__(self):
        current_relative_path = os.path.abspath("")
        self.current_path_string = os.path.join(current_relative_path)
        
        self.dex_data_url = self.current_path_string + "/dex.json"
        self.move_data_url = self.current_path_string + "/move.json"
        self.ability_data_url = self.current_path_string + "/ability.json"
        self.item_data_url = self.current_path_string + "/items.json"
       
        self.dex_data = os.path.join(self.current_path_string, self.dex_data_url)
        self.move_data = os.path.join(self.current_path_string, self.move_data_url)
        self.ability_data = os.path.join(self.current_path_string, self.ability_data_url)
        self.item_data = os.path.join(self.current_path_string, self.item_data_url)

        self.dex_js_object = None
        self.move_js_array = None
        self.ability_js_object = None
        self.item_js_object = None

        self.exists = self.check_files_exist()
        self.built = False

    def build(self) -> bool:
        
        try:
            # Dex Object building
            with open(self.dex_data, "r", encoding="utf-8") as f:
                dex_json_txt = f.read()
                self.dex_js_object = json.loads(dex_json_txt)

            # Move Object building
            with open(self.move_data, "r", encoding="utf-8") as f:
                move_json_txt = f.read()
                move_js_object = json.loads(move_json_txt)
                self.move_js_array = move_js_object["Array"]

            # Ability Object building
            with open(self.ability_data, "r", encoding="utf-8") as f:
                ability_json_txt = f.read()
                self.ability_js_object = json.loads(ability_json_txt)

            # Item object building
            with open(self.item_data, "r", encoding="utf-8") as f:
                item_json_txt = f.read()
                self.item_js_object = json.loads(item_json_txt)
                
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return False
        except Exception as e:
            print(f"Error reading dex.json: {e}")
            return False

        self.built = True
        return True

    def get_monster_json_by_dex_id(self, dex_id: int) -> json:
        if not self.dex_js_object:
            print("Error: dex_js_object is None.")
            return None

        keys = list(self.dex_js_object.keys())
        index = keys[dex_id-1]
        return self.dex_js_object.get(index)


    def get_monster_by_dex_id(self, dex_id: int) -> Monster:
        monster_json = self.get_monster_json_by_dex_id(dex_id)

        if not monster_json:
            print(f"Error: Could not retrieve monster JSON for dex_id {dex_id}.")
            return None

        new_monster = Monster.Monster()
        try:
            # Set the name
            new_monster.nameStr = monster_json["Name"]
            # Set the typing
            new_monster.type = monster_json["Type"]
            # Set the stat array
            new_monster.baseStats = monster_json["Base Stats"]
            
            # Set the known moves
            known_moves_index = list(monster_json["Move List"])
            known_moves = [self.move_js_array[i] for i in known_moves_index]
            new_monster.setMoveList(known_moves)
            new_monster.levelUp(20)
            new_monster.setMonsterStats()
            new_monster.generate_health()
            

        except KeyError as ke:
            print(f"Error: Missing key in monster JSON - {ke}")
            return None

        except TypeError as te:
            print(f"Error: Type mismatch in monster JSON - {te}")
            return None

        return new_monster


    def check_files_exist(self) -> bool:
        return all(
            [os.path.exists(self.move_data), os.path.exists(self.ability_data), os.path.exists(self.dex_data), os.path.exists(self.item_data)]
        )

    def get_move_data(self) -> str:
        return self.move_data

    def set_move_data(self, move_data: str) -> None:
        self.move_data = move_data

    def get_ability_data(self) -> str:
        return self.ability_data

    def set_ability_data(self, ability_data: str) -> None:
        self.ability_data = ability_data

    def get_dex_data(self) -> str:
        return self.dex_data

    def set_dex_data(self, dex_data: str) -> None:
        self.dex_data = dex_data

    def get_item_data(self) -> str:
        return self.item_data

    def set_item_data(self, item_data: str) -> None:
        self.item_data = item_data

    def is_exists(self) -> bool:
        return self.exists

    def set_exists(self, exists: bool) -> None:
        self.exists = exists
