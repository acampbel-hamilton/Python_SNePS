from typing import List

# =====================================
# --------------- PATH ----------------
# =====================================

class Path:
    """ Superclass for all paths """

    def __init__(self):
        self.converse = False # Set to true if path should be followed in reverse

    def reverse(self):
        # A converse within a converse is read forward
        self.converse = not self.converse

class ComposedPaths(Path):
    """ A composed list of path objects, following one after another """

    def __init__(self, paths: List[Path]):
        self.paths = paths
        super().__init__()

    def derivable(self, start_node, parent_converse: bool = False):
        """ Returns a set of all nodes which might be derived by following this path. """

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

    def __str__(self) -> str:
        return "compose({})".format(", ".join([str(path) for path in self.paths]))

class AndPaths(ComposedPaths):
    """ A composed list of path objects, following one after another """

    def derivable(self, start_node, parent_converse: bool = False):
        """ Returns a set of all nodes which might be derived by following this path. """

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Follow each of the paths
        derived = set()
        first  = True
        for path in self.paths:
            if first:
                derived = path.derivable(start_node, converse)
                first = False
            else:
                # Store the intersection of the derived nodes from each path
                derived.intersection_update(path.derivable(start_node, converse))
        return derived

    def __str__(self) -> str:
        return "and({})".format(", ".join([str(path) for path in self.paths]))

class OrPaths(ComposedPaths):
    def derivable(self, start_node, parent_converse: bool = False):
        """ Returns a set of all nodes which might be derived by following this path. """

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Follow each of the paths
        derived = set()
        for path in self.paths:
            # Store the union of the derived nodes from each path
            derived.update(path.derivable(start_node, converse))
        return derived

    def __str__(self) -> str:
        return "or({})".format(", ".join([str(path) for path in self.paths]))

class ModPath(Path):
    """ Performs some modification on a single path """

    def __init__(self, path: Path):
        super().__init__()
        self.path = path

class KPlusPath(ModPath):
    """ Follows one or more instances of the given path """

    def derivable(self, start_node, parent_converse: bool = False):
        """ Returns a set of all nodes which might be derived by following this path. """

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Traverse path until every node derivable located
        derived = set()
        next = set([start_node])
        while next != set():
            # Get new nodes from traversing the path another time
            temp_next = set()
            [temp_next.update(self.path.derivable(next_node, converse)) for next_node in next]
            next = temp_next

            # Ensures derivations not repeated - prevents infinite recursion
            next = next - derived
            derived.update(next)
        return derived

    def __str__(self) -> str:
        return "kplus({})".format(self.path)

class KStarPath(KPlusPath):
    """ Follows zero or more instances of the given path """

    def derivable(self, start_node, parent_converse=False):
        """ Returns a set of all nodes which might be derived by following this path. """

        # KPlus paths, plus the starting node (the starting node represents zero traversals)
        derived = super().derivable(start_node, self.converse != parent_converse)
        derived.add(start_node)
        return derived

    def __str__(self) -> str:
        return "kstar({})".format(self.path)

class IRPath(ModPath):
    """ Follows paths provided end node is not start node """

    def derivable(self, start_node, parent_converse=False):
        """ Returns a set of all nodes which might be derived by following this path. """
        derived = self.path.derivable(start_node, self.converse != parent_converse)

        # Ignores any paths that return to where they began
        derived.discard(start_node)
        return derived

    def __str__(self) -> str:
        return "irreflexive-restrict({})".format(self.path)

class BasePath(Path):
    """ Atomic path existing on a single non-repeated slot """

    def __init__(self, slot, backward=False):
        self.slot = slot # The single slot to follow
        self.backward = backward # Whether to folow an upcable instead
        super().__init__()

    def derivable(self, start_node, parent_converse=False):
        """ Returns a set of all nodes which might be derived by following this path. """
        # Follows the single cable up or down
        if (self.converse != parent_converse) == self.backward:
            return start_node.follow_down_cable(self.slot)
        else:
            return start_node.follow_up_cable(self.slot)

    def __str__(self) -> str:
        return self.slot.name + ("-" if self.backward else "")

class AssertedPath(Path):
    """ Ensures the starting node provided is asserted within the current context """

    def __init__(self, current_network):
        self.current_network = current_network

    def derivable(self, start_node, parent_converse: bool = False):
        """ Returns a set of all nodes which might be derived by following this path. """

        # If asserted, returns a set containing the starting_node
        if start_node in self.current_network.current_context:
            return set([start_node])
        # Otherwise returns the empty set
        else:
            return set()

    def __str__(self) -> str:
        return "!"

# =====================================
# --------------- MIXIN ---------------
# =====================================

# This is here instead of at the top of the file to avoid circular imports.
from .path.PathParse import path_parser, SNePSPathError

class PathMixin:
    """ Provides functions related to paths to Network """

    def define_path(self, slot_str: str, path_str: str):
        """ The slot slot_str exists between two nodes when the path path_str
            can be followed from one to the other """
        path = path_parser(path_str, self)
        if path is not None:
            slot = self.find_slot(slot_str)
            slot.add_path(path)

    def paths_from(self, terms: List[str], path_str: str):
        """ Given a starting list of node names and a path, follows the path from
            each of the nodes and returns the set of nodes derived """
        path = path_parser(path_str, self)
        derived = set()
        for term in terms:
            start_node = self.find_term(term)
            derived.update(path.derivable(start_node))
        return derived
