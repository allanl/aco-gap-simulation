
from utilities import (evaporate_pheromones,
    get_base_min_pheromones)

class Connection(object):
    def __init__(self, node, erate, base_ph, bp_prob):
        self.node = node
        self.evaporation_rate = erate
        self.base_pheromone = base_ph
        self.best_path_prob = bp_prob
        self.pheromone = {}
        self.max_pheromone = {}
        self.min_pheromone = {}

    def get_node(self):
        return self.node

    def initialise_pheromone(self, task):
        if task not in self.pheromone:
            self.pheromone[task] = self.base_pheromone
        if task not in self.max_pheromone:
            self.max_pheromone[task] = self.base_pheromone

    def add_pheromone(self, task, path_length):
        quantity = 100 / path_length
        self.set_pheromone(task, self.get_pheromone(task) + quantity)

    def evaporate_pheromone(self):
        for task in self.pheromone:
            self.set_pheromone(task, evaporate_pheromones(self.evaporation_rate,
                                        self.get_pheromone(task)))

    def get_pheromone(self, task):
        self.initialise_pheromone(task)
        return self.pheromone[task]

    def set_pheromone(self, task, quantity):
        self.pheromone[task] = quantity
        self.check_limits(task)

    def get_annotated_pheromone(self, task):
        pheromones = self.get_pheromone(task)
        pheromones_str = "%s" % pheromones
        if (pheromones == self.get_min_pheromone(task)):
            pheromones_str = "%sm" % pheromones_str
        if (pheromones == self.get_max_pheromone(task)):
            pheromones_str = "%sM" % pheromones_str
        return pheromones_str

    def get_max_pheromone(self, task):
        return self.max_pheromone.get(task, self.base_pheromone)

    def _get_base_min(self):
        return get_base_min_pheromones(self.base_pheromone)

    def get_min_pheromone(self, task):
        return self.min_pheromone.get(task, self._get_base_min())

    def set_max_pheromone(self, task, max_ph):
        self.max_pheromone[task] = max_ph
        if max_ph < self.get_min_pheromone(task):
            self.set_min_pheromone(task, max_ph)
        self.check_limits(task)

    def set_min_pheromone(self, task, min_ph):
        if min_ph > self.get_max_pheromone(task):
            self.min_pheromone[task] = self.get_max_pheromone(task)
        else:
            self.min_pheromone[task] = min_ph
        self.check_limits(task)

    def check_limits(self, task):
        task_ph = self.get_pheromone(task)
        if task_ph > self.get_max_pheromone(task):
            self.pheromone[task] = self.get_max_pheromone(task)
        elif task_ph < self.get_min_pheromone(task):
            self.pheromone[task] = self.get_min_pheromone(task)
