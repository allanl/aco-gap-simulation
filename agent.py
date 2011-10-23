
class Agent:
    def __init__(self, name, max_connections):
        self.name = name
        self.connections = []
        self.max_connections = max_connections
        self.tasks = []

    def add_connection(self, connection):
        if len(self.connections) < max_connections:
            self.connections.append(connection)

    def add_task(self, task):
        self.tasks.append(task)

    def __str__(self):
        return '''
Agent:
Name: %s
Connections: %s
Max Connections: %d
Tasks: %s''' % (self.name, self.connections, self.max_connections, self.tasks)
