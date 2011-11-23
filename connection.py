
from utilities import evaporate_pheromones

class Connection(object):
    def __init__(self, node, erate, base_ph):
        self.node = node
        self.evaporation_rate = erate
        self.base_pheromone = base_ph
        self.pheromone = {}
        self.max_pheromone = {}

    def get_node(self):
        return self.node

    def initialise_pheromone(self, task):
        if task not in self.pheromone:
            self.pheromone[task] = self.base_pheromone
            self.max_pheromone[task] = self.base_pheromone

    def add_pheromone(self, task, path_length):
        quantity = 100 / path_length
        self.initialise_pheromone(task)
        self.pheromone[task] = self.pheromone.get(task, self.base_pheromone) + quantity
        self.check_limits(task)

    def evaporate_pheromone(self):
        for task in self.pheromone:
            self.pheromone[task] = evaporate_pheromones(self.evaporation_rate,
                                        self.pheromone[task])

    def get_pheromone(self, task):
        self.initialise_pheromone(task)
        return self.pheromone[task]

    def get_max_pheromone(self, task):
        return self.max_pheromone.get(task, self.base_pheromone)

    def set_max_pheromone(self, task, max_ph):
        self.max_pheromone[task] = max_ph
        self.check_limits(task)

    def check_limits(self, task):
        if task in self.pheromone:
            if self.pheromone[task] > self.max_pheromone[task]:
                self.pheromone[task] = self.max_pheromone[task]
