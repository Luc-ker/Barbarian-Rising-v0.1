from Attack import Attack

class BattleAttack(Attack):
    def __init__(self,attack):
        super().__init__(attack)

    def convert(self):
        attack_class = globals()[f"BattleAttack_{self.effectCode}"]
        atk = attack_class(self.internal_name)
        return atk

    def effect(self,battle,user,target): pass
    def additionalEffect(self,battle,user,target): pass
    def getPower(self,battle,user,target): return self.power
    def slashes(self): return False

class BattleAttack_000(BattleAttack):
    pass
    
class BattleAttack_IncreaseUserSpd10(BattleAttack):
    def effect(self,battle,user,target):
        user.changeSpeed(battle.queue,self,self.effectTurns,user.stats["speed"]*0.1)
        battle.queue.printActionOrder()

class BattleAttack_LowerTargetDef10(BattleAttack):
    def effect(self,battle,user,target):
        target.debuff("Defence Reduction",self,self.effectTurns,"defence","mult",0.9)