from Cryptodome.Random import random


def possible_actions(position):

    x, y = position[0], position[1]
    return [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]


def exclude_walls(position, size):

    x, y = position[0], position[1]
    return x > 0 and y > 0 and x < size - 1 and y < size - 1


def random_pair(size):

    x = random.randrange(size)
    y = random.randrange(size)

    return x, y
