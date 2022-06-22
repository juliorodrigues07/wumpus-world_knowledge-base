from environment import WumpusWorld
from environment import random
from environment import size
from environment import player_position
from environment import adj1
from environment import adj2
from utilities import possible_actions


class KnowledgeBase:

    def __init__(self, world : WumpusWorld):

        self.visited = [[size - 2, 1]]
        self.safe = list()
        self.possible_danger = list()
        self.limits = list()
        self.danger = list()
        self.unknown = None
        self.get_unknown_positions()

    def get_unknown_positions(self):

        positions = list()

        for x in range(size):
            for y in range(size):
                if [x, y] != player_position and [x, y] != adj1 and [x, y] != adj2:
                    positions.append([x, y])

        self.unknown = positions

    def tell_perception(self, position, previous_position, perception):

        # Se o agente caminha para uma parede, este recebe uma percepção de impacto e deve voltar para sua posição anterior
        if perception[3] == 'Impacto':
            self.limits.append(position)
            return False

        # Obtém todos os adjacentes da posição atual, excetuando a anterior
        n = possible_actions(position)
        n.remove(previous_position)

        # Se a percepção atual indica perigo, as posições adjacentes são marcadas indicando os locais onde o agente não poderia se arriscar
        for i in range(3):
            if perception[0] == 'Fedor' or perception[1] == 'Brisa':
                self.possible_danger.append(n[i])
            else:
                self.safe.append(n[i])

        print(perception)
        print(self.possible_danger)
        print(self.safe)
        print(position)

        return True

    def ask_knowledge_base(self, position):

        if position in self.possible_danger or position in self.danger:
            return True


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
