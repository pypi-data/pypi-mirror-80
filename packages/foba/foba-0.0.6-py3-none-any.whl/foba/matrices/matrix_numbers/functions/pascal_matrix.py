from veho.matrix import iso


def upper_pascal_matrix(size):
    m = iso(size, size, None)
    c = -1
    while (c := c + 1) < size: m[0][c] = 1
    r = 0
    while (r := r + 1) < size:
        c = r - 1
        while (c := c + 1) < size:
            m[r][c] = m[r - 1][c - 1] + (0 if (v := m[r][c - 1]) is None else v)
    return m


def lower_pascal_matrix(size):
    m = iso(size, size, None)
    r = -1
    while (r := r + 1) < size: m[r][0] = 1
    c = 0
    while (c := c + 1) < size:
        r = c - 1
        while (r := r + 1) < size:
            m[r][c] = m[r - 1][c - 1] +(0 if (v := m[r - 1][c]) is None else v)
    return m


def symmetric_pascal_matrix(size):
    m = iso(size, size, None)
    i = -1
    while (i := i + 1) < size: m[0][i] = m[i][0] = 1
    r = 0
    while (r := r + 1) < size:
        c = 0
        while (c := c + 1) < size:
            m[r][c] = m[r - 1][c] + m[r][c - 1]
    return m
