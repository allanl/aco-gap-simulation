#!/usr/bin/python

import unittest
from node import create_nodes, Node, TooManyConnections
from ant import Ant
from connection import Connection
from task import TaskA, TaskB, TaskC
from taskfactory import TaskFactory
from utilities import (calc_max_pheromones, calc_min_pheromones, calc_nth_root,
    get_base_min_pheromones)

base_pheromones = 1000
evaporation_rate = 0.1
best_path_prob = 0.05
def evaporate_pheromones(pheromones):
    return pheromones * (1 - evaporation_rate)
def calc_max_ph_erate(best_path_length):
    return calc_max_pheromones(evaporation_rate, best_path_length)
def ant_walk_till_home(ant):
    while ant.is_home() == False:
        ant.walk()

class TestNode(unittest.TestCase):
    def setUp(self):
        self.max_connections = 2
        (self.node1, self.node2, self.node3, self.node4) = create_nodes(
            4, self.max_connections, evaporation_rate, base_pheromones,
            best_path_prob)

    def test_connection_list_empty(self):
        self.assertEqual(self.node1.connections, [])

    def test_max_connections_set(self):
        self.assertEqual(self.node1.max_connections, self.max_connections)

    def test_connection_reciprocal(self):
        self.node1.add_connection(self.node2)
        self.assertTrue(self.node1.has_connection(self.node2))
        self.assertTrue(self.node2.has_connection(self.node1))
        self.assertFalse(self.node1.has_connection(self.node3))
        self.assertFalse(self.node2.has_connection(self.node3))

    def test_connecting_to_max(self):
        self.node1.add_connection(self.node2)
        self.node1.add_connection(self.node3)
        with self.assertRaises(TooManyConnections):
            self.node1.add_connection(self.node4)
        with self.assertRaises(TooManyConnections):
            self.node4.add_connection(self.node1)
        self.assertFalse(self.node4.has_connection(self.node1))

    def test_remove_connection(self):
        self.node1.add_connection(self.node2)
        self.node1.add_connection(self.node3)
        self.assertTrue(self.node1.has_connection(self.node2))
        self.assertTrue(self.node1.has_connection(self.node3))
        self.node1.remove_connection(self.node2)
        self.assertFalse(self.node1.has_connection(self.node2))
        self.assertFalse(self.node2.has_connection(self.node1))
        self.assertTrue(self.node1.has_connection(self.node3))
        self.assertTrue(self.node3.has_connection(self.node1))

    def test_set_check_task(self):
        task = TaskA()
        self.assertFalse(self.node1.has_task(task))
        self.node1.add_task(task)
        self.assertTrue(self.node1.has_task(task))

    def test_remove_task(self):
        task = TaskA()
        self.assertFalse(self.node1.has_task(task))
        self.node1.add_task(task)
        self.assertTrue(self.node1.has_task(task))
        self.node1.remove_task(task)
        self.assertFalse(self.node1.has_task(task))

    def test_remove_not_set_task(self):
        task = TaskA()
        self.assertFalse(self.node1.has_task(task))
        self.node1.remove_task(task)
        self.assertFalse(self.node1.has_task(task))

    def test_set_check_task_instance(self):
        task = TaskA()
        self.assertFalse(self.node1.has_task(task))
        self.node1.add_task(task)
        self.assertTrue(self.node1.has_task(task))
        taska = TaskA()
        self.assertFalse(self.node1.has_task(taska))

    def test_no_connect_to_self(self):
        self.assertFalse(self.node1.has_connection(self.node1))
        self.node1.add_connection(self.node1)
        self.assertFalse(self.node1.has_connection(self.node1))

    def test_set_get_pheromones(self):
        task = TaskA()
        self.node1.add_connection(self.node2)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, task), base_pheromones)
        self.node1.get_connection(self.node2).set_pheromone(task, 100)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, task), 100)
        self.node1.add_conn_pheromones(self.node2, task, 3)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, task), 133)

    def test_annotated_pheromones_no_conn(self):
        task = TaskA()
        self.assertEqual(self.node1.get_conn_annotated_pheromones(self.node2,
            task), '0')
        self.node1.add_connection(self.node2)
        self.assertEqual(self.node1.get_conn_annotated_pheromones(self.node2,
            task), "%dM" % base_pheromones)

    def test_annotated_pheromones(self):
        task = TaskA()
        self.node1.add_connection(self.node2)
        self.assertEqual(self.node1.get_conn_annotated_pheromones(self.node2,
            task), "%dM" % base_pheromones)
        self.node1.get_connection(self.node2).set_pheromone(task, 100)
        self.assertEqual(self.node1.get_conn_annotated_pheromones(self.node2,
            task), '100')
        self.node1.add_conn_pheromones(self.node2, task, 3)
        self.assertEqual(self.node1.get_conn_annotated_pheromones(self.node2,
            task), '133')
        self.node1.set_max_pheromones(task, 100)
        self.assertEqual(self.node1.get_conn_annotated_pheromones(self.node2, task),
            '100M')

    def test_initialise_pheromones(self):
        self.task = TaskA()
        self.node1.add_connection(self.node2)
        self.node1.initialise_pheromones(self.task)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, self.task), base_pheromones) 

    def test_complete_round(self):
        self.test_initialise_pheromones()
        self.node1.complete_round()
        pheromones = evaporate_pheromones(base_pheromones)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, self.task), pheromones)

    def test_return_home(self):
        self.task = TaskA()
        self.ant = Ant(self.node1, self.task, None)
        self.node1.add_connection(self.node2)
        self.node2.add_task(self.task)
        self.assertFalse(self.node1.get_best_path(self.task))
        self.ant.walk()
        self.ant.walk()
        self.assertEqual(self.node1.get_best_path(self.task), self.ant.get_path())

    def test_get_best_path_length(self):
        self.test_return_home()
        # not relevant input - return path length of 0
        self.assertEqual(self.node1.get_best_path_length(self.ant), 0)
        self.assertEqual(self.node1.get_best_path_length(self.task), 2)

    def test_overwrite_best_path_length(self):
        self.task = TaskA()
        self.ant = Ant(self.node1, self.task, None)
        self.node1.add_connection(self.node2)
        self.node2.add_connection(self.node3)
        self.node3.add_task(self.task)
        self.assertFalse(self.node1.get_best_path(self.task))
        self.assertEqual(self.node1.get_best_path_length(self.task), 0)
        while self.ant.is_home() == False:
            self.ant.walk()
        self.assertEqual(self.node1.get_best_path(self.task), self.ant.get_path())
        self.assertEqual(self.node1.get_best_path_length(self.task), 3)
        self.node2.add_task(self.task)
        self.ant2 = Ant(self.node1, self.task, None)
        while self.ant2.is_home() == False:
            self.ant2.walk()
        self.assertEqual(self.node1.get_best_path(self.task), self.ant2.get_path())
        self.assertEqual(self.node1.get_best_path_length(self.task), 2)

    def test_set_max_pheromones(self):
        self.test_return_home()
        # not relevant input - return base level of pheromones
        self.assertEqual(self.node1.get_max_pheromones(self.ant), base_pheromones)
        max_pheromones = calc_max_ph_erate(self.node1.get_best_path_length(self.task))
        self.assertEqual(self.node1.get_max_pheromones(self.task), max_pheromones)
        self.assertEqual(self.node1.get_max_pheromones(self.task), 555)

    def test_max_pheromone_changes(self):
        self.task = TaskA()
        self.ant = Ant(self.node1, self.task, None)
        self.node1.add_connection(self.node2)
        self.node2.add_connection(self.node3)
        self.node3.add_task(self.task)
        self.assertEqual(self.node1.get_max_pheromones(self.task), base_pheromones)
        ant_walk_till_home(self.ant)
        max_pheromones = calc_max_ph_erate(self.node1.get_best_path_length(self.task))
        self.assertEqual(self.node1.get_max_pheromones(self.task), max_pheromones)
        self.assertEqual(self.node1.get_max_pheromones(self.task), 370)
        self.node2.add_task(self.task)
        self.ant2 = Ant(self.node1, self.task, None)
        ant_walk_till_home(self.ant2)
        max_pheromones = calc_max_ph_erate(self.node1.get_best_path_length(self.task))
        self.assertEqual(self.node1.get_max_pheromones(self.task), max_pheromones)
        self.assertEqual(self.node1.get_max_pheromones(self.task), 555)

    def test_max_pheromone_enforced_on_set(self):
        self.task = TaskA()
        self.ant = Ant(self.node1, self.task, None)
        self.node1.add_connection(self.node2)
        self.node2.add_task(self.task)
        self.assertEqual(self.node1.get_max_pheromones(self.task), base_pheromones)
        conn = self.node1.get_connection(self.node2)
        self.assertEqual(conn.get_pheromone(self.task), base_pheromones)
        ant_walk_till_home(self.ant)
        self.assertEqual(conn.get_pheromone(self.task), self.node1.get_max_pheromones(self.task))

    def test_connection_max_pheromones(self):
        task = TaskA()
        self.node1.add_connection(self.node2)
        self.node2.add_connection(self.node3)
        self.node3.add_task(task)
        self.ant1 = Ant(self.node1, task, None)
        self.ant2 = Ant(self.node2, task, None)
        ant_walk_till_home(self.ant1)
        ant_walk_till_home(self.ant2)
        self.assertEqual(self.node1.get_max_pheromones(task), calc_max_ph_erate(3))
        self.assertEqual(self.node1.get_connection(self.node2).get_max_pheromone(task), calc_max_ph_erate(3))
        self.assertEqual(self.node2.get_max_pheromones(task), calc_max_ph_erate(2))
        self.assertEqual(self.node2.get_connection(self.node1).get_max_pheromone(task), calc_max_ph_erate(2))

    def test_connection_min_pheromones(self):
        task = TaskA()
        self.node1.add_connection(self.node2)
        min_ph = get_base_min_pheromones(base_pheromones)
        #min_ph = calc_min_pheromones(base_pheromones, 10, 10, best_path_prob)
        self.assertEqual(self.node1.get_connection(self.node2).get_min_pheromone(task), min_ph)
        self.node2.add_connection(self.node3)
        # still not initialised because no ants returned
        self.assertEqual(self.node2.get_connection(self.node1).get_min_pheromone(task), min_ph)
        # get results
        ant = Ant(self.node2, task, None)
        self.node3.add_task(task)
        ant_walk_till_home(ant)
        # min pheromones initialised
        max_ph = self.node2.get_max_pheromones(task)
        min_ph = calc_min_pheromones(max_ph, 2, 2, best_path_prob)
        self.assertEqual(self.node2.get_connection(self.node1).get_min_pheromone(task), min_ph)
        self.assertEqual(self.node2.get_connection(self.node3).get_min_pheromone(task), min_ph)

