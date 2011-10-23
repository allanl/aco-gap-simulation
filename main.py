#!/usr/bin/python

from agent import Agent
from ant import Ant
from taskfactory import TaskFactory

if __name__ == '__main__':
    agents = [Agent('agent1', 2), Agent('agent2', 2)]
    for agent in agents:
        print agent

    ants = [Ant(agents[0], TaskFactory.get_task('a'))]
    ants.append(Ant(agents[1], TaskFactory.get_task('b')))
    for ant in ants:
        print ant
        ant.goal.process(None)
