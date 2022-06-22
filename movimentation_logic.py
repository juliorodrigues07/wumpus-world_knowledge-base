from knowledge_base import KnowledgeBase
from environment import WumpusWorld
from environment import random

# Medida de desempenho
got_gold = 1000
got_killed = -1000
action_exe = 1
arrow_use = -10


class Exploration:

    def __init__(self, world : WumpusWorld, base : KnowledgeBase):

        self.world = world
        self.base = base
        self.position = world.agent
        self.pointing = 'Direita'
        self.time = 0
        self.points = 0
        self.gold = False
        self.alive = True

        self.previous_position = world.agent
        self.wumpus_killed = 0
        self.pits_fallen = 0
        self.visited_positions = 0
        self.actual_action = None
        self.total_actions = 0
        self.arrows_used = 0

    @staticmethod
    def possible_actions(position):

        return [[position[0] - 1, position[1]], [position[0], position[1] - 1],
                [position[0] + 1, position[1]], [position[0], position[1] + 1]]

    def moving(self):

        n = self.possible_actions(self.position)
        x = random.randrange(4)

        next_action = n[x]
        self.position = next_action

        perception = self.world.get_perception(self.position)
        self.base.tell_perception(self.position, perception)

    # def analyze perception(): tell


# Teste
def main():

    world = WumpusWorld()
    base = KnowledgeBase(world)
    t = Exploration(world, base)
    t.moving()


if __name__ == '__main__':
    main()
