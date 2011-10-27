
class Ant:
    index = 0

    def __init__(self, node, goal, payload):
        self.number = Ant.index
        Ant.index += 1
        self.path = [node]
        self.goal = goal
        self.payload = payload
        if node.has_task(goal):
            self.going_home = True
        else:
            self.going_home = False

    def show_path(self):
        return ', '.join([agent.get_name() for agent in self.path])

    def get_location(self):
        return self.path[-1]

    def walk(self):
        self.path.append(self.get_location().choose_path(self.goal))
        if self.get_location().has_task(self.goal):
            self.going_home = True

    def is_going_home(self):
        return self.going_home

    def __str__(self):
        return '''
Ant %d:
path: %s
goal: %s
payload: %s''' % (
        self.number, self.show_path(), self.goal.name, self.payload)

