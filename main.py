#!/usr/bin/python

from agent import Agent
from ant import Ant
from taskfactory import TaskFactory

max_connections = 2

def create_agents(agents_list, count):
    for index in range(count):
        agents_list.append(Agent('agent %d' % (index), max_connections))

def print_agents(agents_list):
    print 'Agents:'
    for index in range(len(agents_list)):
        print agents_list[index]

def link(agent1, agent2):
    agent1.add_connection(agent2)

if __name__ == '__main__':
    agents = []
    create_agents(agents, 10)

    link(agents[0], agents[3])
    link(agents[0], agents[7])
    link(agents[1], agents[2])
    link(agents[1], agents[8])
    link(agents[2], agents[9])
    link(agents[3], agents[9])
    link(agents[4], agents[5])
    link(agents[4], agents[6])
    link(agents[5], agents[7])
    link(agents[6], agents[8])

    print_agents(agents)
    print agents

    ants = [Ant(agents[0], TaskFactory.get_task('a'), None)]
    ants.append(Ant(agents[1], TaskFactory.get_task('b'), None))
    for ant in ants:
        print ant
        ant.goal.process(None)
