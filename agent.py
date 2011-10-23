
class Agent:
    def __init__(self, name, max_connections):
        self.name = name
        self.connections = []
        self.max_connections = max_connections
        self.tasks = []

    def add_connection(self, agent):
        if len(self.connections) < self.max_connections:
            self.connections.append(agent)
            if (not agent.has_connection(self)):
                agent.add_connection(self)
        else:
            raise Exception('too many connections')

    def has_connection(self, agent):
        if (self.connections.count(agent) > 0):
            return True
        return False

    def add_task(self, task):
        self.tasks.append(task)

    def get_name(self):
        return self.name

    def __str__(self):
        return '''
Agent: %s
Connections: %s
Max Connections: %d
Tasks: %s''' % (
        self.name, [conn.get_name() for conn in self.connections],
        self.max_connections, self.tasks)
