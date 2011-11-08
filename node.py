import random

from connection import Connection

class TooManyConnections(Exception):
    pass

class Node:
    rand = random.SystemRandom()

    def __init__(self, name, max_connections):
        self.name = name
        self.connections = []
        self.max_connections = max_connections
        self.tasks = {}

    def add_connection(self, node):
        # check not already connected
        # check not same object
        if (not self.has_connection(node)) and (not self is node):
            # check connections still available
            if len(self.connections) < self.max_connections:
                self.connections.append(Connection(node))
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

    def get_connection_str(self):
        return ', '.join(
                [conn.get_node().get_name() for conn in self.connections]
                )

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

    def get_name(self):
        return self.name

    def __str__(self):
        return '''Node: %s
Tasks: %s''' % (self.name, self.tasks)
