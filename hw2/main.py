from typing import Sequence, Union


Element = Union[bool, int, float, str, bytes]


def encode_row(row: Sequence[Element]) -> str:
    return ' & '.join(map(str, row))


def get_latex_str(table: Sequence[Sequence[Element]]) -> str:
    m = len(table[0])

    header = "\\begin{tabular}{" + 'c'.join('|' for i in range(m + 1)) + '}\n    \\hline\n'
    footer = "\n    \\hline \n\\end{tabular}"
    return header + '\n    \\hline\n'.join('    ' + r + ' \\' for r in map(encode_row, table)) + footer


if __name__ == '__main__':
    t = \
        [
            ['aaa', 1, 2, 3],
            ['bbb', 4, 5, 6],
            ['ccc', 7, 8, 9],
            ['ddd', 10, 11, 12],
        ]

    print(get_latex_str(t))
