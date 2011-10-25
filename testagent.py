#!/usr/bin/python

import unittest
from agent import Agent, TooManyConnections

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAgent)
    unittest.TextTestRunner(verbosity=2).run(suite)