#!/usr/bin/python

import unittest
from agent import Agent, TooManyConnections
from ant import Ant
from connection import Connection
from task import TaskA, TaskB, TaskC

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.max_connections = 2
        self.agent1 = Agent('agent1', self.max_connections)
        self.agent2 = Agent('agent2', self.max_connections)
        self.agent3 = Agent('agent3', self.max_connections)
        self.agent4 = Agent('agent4', self.max_connections)

    def test_connection_list_empty(self):
        self.assertEqual(self.agent1.connections, [])

    def test_max_connections_set(self):
        self.assertEqual(self.agent1.max_connections, self.max_connections)

    def test_connection_reciprocal(self):
        self.agent1.add_connection(self.agent2)
        self.assertTrue(self.agent1.has_connection(self.agent2))
        self.assertTrue(self.agent2.has_connection(self.agent1))
        self.assertFalse(self.agent1.has_connection(self.agent3))
        self.assertFalse(self.agent2.has_connection(self.agent3))

    def test_connecting_to_max(self):
        self.agent1.add_connection(self.agent2)
        self.agent1.add_connection(self.agent3)
        with self.assertRaises(TooManyConnections):
            self.agent1.add_connection(self.agent4)
        with self.assertRaises(TooManyConnections):
            self.agent4.add_connection(self.agent1)
        self.assertFalse(self.agent4.has_connection(self.agent1))

    def test_remove_connection(self):
        self.agent1.add_connection(self.agent2)
        self.agent1.add_connection(self.agent3)
        self.assertTrue(self.agent1.has_connection(self.agent2))
        self.assertTrue(self.agent1.has_connection(self.agent3))
        self.agent1.remove_connection(self.agent2)
        self.assertFalse(self.agent1.has_connection(self.agent2))
        self.assertFalse(self.agent2.has_connection(self.agent1))
        self.assertTrue(self.agent1.has_connection(self.agent3))
        self.assertTrue(self.agent3.has_connection(self.agent1))

    def test_set_check_task(self):
        task = TaskA()
        self.assertFalse(self.agent1.has_task(task))
        self.agent1.add_task(task)
        self.assertTrue(self.agent1.has_task(task))

class TestAnt(unittest.TestCase):
    def setUp(self):
        max_connections = 3
        self.agent1 = Agent('agent1', max_connections)
        self.agent2 = Agent('agent2', max_connections)
        self.agent1.add_connection(self.agent2)
        self.taska = TaskA()
        self.ant = Ant(self.agent1, self.taska, None)

    def test_walk(self):
        self.assertEqual(self.ant.get_location(), self.agent1)
        self.ant.walk()
        self.assertEqual(self.ant.get_location(), self.agent2)

    def test_clean_path(self):
        self.assertEqual(self.ant.get_location(), self.agent1)
        self.ant.walk()
        self.assertEqual(self.ant.get_location(), self.agent2)
        self.ant.walk()
        self.assertEqual(self.ant.get_location(), self.agent1)
        path = [self.agent1, self.agent2, self.agent1]
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        self.assertEqual(self.ant.get_path(), [self.agent1])

    def test_clean_path_start(self):
        agent1 = self.agent1
        agent2 = self.agent2
        agent3 = Agent('agent3', 2)
        agent4 = Agent('agent4', 2)
        path = [agent1, agent2, agent3, agent1, agent4, agent3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [agent1, agent4, agent3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_middle(self):
        agent1 = self.agent1
        agent2 = self.agent2
        agent3 = Agent('agent3', 2)
        agent4 = Agent('agent4', 2)
        path = [agent1, agent2, agent3, agent4, agent3, agent4]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [agent1, agent2, agent3, agent4]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_end(self):
        agent1 = self.agent1
        agent2 = self.agent2
        agent3 = Agent('agent3', 2)
        agent4 = Agent('agent4', 2)
        path = [agent1, agent2, agent3, agent4, agent3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [agent1, agent2, agent3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_clean_path_multiple(self):
        agent1 = self.agent1
        agent2 = self.agent2
        agent3 = Agent('agent3', 2)
        agent4 = Agent('agent4', 2)
        path = [agent1, agent2, agent3, agent1, agent3, agent4, agent3]
        self.ant.path = path
        self.assertEqual(self.ant.get_path(), path)
        self.ant.clean_path()
        path2 = [agent1, agent3]
        self.assertEqual(self.ant.get_path(), path2)

    def test_is_home_no_walk(self):
        self.assertFalse(self.ant.is_home())
        self.ant.walk()
        self.assertFalse(self.ant.is_home())
        self.agent1.add_task(self.taska)
        ant2 = Ant(self.agent1, self.taska, None)
        self.assertTrue(ant2.is_home())

    def test_is_going_home(self):
        self.assertFalse(self.ant.is_going_home())
        self.agent2.add_task(self.taska)
        self.ant.walk()
        self.assertTrue(self.ant.is_going_home())

    def test_is_home_after_walk(self):
        self.assertFalse(self.ant.is_going_home())
        self.agent2.add_task(self.taska)
        self.ant.walk()
        self.assertTrue(self.ant.is_going_home())
        self.assertFalse(self.ant.is_home())
        self.ant.walk()
        self.assertTrue(self.ant.is_home())

class TestConnection(unittest.TestCase):
    def setUp(self):
        self.max_connections = 7
        self.agent1 = Agent('agent1', self.max_connections)
        self.conn1 = Connection(self.agent1)

    def test_get_agent(self):
        self.assertEqual(self.agent1, self.conn1.get_agent())

    def test_add_pheromone(self):
        task = TaskA()
        self.assertEqual(self.conn1.get_pheromone(task), 0)
        self.conn1.add_pheromone(task, 3)
        self.assertEqual(self.conn1.get_pheromone(task), 3)
        self.conn1.add_pheromone(task, 3)
        self.assertEqual(self.conn1.get_pheromone(task), 6)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgent)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAnt)
    unittest.TextTestRunner(verbosity=2).run(suite)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConnection)
    unittest.TextTestRunner(verbosity=2).run(suite)
