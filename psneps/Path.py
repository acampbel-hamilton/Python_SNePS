class Path:
    """ Superclass for all paths """
    def __init__(self):
        self.converse = False

    def reverse(self):
        self.converse = not self.converse

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

    def __str__(self) -> str:
        return "compose({})".format(", ".join([str(path) for path in self.paths]))

class AndPaths(ComposedPaths):
    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Follow paths consecutively
        derived = set()
        for path in paths:
            derived.intersection_update(path.derivable(start_node, converse))
        return derived

    def __str__(self) -> str:
        return "and({})".format(", ".join([str(path) for path in self.paths]))

class OrPaths(ComposedPaths):
    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        # Follow paths consecutively
        derived = set()
        for path in paths:
            derived.update(path.derivable(start_node, converse))
        return derived

    def __str__(self) -> str:
        return "or({})".format(", ".join([str(path) for path in self.paths]))

class ModPath(Path):
    """ Performs some modification on a single path """

    def __init__(self, path):
        super().__init__()
        self.path = path

class KPlusPath(ModPath):
    """ Follows one or more instances of the given path """

    def derivable(self, start_node, parent_converse=False):

        # Exclusive or for whether to use converse
        converse = self.converse != parent_converse

        derived = set()
        next = [start_node]
        while next != []:
            # Get new nodes from traversing the path another time
            next = self.path.derivable(next_node, converse) for next_node in next]
            derived.update(set(next))
        return derived

    def __str__(self) -> str:
        return "kplus({})".format(self.path)

class KStarPath(KPlusPath):
    """ Follows zero or more instances of the given path """
    def derivable(self, start_node, parent_converse=False):
        return super().derivable(start_node, self.converse != parent_converse).add(start_node)

    def __str__(self) -> str:
        return "kstar({})".format(self.path)

class IRPath(ModPath):
    """ Follows paths provided end node is not start node """

    def derivable(self, start_node, parent_converse=False):
        derived = self.path.derivable(next_node, self.converse != parent_converse)
        derived.discard(start_node)
        return derived

    def __str__(self) -> str:
        return "irreflexive-restrict({})".format(self.path)

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

    def __str__(self) -> str:
        return self.slot.name + ("-" if self.backward else "")

# Asserted Path singleton
class AssertedPath(Path):
    def __init__(self, current_network):
        self.current_network = current_network

    def derivable(self, start_node, converse=False):
        if self.current_network.current_context.is_asserted(start_node):
            return set([start_node])
        else:
            return set()

    def __str__(self) -> str:
        return "!"

# =====================================
# --------------- MIXIN ---------------
# =====================================

from .path.PathParse import path_parser, SNePSPathError
from typing import List

class PathMixin:
    """ Provides functions related to paths to Network """

    def define_path(self, slot_str : str, path_str : str):
        path = path_parser(path_str, self)
        if path is not None:
            slot = self.find_slot(slot_str)
            slot.add_path(path)

    def paths_from(self, terms : List[str], path_str : str):
        path = path_parser(path_str, self)
        derived = set()
        for term in terms:
            start_node = self.find_term(term)
            derived.update(path.derivable(start_node))
