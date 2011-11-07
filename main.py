#!/usr/bin/python

import random
import sys

from node import Node, TooManyConnections
from ant import Ant
from taskfactory import TaskFactory

max_connections = 7

def create_nodes(count):
    nodes_list = []
    for index in range(count):
        nodes_list.append(Node('node %d' % (index), max_connections))
    return nodes_list

def print_nodes(nodes_list):
    print 'Nodes:'
    for index in range(len(nodes_list)):
        print nodes_list[index]

def print_connections(nodes_list):
    print 'Connections:'
    for index in range(len(nodes_list)):
        print '%s - %s' % (
            nodes_list[index].get_name(),
            nodes_list[index].get_connection_str()
            )

def display_adjacency_matrix(nodes_list, task):
    for node in nodes_list:
        sys.stdout.write('%s,' % (node.get_name()))
        sys.stdout.write(','.join([repr(node.get_conn_pheromones(onode, task))
            for onode in nodes_list]))
        sys.stdout.write('\n')

def link(node1, node2):
    node1.add_connection(node2)

if __name__ == '__main__':
    nodes = create_nodes(10)

    random.SystemRandom()
    for x in range(len(nodes)):
        for y in range(max_connections):
            other = random.randint(0, len(nodes) - 1)
            print "link %d,%d" % (x, other)
            try:
                link(nodes[x], nodes[other])
            except TooManyConnections:
                break

    print ""
    print_nodes(nodes)
    print ""
    display_adjacency_matrix(nodes, 'z')

    ants = [Ant(nodes[0], TaskFactory.get_task(TaskFactory.tasks.TASKA), None)]
    ants.append(Ant(nodes[1], TaskFactory.get_task(TaskFactory.tasks.TASKB), None))
    for ant in ants:
        for f in range(10): ant.walk()
        print ant
        ant.goal.process(None)
