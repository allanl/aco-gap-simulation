
class Task(object):
    def process(self, payload):
        print "%s processing %s" % (self.name, payload)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

class TaskA(Task):
    def __init__(self):
        self.name = 'TaskA'

class TaskB(Task):
    def __init__(self):
        self.name = 'TaskB'

class TaskC(Task):
    def __init__(self):
        self.name = 'TaskC'

