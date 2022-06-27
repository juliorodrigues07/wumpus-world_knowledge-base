from movimentation_logic import Exploration
from knowledge_base import KnowledgeBase
from environment import WumpusWorld
from environment import size


class Main:

    print('\nGerando a configuração inicial do Mundo do Wumpus ' + str(size - 1) + 'x' + str(size - 1) + '...\n')
    world = WumpusWorld()

    print("\n\t MUNDO GERADO:")
    print('\n')
    for i in range(size):
        print(world.field[i])
    print('\n')
    for i in range(size):
        print(world.perceptions[i])

    base = KnowledgeBase(world)
    t = Exploration(world, base)
    t.move_agent()

    if t.gold:
        print('\nOuro encontrado!')
    else:
        print('\nO agente não conseguiu encontrar o ouro!')

    print('\nPontuação: ' + str(t.points))


if __name__ == '__main__':
    Main()
