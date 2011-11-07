from task import *
from utilities import enum

class TaskFactory(object):
    tasks = enum("TASKA", "TASKB", "TASKC")

    @staticmethod
    def get_task(task):
        if (task == TaskFactory.tasks.TASKA):
            return TaskA()
        elif (task == TaskFactory.tasks.TASKB):
            return TaskB()
        elif (task == TaskFactory.tasks.TASKC):
            return TaskC()
        else:
            raise NotImplementedError
