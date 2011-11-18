
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
        self.pheromone[task.__class__] = self.base_pheromone

    def add_pheromone(self, task, path_length):
        quantity = 100 / path_length
        if (task.__class__ in self.pheromone):
            self.pheromone[task.__class__] += quantity
        else:
            self.pheromone[task.__class__] = self.base_pheromone + quantity

    def evaporate_pheromone(self):
        for task in self.pheromone:
            self.pheromone[task] = evaporate_pheromones(self.evaporation_rate,
                                        self.pheromone[task])

    def get_pheromone(self, task):
        return self.pheromone.get(task.__class__, self.base_pheromone)

    def set_max_pheromone(self, task, max_ph):
        self.max_pheromone[task.__class__] = max_ph
        self.check_limits(task)

    def check_limits(self, task):
        c_task = task.__class__
        if c_task in self.pheromone:
            if self.pheromone[c_task] > self.max_pheromone[c_task]:
                self.pheromone[c_task] = self.max_pheromone[c_task]
