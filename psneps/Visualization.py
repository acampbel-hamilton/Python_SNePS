from .Node import Molecular, MinMaxOpNode, Variable, Indefinite
try:
    import networkx as nx
    has_nx = True
except ModuleNotFoundError:
    has_nx = False
try:
    import pydot as pyd
    has_pydot = True
except ModuleNotFoundError:
    has_pydot = False
try:
    import matplotlib.pyplot as plt
    has_mpl = True
except ModuleNotFoundError:
    has_mpl = False
try:
    import netgraph as ng
    has_ng = True
except ModuleNotFoundError:
    has_ng = False

class VisualizationMixin:
    """ Provides graph visualization related to nodes to Network """

    def __init__(self) -> None:
        if type(self) is VisualizationMixin:
            raise NotImplementedError("Mixins can't be instantiated.")

    def print_graph(self) -> None:
        if not has_nx:
            print("In order to use this function, you must pip install networkx")
            return
        if not has_mpl:
            print("In order to use this function, you must pip install matplotlib")
            return

        node_labels = {}

        G = nx.DiGraph()
        edge_labels = {}
        for node in self.nodes.values():
            node_name = node.name
            if self.current_context.is_hypothesis(node):
                node_name += '!'
            node_labels[node_name] = node_name
            G.add_node(node_name)
            if isinstance(node, Molecular):
                for i in range(len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name
                    if isinstance(node, MinMaxOpNode) and name in ["threshargs", "andorargs"]:
                        name += " ({}, {})".format(node.min, node.max)
                    if name == "nor" and len(fillers) == 1:
                        name = "not"
                    for filler in fillers.nodes:
                        filler_name = filler.name
                        if self.current_context.is_hypothesis(filler):
                            filler_name += '!'
                        if (node_name, filler_name) in edge_labels:
                            edge_labels[(node_name, filler_name)] += ", " + name
                        else:
                            G.add_edge(node_name, filler_name)
                            edge_labels[(node_name, filler_name)] = name
            if isinstance(node, Variable):
                for restriction_node in node.restriction_set:
                    restriction_name = restriction_node.name
                    if self.current_context.is_hypothesis(restriction_node):
                        restriction_name += '!'
                    if (node_name, restriction_name) in edge_labels:
                        edge_labels[(node_name, restriction_name)] += ", restriction"
                    else:
                        G.add_edge(node_name, restriction_name)
                        edge_labels[(node_name, restriction_name)] = "restriction"
                if isinstance(node, Indefinite):
                    for dependency_node in node.dependency_set:
                        dependency_name = dependency_node.name
                        if self.current_context.is_hypothesis(dependency_node):
                            dependency_name += '!'
                        if (node_name, dependency_name) in edge_labels:
                            edge_labels[(node_name, dependency_name)] += ", dependency"
                        else:
                            G.add_edge(node_name, dependency_name)
                            edge_labels[(node_name, dependency_name)] = "dependency"

        pos = nx.circular_layout(G)
        if has_ng and self.nodes != {}:
            # This is a buggy module.
            # If you want adjustable graphs, you have to do an assignment for some reason
            _ = ng.InteractiveGraph(G, pos, node_size=10, node_label_font_size=12.0, node_color='grey', alpha=0.8,
                                    node_labels=node_labels, edge_labels=edge_labels, font_color='black')
        else:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
            nx.draw_networkx(G, pos, node_size=800, node_color='grey', alpha=0.8)
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.show()


    def export_graph(self) -> None:
        if not has_nx:
            print("In order to use this function, you must pip install networkx")
            return
        if not has_pydot:
            print("In order to use this function, you must pip install pydot")

        node_labels = {}

        G = nx.MultiDiGraph()
        for node in self.nodes.values():
            node_name = node.name
            if self.current_context.is_hypothesis(node):
                node_name += '!'
            node_labels[node_name] = node_name
            G.add_node(node_name)
            if isinstance(node, Molecular):
                for i in range(len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name
                    if isinstance(node, MinMaxOpNode) and name in ["threshargs", "andorargs"]:
                        name += " ({}, {})".format(node.min, node.max)
                    if name == "nor" and len(fillers) == 1:
                        name = "not"
                    for filler in fillers.nodes:
                        filler_name = filler.name
                        if self.current_context.is_hypothesis(filler):
                            filler_name += '!'
                        G.add_edge(node_name, filler_name, label=name)
            if isinstance(node, Variable):
                for restriction_node in node.restriction_set:
                    restriction_name = restriction_node.name
                    if self.current_context.is_hypothesis(restriction_node):
                        restriction_name += '!'
                    G.add_edge(node_name, restriction_name, label="restriction")
                if isinstance(node, Indefinite):
                    for dependency_node in node.dependency_set:
                        dependency_name = dependency_node.name
                        if self.current_context.is_hypothesis(dependency_node):
                            dependency_name += '!'
                        G.add_edge(node_name, dependency_name, label="dependency")

        nx.nx_pydot.write_dot(G, 'graph.dot')
