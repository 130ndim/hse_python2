import ast


def fib(n):
    out = [0, 1]
    for i in range(n - 2):
        out.append(out[-1] + out[-2])
    return out[:n]


