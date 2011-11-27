#!/usr/bin/python

from itertools import chain
import random
import sys

from graph import graph_pheromones
from node import create_nodes, Node, TooManyConnections
from ant import Ant
from taskfactory import TaskFactory


def create_ants(count, node, task, payload):
    return [Ant(node, task, payload) for index in range(count)]

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

# better performance
def create_adjacency_matrix(nodes_list, task):
    return ['%s,%s' % (node.get_name(),
            ','.join([node.get_conn_annotated_pheromones(onode, task)
            for onode in nodes_list]))
            for node in nodes_list]

# better memory?
def create_adjacency_matrix_alt(nodes_list, task):
    for node in nodes_list:
        yield '%s,%s' % (node.get_name(),
            ','.join([node.get_conn_annotated_pheromones(onode, task)
            for onode in nodes_list]))

def link(node1, node2):
    node1.add_connection(node2)

def average(l):
    return sum(l, 0.0) / len(l)

def show_path_lengths(node, task, ants):
    ant_path_lengths = [ant.get_path_length() for ant in ants]
    print 'r%d,path_length,%s,%s,%s' % (i, node.get_name(), task,
        ','.join(str(length) for length in ant_path_lengths))
    print 'r%d,path_average,%s,%s,%f' % (i, node.get_name(), task,
        average(ant_path_lengths))

if __name__ == '__main__':
    number_of_ants = 10
    number_of_nodes = 10
    evaporation_rate = 0.1
    base_pheromones = 1000
    best_path_prob = 0.05
    max_connections = 7

    nodes = create_nodes(number_of_nodes, max_connections, evaporation_rate,
            base_pheromones, best_path_prob)

    random.SystemRandom()
    for x in range(len(nodes)):
        for y in range(max_connections):
            other = random.randint(0, len(nodes) - 1)
            print "link %d,%d" % (x, other)
            try:
                link(nodes[x], nodes[other])
            except TooManyConnections:
                continue

    taskfactory = TaskFactory()
    nodes[5].add_task(taskfactory.get_task(TaskFactory.tasks.TASKA))
    nodes[3].add_task(taskfactory.get_task(TaskFactory.tasks.TASKA))
    nodes[8].add_task(taskfactory.get_task(TaskFactory.tasks.TASKB))
    nodes[6].add_task(taskfactory.get_task(TaskFactory.tasks.TASKB))

    print ""
    print_nodes(nodes)
    print ""

    # initialise pheromones
    for task in TaskFactory.get_task_names():
        task = taskfactory.get_task(task)
        for node in nodes:
            node.initialise_pheromones(task)

    for i in range(101):
        for node in nodes:
            for task in TaskFactory.get_task_names():
                ants = create_ants(number_of_ants, node,
                    taskfactory.get_task(task), None)
                for ant in ants:
                    for f in range(100): ant.walk()
                if i % 10 == 0:
                    show_path_lengths(node, task, ants)
            node.complete_round()
        if i % 10 == 0:
            # show adjacency matrix
            for task in TaskFactory.get_task_names():
                task = taskfactory.get_task(task)
                print 'adjacency matrix - %s - round %d' % (task, i)
                for line in create_adjacency_matrix(nodes, task):
                    print 'r%d,%s' % (i, line)

    for task in TaskFactory.get_task_names():
        task = taskfactory.get_task(task)
        graph_pheromones(nodes, task, 'graph%s' % (str(task).lower()))
