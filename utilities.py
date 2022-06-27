from Cryptodome.Random import random


def possible_actions(position):

    return [[position[0] - 1, position[1]], [position[0], position[1] - 1],
            [position[0] + 1, position[1]], [position[0], position[1] + 1]]


def random_pair(size):

    x = random.randrange(size)
    y = random.randrange(size)

    return x, y


def invert_position(previous_pointing):

    if previous_pointing == 'Direita':
        return 'Esquerda'
    elif previous_pointing == 'Esquerda':
        return 'Direita'
    elif previous_pointing == 'Cima':
        return 'Baixo'
    else:
        return 'Cima'


def calculate_action(previous_position, previous_pointing, position):

    pointing = str()
    actions = 1
    x1, y1 = previous_position[0], previous_position[1]
    x2, y2 = position[0], position[1]

    if x2 > x1 and y2 == y1:
        pointing = 'Baixo'

        if previous_pointing == 'Cima':
            actions += 2
        elif previous_pointing == 'Direita' or previous_position == 'Esquerda':
            actions += 1

    elif x2 < x1 and y2 == y1:
        pointing = 'Cima'

        if previous_pointing == 'Baixo':
            actions += 2
        elif previous_pointing == 'Direita' or previous_position == 'Esquerda':
            actions += 1

    elif x2 == x1 and y2 > y1:
        pointing = 'Direita'

        if previous_pointing == 'Esquerda':
            actions += 2
        elif previous_pointing == 'Cima' or previous_position == 'Baixo':
            actions += 1

    elif x2 == x1 and y2 < y1:
        pointing = 'Esquerda'

        if previous_pointing == 'Direita':
            actions += 2
        elif previous_pointing == 'Cima' or previous_position == 'Baixo':
            actions += 1

    return actions, pointing
