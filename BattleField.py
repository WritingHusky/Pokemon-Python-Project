import logging

class BattleField:
    def __init__(self):
        self.weather = 0
        self.weather_change = False
        self.terrain = 0
        self.terrain_change = False
        self.trap = 0
        self.trap_change =False
        self.hazard = 0
        
        self.current_field_triggers = []
        logging.basicConfig(filename='logfile.log', level=logging.INFO, format='%(levelname)s - %(message)s')
        self.logger = logging.getLogger('BattleFieldLogger')

    def get_all_reaction_pairs(self):
        reaction_pairs = list(self.current_field_triggers)
        return reaction_pairs

    def get_field_reaction_pairs(self):
        return self.current_field_triggers

    def set_reaction_pair(self, trigger, result):
        pair = {trigger: result}
        self.current_field_triggers.append(pair)

    def remove_reaction_pair(self, trigger, result):
        pair = {trigger: result}

        try:
            self.current_field_triggers.remove(pair)
        except ValueError:
            self.logger.warning(f"Tried to remove Reaction pair: {pair}\n But it was not in the current_field_triggers list.")

