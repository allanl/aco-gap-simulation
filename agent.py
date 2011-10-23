from connection import Connection

class Agent:
    def __init__(self, name, max_connections):
        self.name = name
        self.connections = []
        self.max_connections = max_connections
        self.tasks = []

    def add_connection(self, agent):
        if len(self.connections) < self.max_connections:
            self.connections.append(Connection(agent))
            if (not agent.has_connection(self)):
                agent.add_connection(self)
        else:
            raise Exception('too many connections')

    def has_connection(self, agent):
        if (agent in [conn.get_agent() for conn in self.connections]):
            return True
        return False

    def add_task(self, task):
        self.tasks.append(task)

    def get_connection_str(self):
        return reduce(
                lambda a, b: '%s, %s' % (a, b),
                [conn.get_agent().get_name() for conn in self.connections],
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
