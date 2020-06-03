try:
    import networkx as nx
    import matplotlib.pyplot as plt
    has_nx = True
except ModuleNotFoundError:
    has_nx = False

parse_tree_node_id = 0
class ParseTree:
    def __init__(self, description=None, value=None):
        if description is value is None:
            raise ValueError("Parse tree initialized with no description and no value.")

        global parse_tree_node_id
        self.id = parse_tree_node_id
        parse_tree_node_id += 1

        self.description = description
        self.value = value

        self.children = []

    def add_children(self, *children):
        self.children += children

    def __repr__(self):
        attrs = ["(" + str(self.id) + ")"]
        if self.description is not None:
            attrs.append(str(self.description))
        if self.value is not None:
            attrs.append(str(self.value))
        return attrs[0] + ": " + ", ".join(attrs[1:])

    def to_networkx(self, G=None):
        if not has_nx:
            raise ModuleNotFoundError("Networkx and matplotlib are required to visualize a parse tree.")

        if G is None:
            G = nx.Graph()
            is_root = True
        else:
            is_root = False

        for child in self.children:
            G.add_edge(repr(self), repr(child))
            child.to_networkx(G)

        if is_root:
            nx.draw_networkx(G)
            plt.show()
