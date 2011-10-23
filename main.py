#!/usr/bin/python

from agent import Agent
from ant import Ant
from taskfactory import TaskFactory

def create_agents(agents_list, count):
    for index in range(count):
        agents_list.append(Agent('agent %d' % (index), 2))

def print_agents(agents_list):
    for index in range(len(agents_list)):
        print agents_list[index]

if __name__ == '__main__':
    agents = []
    create_agents(agents, 10)
    print_agents(agents)
    print agents

    ants = [Ant(agents[0], TaskFactory.get_task('a'), None)]
    ants.append(Ant(agents[1], TaskFactory.get_task('b'), None))
    for ant in ants:
        print ant
        ant.goal.process(None)
