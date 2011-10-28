
from utilities import Enum

class Ant:
    move = Enum(["SEEK","RETURN","HOME"])
    index = 0

    def __init__(self, node, goal, payload):
        self.number = Ant.index
        Ant.index += 1
        self.path_index = 0
        self.path = [node]
        self.goal = goal
        self.payload = payload
        if node.has_task(goal):
            self.status = Ant.move.HOME
        else:
            self.status = Ant.move.SEEK

    def show_path(self):
        return ', '.join([agent.get_name() for agent in self.path])

    def get_location(self):
        return self.path[self.path_index]

    def walk(self):
        self.path.append(self.get_location().choose_path(self.goal))
        self.path_index += 1
        if self.get_location().has_task(self.goal):
            self.status = Ant.move.RETURN

    def is_going_home(self):
        return self.status == Ant.move.RETURN

    def is_home(self):
        return self.status == Ant.move.HOME

    def __str__(self):
        return '''
Ant %d:
path: %s
goal: %s
payload: %s''' % (
        self.number, self.show_path(), self.goal.name, self.payload)

