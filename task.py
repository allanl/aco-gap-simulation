
class Task(object):
    def process(self, payload):
        print "%s processing %s" % (self.name, payload)

class TaskA(Task):
    def __init__(self):
        self.name = 'TaskA'

class TaskB(Task):
    def __init__(self):
        self.name = 'TaskB'

class TaskC(Task):
    def __init__(self):
        self.name = 'TaskC'

