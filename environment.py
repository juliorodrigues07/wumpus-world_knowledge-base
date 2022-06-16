from Cryptodome.Random import random


# Dimensão do tamanho da malha
# 6 -> matriz 4 x 4, as linhas e colunas 0 e 5 correspondem apenas às paredes do mundo como delimitadores
size = 6

# Probabilidade de uma posição qualquer do mundo (exceto a inicial) ser um poço
prob = 0.2

# Posições adjacentes ao jogador em que não podem ser colocados poços ou o Wumpus
adj1 = [size - 2, 0]
adj2 = [size - 1, 1]


class WumpusWorld:

    def __init__(self):

        self.field = [['0'] * size for i in range(size)]
        self.limits = [['0'] * size for i in range(size)]
        self.player = [size - 1, 0]
        self.perceptions = None
        self.wumpus = 0

        self.place_limits()
        self.place_player()
        self.place_gold()
        self.place_wumpus()
        self.place_pits()
        self.perceptions_build()

    @staticmethod
    def random_pair():

        x = random.randrange(size)
        y = random.randrange(size)

        return x, y

    def place_player(self):

        self.field[size - 2][1] = 'Jogador'

    def place_gold(self):

        while True:
            x, y = self.random_pair()

            if self.field[x][y] == '0' and self.limits[x][y] != 'Wall':
                self.field[x][y] = 'Ouro'
                break

    def place_wumpus(self):

        while True:
            x, y = self.random_pair()

            if self.field[x][y] == '0' and [x, y] != adj1 and [x, y] != adj2 and self.limits[x][y] != 'Wall':
                self.field[x][y] = 'Wumpus'
                self.wumpus = 1
                break

    def place_pits(self):
        n_pits = int((pow(size - 2, 2) - 1) * prob)

        i = 0
        while i < n_pits:
            x, y = self.random_pair()

            if self.field[x][y] == '0' and [x, y] != adj1 and [x, y] != adj2 and self.limits[x][y] != 'Wall':
                self.field[x][y] = 'Poço'
                i += 1

    def place_limits(self):

        for x in range(size):
            for y in range(size):
                if (x == 0) or (y == 0) or (x == size - 1) or (y == size - 1):
                    self.limits[x][y] = 'Wall'

    # Checa se existem posições válidas acima, abaixo, à esquerda e à direta da posição dada, respectivamente
    def adjacent(self, x, y):

        adjacents = list()

        if x - 1 > 0:
            adjacents.append(self.field[x - 1][y])
        else:
            adjacents.append('None')

        if x + 1 < size - 1:
            adjacents.append(self.field[x + 1][y])
        else:
            adjacents.append('None')

        if y - 1 > 0:
            adjacents.append(self.field[x][y - 1])
        else:
            adjacents.append('None')

        if y + 1 < size - 1:
            adjacents.append(self.field[x][y + 1])
        else:
            adjacents.append('None')

        return adjacents

    def perceptions_build(self):

        field = list()

        for x in range(size):
            perception_line = list()

            for y in range(size):

                perception = ['Nada', 'Nada', 'Nada', 'Nada', 'Nada']
                neighbors = self.adjacent(x, y)

                if self.limits[x][y] == 'Wall':
                    perception[3] = 'Impacto'
                else:
                    if 'Wumpus' in neighbors:
                        perception[0] = 'Fedor'
                    elif 'Poço' in neighbors:
                        perception[1] = 'Brisa'
                    elif self.field[x][y] == 'Ouro':
                        perception[2] = 'Resplendor'

                perception_line.append(perception)

            field.append(perception_line)

        self.perceptions = field


def main():

    test = WumpusWorld()
    for i in range(size):
        print(test.field[i])

    for i in range(size):
        print(test.perceptions[i])


if __name__ == '__main__':
    main()