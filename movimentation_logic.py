from environment import WumpusWorld
from environment import random

# Medida de desempenho
got_gold = 1000
got_killed = -1000
action_exe = 1
arrow_use = -10


class Exploration:

    def __init__(self, world : WumpusWorld):

        self.world = world
        self.position = None
        self.pointing = 'Direita'
        self.time = 0
        self.points = 0
        self.gold = 0
        self.alive = 0

        self.wumpus_killed = 0
        self.pits_fallen = 0
        self.visited_positions = 0
        self.actual_action = 0
        self.total_actions = 0
        self.arrows_used = 0

