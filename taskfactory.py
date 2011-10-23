from task import *

class TaskFactory(object):
    @staticmethod
    def get_task(name):
        if (name == 'a'):
            return TaskA()
        elif (name == 'b'):
            return TaskB()
        elif (name == 'c'):
            return TaskC()
        else:
            raise NotImplementedError
