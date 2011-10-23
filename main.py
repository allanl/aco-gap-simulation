#!/usr/bin/python

from agent import Agent
from ant import Ant

if __name__ == '__main__':
    agents = [Agent('agent1', 2), Agent('agent2', 2)]
    for agent in agents:
        print agent

    ants = [Ant(agents[0], 'service A')]
    ants.append(Ant(agents[1], 'service B'))
    for ant in ants:
        print ant
