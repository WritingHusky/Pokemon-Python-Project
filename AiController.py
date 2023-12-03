import random
import MainBattlerAi
import keyboard
import time

# Types of ai use
# Genetic on heurtistic
# Neural on move Choice
# Adversary


# Options for how to analyze the senario
class AiController:
    def __init__(self):
        self.H_COUNT = 40
        self.POPULATION_SIZE = 50
        self.MAX_SIZE = 100
        self.beta:float # How much to change the values
        self.epoch:list[list[float]]
        self.generation = 0
        self.f_list:list[int]
        self.SURVIVE_LIMIT = 20
        self.battler = MainBattlerAi.MainBattler()
        self.run()
        
    def run(self):
        running = True
        print("Program begining")
        
        while running:
            print(f"Beginning Generation:{self.generation}")
            self.generate_epoch()
            
            self.test_epoch(running)
            high_score = max(self.f_list) 
            high_score_count = self.f_list.count(high_score)
            high_score_index = self.f_list.index(high_score) 
            high_score_h = self.epoch[high_score_index]
            print(f"Epoch ran with High Score:{high_score} ({high_score_count} times) with heuristics: \n{high_score_h}")
            
            if keyboard.is_pressed('q'):
                running = False
            time.sleep(1)
        
    def test_epoch(self, running:bool):
        # round robin tournement
        for x in range(0,self.POPULATION_SIZE):
            for y in range(x,self.POPULATION_SIZE): 
                    # print(f"Battling: {x} vs {y}")
                    if keyboard.is_pressed('q'):
                        running = False
                        return 
                    result = self.battler.fight(self.epoch[x],self.epoch[y])
                    if result == 0:
                        self.f_list[x] += 2
                    elif result == 1:
                        self.f_list[y] += 2
                    elif result == 2:
                        self.f_list[x] += 1
                        self.f_list[y] += 1
                    time.sleep(0.01)
        return

           
    def generate_H_List(self) -> list[float]:
        h_list:list[float]
        h_list = [0]*self.H_COUNT
        for i in range(0, self.H_COUNT):
            h_list[i] = random.uniform(-self.MAX_SIZE,self.MAX_SIZE)
        assert len(h_list) == self.H_COUNT
        return h_list
    
    def generate_epoch(self):
        
        # Build it if it's empty
        if self.generation == 0:
            self.epoch = [0] * self.POPULATION_SIZE
            self.f_list = [0] * self.POPULATION_SIZE
            for i in range(0,self.POPULATION_SIZE):
                self.epoch[i] = self.generate_H_List()
            self.f_list = [0] * self.POPULATION_SIZE
            return
        
        # Selection
        assert len(self.f_list) == len(self.epoch)
        paired = zip(self.epoch, self.f_list)
        sorted_pairs = sorted(paired, key=lambda x: x[1])
        sorted_epoch = [pair[0] for pair in sorted_pairs]
        
        # Selection
        # Randomly remove values
        max_fit = max(self.f_list)
        for index in reversed(range(0,self.POPULATION_SIZE)):
            rand_num = random.randint(0,max_fit)
            if sorted_epoch[index] < rand_num:
                sorted_epoch.pop(index)
                
        # Limit the surviving epoch
        if len(sorted_epoch) > self.SURVIVE_LIMIT:
            remove_count = len(sorted_epoch) - self.SURVIVE_LIMIT
            for x in range(0,remove_count):
                sorted_epoch.pop(random.randint(0,len(sorted_epoch)-1))
             
        # Clear epoch and cross 
        self.epoch = []  
        
        for y in range(0, len(sorted_epoch),2):
            if y+1 >= len(sorted_epoch):
                continue
            swapped = self.cross(sorted_epoch[y],sorted_epoch[y+1])
            self.epoch.append(swapped[0])
            self.epoch.append(swapped[1])
            self.epoch.append(sorted_epoch[y])
            self.epoch.append(sorted_epoch[y+1])
            
        # Fill in gaps in the generation 
        if len(self.epoch) > self.POPULATION_SIZE:
            for i in range(self.POPULATION_SIZE, len(self.epoch)):
                self.epoch.pop()
                
        if len(self.epoch) < self.POPULATION_SIZE:
            for i in range(0, self.POPULATION_SIZE - len(self.epoch)):
                self.epoch.append(self.generate_H_List())
        
        # Mutate
        for i in range(0,self.POPULATION_SIZE):
            self.mutate(i)
        self.f_list = [0] * self.POPULATION_SIZE
        
        assert len(self.epoch) == self.POPULATION_SIZE
        self.generation +=1
        
        return
        
    def mutate(self, index:int):
        for i in range(0,self.H_COUNT):
            self.epoch[index][i] += self.beta * random.uniform(-1,1)
            self.epoch[index][i] = round(self.epoch[index][i], 2)
            # Cap the value
            if self.epoch[index][i] > self.MAX_SIZE:
                self.epoch[index][i] = self.MAX_SIZE
            if self.epoch[index][i] < -self.MAX_SIZE:
                self.epoch[index][i] = - self.MAX_SIZE
        pass
    
    def cross(self, gene1:list[float], gene2:list[float]) -> list[list[float]]:
        size = len(gene1)
        gene_swap_indices = random.sample(range(0,size),int(round(size/2)))
        
        for index in gene_swap_indices:
            temp = gene1[index]
            gene1[index] = gene2[index]
            gene2[index] = temp
        
        return [gene1, gene2]

AiController()