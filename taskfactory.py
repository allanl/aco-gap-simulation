from task import *
from utilities import enum

class TaskFactory(object):
    tasks = enum("TASKA", "TASKB", "TASKC")

    # instances
    taska = TaskA()
    taskb = TaskB()
    taskc = TaskC()

    @staticmethod
    def get_task_names():
        return [TaskFactory.tasks.TASKA,
            TaskFactory.tasks.TASKB,
            TaskFactory.tasks.TASKC]

    def get_task(self, task):
        if (task == TaskFactory.tasks.TASKA):
            return self.taska
        elif (task == TaskFactory.tasks.TASKB):
            return self.taskb
        elif (task == TaskFactory.tasks.TASKC):
            return self.taskc
        else:
            raise NotImplementedError
