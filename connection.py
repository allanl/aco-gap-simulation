
class Connection(object):
    base_pheromone = 1000
    evaporation_rate = 0.1

    def __init__(self, node):
        self.node = node
        self.pheromone = {}

    def get_node(self):
        return self.node

    def add_pheromone(self, task, path_length):
        quantity = 100 / path_length
        if (task.__class__ in self.pheromone):
            self.pheromone[task.__class__] += quantity
        else:
            self.pheromone[task.__class__] = Connection.base_pheromone + quantity

    def evaporate_pheromone(self):
        for pheromone in self.pheromone:
            self.pheromone[pheromone] = int((1 - Connection.evaporation_rate) *
                                        self.pheromone[pheromone])

    def get_pheromone(self, task):
        if (task.__class__ in self.pheromone):
            return self.pheromone[task.__class__]
        else:
            return Connection.base_pheromone
