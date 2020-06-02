try:
    import networkx as nx
    import matplotlib.pyplot as plt
    has_nx = True
except ModuleNotFoundError:
    has_nx = False

parse_tree_node_id = 0
class ParseTree:
    def __init__(self, description=None, value=None, *children):
        if description is value is None:
            raise ValueError("Parse tree initialized with no description and no value.")

        global parse_tree_node_id
        self.id = parse_tree_node_id
        parse_tree_node_id += 1

        self.description = description
        self.value = value
        self.children = children

        if isinstance(value, ParseTree):
            self.children = (value,) + self.children
            self.value = None
        if isinstance(description, ParseTree):
            self.children = (description,) + self.children
            self.description = None

    def add_child(self, *children):
        self.children += children

    def __repr__(self):
        return ", ".join(["(" + str(self.id) + ")", str(self.description), str(self.value)])

    def to_networkx(self, G=None):
        if not has_nx:
            raise ModuleNotFoundError("Networkx and matplotlib are required to visualize a parse tree.")

        if G is None:
            G = nx.DiGraph()
            is_root = True
        else:
            is_root = False

        for child in self.children:
            G.add_edge(repr(self), repr(child))
            child.to_networkx(G)

        if is_root:
            nx.draw_networkx(G)
            plt.show()
