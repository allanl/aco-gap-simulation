import random

from connection import Connection
from utilities import calc_max_pheromones, calc_min_pheromones

def create_nodes(number, max_conn, e_rate, base_ph, bp_prob):
    return [Node('n%d' % i, max_conn, e_rate, base_ph, bp_prob) for i in range(number)]

class TooManyConnections(Exception):
    pass

class Node:
    rand = random.SystemRandom()

    def __init__(self, name, max_connections, erate, base_ph, bp_prob):
        self.name = name
        self.connections = []
        self.best_path = {}
        self.max_pheromones = {}
        self.max_connections = max_connections
        self.evaporation_rate = erate
        self.base_pheromones = base_ph
        self.best_path_prob = bp_prob
        self.tasks = {}

    def add_connection(self, node):
        # check not already connected
        # check not same object
        if (not self.has_connection(node)) and (not self is node):
            # check connections still available
            if len(self.connections) < self.max_connections:
                self.connections.append(Connection(node, self.evaporation_rate,
                    self.base_pheromones, self.best_path_prob))
                try:
                    node.add_connection(self)
                    self.set_min_pheromones()
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
        self.tasks[task] = 1

    def has_task(self, task):
        if self.tasks.get(task, 0) == 1:
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
        if task in self.best_path:
            if len(self.best_path[task]) > ant.get_path_length():
                new_best = 1
        else:
            new_best = 1

        if new_best:
            self.best_path[task] = ant.get_path()
            self.set_max_pheromones(task, calc_max_pheromones(self.evaporation_rate, ant.get_path_length()))
            self.set_task_min_pheromones(task)

    def set_max_pheromones(self, task, max_ph):
        self.max_pheromones[task] = max_ph
        for conn in self.connections:
            conn.set_max_pheromone(task, max_ph)

    def set_min_pheromones(self):
        for task in self.max_pheromones:
            self.set_task_min_pheromones(task)

    def set_task_min_pheromones(self, task):
        max_ph = self.get_max_pheromones(task)
        conn_num = len(self.get_connections())
        best_path_len = self.get_best_path_length(task)
        min_ph = calc_min_pheromones(max_ph,
                conn_num, best_path_len, self.best_path_prob)
        for conn in self.connections:
            conn.set_min_pheromone(task, min_ph)

    def get_name(self):
        return self.name

    def get_best_path(self, task):
        return self.best_path.get(task, False)

    def get_best_path_length(self, task):
        return len(self.best_path.get(task, []))

    def get_max_pheromones(self, task):
        return self.max_pheromones.get(task, self.base_pheromones)

    def __str__(self):
        return '''Node: %s
Tasks: %s''' % (self.name, self.tasks)
