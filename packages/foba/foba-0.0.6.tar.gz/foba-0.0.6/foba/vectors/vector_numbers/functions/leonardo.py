def leonardo_generator():
    yield (prev := 1)
    yield (curr := 1)
    while True:
        prev, curr = curr, prev + curr + 1
        yield curr


def leonardo(n):
    gen = leonardo_generator()
    return [next(gen) for _ in range(n)]
