from knowledge_base import KnowledgeBase
from environment import WumpusWorld
from environment import random
from environment import size
from utilities import possible_actions

# Medida de desempenho
got_gold = 1000
got_killed = -1000
action_exe = -1
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

        i = 0
        while True:

            if i == 0:
                self.previous_position = self.position
                perception = self.world.get_perception(self.position)
                status, count = self.base.tell_perception(self.position, self.previous_position, perception)
            else:
                actions = possible_actions(self.position)
                next_action = self.base.ask_knowledge_base(actions, self.previous_position)

                self.previous_position = self.position
                self.position = next_action

                perception = self.world.get_perception(self.position)
                status, count = self.base.tell_perception(self.position, self.previous_position, perception)

            if status == 'Volte':
                self.position = self.previous_position
                self.total_actions += 3
            elif status == 'Ouro':
                self.total_actions += 1
                self.points += got_gold
                print("GOLD!")
                return True

            if count > 20:
                break

            i += 1

        print(self.total_actions)


# Teste
def main():

    world = WumpusWorld()

    print('\n')
    for i in range(size):
        print(world.field[i])
    print('\n')
    for i in range(size):
        print(world.perceptions[i])

    base = KnowledgeBase(world)
    t = Exploration(world, base)
    t.move_agent()


if __name__ == '__main__':
    main()
