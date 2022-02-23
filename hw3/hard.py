from easy import Matrix
from utils import MatrixLike, elementwise_binary
import operator

import numpy as np


class HashMixin:
    data: MatrixLike

    def __hash__(self):
        # sum_ij(pow(i, x_ij)) % 1337
        return int(sum(sum(map(lambda x: (i + 1) ** x, row)) for i, row in enumerate(self.data)) % 1337)


class EqualMixin:
    data: MatrixLike

    def __eq__(self, other: "HashableMatrix") -> bool:
        return all(map(all, elementwise_binary(operator.eq, self.data, other.data)))


class CacheMixin:
    __cache__: dict[tuple[int, int], int] = {}

    @classmethod
    def reset_cache(cls):
        cls.__cache__.clear()


class HashableMatrix(Matrix, HashMixin, CacheMixin):
    __cache__ = {}
    __hash__ = HashMixin.__hash__

    def __matmul__(self, other: "HashableMatrix") -> "HashableMatrix":
        key = (hash(self), hash(other))
        if key not in self.__cache__:
            self.__cache__[key] = super().__matmul__(other)
        return self.__cache__[key]


if __name__ == '__main__':
    np.random.seed(1337)
    a = HashableMatrix(np.random.randint(0, 10, (10, 10)).tolist())  # noqa
    b = HashableMatrix(np.random.randint(0, 10, (10, 10)).tolist())  # noqa

    c = HashableMatrix(np.random.randint(0, 10, (10, 10)).tolist())  # noqa

    a_hash = hash(a)
    while True:
        ab, cd = a @ b, c @ b
        if a_hash == hash(c) and a != c:
            break
        c = HashableMatrix(np.random.randint(0, 10, (10, 10)).tolist())  # noqa

    HashableMatrix.reset_cache()
    cd = c @ b

    with open('./artifacts/A.txt', 'w') as f:
        f.write(str(a.data))

    with open('./artifacts/B.txt', 'w') as f:
        f.write(str(b.data))

    with open('./artifacts/C.txt', 'w') as f:
        f.write(str(c.data))

    with open('./artifacts/D.txt', 'w') as f:
        f.write(str(b.data))

    with open('./artifacts/AB.txt', 'w') as f:
        f.write(str(ab.data))

    with open('./artifacts/CD.txt', 'w') as f:
        f.write(str(cd.data))

    with open('./artifacts/hash.txt', 'w') as f:
        f.write(str(hash(ab)) + ' ' + str(hash(cd)))
