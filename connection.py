
class Connection(object):
    base_pheromone = 1

    def __init__(self, node):
        self.node = node
        self.pheromone = {}

    def get_node(self):
        return self.node

    def add_pheromone(self, task, quantity):
        if (task.__class__ in self.pheromone):
            self.pheromone[task.__class__] += quantity
        else:
            self.pheromone[task.__class__] = Connection.base_pheromone + quantity

    def evaporate_pheromone(self):
        pass

    def get_pheromone(self, task):
        if (task.__class__ in self.pheromone):
            return self.pheromone[task.__class__]
        else:
            return Connection.base_pheromone
