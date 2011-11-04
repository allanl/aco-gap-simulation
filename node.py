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
            index = random.randint(0, len(self.connections) - 1)
            node = self.connections[index].get_node()

        return node

    def get_connection_str(self):
        return ', '.join(
                [conn.get_node().get_name() for conn in self.connections]
                )

    def get_name(self):
        return self.name

    def __str__(self):
        return '''
Node: %s
Connections: %s
Max Connections: %d
Tasks: %s''' % (
        self.name, self.get_connection_str(),
        self.max_connections, self.tasks)
