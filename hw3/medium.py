import numpy as np
import numpy.typing as npt

import numbers


class DataMixin:
    _data: npt.ArrayLike

    @property
    def data(self) -> npt.ArrayLike:
        return self._data

    @data.setter
    def data(self, data: npt.ArrayLike) -> None:
        if len(set(map(len, data))) > 1:
            raise ValueError('The number of elements in each row is not the same')
        self._data = data


class ReprMixin:
    data: npt.ArrayLike

    def __repr__(self) -> str:
        return '\n'.join(map(lambda x: '| ' + str(x)[1:-1] + ' |', self.data))


class SaveToFileMixin:
    def save(self, path: str) -> None:
        with open(path, 'w') as f:
            f.write(str(self))


class Matrix(
    np.lib.mixins.NDArrayOperatorsMixin,
    DataMixin,
    ReprMixin,
    SaveToFileMixin,
):
    _HANDLED_TYPES = (np.ndarray, numbers.Number, list, tuple)

    def __init__(self, data: npt.ArrayLike):
        self.data = data

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # From NDArrayOperatorsMixin doc
        out = kwargs.get('out', ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.data if isinstance(x, Matrix) else x for x in inputs)
        if out:
            kwargs['out'] = tuple(x.data if isinstance(x, Matrix) else x for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


if __name__ == '__main__':
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = np.random.randint(0, 10, (10, 10))

    print(a @ b.tolist())
