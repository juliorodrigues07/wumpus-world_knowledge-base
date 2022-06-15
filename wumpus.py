from Cryptodome.Random import random


# Dimensão do tamanho da malha
size = 4

# Probabilidade de uma posição qualquer do mundo (exceto a inicial) ser um poço
prob = 0.2

# Posições adjacentes ao jogador em que não podem ser colocados poços ou o Wumpus
adj1 = [size - 2, 0]
adj2 = [size - 1, 1]


class WumpusWorldBuilder:

    def __init__(self):

        self.field = [['0'] * size for i in range(size)]
        self.player = None
        self.perceptions = None
        self.wumpus = 0
        self.place_player()
        self.place_gold()
        self.place_wumpus()
        self.place_pits()

    @staticmethod
    def random_pair():

        x = random.randrange(size)
        y = random.randrange(size)

        return x, y

    def place_player(self):

        self.field[size - 1][0] = 'Player'

    def place_gold(self):

        while True:
            x, y = self.random_pair()

            if self.field[x][y] == '0':
                self.field[x][y] = 'Gold'
                break

    def place_wumpus(self):

        while True:
            x, y = self.random_pair()

            if self.field[x][y] == '0' and [x, y] != adj1 and [x, y] != adj2:
                self.field[x][y] = 'Wumpus'
                self.wumpus = 1
                break

    def place_pits(self):

        n_pits = int((pow(size, 2) - 1) * prob)

        i = 0
        while i < n_pits:
            x, y = self.random_pair()

            if self.field[x][y] == '0' and [x, y] != adj1 and [x, y] != adj2:
                self.field[x][y] = 'Pit'
                i += 1


def main():

    test = WumpusWorldBuilder()
    for i in range(size):
        print(test.field[i])


if __name__ == '__main__':
    main()
