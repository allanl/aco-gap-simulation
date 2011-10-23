#!/usr/bin/python

from agent import Agent

if __name__ == '__main__':
    agents = [Agent('agent1', 2), Agent('agent2', 2)]
    for agent in agents:
        print agent
