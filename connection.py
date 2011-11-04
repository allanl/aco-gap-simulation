
class Connection(object):
    def __init__(self, node):
        self.node = node
        self.pheromone = {}

    def get_node(self):
        return self.node

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
