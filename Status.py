class Status():
  def __init__(self,name,turns,stat=None,operand=None,mult=None):
    self.name = name
    self.stat = stat
    self.operand = operand
    self.mult = mult
    self.turns = turns