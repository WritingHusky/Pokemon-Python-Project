import random
import math

MOVECOUNT = 4
class Monster:
    def __init__(self, name:str, id:int, level:int, maxhp:int, typping:str, monsterStat:list[int],
                height:int, weight:int, monsterCode:int, moveList:list[int]):
        self.nameStr = name
        self.dexID = id
        self.level = level
        self.maxHP = maxhp
        self.currentHP = self.maxHP
        self.type = typping
        self.monsterStats = monsterStat
        self.height = round( (random.random()-0.5) * height + 1 )
        self.weight = round( (random.random()-0.5) * weight + 1 )
        
        self.baseStats = [0,0,0,0,0]
        self.levelUpStats = [0,0,0,0,0,0]
        self.monsterStats = [0,0,0,0,0,0]
        self.monsterStatChange = [0,0,0,0,0,0]
        self.beyondStatChange = [0,0,0,0,0,0]
        self.movesUsable = [True, True, True, True]
        
        self.monsterCode = monsterCode
        self.statusOccured = False
        self.satusType:int
        self.timer = 0
        self.sleepTimer = 0
        self.multiMoveTimer = 0
        
        self.moveListIndex = moveList
        self.moveList:list[dict]
        self.knownMoves: list[dict]      
        
        self.useNextMove = False
        self.nextMove:dict
        
        self.useNothingMove = False
        self.nothingMove = {
            "Accuracy": 0,
            "effects": [],
            "Type": "Normal",
            "Priority": 0,
            "Move name": "Nothing",
            "Power": 0
        }
        return
    
    def __init__(self):
        self.nameStr:str
        self.dexID:int
        self.level:int = 0
        self.maxHP:int
        self.currentHP:int
        self.type:str
        self.monsterStats:list[int]
        self.height:int
        self.weight:int
        
        self.baseStats = [0,0,0,0,0,0]
        self.levelUpStats = [0,0,0,0,0,0]
        self.monsterStats = [0,0,0,0,0,0]
        self.monsterStatChange = [0,0,0,0,0,0]
        self.beyondStatChange = [0,0,0,0,0,0]
        self.movesUsable = [True, True, True, True]
        
        self.monsterCode:int
        self.statusOccured = False
        self.satusType:int
        self.timer = 0
        self.sleepTimer = 0
        self.multiMoveTimer = 0
        
        self.moveListIndex:list[int]
        self.moveList:list[dict]
        self.knownMoves: list[dict]      
        
        self.useNextMove = False
        self.nextMove:dict
        
        self.useNothingMove = False
        self.nothingMove = {
            "Accuracy": 0,
            "effects": [],
            "Type": "Normal",
            "Priority": 0,
            "Move name": "Nothing",
            "Power": 0
        }
        return
    
    def doDamage(self, damage:int):
        self.currentHP -= damage
        if self.currentHP <= 0:
            self.currentHP = 0
        elif self.currentHP > self.maxHP:
            self.currentHP = self.maxHP
        return
    
    def alterStats(self, statIndex:int, statAlter:int):
        self.monsterStatChange[statIndex] += statAlter
        if self.monsterStatChange[statIndex] > 6:
            self.monsterStatChange[statIndex] = 6
        elif self.monsterStatChange[statIndex] < -6:
            self.monsterStatChange[statIndex] = -6
        return
    
    def getAlterStats(self) -> list[int]:
        alterStats = [0,0,0,0,0,0]
        
        try:
            for i in range(0,6):
                alterStats[i] = self.monsterStats[i] + self.levelUpStats[i]
                monsterChange = self.monsterStatChange[i]
                beyondChange = self.beyondStatChange[i]
                
                if monsterChange > 0:
                    alterStats[i] *= (3+monsterChange) /3
                elif monsterChange < 0:
                    alterStats[i] *= 3/(3 + abs(monsterChange))
            
                if beyondChange > 0:
                    alterStats[i] *= beyondChange
                elif beyondChange < 0:
                    alterStats[i] /= abs(beyondChange)
                    
                alterStats[i] = round(alterStats[i])
        except Exception as e:
            try:
                self.monsterStats[i]
            except:
                print(6)
            try:
                self.levelUpStats[i]
            except:
                print(7)
                
            print(f"Thing Happended {i} {e.with_traceback}")
            exit()
            
        return alterStats
    
    def getMovelist(self) -> list[dict]:
        if self.useNothingMove:
            return [self.nothingMove]
        if self.useNextMove:
            return [self.nextMove]
        
        moveListCopy = self.knownMoves.copy()
        for i in range(0,MOVECOUNT):
            x = MOVECOUNT-i-1
            if not self.movesUsable[x]:
                try:
                    moveListCopy.pop(x)
                except:
                    break  
        return moveListCopy      
        
    def setMoveList(self, moveList:list[dict]):
        self.moveList = moveList
        length = len(moveList)

        if length <= MOVECOUNT:
            self.knownMoves = self.moveList
            return
    
        knownMoves:list[dict] =[]
        
        for i in range(0,MOVECOUNT):
            randIndex = random.randint(0,length-1)
            knownMoves.insert(i,self.moveList[randIndex])
            
        self.knownMoves = knownMoves
        return
    
    def setMonsterStats(self):
               
        for i in range(0, len(self.monsterStats)):
            self.monsterStats[i] = math.floor(((self.baseStats[i]*2)*self.level) / 100) + 5
        self.monsterStats[0] += 5
        return
            
    def levelUp(self, level:int):
        if level <= self.level:
            return
        
        delta = self.level - level
        self.levelUpStats += [int((stat / 50) + 0.5) for stat in self.baseStats for _ in range(delta)]
        return
    
    def generate_health(self):
        self.maxHP = self.monsterStats[0]
        self.currentHP = self.maxHP