from BattleTroop import BattleTroop

class PriorityQueue():
  def __init__(self):
    self.queue = []

  def isEmpty(self):
    return len(self.queue) == 0

  def lessThanTwo(self):
    return len(self.queue) < 2
    
  # Rules for queueing an troop in the queue:
  # - If faster than everything add to front of queue
  # - If slower than or same speed as last thing add to back of queue
  # - If same speed as another then add new troop after old troop
  def enqueue(self, troop):
    if type(troop) is BattleTroop:
      if self.lessThanTwo():
        if self.isEmpty() or self.queue[0].action < troop.action:
          self.queue.append(troop)
        else:
          self.queue.insert(0,troop)
      elif troop.action >= self.queue[-1].action:
        self.queue.append(troop)
      elif troop.action < self.queue[0].action:
        self.queue.insert(0,troop)
      else:
        for i,x in enumerate(self.queue):
          if troop.action >= x.action and troop.action < self.queue[i+1].action:
            self.queue.insert(i+1,troop)
            break
    else:
      print("Invalid troop type.")

  def dequeue(self, pos=0):
    if pos == -1: return
    try:
      return self.queue.pop(pos)
    except IndexError:
      print()
      exit()

  def getPos(self, troop):
    for i,x in enumerate(self.queue):
      if troop == x:
        return i
    return -1

  def toZero(self):
    dequeue = self.queue[0].action
    for i in self.queue:
      i.action -= dequeue

  def newRound(self):
    self.printActionOrder()
    troop = self.dequeue()
    troop.unbreak()
    troop.resetAV()
    self.toZero()
    self.enqueue(troop)

  def __str__(self):
    return ' '.join([str(i) for i in self.queue])

  def printActionOrder(self):
    print("Current Action Order:")
    for i in self.queue:
      if self.queue[0] == i and i.action == 0:
        print(i.name)
      else:
        print(i.name, round(i.action))


if __name__ == '__main__':
  myQueue = PriorityQueue()
  myQueue.enqueue(BattleTroop("A", 3, 3, 130))
  myQueue.enqueue(BattleTroop("B", 6, 4, 120))
  myQueue.enqueue(BattleTroop("C", 2, 1, 119))
  myQueue.enqueue(BattleTroop("D", 2, 1, 122))
  myQueue.printActionOrder()
  myQueue.queue[0].changeSpeed(myQueue,-25)
  myQueue.printActionOrder()
  myQueue.toZero()
  myQueue.newRound()
  for troop in myQueue.queue:
    troop.advanceForward(myQueue, 16)
  print("After Advance Forward:")
  myQueue.printActionOrder()
  myQueue.queue[1].breakShield(myQueue)
  print(myQueue.queue[3].action,myQueue.queue[3].broken)
  print("After breaking:")
  myQueue.printActionOrder()
  myQueue.newRound()
  myQueue.newRound()
  myQueue.newRound()
  myQueue.newRound()
  myQueue.newRound()
  myQueue.printActionOrder()
  input("Press Enter to close.")
