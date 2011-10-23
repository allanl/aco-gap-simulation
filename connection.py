
class Connection(object):
    def __init__(self, agent):
        self.agent = agent
        self.pheromone = {}

    def get_agent(self):
        return self.agent

    def add_pheromone(self, task, quantity):
        self.pheromone[task.__class__] += quantity

    def evaporate_pheromone(self):
        pass

    def get_pheromone(self, task):
        return self.pheromone[task.__class__]
