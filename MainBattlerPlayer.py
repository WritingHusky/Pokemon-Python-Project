from Battler import ReactionHandler, Battler
from BattleField import BattleField
import DatabaseController
import Monster

def display_monster_data(monster:Monster):
    print(f"{monster.nameStr}: {monster.monsterCode}\n"
          f"Health: {monster.currentHP} / {monster.maxHP}\n")

# This is the main loop of the system.
battler = Battler()
battle_field = BattleField()
reaction_handler = ReactionHandler.ReactionHandler()
database_controller = DatabaseController.DatabaseController()

# Check that the database can build
if not database_controller.build():
    print("The DataBase could not build correctly")
    exit()

# Load up monsters to fight
player_mon = database_controller.get_monster_by_dex_id(1)
enemy_mon = database_controller.get_monster_by_dex_id(1)

if player_mon is None:
    print("Error: Player monster is None.")
    exit()

if enemy_mon is None:
    print("Error: Enemy monster is None.")
    exit()

player_mon.monsterCode = 0
enemy_mon.monsterCode = 1
# This will one day be expanded

# Start the fight
battling = True

# Battle loop begins
while battling:
    player_mon.useNothingMove = False
    enemy_mon.useNothingMove = False

    # Get the possible moves from the monster
    player_move_list = battler.get_move_list(player_mon)
    enemy_move_list = battler.get_move_list(enemy_mon)

    # Pick a move
    print("Player mon")
    display_monster_data(player_mon)

    print("Enemy mon")
    display_monster_data(enemy_mon)

    player_move = battler.pick_move(player_move_list)  # Uses move list

    print("Player mon")
    display_monster_data(player_mon)

    print("Enemy mon")
    display_monster_data(enemy_mon)

    enemy_move = battler.pick_move(enemy_move_list)

    # Attack Structure begins

    # Speed Check (loops start)
    if battler.speed_check(player_mon, player_move, enemy_mon, enemy_move):
        # Player won speed tie
        # Do transformations (unimplemented)

        # Do items (unimplemented)

        # Player attacks first
        battler.do_attack(reaction_handler, battle_field, player_mon, player_move, enemy_mon)
        reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
        reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

        # Death check
        if enemy_mon.currentHP <= 0 or player_mon.currentHP <= 0:
            message = "Enemy is dead" if enemy_mon.currentHP <= 0 else "Player is dead"
            print(message)
            battling = False

        # If mon2 is not dead, it can attack
        elif not battling:
            # Enemy attacks next
            battler.do_attack(reaction_handler, battle_field, enemy_mon, enemy_move, player_mon)
            reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
            reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

    else:
        # Player won speed tie
        # Do transformations (unimplemented)

        # Do items (unimplemented)

        # Enemy attacks first
        battler.do_attack(reaction_handler, battle_field, enemy_mon, enemy_move, player_mon)

        # Reactions to the first attack
        reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
        reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

        # Death Check
        if player_mon.currentHP <= 0 or enemy_mon.currentHP <= 0:
            message = "Player is dead" if player_mon.currentHP <= 0 else "Enemy is dead"
            print(message)
            battling = False

        # If mon2 is not dead, it can attack
        elif not battling:
            # Player attacks next
            battler.do_attack(reaction_handler, battle_field, player_mon, player_move, enemy_mon)

            # Reactions to the second attack
            reaction_handler.handle_results(player_mon, enemy_mon, enemy_move)
            reaction_handler.handle_results(enemy_mon, player_mon, enemy_move)

    # Check if the loop ends
    if not battling:
        # Clean up things
        break

    # Turn end clean up
    player_mon.statusOccured = False
    enemy_mon.statusOccured = False

    print("\n End of turn \n\n")

reaction_handler.clear_results()

# Battle ends
# TODO: Build an End Screen
# EOF


print("Player mon")
display_monster_data(player_mon)

print("Enemy mon")
display_monster_data(enemy_mon)
