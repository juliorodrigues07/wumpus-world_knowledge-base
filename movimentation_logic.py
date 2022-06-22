from knowledge_base import KnowledgeBase
from environment import WumpusWorld
from environment import random
from utilities import possible_actions

# Medida de desempenho
got_gold = 1000
got_killed = -1000
action_exe = 1
arrow_use = -10


class Exploration:

    def __init__(self, world: WumpusWorld, base: KnowledgeBase):

        self.world = world
        self.base = base
        self.position = world.agent
        self.pointing = 'Direita'
        self.time = 0
        self.points = 0
        self.gold = False
        self.alive = True

        self.previous_position = world.agent
        self.previous_pointing = 'Direita'
        self.wumpus_killed = 0
        self.pits_fallen = 0
        self.visited_positions = 0
        self.actual_action = None
        self.total_actions = 0
        self.arrows_used = 0

    def move_agent(self):

        n = possible_actions(self.position)
        s = random.randrange(4)
        next_action = n[s]

        while self.base.ask_knowledge_base(next_action):
            s = random.randrange(4)
            next_action = n[s]

        self.previous_position = self.position
        self.position = next_action

        perception = self.world.get_perception(self.position)
        wall = self.base.tell_perception(self.position, self.previous_position, perception)

        if not wall:
            self.position = self.previous_position
            self.total_actions += 3

        print(self.total_actions)

    # def analyze perception(): tell


# Teste
def main():

    world = WumpusWorld()
    base = KnowledgeBase(world)
    t = Exploration(world, base)
    t.move_agent()


if __name__ == '__main__':
    main()
