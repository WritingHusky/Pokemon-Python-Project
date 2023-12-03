import logging
from Monster import Monster
import random
from ReactionHandler import ReactionHandler
from BattleField import BattleField

class Battler:
    def __init__(self):
        try:
            self.logger = logging.getLogger("BattlerLogger")
            
            file_handler = logging.FileHandler(filename="battler.log")
            file_handler.setLevel(logging.INFO)
            self.logger.addHandler(file_handler)
            self.reaction_handler:ReactionHandler

        except (IOError) as e:
            print(e)
    def get_move_list(self, active_mon:Monster):
        return active_mon.getMovelist()

    def do_attack(self, reaction_handler:ReactionHandler, battle_field, attacking_monster:Monster, attacking_move:dict[str, any], defending_monster:Monster, auto_hit = False):
        # See if the move happens (implement later)
        self.reaction_handler = reaction_handler
        # Get the move effects
        move_effect_array = attacking_move["effects"]
        move_effect_count = len(move_effect_array)
        move_type = attacking_move["Type"]

        # Do the effects of the move (looping point)
        for i in range(move_effect_count):
            current_effect = move_effect_array[i]
            current_effect_type = current_effect["EffectType"]
            case_mapping = {
                "Damage": self.do_damage_attack,
                "State": self.do_state_attack,
                "Alter": self.do_alter_attack
            }
            # Handle default case
            default_case = lambda: self.logger.log(logging.INFO, f"Invalid move Effect found: {current_effect_type}\nFound in move:\n{attacking_move}")
            case_mapping.get(current_effect_type, default_case)(battle_field, attacking_monster, current_effect, defending_monster, move_type, auto_hit = auto_hit)
            
            self.reaction_handler.handle_results(attacking_monster, defending_monster, attacking_move)

    def do_damage_attack(self, battle_field, attacking_monster:Monster, current_effect:dict[str,any], defending_monster:Monster, attacking_type:str, auto_hit = False):
        # TODO Add stat change info to output

        # Get effect info
        attack_result = current_effect["Result"]
        attack_value = current_effect["Value"]

        # Set the relevant variables
        attack_stat, defense_stat, move_damage = 0, 0, 0
        monster_stats = attacking_monster.getAlterStats()
        type_mult = self.type_advantage(attacking_type, defending_monster.type)

        # Do the result according to the MoveEffect List
        if attack_result == "Physical Damage":
            attack_stat, defense_stat = monster_stats[1], monster_stats[2]
            move_damage = self.damage_calc(attacking_monster.level, False, attack_value, attack_stat, defense_stat, False, type_mult)
            self.reaction_handler.set_off_trigger_by_code("Damage-Physical")
        elif attack_result == "Special Damage":
            attack_stat, defense_stat = monster_stats[3], monster_stats[4]
            move_damage = self.damage_calc(attacking_monster.level, False, attack_value, attack_stat, defense_stat, False, type_mult)
            self.reaction_handler.set_off_trigger_by_code("Damage-Special")
        elif attack_result == "Set Damage":
            move_damage = round(defending_monster.maxHP * (attack_value / 100))
        elif attack_result == "OHKO":
            if self.random_check(attack_value, auto_hit = auto_hit):
                move_damage = defending_monster.maxHP + 1
            else:
                move_damage = 0  # If OHKO fails then nothing happens
        elif attack_result == "Heal":
            # Healing is actually negative damage
            move_damage = -round(defending_monster.maxHP / (attack_value / 100))
        else:
            self.logger.log(logging.INFO, f"Invalid Damage Effect: {attack_result}")
            return

        # System.out.println("Move does: " + move_damage)

        self.reaction_handler.set_off_trigger_by_code("Damage")
        # Apply the damage to the defender
        defending_monster.doDamage(move_damage)

        # Check to set the death reaction flag
        if defending_monster.currentHP <= 0:
            self.reaction_handler.set_off_trigger_by_code("Pokemon-Death")
            
    def do_alter_attack(self, battle_field:BattleField, attacking_monster:Monster, current_effect:dict[str,any], defending_monster:Monster, attacking_type:str, auto_hit = False):
        # TODO Implement 
        """
        Does not use inputed monsters
        Will use them for reactions 
        """
        attack_result = current_effect["Result"]
        attack_value = current_effect["Value"]

        switch_result = {
            "Weather": self.handle_weather,
            "Terrain": self.handle_terrain,
            "Switch Out": self.handle_switch_out,
            "Trap": self.handle_trap,
            "Hazard Set": self.handle_hazard_set,
            "Hazard Clear": self.handle_hazard_clear
        }

        # Execute the corresponding function based on the attackResult
        switch_result.get(attack_result, lambda: self.logger.log(logging.INFO, f"Invalid Alter Effect: {attack_result}"))(attack_value, battle_field)

    def handle_weather(self, attack_value, battleField):
        # Implement logic for handling weather alteration
        switch_weather = {
            0: self.clear_weather,
            1: self.harsh_sunlight,
            2: self.rain,
            3: self.sandstorm,
            4: self.snow,
            5: self.fog
        }
        # Execute the corresponding function based on the attackValue
        switch_weather.get(attack_value, lambda: None)(battleField)
        battleField.weather_change = True

    def clear_weather(self,battleField:BattleField):
        # Implement logic for clearing weather
        battleField.weather = 0
        pass

    def harsh_sunlight(self,battleField:BattleField):
        # Implement logic for harsh sunlight
        battleField.weather = 1
        pass

    def rain(self,battleField:BattleField):
        # Implement logic for rain
        battleField.weather = 2
        pass

    def sandstorm(self,battleField:BattleField):
        # Implement logic for sandstorm
        battleField.weather = 3
        pass

    def snow(self,battleField:BattleField):
        # Implement logic for snow
        battleField.weather = 4
        pass

    def fog(self,battleField):
        # Implement logic for fog
        battleField.weather = 5
        pass

    def handle_terrain(self, attack_value:int, battleField:BattleField):
        battleField.terrain = attack_value 
        battleField.terrain_change = True
        # Implement logic for handling terrain alteration
        pass

    def handle_switch_out(self, attack_value:int,battleField:BattleField):
        # Implement logic for handling switch out
        pass

    def handle_trap(self, attack_value:int,battleField:BattleField):
        # Implement logic for handling trap
        battleField.trap = attack_value
        battleField.trap_change = True
        pass

    def handle_hazard_set(self, attack_value:int,battleField:BattleField):
        # Implement logic for setting hazards
        battleField.hazard = attack_value
        pass

    def handle_hazard_clear(self, attack_value:int,battleField:BattleField):
        # Implement logic for clearing hazards
        battleField.hazard = 0
        pass

    def do_state_attack(self, battle_field, attacking_monster:Monster, current_effect:dict[str,any], defending_monster:Monster, attacking_type:str, auto_hit = False):
        attack_result = current_effect["Result"]
        attack_value = current_effect["Value"]

        switch_result = {
            "MultiTurn": self.multi_turn,
            "Status": self.handle_status,
            "Flinch": self.handle_flinch,
            "Form Change": self.handle_form_change,
            "Item Manipulation": self.handle_item_manipulation,
            "Stat Change": self.handle_stat_change
        }

        # Execute the corresponding function based on the attackResult
        switch_result.get(attack_result, lambda: self.logger.log(logging.INFO, f"Invalid State attack Effect: {attack_result}"))( defending_monster, attack_value, auto_hit = auto_hit)

        self.reaction_handler.set_off_trigger_by_code("StateAttack")

    def multi_turn(self, defending_monster:Monster, attack_value:int,auto_hit = False):
        defending_monster.multiMoveTimer = attack_value
        self.reaction_handler.set_result_by_code("Move-MultiTurn", defending_monster.monsterCode)

    def handle_status(self, defending_monster:Monster, attack_value:int,auto_hit = False):
        switch_status = {
            0: lambda: self.reaction_handler.set_result_by_code("Clear", defending_monster.monsterCode),
            1: lambda: self.reaction_handler.set_result_by_code("Burn", defending_monster.monsterCode),
            2: lambda: self.reaction_handler.set_result_by_code("Freeze", defending_monster.monsterCode),
            3: lambda: self.reaction_handler.set_result_by_code("Paralysis", defending_monster.monsterCode),
            4: lambda: self.reaction_handler.set_result_by_code("Poison", defending_monster.monsterCode),
            5: lambda: self.reaction_handler.set_result_by_code("Badly Poison", defending_monster.monsterCode),
            6: lambda: self.sleep(defending_monster)
        }
        # Execute the corresponding function based on the attackValue
        switch_status.get(attack_value, lambda: self.logger.log(logging.INFO, f"Invalid Code for the Status effect: {attack_value}"))()

    def sleep(self, defending_monster:Monster):
        defending_monster.sleepTimer = (random.random() * 3) + 1
        self.reaction_handler.set_result_by_code("Sleep", defending_monster.monster_code)

    def handle_flinch(self, defending_monster:Monster, attack_value:int,auto_hit = False):
        if self.random_check(attack_value, auto_hit= auto_hit):
            defending_monster.useNothingMove = True

    def handle_form_change(self, defending_monster, attack_value,auto_hit = False):
        self.reaction_handler.set_off_trigger_by_code("Form-Change")

    def handle_item_manipulation(self, defending_monster:Monster, attack_value:int, auto_hit = False):
        switch_item_manipulation = {
            1: self.remove_item,
            2: self.give_item,
            3: self.exchange_items
        }
        # Execute the corresponding function based on the attackValue
        switch_item_manipulation.get(attack_value, lambda: self.logger.log(logging.INFO, f"Invalid Item Manipulation code: {attack_value}"))()

    def remove_item(self):
        # Implement logic for removing item
        pass

    def give_item(self):
        # Implement logic for giving item
        pass

    def exchange_items(self):
        # Implement logic for exchanging items
        pass

    def handle_stat_change(self, defending_monster:Monster, attack_value:int, auto_hit = False):
        stat_index = abs(attack_value % 10)
        stat_change = (attack_value - stat_index) // 10
        defending_monster.alterStats(stat_index, stat_change)
        self.reaction_handler.set_off_trigger_by_code("Stat-Change")
        
    def speed_check(self, player_monster:Monster, player_move:dict[str, any], enemy_monster:Monster, enemy_move:dict[str,any]):
        player_move_priority = player_move["Priority"]
        enemy_move_priority = enemy_move["Priority"]

        player_speed = player_monster.getAlterStats()[5]
        enemy_speed = enemy_monster.getAlterStats()[5]

        # Check priority
        if player_move_priority > enemy_move_priority:
            return True
        elif player_move_priority < enemy_move_priority:
            return False
        elif player_move_priority == enemy_move_priority:
            # Speed check
            if player_speed > enemy_speed:
                return True
            elif player_speed < enemy_speed:
                return False
            elif player_speed == enemy_speed:
                return self.random_check(50)
            else:
                self.logger.log(logging.INFO, f"SpeedCheck failed. \nPlayer(Priority = {player_move_priority}. Speed = {player_speed})"
                                        + f"\nEnemy(Priority = {enemy_move_priority}. Speed = {enemy_speed})")
                return False
        else:
            self.logger.log(logging.INFO, f"SpeedCheck failed. \nPlayer(Priority = {player_move_priority}. Speed = {player_speed})"
                                    + f"\nEnemy(Priority = {enemy_move_priority}. Speed = {enemy_speed})")
            return True
        
    def damage_calc(self, attacking_level:int, is_critical:bool, attack_power:int, attack_stat:int, defence_stat:int, is_stab:bool, type_value:int):
        
        # No Effect
        if type_value == 0 or attack_power == 0:
            return 0

        # Set the critical value
        critical_value = 2 if is_critical else 1

        # Set the STAB bonus
        stab = 1.5 if is_stab else 1

        total_damage = (2 * attacking_level) / 5 + 2
        total_damage *= (attack_power * (attack_stat / defence_stat)) / 50 + 2
        random_value = (random.random() * 15 + 85) / 100  # 15 = 100 - 85
        total_damage *= critical_value * stab * (type_value / 2) * random_value

        damage_dealt = int(total_damage)

        if damage_dealt == 0:
            damage_dealt = 1

        return damage_dealt
    
    def type_advantage(self, attacking_type:str, defending_type:str):
        attacking_index = self.find_index_from_name(attacking_type)
        defending_index = self.find_index_from_name(defending_type)

        type_chart = [
            # Normal  Fire  Water  Electric  Grass  Ice  Fighting  Poison  Ground Flying Psychic  Bug  Rock  Ghost  Dragon  Dark  Steel  Fairy
            [   2,     2,    2,     2,       2,     2,   2,        2,      2,     2,      2,      2,   2,    0,     2,      2,    1,     2], # Normal
            [   2,     1,    1,     2,       4,     4,   2,        2,      2,     2,      2,      4,   1,    2,     1,      2,    4,     2], # Fire
            [   2,     4,    1,     2,       1,     2,   2,        2,      4,     2,      2,      2,   4,    2,     1,      2,    2,     2], # Water
            [   2,     2,    4,     1,       1,     2,   2,        2,      0,     4,      2,      2,   2,    2,     1,      2,    2,     2], # Electric
            [   2,     1,    4,     2,       1,     2,   2,        1,      4,     1,      2,      1,   4,    2,     1,      2,    1,     2], # Grass
            [   2,     1,    1,     2,       4,     1,   2,        2,      4,     4,      2,      2,   2,    2,     4,      2,    1,     2], # Ice
            [   4,     2,    2,     2,       2,     4,   2,        1,      2,     1,      1,      1,   4,    0,     2,      4,    4,     1], # Fighting
            [   2,     2,    2,     2,       4,     2,   2,        1,      1,     2,      2,      2,   1,    1,     2,      2,    0,     4], # Poison
            [   2,     4,    2,     4,       1,     2,   2,        4,      2,     0,      2,      1,   4,    2,     2,      2,    4,     2], # Ground
            [   2,     2,    2,     1,       4,     2,   4,        2,      2,     2,      2,      4,   1,    2,     2,      2,    1,     2], # Flying
            [   2,     2,    2,     2,       2,     2,   4,        4,      2,     2,      1,      2,   2,    2,     2,      0,    1,     2], # Psychic
            [   2,     1,    2,     2,       4,     2,   1,        1,      2,     1,      4,      2,   2,    1,     2,      4,    1,     1], # Bug
            [   2,     4,    2,     2,       2,     4,   1,        2,      1,     4,      2,      4,   2,    2,     1,      2,    1,     2], # Rock
            [   0,     2,    2,     2,       2,     2,   2,        2,      2,     2,      4,      2,   2,    4,     2,      1,    2,     2], # Ghost
            [   2,     2,    2,     2,       2,     2,   2,        2,      2,     2,      2,      2,   2,    2,     4,      2,    1,     0], # Dragon
            [   2,     2,    2,     2,       2,     2,   1,        2,      2,     2,      4,      2,   2,    4,     2,      1,    2,     1], # Dark
            [   2,     1,    1,     1,       2,     4,   2,        2,      2,     2,      2,      2,   4,    2,     2,      2,    1,     4], # Steel
            [   2,     1,    2,     2,       2,     2,   4,        1,      2,     2,      2,      2,   2,    2,     4,      4,    1,     2] # Fairy
        ]

        return type_chart[attacking_index][defending_index]
    
    def random_check(self, chance:int, auto_hit = False):
        rand_value = random.randint(0, 100)
        return rand_value >= chance or auto_hit
    
    def find_index_from_name(self, name:str):
        name = name.lower()
        index_map = {
            "normal": 0,
            "fire": 1,
            "water": 2,
            "electric": 3,
            "grass": 4,
            "ice": 5,
            "fighting": 6,
            "poison": 7,
            "ground": 8,
            "flying": 9,
            "psychic": 10,
            "bug": 11,
            "rock": 12,
            "ghost": 13,
            "dragon": 14,
            "dark": 15,
            "steel": 16,
            "fairy": 17,
        }
        return index_map.get(name, 0)
    
    def pick_move(self, move_list:list[dict]):
        print("Please choose a move to use:")

        for j, move in enumerate(move_list):
            print(f"{j}: {move['Move name']}\n\tPower: {move['Power']}  Accuracy: {move['Accuracy']}")
        valid = True
        while valid:
            print("Please enter the index number:")
            result = int(input())
            valid = not result.__str__().isdigit()
                

        if result >= len(move_list):
            print("Invalid index, so no nothing move will be used")
            return {"Move name": "Nothing Move", "Power": 0, "Accuracy": 0}

        return move_list[result]