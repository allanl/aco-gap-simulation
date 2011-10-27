
class Connection(object):
    def __init__(self, agent):
        self.agent = agent
        self.pheromone = {}

    def get_agent(self):
        return self.agent

    def add_pheromone(self, task, quantity):
        if (task.__class__ in self.pheromone):
            self.pheromone[task.__class__] += quantity
        else:
            self.pheromone[task.__class__] = quantity

    def evaporate_pheromone(self):
        pass

    def get_pheromone(self, task):
        if (task.__class__ in self.pheromone):
            return self.pheromone[task.__class__]
        else:
            return 0
