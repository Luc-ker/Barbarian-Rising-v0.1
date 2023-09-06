from Troop import Troop

class Player():
    name = ""
    id = ""

    def __init__(self,name):
        self.name = name
        self.id = ""
        self.gold = 500
        self.elixir = 500
        self.d_elixir = 0
        self.barbarian = Troop("barbarian")
        self.powers = []
    