class ComposedPaths:
    """ A composed list of path objects, following one after another """
    def __init__(self, paths):
        self.paths = paths
        self.asserted = False

    def derivable(self, start_node):
        # Gets list of all nodes derived by following this path
        derived = set([start_node])

        # Follow paths consecutively
        for path in self.paths:
            temp_derived = set()
            for node in derived:
                # Store all nodes derived by following the next path
                temp_derived.update(path.derivable(node))
            derived = temp_derived
        return derived

class AndPaths(ComposedPaths):
    def derivable(self, start_node):
        # Gets list of all nodes that can be derived from all of these paths
        derived = set()
        for path in self.paths:
            temp_derived = set()
            temp_derived = path.derivable(start_node)
            derived = derived.intersection(temp_derived)
        return derived

class OrPaths(ComposedPaths):
    def derivable(self, start_node):
        derived = set()
        for path in self.paths:
            temp_derived = set()
            temp_derived = path.derivable(start_node)
            derived.update(temp_derived)
        return derived

class KPlusPaths():
    """ Follows one or more instances of the given path """
    def __init__(self, path):
        self.path = path
        self.asserted = False

    def derivable(self, start_node):
        # Gets list of all nodes derived by following this path any number of times
        derived = set()
        next = [start_node]
        while next != []:
            # Get new nodes from traversing the path another time
            next = [self.path.derivable(node) for node in next]
            derived.update(set(next))
        return derived

class KStarPaths(KPlusPaths):
    """ Follows zero or more instances of the given path """
    def derivable(self, start_node):
        return super().derivable(start_node).update([start_node])

class BasePath:
    """ Atomic path existing on a single non-repeated slot """
    def __init__(self, slot, backward=False):
        self.slot = slot
        self.backward = backward
        self.asserted = False

    def derivable(self, start_node):
        if !self.backward
            derived = start_node.filler_set(slot)
        else:
            derived = set() # TODO: follow up cables instead of down cables

        # if self.asserted filter the set for only nodes asserted in current context
