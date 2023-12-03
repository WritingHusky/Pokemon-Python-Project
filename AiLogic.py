import copy
import Monster
from Battler import Battler
from ReactionHandler import ReactionHandler
from BattleField import BattleField
import random

class AILogic: 
    def __init__(self, h_list:list[float]) -> None:
        self.H_COUNT = 40
        self.h_list = h_list
        assert len(h_list) == self.H_COUNT
        
        self.battler = Battler()
        self.reaction = ReactionHandler()
        self.battlefield = BattleField()
        
        self.self_Monster:Monster
        self.self_Monster:Monster
    
    def pickMove(self, move_List:list[dict]) -> dict[str, any]:
        max_score = 0
        move_to_use:dict[str,any] = {}
        for move in move_List:
            score = self.analyze_option(move)
            if score > max_score:
                max_score = score
                move_to_use = move
        
        if max_score == 0:
            move_to_use = move_List[random.randint(0,len(move_List)-1)]
        return move_to_use
    
    def analyze_option(self, move:dict[str, any]) -> int:
        copy_self_monster = copy.copy( self.self_Monster)
        copy_oppenent_monster = copy.copy(self.oppenent_Monster)
        # TODO Account for acuracy
        self.battler.do_attack(self.reaction, self.battlefield,copy_self_monster,move,copy_oppenent_monster,auto_hit=True)
    
        return self.H(copy_self_monster,copy_oppenent_monster, move)
    
    def update_data(self, self_Monster:Monster, opponent:Monster):
        self.self_Monster = self_Monster
        self.oppenent_Monster = opponent
        return
    
    def update_H_List(self, h_list:list[float]):
        self.h_list = h_list
        assert len(h_list) == self.H_COUNT
    
    def H(self, copy_self_monster:Monster, copy_opponent_monster:Monster, move:dict[str, any]) -> int:
        """
        Heuristics: \n
            # Per Turn Pramaters\n
                Self HP %Delta(0), Opponent HP %Delta(1), Self Stat Changes(2), Opponent stat Changes(3), \n 
                Status Occured(4), Clear(5), Burn(6), Freeze(7), Paralysis(8), Poison(9), Badly Poison(10), Sleep(11) \n
                Weather(12), Clear Weather(13), Harsh Sunlight(14), Rain(15), Sandstorm(16), Snow(17), Fog(18),\n
                Terrain(19), Clear(20), Electric(21), Grassy(22), Misty(23), Psyhic(24),\n
                Traps(25), Escape Prevention(26), Bind(27), Vortex(28),\n
                Hazard(29), Active(30), Passive(31),\n
                Multi Turn(32), Nothing Move(33),\n
                Effectiveness of move(34), Accuracy(35), Priority(36),\n
                Self is Dead(37), Opponent is dead(38) \n
                Move Power(39)
            \n
            # Static variable\n
                Self Level, Opponent Level
        """       
        self_delta_score = self.self_Monster.currentHP - copy_self_monster.currentHP
        self_delta_score *= self.h_list[0]
        
        opponent_delta_score = self.oppenent_Monster.currentHP - copy_opponent_monster.currentHP
        opponent_delta_score *= self.h_list[1]
        
        self_stat_score_change = sum(self.self_Monster.getAlterStats()) - sum(copy_self_monster.getAlterStats())
        self_stat_score_change *= self.h_list[2]
        
        opponent_stat_score_change = sum(self.oppenent_Monster.getAlterStats()) - sum(copy_opponent_monster.getAlterStats())
        opponent_stat_score_change *= self.h_list[3]
        
        # Score Status Effects
        status_index = 4
        if copy_opponent_monster.statusOccured:
            status_score = self.h_list[status_index]
            assert copy_opponent_monster.statusType <=6 and copy_opponent_monster.statusType >=0
            # (4-11)
            status_score *= self.h_list[status_index+1+copy_opponent_monster.statusType]
        else:
            status_score = 0
            
            
        # Score Weather
        weather_index = 12
        if self.battlefield.weather_change:
            weather_score = self.h_list[weather_index]
            assert self.battlefield.weather <= 5 and self.battlefield.weather >=0
            #(12-18)
            weather_score *= self.h_list[weather_index+1+ self.battlefield.weather]
        else:
            weather_score = self.h_list[weather_index+1+ self.battlefield.weather]
            
        # Score Terrain
        terrain_index = 19
        if self.battlefield.terrain_change:
            terrain_score = self.h_list[terrain_index]
            assert self.battlefield.terrain <= 4 and self.battlefield.terrain >=0
            #(19-2)
            terrain_score *= self.h_list[terrain_index+1+ self.battlefield.terrain]
        else:
            terrain_score = self.h_list[terrain_index+1+ self.battlefield.terrain]
         
        # Score Trap
        trap_index = 25
        if self.battlefield.trap_change:
            trap_score = self.h_list[trap_index]
            assert self.battlefield.trap <= 3 and self.battlefield.trap >=0
            #(25-28)
            trap_score *= self.h_list[trap_index+1+ self.battlefield.trap]
        else:
            trap_score = self.h_list[trap_index+1+ self.battlefield.trap] 
            
        # Score Hazard
        hazard_index = 29
        assert self.battlefield.hazard <= 2 and self.battlefield.hazard >=0
        hazard_score = self.h_list[hazard_index+self.battlefield.hazard]
        
        if copy_opponent_monster.useNothingMove:
            use_nothing_score = self.h_list[33]
        else:
            use_nothing_score = 0
            
        if copy_opponent_monster.useNextMove:
            use_next_move_score = self.h_list[34]
        else:
            use_next_move_score = 0
            
        type_effect_score = self.battler.type_advantage(move["Type"], copy_opponent_monster.type)*self.h_list[35]
        
        move_accuracy_score = move["Accuracy"] * self.h_list[36]
        
        if copy_self_monster.currentHP == 0:
            self_dead_score = self.h_list[37] 
        else:
            self_dead_score = 0
            
        if copy_opponent_monster.currentHP == 0:
            opponent_dead_score = self.h_list[38] 
        else:
            opponent_dead_score = 0
        
        move_power_score = move["Power"]*self.h_list[39]
        
        result = self_delta_score + opponent_delta_score + self_stat_score_change + opponent_stat_score_change + move_power_score
        result +=  status_score + weather_score + terrain_score + trap_score + hazard_score  + use_nothing_score 
        result += use_next_move_score + type_effect_score + move_accuracy_score + self_dead_score + opponent_dead_score
        return result
