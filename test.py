#!/usr/bin/python

import unittest
from node import Node, TooManyConnections
from ant import Ant
from connection import Connection
from task import TaskA, TaskB, TaskC
from taskfactory import TaskFactory

class TestNode(unittest.TestCase):
    def setUp(self):
        self.max_connections = 2
        self.node1 = Node('node1', self.max_connections)
        self.node2 = Node('node2', self.max_connections)
        self.node3 = Node('node3', self.max_connections)
        self.node4 = Node('node4', self.max_connections)

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

    def test_set_check_task_instance(self):
        task = TaskA()
        self.assertFalse(self.node1.has_task(task))
        self.node1.add_task(task)
        self.assertTrue(self.node1.has_task(task))
        taska = TaskA()
        self.assertTrue(self.node1.has_task(taska))

    def test_no_connect_to_self(self):
        self.assertFalse(self.node1.has_connection(self.node1))
        self.node1.add_connection(self.node1)
        self.assertFalse(self.node1.has_connection(self.node1))

    def test_set_get_pheromones(self):
        task = TaskA()
        self.node1.add_connection(self.node2)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, task), 1000)
        self.node1.add_conn_pheromones(self.node2, task, 3)
        self.assertEqual(self.node1.get_conn_pheromones(self.node2, task), 1033)

class TestAnt(unittest.TestCase):
    def setUp(self):
        max_connections = 3
        self.node1 = Node('node1', max_connections)
        self.node2 = Node('node2', max_connections)
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
        node3 = Node('node3', 2)
        node4 = Node('node4', 2)
        path = [node1, node2, node3, node1, node4, node3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node4, node3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_middle(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2)
        node4 = Node('node4', 2)
        path = [node1, node2, node3, node4, node3, node4]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node2, node3, node4]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_end(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2)
        node4 = Node('node4', 2)
        path = [node1, node2, node3, node4, node3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [node1, node2, node3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_multiple(self):
        node1 = self.node1
        node2 = self.node2
        node3 = Node('node3', 2)
        node4 = Node('node4', 2)
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

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.max_connections = 7
        self.node1 = Node('node1', self.max_connections)
        self.conn1 = Connection(self.node1)

    def test_get_node(self):
        self.assertEqual(self.node1, self.conn1.get_node())

    def test_add_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), 1000)
        self.conn1.add_pheromone(task, 3)
        self.assertEqual(self.conn1.get_pheromone(task), 1033)
        self.conn1.add_pheromone(task, 3)
        self.assertEqual(self.conn1.get_pheromone(task), 1066)

    def test_evaporate_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), 1000)
        # initialise pheromone
        self.conn1.add_pheromone(task, 1)
        self.assertEqual(self.conn1.get_pheromone(task), 1100)
        # 10% evaporation -> 1100 * .9 = 990
        self.conn1.evaporate_pheromone()
        self.assertEqual(self.conn1.get_pheromone(task), 990)
        # 10% evaporation -> 990 * .9 = 891
        self.conn1.evaporate_pheromone()
        self.assertEqual(self.conn1.get_pheromone(task), 891)

class TestTaskFactory(unittest.TestCase):
    def setUp(self):
        pass

    def test_create_task(self):
        isinstance(TaskFactory.get_task(TaskFactory.tasks.TASKA), TaskA)
        isinstance(TaskFactory.get_task(TaskFactory.tasks.TASKA), TaskB)
        isinstance(TaskFactory.get_task(TaskFactory.tasks.TASKA), TaskC)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNode)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnt)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConnection)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTaskFactory)
    unittest.TextTestRunner(verbosity=2).run(suite)
