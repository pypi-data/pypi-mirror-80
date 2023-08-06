from veho.matrix import iso


def zig_zag_matrix(n):
    mx = iso(n, n, 0)
    i, j, x = 1, 1, -1
    while ((x := x + 1) < n * n):
        mx[i - 1][j - 1] = x
        if (i + j) % 2 > 0:
            if i < n: i += 1
            else: j += 2
            if j > 1: j -= 1
        else:
            if j < n: j += 1
            else: i += 2
            if i > 1: i -= 1
    return mx
