
class Ant:
    index = 0

    def __init__(self, node, goal, payload):
        self.number = Ant.index
        Ant.index += 1
        self.path = [node]
        self.goal = goal
        self.payload = payload

    def show_path(self):
        return ', '.join([agent.get_name() for agent in self.path])

    def walk(self):
        self.path.append(self.path[-1].choose_path(self.goal))

    def __str__(self):
        return '''
Ant %d:
path: %s
goal: %s
payload: %s''' % (
        self.number, self.show_path(), self.goal.name, self.payload)

