
from utilities import enum

class Ant:
    move = enum("SEEK","RETURN","HOME")
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

    def get_path(self):
        return self.path

    def get_goal(self):
        return self.goal

    def get_path_length(self):
        return len(self.path)

    def show_path(self):
        return ', '.join([node.get_name() for node in self.path])

    def clean_path(self):
        i = 0
        while i < len(self.path):
            node = self.path[i]
            j = len(self.path) - 1
            # find last entry in list
            while j > i:
                if node == self.path[j]:
                    self.path = self.path[:i] + self.path[j:]
                    break
                j -= 1
            i += 1
        self.path_index = len(self.path) - 1

    def get_location(self):
        return self.path[self.path_index]

    def lay_pheromones(self):
        path_length = len(self.path)
        self.path[self.path_index].add_conn_pheromones(self.path[self.path_index
            + 1], self.goal, path_length)

    def walk(self):
        if self.status == Ant.move.HOME:
            # do nothing
            pass
        elif self.status == Ant.move.RETURN:
            # move back one node
            self.path_index -= 1
            self.lay_pheromones()
            if self.path_index == 0:
                self.status = Ant.move.HOME
        else:
            # keep searching
            self.path.append(self.get_location().choose_path(self.goal))
            self.path_index += 1
            if self.get_location().has_task(self.goal):
                self.clean_path()
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

