class ComposedPaths:
    """ A composed list of path objects, following one after another """
    def __init__(self, paths):
        self.paths = paths

    def derivable(self, start_node):
        # Gets list of all nodes derived by following this path
        derived = [start_node]

        # Follow paths consecutively
        for path in self.paths:
            temp_derived = []
            for node in derived:
                # Store all nodes derived by following the next path
                temp_derived += path.derivable(node)
            derived = temp_derived
        return derived

class AndPaths:
    def __init__(self, paths):
        pass

class OrPaths:
    def __init__(self, paths):
        pass

class KStarPaths:
    """ Follows zero or more instances of the given path """
    def __init__(self, path):
        self.path = path

class KPlusPaths:
    """ Follows one or more instances of the given path """

    def __init__(self, path):
        self.path = path

    def derivable(self, start_node):
        # Gets list of all nodes derived by following this path
        derived = []
        temp_derived = [start_node]

        # Follow path until reaching an end or a loop
        while len(derived) < len(temp_derived):
            derived += temp_derived
            for node in derived:
                derived_nodes = self.path.derivable(node)
                for derived_node in derived_nodes:
                    if derived_node not in temp_derived:
                        temp_derived.append(derived_nodes)

        # nextNodes += [n for n in next if n not in nextNodes]
        derived = []
        next = [start_node]
        while next != []:
            # get nodes from traversing the path another time
            next = self.path.derivable(next, path, context)
            # add those nodes to nextNodes
            derived += [n for n in next if n not in derived]
        return derived

class BasePath:
    """ Atomic path existing on a single non-repeated slot """
    def __init__(self, slot, self.backward=False, self.asserted=False):
        self.backward = backward

    def derivable(self, start_node):
        pass
