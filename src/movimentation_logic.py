from knowledge_base import KnowledgeBase
from environment import WumpusWorld
from utilities import calculate_action
from utilities import possible_actions
from utilities import invert_position

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
        self.arrows_used = 0
        self.total_actions = 0

    def move_agent(self):

        i = 0
        while True:

            if i == 0:
                self.previous_position = self.position

                perception = self.world.get_perception(self.position)
                status, count = self.base.tell_perception(self.position, self.previous_position, perception)
            else:
                # Obtém todas as posições adjacentes e pergunta à base de conhecimento qual o melhor movimento
                actions = possible_actions(self.position)
                next_action = self.base.ask_knowledge_base(actions, self.previous_position)

                # Atualiza as posições anterior e atual do agente
                self.previous_position = self.position
                self.position = next_action

                # Atualiza a pontuação, direção anterior e atual do agente
                self.previous_pointing = self.pointing
                actual, self.pointing = calculate_action(self.previous_position, self.previous_pointing, self.position)
                self.total_actions += actual

                # Obtém a percepção da posição atual do agente
                perception = self.world.get_perception(self.position)

                # Informa à base de conhecimento a percepção atual para inferir possíveis objetos ao redor do agente
                status, count = self.base.tell_perception(self.position, self.previous_position, perception)

            # Caso em que o agente encontra uma parede
            if status == 'Volte':
                self.pointing = invert_position(self.previous_pointing)
                self.position = self.previous_position
                self.total_actions += 3     # Gira 180° e move para frente
                print('\nO agente encontrou uma parede e ficou na posição ' + str(self.position))

            # Caso em que o agente encontra o ouro
            elif status == 'Ouro':
                self.total_actions += 1     # Agarrar o ouro
                self.points += got_gold
                self.gold = True
                break

            # Se o agente estagna em busca pelo ouro, a exploração se encerra
            if count > 5:
                break

            i += 1

        self.points += self.total_actions * action_exe
