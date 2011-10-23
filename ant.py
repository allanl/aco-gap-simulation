
class Ant:
    index = 0

    def __init__(self, source, goal, payload):
        self.number = Ant.index
        Ant.index += 1
        self.path = [source]
        self.goal = goal
        self.payload = payload

    def __str__(self):
        return '''
Ant %d:
path: %s
goal: %s
payload: %s''' % (
        self.number, self.path, self.goal, self.payload)

