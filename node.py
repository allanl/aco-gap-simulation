import random

from connection import Connection
from utilities import calc_max_pheromones

class TooManyConnections(Exception):
    pass

class Node:
    rand = random.SystemRandom()

    def __init__(self, name, max_connections, erate, base_ph):
        self.name = name
        self.connections = []
        self.best_path = {}
        self.max_pheromones = {}
        self.max_connections = max_connections
        self.evaporation_rate = erate
        self.base_pheromones = base_ph
        self.tasks = {}

    def add_connection(self, node):
        # check not already connected
        # check not same object
        if (not self.has_connection(node)) and (not self is node):
            # check connections still available
            if len(self.connections) < self.max_connections:
                self.connections.append(Connection(node, self.evaporation_rate, self.base_pheromones))
                try:
                    node.add_connection(self)
                except TooManyConnections:
                    # other side connections already full
                    self.remove_connection(node)
                    raise
            else:
                raise TooManyConnections

    def has_connection(self, node):
        if (node in [conn.get_node() for conn in self.connections]):
            return True
        return False

    def get_connection(self, node):
        for conn in self.connections:
            if (conn.get_node() == node):
                return conn
        return None

    def remove_connection(self, node):
        count = 0
        while (count < len(self.connections)):
            if (self.connections[count].get_node() == node):
                del self.connections[count]
                node.remove_connection(self)
                break
            count += 1

    def add_task(self, task):
        self.tasks[task.__class__] = 1

    def has_task(self, task):
        if self.tasks.get(task.__class__, 0) == 1:
            return True
        else:
            return False

    def choose_path(self, task):
        node = None
        if (self.connections != []):
            weightings = [conn.get_pheromone(task) for conn in self.connections]
            total_weight = sum(weightings)
            number = random.randint(0, total_weight)

            count = 0
            cumulative_weight = 0
            while count < len(weightings):
                if cumulative_weight > number:
                    # index correct as set below
                    # in last loop
                    break
                elif cumulative_weight == number:
                    index = count
                    break
                cumulative_weight += weightings[count]
                index = count
                count += 1

            #print "weightings = %s" % (weightings)
            #print "cumulative_weight = %s" % (cumulative_weight)
            #print "total_weight = %s" % (total_weight)
            #print "number = %s" % (number)
            #print "index = %s" % (index)
            node = self.connections[index].get_node()

        return node

    def get_connections(self):
        return self.connections

    def get_connection_str(self):
        return ', '.join(
                [conn.get_node().get_name() for conn in self.connections]
                )

    def initialise_pheromones(self, task):
        for conn in self.get_connections():
            conn.initialise_pheromone(task)

    def add_conn_pheromones(self, onode, task, path_length):
        conn = self.get_connection(onode)
        if conn is not None:
            conn.add_pheromone(task, path_length)

    def get_conn_pheromones(self, onode, task):
        conn = self.get_connection(onode)
        if conn is not None:
            return conn.get_pheromone(task)
        else:
            return 0
        #self.get_connection(onode).get_pheromone(task))

    def complete_round(self):
        for conn in self.connections:
            conn.evaporate_pheromone() 

    def return_home(self, ant):
        new_best = 0
        task = ant.get_goal()
        c_task = task.__class__
        if c_task in self.best_path:
            if len(self.best_path[c_task]) > ant.get_path_length():
                new_best = 1
        else:
            new_best = 1

        if new_best:
            self.best_path[c_task] = ant.get_path()
            self.set_max_pheromones(task, calc_max_pheromones(self.evaporation_rate, ant.get_path_length()))

    def set_max_pheromones(self, task, max_ph):
        self.max_pheromones[task.__class__] = max_ph
        for conn in self.connections:
            conn.set_max_pheromone(task, max_ph)

    def get_name(self):
        return self.name

    def get_best_path(self, task):
        return self.best_path.get(task.__class__, False)

    def get_best_path_length(self, task):
        return len(self.best_path.get(task.__class__, []))

    def get_max_pheromones(self, task):
        return self.max_pheromones.get(task.__class__, self.base_pheromones)

    def __str__(self):
        return '''Node: %s
Tasks: %s''' % (self.name, self.tasks)
