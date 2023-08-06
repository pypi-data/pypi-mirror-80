from random import uniform


def compound_interest(hi, r=uniform(0.01, 0.3), d=3):
    r += 1
    n = 1
    return [round(n := n * r, d) for _ in range(hi)]
