def fibonacci_generator():
    prev, curr = 0, 1
    while True:
        yield curr
        prev, curr = curr, prev + curr


def fibonacci(n):
    # vec = []
    gen = fibonacci_generator()
    # while (n := n - 1) >= 0:
    #     vec.append(next(gen))
    # return vec
    return [next(gen) for _ in range(n)]
