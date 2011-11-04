#!/usr/bin/python

import random

from node import Node, TooManyConnections
from ant import Ant
from taskfactory import TaskFactory

max_connections = 7

def create_agents(count):
    agents_list = []
    for index in range(count):
        agents_list.append(Node('agent %d' % (index), max_connections))
    return agents_list

def print_agents(agents_list):
    print 'Nodes:'
    for index in range(len(agents_list)):
        print agents_list[index]

def print_connections(agents_list):
    print 'Connections:'
    for index in range(len(agents_list)):
        print '%s - %s' % (
            agents_list[index].get_name(),
            agents_list[index].get_connection_str()
            )

def link(agent1, agent2):
    agent1.add_connection(agent2)

if __name__ == '__main__':
    agents = create_agents(10)

    random.SystemRandom()
    for x in range(len(agents)):
        for y in range(max_connections):
            other = random.randint(0, len(agents) - 1)
            print "link %d,%d" % (x, other)
            try:
                link(agents[x], agents[other])
            except TooManyConnections:
                break

    print_agents(agents)
    print_connections(agents)

    ants = [Ant(agents[0], TaskFactory.get_task('a'), None)]
    ants.append(Ant(agents[1], TaskFactory.get_task('b'), None))
    for ant in ants:
        for f in range(10): ant.walk()
        print ant
        ant.goal.process(None)
