from environment import WumpusWorld
from environment import size
from environment import player_position
from utilities import possible_actions
from utilities import exclude_walls
from utilities import random


class KnowledgeBase:

    def __init__(self, world: WumpusWorld):

        self.visited = [world.agent]
        self.safe = [world.agent]
        self.limits = list()
        self.danger = list()
        self.unknown = list()

        self.possible_pit = list()
        self.possible_wumpus = list()
        self.no_pits = list()
        self.no_wumpus = list()
        self.max_iterations = 0

        self.get_unknown_positions()

    def get_unknown_positions(self):

        positions = list()

        # Obtém todas as posições do mundo, exceto a que o agente começa
        for x in range(size):
            for y in range(size):
                if [x, y] != player_position:
                    positions.append([x, y])

        self.unknown = positions.copy()

    def tell_perception(self, position, previous_position, perception):

        # Se a posição atual é visitada pela primeira vez, adiciona-se a lista de visitados e zera o contador para continuar a exploração
        if position not in self.visited:
            self.max_iterations = 0
            self.visited.append(position)
        else:
            self.max_iterations += 1

        # Se a posição atual era desconhecida, obviamente ela é conhecida agora
        if position in self.unknown:
            self.unknown.remove(position)

        print('\n')
        print("Posição atual:          " + str(position))
        print("Percepção atual:        " + str(perception))
        print("Posições desconhecidas: " + str(self.unknown))

        # Se o agente caminha para uma parede, este recebe uma percepção de impacto e deve voltar para sua posição anterior
        if perception[3] == 'Impacto':
            self.limits.append(position)
            return 'Volte', self.max_iterations

        if perception[2] == 'Resplendor':
            return 'Ouro', self.max_iterations

        if position not in self.safe:
            self.safe.append(position)

        # Obtém todos os adjacentes da posição atual, excetuando a anterior
        adjacent = possible_actions(position)
        if position != previous_position:
            adjacent.remove(previous_position)

        # Se a percepção atual indica perigo, as posições adjacentes são marcadas indicando os locais onde o agente não poderia se arriscar
        for i in range(len(adjacent)):

            # Analisa somente posições interiores ao mundo (Exclui as paredes)
            if exclude_walls(adjacent[i], size):

                # Se não há brisa ou fedor, as posições adjacentes são seguras
                if perception[0] == 'Nada' and perception[1] == 'Nada' and adjacent[i] not in self.safe:
                    self.safe.append(adjacent[i])

                if perception[0] == 'Fedor' and adjacent[i] not in self.safe and\
                        adjacent[i] not in self.possible_wumpus and adjacent[i] not in self.no_wumpus:
                    self.possible_wumpus.append(adjacent[i])
                if perception[1] == 'Brisa' and adjacent[i] not in self.safe and\
                        adjacent[i] not in self.possible_pit and adjacent[i] not in self.no_pits:
                    self.possible_pit.append(adjacent[i])

                # O agente pode descartar possíveis Wumpus e poços em determinadas posições de acordo com percepções anteriores
                if perception[0] == 'Nada' and adjacent[i] in self.possible_wumpus:
                    self.no_wumpus.append(adjacent[i])
                if perception[1] == 'Nada' and adjacent[i] in self.possible_pit:
                    self.no_pits.append(adjacent[i])

        for x in self.no_wumpus:
            if x in self.possible_wumpus:
                self.possible_wumpus.remove(x)

        for x in self.no_pits:
            if x in self.possible_pit:
                self.possible_pit.remove(x)

        print("Possível Poço em:       " + str(self.possible_pit))
        print("Possível Wumpus em:     " + str(self.possible_wumpus))
        print("Posições seguras:       " + str(self.safe))

        return 'Continue', self.max_iterations

    def ask_knowledge_base(self, actions):

        safe_spots = list()

        # Este laço possibilita o agente caminha para uma parede, recebendo como percepção um impacto
        # Retorna uma ação que garante a segurança do agente, priorizando por posições desconhecidas no mundo
        for i in range(len(actions)):
            if actions[i] in self.unknown and actions[i] not in self.possible_wumpus and actions[i] not in self.possible_pit:
                return actions[i]

        # Procura por posições seguras, mas não visitadas
        for i in range(len(actions)):
            if actions[i] in self.safe and actions[i] not in self.visited:
                return actions[i]

        # Por fim, retorna uma posição segura e já visitada, em caso negativo nas 2 condições anteriores
        for i in range(len(actions)):
            if actions[i] in self.safe:
                safe_spots.append(actions[i])

        return random.choice(safe_spots)
