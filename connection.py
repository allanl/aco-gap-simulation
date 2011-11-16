
class Connection(object):
    base_pheromone = 1000

    def __init__(self, node, erate):
        self.node = node
        self.evaporation_rate = erate
        self.pheromone = {}

    def get_node(self):
        return self.node

    def initialise_pheromone(self, task):
        self.pheromone[task.__class__] = Connection.base_pheromone

    def add_pheromone(self, task, path_length):
        quantity = 100 / path_length
        if (task.__class__ in self.pheromone):
            self.pheromone[task.__class__] += quantity
        else:
            self.pheromone[task.__class__] = Connection.base_pheromone + quantity

    def evaporate_pheromone(self):
        for task in self.pheromone:
            self.pheromone[task] = int((1 - self.evaporation_rate) *
                                        self.pheromone[task])

    def get_pheromone(self, task):
        if (task.__class__ in self.pheromone):
            return self.pheromone[task.__class__]
        else:
            return Connection.base_pheromone