class TestAnt(unittest.TestCase):
    def setUp(self):
        max_connections = 3
        self.node1 = Node('node1', max_connections, evaporation_rate,
                base_pheromones, best_path_prob)
        self.node2 = Node('node2', max_connections, evaporation_rate,
                base_pheromones, best_path_prob)
        self.node1.add_connection(self.node2)
        self.taska = TaskA()
        self.ant = Ant(self.node1, self.taska, None)

    def test_walk(self):
        self.assertEqual(self.ant.get_location(), self.node1)
        self.ant.walk()
        self.assertEqual(self.ant.get_location(), self.node2)

    def test_clean_path(self):
        self.assertEqual(self.ant.get_location(), self.node1)
        self.ant.walk()
        self.assertEqual(self.ant.get_location(), self.node2)
        self.ant.walk()
        self.assertEqual(self.ant.get_location(), self.node1)
        path = [self.node1, self.node2, self.node1]
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        self.assertEqual(self.ant.get_path(), [self.node1])

    def test_clean_path_start(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        node4 = Node('node4', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        path = [node1, node2, node3, node1, node4, node3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node4, node3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_middle(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        node4 = Node('node4', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        path = [node1, node2, node3, node4, node3, node4]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node2, node3, node4]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_end(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        node4 = Node('node4', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        path = [node1, node2, node3, node4, node3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node2, node3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_multiple(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        node4 = Node('node4', 2, evaporation_rate, base_pheromones,
                best_path_prob)
        path = [node1, node2, node3, node1, node3, node4, node3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_is_home_no_walk(self):
        self.assertFalse(self.ant.is_home())
        self.ant.walk()
        self.assertFalse(self.ant.is_home())
        self.node1.add_task(self.taska)
        ant2 = Ant(self.node1, self.taska, None)
        self.assertTrue(ant2.is_home())

    def test_is_going_home(self):
        self.assertFalse(self.ant.is_going_home())
        self.node2.add_task(self.taska)
        self.ant.walk()
        self.assertTrue(self.ant.is_going_home())

    def test_is_home_after_walk(self):
        self.assertFalse(self.ant.is_going_home())
        self.node2.add_task(self.taska)
        self.ant.walk()
        self.assertTrue(self.ant.is_going_home())
        self.assertFalse(self.ant.is_home())
        self.ant.walk()
        self.assertTrue(self.ant.is_home())

    def test_get_goal(self):
        self.assertEqual(self.ant.get_goal(), self.taska)

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.max_connections = 7
        self.node1 = Node('node1', self.max_connections, evaporation_rate,
                base_pheromones, best_path_prob)
        self.conn1 = Connection(self.node1, evaporation_rate, base_pheromones,
                best_path_prob)
        self.conn2 = Connection(self.node1, evaporation_rate, base_pheromones,
                best_path_prob)

    def test_get_node(self):
        self.assertEqual(self.node1, self.conn1.get_node())

    def test_set_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_pheromone(task, 100)
        self.assertEqual(self.conn1.get_pheromone(task), 100)

    def test_add_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_pheromone(task, 100)
        self.assertEqual(self.conn1.get_pheromone(task), 100)
        self.conn1.add_pheromone(task, 3)
        self.assertEqual(self.conn1.get_pheromone(task), 133)
        self.conn1.add_pheromone(task, 3)
        self.assertEqual(self.conn1.get_pheromone(task), 166)

    def test_get_annotated_pheromone_max(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_max_pheromone(task, 100)
        self.assertEqual(self.conn1.get_pheromone(task), 100)
        self.assertEqual(self.conn1.get_annotated_pheromone(task), '100M')
        self.assertTrue(self.conn1.get_annotated_pheromone(task).find('M'))
        self.assertEqual(self.conn1.get_annotated_pheromone(task).find('m'), -1)

    def test_get_annotated_pheromone_min(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_min_pheromone(task, 100)
        self.conn1.set_pheromone(task, 100)
        self.assertEqual(self.conn1.get_annotated_pheromone(task), '100m')
        self.assertTrue(self.conn1.get_annotated_pheromone(task).find('m'))
        self.assertEqual(self.conn1.get_annotated_pheromone(task).find('M'), -1)

    def test_get_annotated_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_max_pheromone(task, 100)
        self.assertEqual(self.conn1.get_pheromone(task), 100)
        self.conn1.set_min_pheromone(task, 100)
        self.assertEqual(self.conn1.get_annotated_pheromone(task), '100mM')
        self.assertTrue(self.conn1.get_annotated_pheromone(task).find('m'))
        self.assertTrue(self.conn1.get_annotated_pheromone(task).find('M'))

    def test_evaporate_pheromone(self):
        task = TaskA()
        # before initialise
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)

        # initialise
        self.conn1.initialise_pheromone(task)
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)

        # evaporate 1
        pheromone = evaporate_pheromones(base_pheromones)
        self.conn1.evaporate_pheromone()
        self.assertEqual(self.conn1.get_pheromone(task), pheromone)

        # evaporate 2
        pheromone = evaporate_pheromones(pheromone)
        self.conn1.evaporate_pheromone()
        self.assertEqual(self.conn1.get_pheromone(task), pheromone)

    def test_initialise_pheromone(self):
        task = TaskA()
        self.conn1.initialise_pheromone(task)
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)

    def test_max_pheromone(self):
        task = TaskA()
        self.conn1.initialise_pheromone(task)
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_max_pheromone(task, 100)
        self.assertEqual(self.conn1.get_pheromone(task), 100)

    def test_get_max_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_max_pheromone(task), base_pheromones)
        self.conn1.initialise_pheromone(task)
        self.assertEqual(self.conn1.get_max_pheromone(task), base_pheromones)
        self.conn1.set_max_pheromone(task, 100)
        self.assertEqual(self.conn1.get_max_pheromone(task), 100)

    def test_add_pheromone_with_max(self):
        task = TaskA()
        max_pheromones = base_pheromones + 10
        self.conn1.initialise_pheromone(task)
        self.assertEqual(self.conn1.get_pheromone(task), base_pheromones)
        self.conn1.set_max_pheromone(task, max_pheromones)
        self.conn1.add_pheromone(task, 1)
        self.assertEqual(self.conn1.get_pheromone(task), max_pheromones)

    def test_different_connection_max_pheromones(self):
        task = TaskA()
        self.conn1.set_max_pheromone(task, 100)
        self.conn2.set_max_pheromone(task, 150)
        self.assertEqual(self.conn1.get_max_pheromone(task), 100)
        self.assertEqual(self.conn2.get_max_pheromone(task), 150)

    def test_get_set_min_pheromone(self):
        task = TaskA()
        self.conn1.set_min_pheromone(task, 100)
        self.conn2.set_min_pheromone(task, 150)
        self.assertEqual(self.conn1.get_min_pheromone(task), 100)
        self.assertEqual(self.conn2.get_min_pheromone(task), 150)

    def test_get_base_min_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_min_pheromone(task),
                get_base_min_pheromones(base_pheromones))

    def test_set_max_ph_below_min_ph(self):
        task = TaskA()
        self.conn1.set_min_pheromone(task, 100)
        self.assertEqual(self.conn1.get_min_pheromone(task), 100)
        self.conn1.set_max_pheromone(task, 80)
        self.assertEqual(self.conn1.get_pheromone(task), 80)
        self.assertEqual(self.conn1.get_min_pheromone(task), 80)
        self.assertEqual(self.conn1.get_max_pheromone(task), 80)

    def test_set_min_ph_above_max_ph(self):
        task = TaskA()
        # not yet initialised
        self.conn1.set_min_pheromone(task, 1001)
        self.assertEqual(self.conn1.get_min_pheromone(task), 1000)
        self.conn1.set_max_pheromone(task, 80)
        self.conn1.set_min_pheromone(task, 800)
        self.assertEqual(self.conn1.get_pheromone(task), 80)
        self.assertEqual(self.conn1.get_min_pheromone(task), 80)
        self.assertEqual(self.conn1.get_max_pheromone(task), 80)

    def test_min_phermone_limit(self):
        task = TaskA()
        # blocked by max pheromones
        self.conn1.set_min_pheromone(task, 1020)
        self.assertEqual(self.conn1.get_pheromone(task), 1000)
        self.assertEqual(self.conn1.get_min_pheromone(task), 1000)
        # raise max pheromones
        self.conn1.set_max_pheromone(task, 1050)
        self.assertEqual(self.conn1.get_pheromone(task), 1000)
        self.assertEqual(self.conn1.get_max_pheromone(task), 1050)
        self.conn1.set_min_pheromone(task, 1020)
        self.assertEqual(self.conn1.get_pheromone(task), 1020)
        self.assertEqual(self.conn1.get_min_pheromone(task), 1020)

class TestTaskFactory(unittest.TestCase):
    def setUp(self):
        self.taskfactory = TaskFactory()

    def test_create_task(self):
        isinstance(self.taskfactory.get_task(TaskFactory.tasks.TASKA), TaskA)
        isinstance(self.taskfactory.get_task(TaskFactory.tasks.TASKA), TaskB)
        isinstance(self.taskfactory.get_task(TaskFactory.tasks.TASKA), TaskC)

class TestUtilities(unittest.TestCase):
    def test_root_function(self):
        self.assertEqual(calc_nth_root(8, 3), 2)
        self.assertEqual(calc_nth_root(16, 2), 4)

    def test_min_pheromones(self):
        min_ph = calc_min_pheromones(base_pheromones, 3, 3, 0.05)
        self.assertEqual(min_ph, 300)
        min_ph = calc_min_pheromones(base_pheromones, 3, 3, 0.25)
        self.assertEqual(min_ph, 128)
        min_ph = calc_min_pheromones(base_pheromones, 3, 3, 0.5)
        self.assertEqual(min_ph, 61)
        min_ph = calc_min_pheromones(base_pheromones, 3, 3, 0.75)
        self.assertEqual(min_ph, 24)
        min_ph = calc_min_pheromones(base_pheromones, 3, 3, 1.0)
        self.assertEqual(min_ph, 0)

    def test_calc_max_pheromones(self):
        self.assertEqual(calc_max_pheromones(evaporation_rate, 1), 1111)
        self.assertEqual(calc_max_pheromones(evaporation_rate, 2), 555)
        self.assertEqual(calc_max_pheromones(evaporation_rate, 3), 370)
        self.assertEqual(calc_max_pheromones(evaporation_rate, 4), 277)
        self.assertEqual(calc_max_pheromones(evaporation_rate, 5), 222)

    def test_base_min_pheromones(self):
        self.assertEqual(get_base_min_pheromones(0), 1)
        self.assertEqual(get_base_min_pheromones(1), 1)
        self.assertEqual(get_base_min_pheromones(base_pheromones), 51)
        self.assertEqual(get_base_min_pheromones(1200), 61)
        self.assertEqual(get_base_min_pheromones(3000), 151)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnt)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConnection)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFactory)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilities)
    unittest.TextTestRunner(verbosity=2).run(suite)
