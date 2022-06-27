from environment import WumpusWorld
from environment import size
from environment import player_position
from utilities import possible_actions


class KnowledgeBase:

    def __init__(self, world: WumpusWorld):

        self.visited = [world.agent]
        self.safe = [world.agent]
        self.limits = list()
        self.danger = list()
        self.unknown = list()

        self.possible_pit = list()
        self.possible_wumpus = list()
        self.max_iterations = 0

        self.get_unknown_positions()

    def get_unknown_positions(self):

        positions = list()

        for x in range(size):
            for y in range(size):
                if [x, y] != player_position:
                    positions.append([x, y])

        self.unknown = positions.copy()

    def tell_perception(self, position, previous_position, perception):

        print('\n')
        print("Posição atual:          " + str(position))
        print("Percepção atual:        " + str(perception))
        print("Posições desconhecidas: " + str(self.unknown))

        if position not in self.visited:
            self.max_iterations = 0
            self.visited.append(position)
        else:
            self.max_iterations += 1

        if position in self.unknown:
            self.unknown.remove(position)

        # Se o agente caminha para uma parede, este recebe uma percepção de impacto e deve voltar para sua posição anterior
        if perception[3] == 'Impacto':
            self.limits.append(position)
            self.safe.remove(position)
            return 'Volte', self.max_iterations

        if perception[2] == 'Resplendor':
            return 'Ouro', self.max_iterations

        # Obtém todos os adjacentes da posição atual, excetuando a anterior
        adjacent = possible_actions(position)
        if position != previous_position:
            adjacent.remove(previous_position)

        # Se a percepção atual indica perigo, as posições adjacentes são marcadas indicando os locais onde o agente não poderia se arriscar
        for i in range(len(adjacent)):
            if perception[0] == 'Fedor' and adjacent[i] not in self.safe and adjacent[i] not in self.possible_wumpus:
                self.possible_wumpus.append(adjacent[i])
            elif perception[1] == 'Brisa' and adjacent[i] not in self.safe and adjacent[i] not in self.possible_pit:
                self.possible_pit.append(adjacent[i])
            elif adjacent[i] not in self.safe:
                self.safe.append(adjacent[i])

        print("Possível Poço em:       " + str(self.possible_pit))
        print("Possível Wumpus em:     " + str(self.possible_wumpus))
        print("Posições seguras:       " + str(self.safe))

        return 'Continue', self.max_iterations

    def ask_knowledge_base(self, actions, previous_position):

        # Retorna uma ação que garante a segurança do agente, priorizando por posições ainda não visitadas no mundo
        for i in range(len(actions)):
            if actions[i] in self.unknown and actions[i] not in self.possible_wumpus and actions[i] not in self.possible_pit:
                return actions[i]

        for i in range(len(actions)):
            if actions[i] in self.safe and actions[i] not in self.visited and\
                    actions[i] not in self.possible_wumpus and actions[i] not in self.possible_pit:
                return actions[i]

        return previous_position
