from Attack import Attack

class BattleAttack(Attack):
    def __init__(self,attack):
        super().__init__(attack)

    def convert(self):
        clas = globals()[f"BattleAttack_{self.effectCode}"]
        atk = clas(self.internal_name)
        return atk

    def effect(self,queue,user,target): pass
    def slashes(self): return False

class BattleAttack_000(BattleAttack):
    pass
    
class BattleAttack_001(BattleAttack):
    def effect(self,queue,user,target):
        user.changeSpeed(queue,user.stats["speed"]*0.2)