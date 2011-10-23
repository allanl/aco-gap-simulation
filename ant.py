
class Ant:
    index = 0

    def __init__(self, source, goal):
        self.number = Ant.index
        Ant.index += 1
        self.path = [source]
        self.goal = goal

    def __str__(self):
        return '''
Ant %d:
path: %s
goal: %s''' % (self.number, self.path, self.goal)

