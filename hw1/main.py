from typing import List


def fib(n: int) -> List[int]:
    out = [0, 1]
    for i in range(n - 2):
        out.append(out[-1] + out[-2])
    return out[:n]


if __name__ == '__main__':
    from visualizer import draw_ast

    draw_ast(fib).savefig('artifacts/ast.png')
