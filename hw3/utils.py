from typing import Callable, Sequence, TypeVar

T = TypeVar('T', int, float)
MatrixLike = Sequence[Sequence[T]]


def elementwise_binary(op: Callable[[tuple[T, T]], T], a: MatrixLike, b: MatrixLike) -> MatrixLike:
    return list(map(lambda x: list(map(lambda tup: op(*tup), zip(*x))), zip(a, b)))


def check_dims_binary(a: MatrixLike, b: MatrixLike) -> None:
    if len(a) != len(b):
        raise ValueError('Dimension 0 size mismatch: %d, %d' % (len(a), len(b)))

    if len(a[0]) != len(b[0]):
        raise ValueError('Dimension 1 size mismatch: %d, %d' % (len(a[0]), len(b[0])))


def check_dims_matmul(a: MatrixLike, b: MatrixLike) -> None:
    if len(a[0]) != len(b):
        raise ValueError('Dimension 1 of a must be equal to dimension 0 of b, got: %d, %d' % (len(a[0]), len(b)))
