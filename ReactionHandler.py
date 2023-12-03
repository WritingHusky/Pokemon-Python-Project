import json
import logging
import random
import Monster
import copy

class ResultList:
    def __init__(self):
        self.map = {}

    def add(self, key, value):
        result = self.map.get(key)

        # Build the map if empty for the key
        if result is None:
            self.map[key] = [value]
            return
        # If the value is not in the map, add it
        elif value not in result:
            result.append(value)
            return
        # If the value is in the map, leave it
        else:
            return

    def get_value_by_key(self, key):
        return self.map.get(key)

    def remove_value_by_key(self, key):
        del self.map[key]

    def get_all_keys(self):
        return iter(self.map.keys())


class TriggerList:
    def __init__(self):
        self.map = {}

    def add(self, key, value):
        self.map[key] = value

    def get_value_by_key(self, key):
        return self.map.get(key)

    def remove_value_by_key(self, key):
        del self.map[key]

    def get_all_keys(self):
        return iter(self.map.keys())


class ReactionHandler:
    def __init__(self):
        self.result_hash = ResultList()
        self.trigger_hash = TriggerList()

        logging.basicConfig(filename='ReactionLogger.log', level=logging.INFO, format='%(message)s')

    def set_result_by_code(self, result_code:str, value:int):
        self.result_hash.add(result_code, value)

    def set_trigger_by_code(self, trigger_code:str, result):
        self.trigger_hash.add(trigger_code, result)

    def set_off_trigger_by_code(self, trigger_code:str):
        if trigger_code not in self.trigger_hash.map:
            # If the trigger has not been set, end
            return

        # Get the results of the trigger
        result_list = self.trigger_hash.get_value_by_key(trigger_code)

        for result in result_list:
            try:
                self.result_hash.add(result[0], result[1])
            except Exception as e:
                logging.info(f"Invalid trigger result format result:\n{result}\nFrom trigger code: {trigger_code}")

    def clear_results(self):
        key_it = self.result_hash.get_all_keys()
        for key in copy.copy(key_it):
            # Catch the results that are not dealt with
            if key == "Burn":
                # Throws a new result every time so this is expected
                continue
            # If it's not expected then log it.
            else:
                logging.info(f"Unused Result Key found: {key}")

            self.result_hash.remove_value_by_key(key)

    def clear_triggers(self):
        for key in self.trigger_hash.get_all_keys():
            logging.info(f"Unresolved Trigger Key found: {key}")
            self.trigger_hash.remove_value_by_key(key)

    def handle_results(self, active_mon:Monster, result_mon:Monster, active_move:json):
        for key in self.result_hash.get_all_keys():
            remove_key = True
            value_list = self.result_hash.get_value_by_key(key)

            for value in value_list:
                result = value
                if key == "LowerStat-Opponent-Attack":
                    result_mon.alterStats(1, result)
                elif key == "LowerStat-Opponent-Defence":
                    result_mon.alterStats(2, result)
                elif key == "LowerStat-Opponent-Sp.Attack":
                    result_mon.alterStats(3, result)
                elif key == "LowerStat-Opponent-Sp.Defence":
                    result_mon.alterStats(4, result)
                elif key == "LowerStat-Opponent-Speed":
                    result_mon.alterStats(5, result)

                elif key == "LowerStat-Self-Attack":
                    active_mon.alterStats(1, result)
                elif key == "LowerStat-Self-Defence":
                    active_mon.alterStats(2, result)
                elif key == "LowerStat-Self-Sp.Attack":
                    active_mon.alterStats(3, result)
                elif key == "LowerStat-Self-Sp.Defence":
                    active_mon.alterStats(4, result)
                elif key == "LowerStat-Self-Speed":
                    active_mon.alterStats(5, result)

                elif key == "RaiseStat-Opponent-Attack":
                    result_mon.alterStats(1, result)
                elif key == "RaiseStat-Opponent-Defence":
                    result_mon.alterStats(2, result)
                elif key == "RaiseStat-Opponent-Sp.Attack":
                    result_mon.alterStats(3, result)
                elif key == "RaiseStat-Opponent-Sp.Defence":
                    result_mon.alterStats(4, result)
                elif key == "RaiseStat-Opponent-Speed":
                    result_mon.alterStats(5, result)

                elif key == "RaiseStat-Self-Attack":
                    active_mon.alterStats(1, result)
                elif key == "RaiseStat-Self-Defence":
                    active_mon.alterStats(2, result)
                elif key == "RaiseStat-Self-Sp.Attack":
                    active_mon.alterStats(3, result)
                elif key == "RaiseStat-Self-Sp.Defence":
                    active_mon.alterStats(4, result)
                elif key == "RaiseStat-Self-Speed":
                    active_mon.alterStats(5, result)

                elif key == "ResetStats-Self":
                    for x in range(len(active_mon.monsterStatChange)):
                        active_mon.monsterStatChange[x] = 0
                elif key == "ResetStats-Opponent":
                    for x in range(len(result_mon.monsterStatChange)):
                        result_mon.monsterStatChange[x] = 0

                elif key == "ResetStat-Opponent-Attack":
                    result_mon.monsterStatChange[1] = 0
                elif key == "ResetStat-Opponent-Defence":
                    result_mon.monsterStatChange[2] = 0
                elif key == "ResetStat-Opponent-Sp.Attack":
                    result_mon.monsterStatChange[3] = 0
                elif key == "ResetStat-Opponent-Sp.Defence":
                    result_mon.monsterStatChange[4] = 0
                elif key == "ResetStat-Opponent-Speed":
                    result_mon.monsterStatChange[5] = 0

                elif key == "ResetStat-Self-Attack":
                    result_mon.monsterStatChange[1] = 0
                elif key == "ResetStat-Self-Defence":
                    result_mon.monsterStatChange[2] = 0
                elif key == "ResetStat-Self-Sp.Attack":
                    result_mon.monsterStatChange[3] = 0
                elif key == "ResetStat-Self-Sp.Defence":
                    result_mon.monsterStatChange[4] = 0
                elif key == "ResetStat-Self-Speed":
                    result_mon.monsterStatChange[5] = 0

                elif key == "Damage-Opponent-Fixed":
                    result_mon.doDamage(result)
                elif key == "Damage-Self-Fixed":
                    active_mon.doDamage(result)
                elif key == "Damage-Opponent-nth":
                    result_mon.doDamage(result_mon.maxHP() / result)
                elif key == "Damage-Self-nth":
                    active_mon.doDamage(result_mon.maxHP() / result)

                elif key == "FormChange":
                    # TODO Implement Form Change
                    pass

                # Status Effects
                elif key == "Burn":
                    remove_key = False
                    # If this result does not affect the active mon, do nothing
                    if active_mon.monsterCode != result:
                        break
                    if active_mon.statusOccured:
                        break

                    damage = active_mon.maxHP / 16
                    if damage == 0:
                        damage = 1
                    active_mon.doDamage(damage)
                    active_mon.statusOccured = True
                    active_mon.statusType = 1

                elif key == "Freeze":
                    # If this result does not affect the active mon, do nothing
                    if active_mon.monsterCode != result:
                        remove_key = False
                        break
                    if active_mon.statusOccured:
                        break
                    
                        
                    if self.random_check(20):
                        active_mon.useNothingMove = True
                        active_mon.statusOccured = True
                        active_mon.statusType = 2
                        remove_key = False
                    else:
                        active_mon.useNothingMove = False
                        active_mon.statusType = 0
                        remove_key = True

                elif key == "Paralysis":
                    remove_key = False
                    # If this result does not affect the active mon, do nothing
                    if active_mon.monsterCode != result:
                        break
                    if active_mon.statusOccured:
                        break
                    
                    active_mon.beyondStatChange[5] = -2
                    active_mon.statusOccured = True
                    active_mon.statusType = 3
                    if self.random_check(75):
                        active_mon.useNothingMove = True

                elif key == "Badly Poison":
                    remove_key = False
                    # If this result does not affect the active mon, do nothing
                    if active_mon.monsterCode != result:
                        break
                    if active_mon.statusOccured:
                        break
                    
                    active_mon.timer += 1
                    active_mon.doDamage(active_mon.maxHP * (active_mon.timer/16))
                    active_mon.statusOccured = True
                    active_mon.statusType = 5

                elif key == "Poison":
                    remove_key = False
                    # If this result does not affect the active mon, do nothing
                    if active_mon.monsterCode != result:
                        break
                    if active_mon.statusOccured:
                        break
                    
                    active_mon.doDamage(active_mon.maxHP / 8)
                    active_mon.statusOccured = True
                    active_mon.statusType = 4

                elif key == "Sleep":
                    remove_key = False
                    # If this result does not affect the active mon, do nothing
                    if active_mon.monsterCode != result:
                        break

                    active_mon.useNothingMove = True
                    active_mon.sleepTimer -= 1
                    # At the end of the time end the sleep
                    if active_mon.sleepTimer <= 0:
                        remove_key = True

                elif key == "Move-MultiTurn":
                    if result != active_mon.monsterCode:
                        remove_key = False
                        break

                    # End of timer
                    if active_mon.multiMoveTimer <= 0:
                        active_mon.multiMoveTimer = 0
                        remove_key = True
                        break

                    active_mon.nextMove = active_move
                    active_mon.useNextMove = True
                    active_mon.multiMoveTimer -= 1

                else:
                    remove_key = False
                    logging.info(f"Result Key did not activate in switch: {key}\nTrace(HandleReactions() from ReactionHandler)")

                if remove_key:
                    try:
                        self.result_hash.remove_value_by_key(key)
                    except Exception as excp:
                        logging.info(f"Could not remove key: ({key}) from the result hash {self.result_hash.__str__}\nException: {excp.with_traceback}")
            

    def random_check(self, chance):
        rand_value = int(round(random.uniform(0, 100)))
        return rand_value <= chance
