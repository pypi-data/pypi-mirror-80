def is_prime(n):
    if n < 2: return False
    if not n % 2: return n == 2
    if not n % 3: return n == 3
    d = 5
    while d * d <= n:
        if not n % d: return False
        d += 2
        if not n % d: return False
        d += 4
    return True


def primes(size):
    vec, num = [], 1
    while True:
        if is_prime(num := num + 1):
            vec.append(num)
            if len(vec) >= size: break
    return vec
