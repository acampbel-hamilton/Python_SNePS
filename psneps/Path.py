class Path:
    """ Superclass for all paths """
    def __init__(self):
        self.converse = False
        self.str_representation = ""

    def reverse(self):
        self.converse = not self.converse

    def __str__(self):
        # Prints original path string entered by user
        return self.str_representation

class ComposedPaths(Path):
    """ A composed list of path objects, following one after another """
    def __init__(self, paths):
        self.paths = paths
        super().__init__()

    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Backward if in converse
        paths = reversed(self.paths) if converse else self.paths

        # Follow paths consecutively
        derived = set([start_node])
        for path in paths:
            temp_derived = set()
            for next_node in derived:
                # Store all nodes derived by following the next path
                temp_derived.update(path.derivable(next_node, converse))
            derived = temp_derived
        return derived

class AndPaths(ComposedPaths):
    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Follow paths consecutively
        derived = set()
        for path in paths:
            derived.intersection_update(path.derivable(start_node, converse))
        return derived

class OrPaths(ComposedPaths):
    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Follow paths consecutively
        derived = set()
        for path in paths:
            derived.update(path.derivable(start_node, converse))
        return derived

class ModPath(Path):
    """ Performs some modification on a single path """

    def __init__(self, path):
        self.path = path
        super().__init__()

class KPlusPaths(ModPath):
    """ Follows one or more instances of the given path """

    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        derived = set()
        next = [start_node]
        while next != []:
            # Get new nodes from traversing the path another time
            next = [self.path.derivable(next_node, converse) for next_node in next]
            derived.update(set(next))
        return derived

class KStarPaths(KPlusPaths):
    """ Follows zero or more instances of the given path """
    def derivable(self, start_node, parent_converse=False):
        return super().derivable(start_node, self.converse != parent_converse).add(start_node)

class IRPath(ModPath):
    """ Follows paths provided end node is not start node """

    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        derived = self.path.derivable(next_node, converse)
        derived.discard(start_node)
        return derived

class BasePath(Path):
    """ Atomic path existing on a single non-repeated slot """
    def __init__(self, slot, current_network, backward=False):
        self.slot = slot
        self.current_network = current_network
        self.backward = backward
        super().__init__()

    def derivable(self, start_node, parent_converse=False):
        if (self.converse != parent_converse) == self.backward:
            return start_node.follow_down_cable(self.slot)
        else:
            return start_node.follow_up_cable(self.slot)

# Asserted Path singleton
class AssertedPath:
    class _AssertedPath:
        def __init__(self, current_network):
            self.current_network = current_network

    instance = None
    def __init__(self, current_network):
        if AssertedPath.instance is None:
            AssertedPath.instance = AssertedPath._AssertedPath(current_network)

    def derivable(self, start_node, converse=False):
        if AssertedPath.instance.current_network.current_context.is_asserted(start_node):
            return set([start_node])
        else:
            return set()
