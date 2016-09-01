from random import shuffle

class Mas:
    
    def __init__(self, agents):
        self.agents = agents
        
    def sort(self):
        shuffle(self.agents)
        return self.agents