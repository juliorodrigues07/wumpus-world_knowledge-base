from environment import WumpusWorld
from environment import random
from environment import size
from environment import player_position
from environment import adj1
from environment import adj2


class KnowledgeBase:

    def __init__(self, world : WumpusWorld):

        self.visited = [[size - 2, 1]]
        self.safe = None
        self.possible_danger = None
        self.danger = None
        self.unknown = None
        self.get_unknown_positions()

    def get_unknown_positions(self):

        positions = list()

        for x in range(size):
            for y in range(size):
                if [x, y] != player_position and [x, y] != adj1 and [x, y] != adj2:
                    positions.append([x, y])

        self.unknown = positions

    def tell_perception(self, position, perception):

        print(perception)


# Teste
def main():

    world = WumpusWorld()
    base = KnowledgeBase(world)

    for i in range(size):
        print(world.field[i])

    print(base.unknown)
    print(base.safe)
    print(base.visited)


if __name__ == '__main__':
    main()
