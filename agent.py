import random

from connection import Connection

class TooManyConnections(Exception):
    pass

class Agent:
    rand = random.SystemRandom()

    def __init__(self, name, max_connections):
        self.name = name
        self.connections = []
        self.max_connections = max_connections
        self.tasks = {}

    def add_connection(self, agent):
        # check not already connected
        # check not same object
        if (not self.has_connection(agent)) and (not self is agent):
            # check connections still available
            if len(self.connections) < self.max_connections:
                self.connections.append(Connection(agent))
                try:
                    agent.add_connection(self)
                except TooManyConnections:
                    # other side connections already full
                    self.remove_connection(agent)
                    raise
            else:
                raise TooManyConnections

    def has_connection(self, agent):
        if (agent in [conn.get_agent() for conn in self.connections]):
            return True
        return False

    def remove_connection(self, agent):
        count = 0
        while (count < len(self.connections)):
            if (self.connections[count].get_agent() == agent):
                del self.connections[count]
                agent.remove_connection(self)
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
        agent = None
        if (self.connections != []):
            index = random.randint(0, len(self.connections) - 1)
            agent = self.connections[index].get_agent()

        return agent

    def get_connection_str(self):
        return ', '.join(
                [conn.get_agent().get_name() for conn in self.connections]
                )

    def get_name(self):
        return self.name

    def __str__(self):
        return '''
Agent: %s
Connections: %s
Max Connections: %d
Tasks: %s''' % (
        self.name, self.get_connection_str(),
        self.max_connections, self.tasks)
