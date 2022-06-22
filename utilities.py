
def possible_actions(position):
    return [[position[0] - 1, position[1]], [position[0], position[1] - 1],
            [position[0] + 1, position[1]], [position[0], position[1] + 1]]
