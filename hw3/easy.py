import operator
from typing import Generic

from utils import T, MatrixLike, check_dims_binary, check_dims_matmul, elementwise_binary


class Matrix(Generic[T]):
    def __init__(self, data: MatrixLike) -> None:
        self.data = data

    def __add__(self, other: "Matrix[T]") -> "Matrix[T]":
        check_dims_binary(self.data, other.data)
        return type(self)(elementwise_binary(operator.add, self.data, other.data))

    def __mul__(self, other: "Matrix[T]") -> "Matrix[T]":
        check_dims_binary(self.data, other.data)
        return type(self)(elementwise_binary(operator.mul, self.data, other.data))

    def __matmul__(self, other: "Matrix[T]") -> "Matrix[T]":
        check_dims_matmul(self.data, other.data)
        return type(self)([[sum(a * b for a, b in zip(ar, bc)) for bc in zip(*other.data)] for ar in self.data])


if __name__ == '__main__':
    import numpy as np

    np.random.seed(0)

    a = Matrix(np.random.randint(0, 10, (10, 10)))  # noqa
    b = Matrix(np.random.randint(0, 10, (10, 10)))  # noqa

    with open('./artifacts/matrix+.txt', 'w') as f:
        f.write(str((a + b).data))

    with open('./artifacts/matrix*.txt', 'w') as f:
        f.write(str((a * b).data))

    with open('./artifacts/matrix@.txt', 'w') as f:
        f.write(str((a @ b).data))
