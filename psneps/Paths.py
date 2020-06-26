from functools import reduce
from operator import concat

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

class KPlusPaths():
    """ Follows one or more instances of the given path """
    def __init__(self, path):
        self.path = path

    def derivable(self, start_node):
        # Gets list of all nodes derived by following this path any number of times
        derived = set()
        next = [start_node]
        while next != []:
            # Get new nodes from traversing the path another time
            next = reduce(concat, [self.path.derivable(node) for node in next])
            for node in next:
                derived.add(node)
        return list(derived)

class KStarPaths(KPlusPaths):
    """ Follows zero or more instances of the given path """
    def derivable(self, start_node):
        return [start_node] + super().derivable(start_node)

class BasePath:
    """ Atomic path existing on a single non-repeated slot """
    def __init__(self, slot, backward=False, asserted=False):
        self.slot = slot
        self.backward = backward
        self.asserted = asserted

    def derivable(self, start_node):
        pass
