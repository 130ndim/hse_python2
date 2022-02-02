import ast
import inspect
from collections import defaultdict
from typing import Any, Callable, Dict, List

import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

COLORMAP = _colormap = defaultdict(
    lambda: "grey",
    {
        "Constant": "blue",
        "FunctionDef": "red",
        "Name": "orange",
        "arg": "yellow",
    },
)


class Visualizer(ast.NodeVisitor):
    _graph: nx.DiGraph
    _stack: List[int]

    def __init__(self):
        self._node_counter = 0
        self._labels = []
        self._colors = []

    def _add_node(self, node: ast.AST, **attrs):
        parent = None
        if len(self._stack) > 0:
            parent = self._stack[-1]

        self._graph.add_node(self._node_counter, label=node.__class__.__name__, **attrs)
        self._stack.append(self._node_counter)

        if parent is not None:
            self._graph.add_edge(parent, self._node_counter)

        self._node_counter += 1
        super().generic_visit(node)
        self._stack.pop()

    def generic_visit(self, node: ast.AST) -> None:
        self._add_node(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        self._add_node(node, value=node.value)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # Set "name" as "name_" to resolve conflict with networkx argument name
        self._add_node(node, name_=node.name)

    def visit_Name(self, node: ast.Name) -> None:
        self._add_node(node, id=node.id)

    def visit_arg(self, node: ast.arg) -> None:
        self._add_node(node, arg=node.arg)

    def to_networkx(self, node: ast.AST) -> nx.DiGraph:
        self._graph = nx.DiGraph()
        self._stack = []

        self.visit(node)

        G = self._graph
        del self._graph
        return G


def draw_ast(fn: Callable[..., Any]) -> plt.Figure:
    root = ast.parse(inspect.getsource(fn)).body[0]
    G = Visualizer().to_networkx(root)  # noqa

    pos = graphviz_layout(G, prog="dot", root=G.nodes[0])

    fig, ax = plt.subplots(figsize=(30, 30))

    def _get_label(node: Dict[str, Any]) -> str:
        node = node.copy()
        label = node.pop("label")
        # Replace "name_" with "name" back
        if len(node) != 0:
            label += "\n" + "\n".join(
                f'{k.replace("_", "")}: {v}' for k, v in node.items()
            )
        return label

    nx.draw_networkx(
        G,
        pos=pos,
        node_shape="s",
        labels={n: _get_label(d) for n, d in G.nodes.items()},
        node_size=[len(d["label"]) * 1000 for _, d in G.nodes.items()],
        node_color=[COLORMAP[d["label"]] for _, d in G.nodes.items()],
        ax=ax,
    )
    return fig
