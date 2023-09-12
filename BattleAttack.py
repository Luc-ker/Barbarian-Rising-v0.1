from Attack import Attack

class BattleAttack(Attack):
    def __init__(self,attack):
        super().__init__(attack)

    def convert(self):
        attack_class = globals()[f"BattleAttack_{self.effectCode}"]
        atk = attack_class(self.internal_name)
        return atk

    def effect(self,queue,user,target): pass
    def slashes(self): return False

class BattleAttack_000(BattleAttack):
    pass
    
class BattleAttack_IncreaseUserSpd10(BattleAttack):
    def effect(self,battle,user,target):
        user.changeSpeed(battle.queue,user.stats["speed"]*0.1)
        battle.queue.printActionOrder()

class BattleAttack_LowerTargetDef10(BattleAttack):
    def effect(self,battle,user,target):
        target.stats["defence"]*=0.9