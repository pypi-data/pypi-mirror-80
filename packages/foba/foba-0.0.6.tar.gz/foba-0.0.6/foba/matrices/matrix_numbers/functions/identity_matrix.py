from veho.matrix import init


def identity_matrix(size):
    return init(size, size, lambda x, y: 1 if x == y else 0)
