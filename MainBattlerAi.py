from Battler import Battler
from ReactionHandler import ReactionHandler
from BattleField import BattleField
from AiLogic import AILogic
import DatabaseController
import Monster

# This is the main loop of the system.

class MainBattler:
    # Check that the database can build
    def __init__(self):
        self.battler = Battler()
        self.battle_field = BattleField()
        self.reaction_handler = ReactionHandler()
        self.database_controller = DatabaseController.DatabaseController()
        self.database_controller.build()
    
    def fight(self, h_list1:list[float], h_list2:list[float]) -> int:
        
        # Load up monsters to fight
        player_mon = self.database_controller.get_monster_by_dex_id(1)
        enemy_mon = self.database_controller.get_monster_by_dex_id(1)

        player_mon.monsterCode = 0
        enemy_mon.monsterCode = 1
        # This will one day be expanded

        # Start the fight
        battling = True
        
        self.player_logic = AILogic(h_list1)
        self.enemy_logic = AILogic(h_list2)
        
        self.player_logic.update_data(player_mon,enemy_mon)
        self.enemy_logic.update_data(enemy_mon,player_mon)

        # Battle loop begins
        while battling:
            player_mon.useNothingMove = False
            enemy_mon.useNothingMove = False
            self.battle_field.weather_change = False
            self.battle_field.terrain_change = False
            self.battle_field.trap_Change = False

            # Get the possible moves from the monster
            player_move_list = self.battler.get_move_list(player_mon)
            enemy_move_list = self.battler.get_move_list(enemy_mon)

            # Pick a move
            player_move = self.player_logic.pickMove(player_move_list)  # Uses move list
            enemy_move = self.enemy_logic.pickMove(enemy_move_list)
        

            # Attack Structure begins

            # Speed Check (loops start)
            if self.battler.speed_check(player_mon, player_move, enemy_mon, enemy_move):
                # Player won speed tie
                # Do transformations (unimplemented)

                # Do items (unimplemented)

                # Player attacks first
                self.battler.do_attack(self.reaction_handler, self.battle_field, player_mon, player_move, enemy_mon)
                self.reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
                self.reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

                # Death check
                if enemy_mon.currentHP <= 0 or player_mon.currentHP <= 0:
                    battling = False

                # If mon2 is not dead, it can attack
                elif not battling:
                    # Enemy attacks next
                    self.battler.do_attack(self.reaction_handler, self.battle_field, enemy_mon, enemy_move, player_mon)
                    self.reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
                    self.reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

            else:
                # Player won speed tie
                # Do transformations (unimplemented)

                # Do items (unimplemented)

                # Enemy attacks first
                self.battler.do_attack(self.reaction_handler, self.battle_field, enemy_mon, enemy_move, player_mon)

                # Reactions to the first attack
                self.reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
                self.reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

                # Death Check
                if player_mon.currentHP <= 0 or enemy_mon.currentHP <= 0:
                    battling = False

                # If mon2 is not dead, it can attack
                elif not battling:
                    # Player attacks next
                    self.battler.do_attack(self.reaction_handler, self.battle_field, player_mon, player_move, enemy_mon)

                    # Reactions to the second attack
                    self.reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
                    self.reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

            # Check if the loop ends
            if not battling:
                # Clean up things
                break

            # Turn end clean up
            player_mon.statusOccured = False
            enemy_mon.statusOccured = False


        self.reaction_handler.clear_results()

        if player_mon.currentHP == 0 and enemy_mon.currentHP == 0:
            return 2
        elif player_mon.currentHP == 0:
            return 1
        elif enemy_mon.currentHP == 0:
            return 0
        # Battle ends
        # TODO: Build an End Screen
        # EOF

