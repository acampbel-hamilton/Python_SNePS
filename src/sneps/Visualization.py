from .Node import Molecular, MinMaxOpNode, Variable, Indefinite

# =====================================
# --------- OPTIONAL IMPORTS ----------
# =====================================
""" These imports are used to create visual representations of a knowledge base.
    Because a knowledge engineer can do everything without the visual representation,
    the packages are not required for regular use. """
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

# =====================================
# -------------- MIXIN ----------------
# =====================================

class VisualizationMixin:
    """ Provides visual representations of the Network and its current context. """

    def __init__(self) -> None:
        if type(self) is VisualizationMixin:
            raise NotImplementedError("Mixins can't be instantiated.")

    def print_graph(self) -> None:
        """ Interactive visual graph opens in new window. """
        # Ensure proper packages available and imported
        if not has_nx:
            print("In order to use this function, you must pip install networkx")
            return
        if not has_mpl:
            print("In order to use this function, you must pip install matplotlib")
            return

        # Used to store the labels for nodes and edges
        node_labels = {}
        edge_labels = {}

        # Stores graph variable
        G = nx.DiGraph()

        # Draws each node in graph
        for node in self.nodes.values():
            node_name = node.name

            # Name followed by ! if asserted in the current context
            if node in self.current_context:
                node_name += '!'
            node_labels[node_name] = node_name
            G.add_node(node_name)

            # Draws edges to other nodes to which node has arcs formed by slots (cables)
            if isinstance(node, Molecular):
                for i in range(len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name

                    # Prints min and max with arc name
                    if isinstance(node, MinMaxOpNode) and name in ["threshargs", "andorargs"]:
                        name += " ({}, {})".format(node.min, node.max)

                    # Nor wire (single down cable) displayed as not
                    if name == "nor" and len(fillers) == 1:
                        name = "not"

                    for filler in fillers.nodes:
                        filler_name = filler.name
                        if filler in self.current_context:
                            filler_name += '!'

                        # If multiple down arcs go from one node to another, display them as one
                        # edge with comma-separated arc names
                        if (node_name, filler_name) in edge_labels:
                            edge_labels[(node_name, filler_name)] += ", " + name
                        else:
                            G.add_edge(node_name, filler_name)
                            edge_labels[(node_name, filler_name)] = name

            # Draws edges to other nodes to which node has arcs formed by restrictions
            if isinstance(node, Variable):
                for restriction_node in node.restriction_set:
                    restriction_name = restriction_node.name
                    if restriction_node in self.current_context:
                        restriction_name += '!'
                    if (node_name, restriction_name) in edge_labels:
                        edge_labels[(node_name, restriction_name)] += ", restriction"
                    else:
                        G.add_edge(node_name, restriction_name)
                        edge_labels[(node_name, restriction_name)] = "restriction"

                # Draws edges to other nodes to which node has arcs formed by dependencies
                if isinstance(node, Indefinite):
                    for dependency_node in node.dependency_set:
                        dependency_name = dependency_node.name
                        if dependency_node in self.current_context:
                            dependency_name += '!'
                        if (node_name, dependency_name) in edge_labels:
                            edge_labels[(node_name, dependency_name)] += ", dependency"
                        else:
                            G.add_edge(node_name, dependency_name)
                            edge_labels[(node_name, dependency_name)] = "dependency"

        # Layout on which to draw nodes
        pos = nx.circular_layout(G)

        # Draggable nodes in graph
        if has_ng and self.nodes != {}:
            # This is a buggy module.
            # If you want adjustable graphs, you have to do an assignment for some reason
            _ = ng.InteractiveGraph(G, pos, node_size=10, node_label_font_size=12.0, node_color='grey', alpha=0.8,
                                    node_labels=node_labels, edge_labels=edge_labels, font_color='black')
        # Static graph
        else:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
            nx.draw_networkx(G, pos, node_size=800, node_color='grey', alpha=0.8)

        # Displays graph
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.show()


    def export_graph(self) -> None:
        """ Generates network.dot graphviz representation. """
        # Ensure proper packages available and imported
        if not has_nx:
            print("In order to use this function, you must pip install networkx")
            return
        if not has_pydot:
            print("In order to use this function, you must pip install pydot")

        # Used to store the labels for nodes
        node_labels = {}

        # Stores graph variable
        G = nx.MultiDiGraph()

        # Draws each node in graph
        for node in self.nodes.values():
            node_name = node.name

            # Name followed by ! if asserted in the current context
            if node in self.current_context:
                node_name += '!'
            node_labels[node_name] = node_name
            G.add_node(node_name)

            # Draws edges to other nodes to which node has arcs formed by slots (cables)
            if isinstance(node, Molecular):
                for i in range(len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name

                    # Prints min and max with arc name
                    if isinstance(node, MinMaxOpNode) and name in ["threshargs", "andorargs"]:
                        name += " ({}, {})".format(node.min, node.max)

                    # Nor wire (single down cable) displayed as not
                    if name == "nor" and len(fillers) == 1:
                        name = "not"

                    for filler in fillers.nodes:
                        filler_name = filler.name
                        if filler in self.current_context:
                            filler_name += '!'
                        G.add_edge(node_name, filler_name, label=name)

            # Draws edges to other nodes to which node has arcs formed by restrictions
            if isinstance(node, Variable):
                for restriction_node in node.restriction_set:
                    restriction_name = restriction_node.name
                    if restriction_node in self.current_context:
                        restriction_name += '!'
                    G.add_edge(node_name, restriction_name, label="restriction")

                # Draws edges to other nodes to which node has arcs formed by dependencies
                if isinstance(node, Indefinite):
                    for dependency_node in node.dependency_set:
                        dependency_name = dependency_node.name
                        if dependency_node in self.current_context:
                            dependency_name += '!'
                        G.add_edge(node_name, dependency_name, label="dependency")

        # Writes graph to network.dot file
        nx.nx_pydot.write_dot(G, 'network.dot')

        # Print message to confirm graph exported
        print("Graph exported to network.dot")
