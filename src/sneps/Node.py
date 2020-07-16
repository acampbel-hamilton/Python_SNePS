from .Caseframe import Frame
from .Slot import Slot
from .SNError import SNError
from .SemanticType import SemanticType
from re import match
from .wft.vars.UniqueRep import *
from typing import Set

# =====================================
# -------------- GLOBALS --------------
# =====================================

class NodeError(SNError):
    pass

# =====================================
# --------------- NODE ----------------
# =====================================

class Node:
    """ Root of syntactic hierarchy (Abstract class) """
    def __init__(self, name: str, sem_type: SemanticType) -> None:
        self.name = name # This is unique to each wft (eg. wft1)
        self.up_cableset = set() # Set of UpCable objects that point to this node
        self.sem_type = sem_type
        self.unique_rep = None
        if type(self) in (Node, Atomic, Variable, MinMaxOpNode): # These are all abstract classes.
            raise NotImplementedError("Bad syntactic type: See syntax tree in wiki; only leaves are valid.")

    def add_up_cable(self, node, slot: Slot) -> None:
        """ Adds an up cable to this node. (Up cables contain a node and a slot.) """
        self.up_cableset.add(UpCable(node, slot))

    def has_upcable(self, name: str) -> bool:
        """ True if this node has an up cable with the provided name. """
        return any(up_cable.name == name for up_cable in self.up_cableset)

    def follow_down_cable(self, slot) -> set:
        """ Since atomic Nodes have no down cables, this returns an empty set. """
        return set()

    def follow_up_cable(self, slot: Slot) -> set:
        """ Returns the set of nodes which point to this node via a downcable on the provided slot. """
        return set(up_cable.node for up_cable in self.up_cableset if up_cable.slot is slot)

    def __str__(self) -> str:
        return self.wft_rep()

    def __repr__(self) -> str:
        return self.wft_rep()

    def wft_rep(self, simplify=None) -> str:
        """ Because repr and str cannot take parameters, this has been created to allow us to simplify
        string representations of nodes (and thereby prevent infinite recursion in nodes that have down cables
        to themselves)"""
        return self.name

    def has_constituent(self, constituent, visited=None) -> bool:
        """ Recursively checks this node and all nodes to which it has down cables,
        looking for a given Node (constituent) """
        return self is constituent

    def get_unique_rep(self) -> UniqueRep:
        """ UniqueRep objects help the system ensure variable uniquness.
        They never change and are therefore cached. """
        if self.unique_rep is None:
            self.unique_rep = self.new_unique_rep()
        return self.unique_rep

    def new_unique_rep(self) -> UniqueRep:
        """ UniqueRep objects help the system ensure variable uniquness. """
        return UniqueRep(name=self.name)

    def follow_down_cable(self, slot) -> set:
        """ Atomic nodes lack down cables so this returns the empty set for them. """
        return set()

# =====================================
# ----------- BASE NODES --------------
# =====================================

class Atomic(Node):
    """ A leaf in a network. (Abstract class) """

    def has_frame(self, frame: Frame) -> bool:
        """ Atomic Nodes don't have frames, so this always returns False. """
        return False

class Base(Atomic):
    """ A constant within the system, represented in the graph by a provided string (e.g. Fido) """

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return id(self)

# =====================================
# ---------- VARIABLE NODES -----------
# =====================================

class Variable(Atomic):
    """ A variable term ranging over a restricted domain. """

    def __init__(self, name: str, sem_type: SemanticType) -> None:
        super().__init__(name, sem_type)
        self.restriction_set = set()
        self.var_rep = VarRep()

    def add_restriction(self, restriction) -> None:
        """ Adds a restriction arc from the variable to another node. """
        self.restriction_set.add(restriction)

    def wft_rep(self, simplify=None) -> str:
        """ String representation """
        return super().wft_rep()

    def __eq__(self, other) -> bool:
        return self.var_rep == other.var_rep

    def __hash__(self) -> int:
        """ __eq__ checks var_reps at creation time.
            Once variables are in the network, uniqueness is guarenteed """
        return id(self)

    def new_unique_rep(self) -> UniqueRep:
        """ UniqueRep objects help the system ensure variable uniquness. """
        return UniqueRep(name=self.var_rep.name)

class Arbitrary(Variable):
    """ An arbitrary variable. Originates from an every statement. """
    counter = 1

    def __init__(self, name, sem_type: SemanticType) -> None:
        super().__init__(name, sem_type)

    def store_in(self, current_network):
        """ Gives an arb# name and stores in the given network. """
        self.name = 'arb' + str(self.counter)
        Arbitrary.counter += 1
        current_network.nodes[self.name] = self

    def wft_rep(self, simplify=None) -> str:
        """ String representation """
        if simplify is None:
            simplify = set()
        if self in simplify: # Gives the arb#-style name within the some statement
            return super().wft_rep()
        else:
            simplify.add(self)
            return "every({}, [{}])".format( \
                self.name, \
                ", ".join([restriction.wft_rep(simplify.copy()) for restriction in self.restriction_set]))

class Indefinite(Variable):
    """ An indefinite object. Originates from a Some statement. """
    counter = 1
    def __init__(self, name, sem_type: SemanticType) -> None:
        self.dependency_set = set()
        super().__init__(name, sem_type)

    def add_dependency(self, dependency: VarRep) -> None:
        """ Adds a dependency arc from the variable to another node. """
        self.dependency_set.add(dependency)

    def store_in(self, current_network):
        """ Gives an arb# name and stores in the given network. """
        self.name = 'ind' + str(self.counter)
        Indefinite.counter += 1
        current_network.nodes[self.name] = self

    def wft_rep(self, simplify=None) -> str:
        """ String representation """
        if simplify is None:
            simplify = set()
        if self in simplify: # Gives the ind#-style name within the some statement
            return super().wft_rep()
        else:
            simplify.add(self)
            return "some({}({}), [{}])".format( \
                   self.name, \
                   ", ".join([dependency.wft_rep(simplify.copy()) for dependency in self.dependency_set]), \
                   ", ".join([restriction.wft_rep(simplify.copy()) for restriction in self.restriction_set]))

# =====================================
# --------- MOLECULAR NODES -----------
# =====================================

class Molecular(Node):
    """ Non-leaf nodes. """
    counter = 1

    def __init__(self, frame: Frame) -> None:
        name = "wft" + str(Molecular.counter)
        Molecular.counter += 1
        self.frame = frame
        super().__init__(name, frame.caseframe.sem_type)

        # Adds up cables corresponding to each down cable in the frame
        for i in range(len(self.frame.filler_set)):
            slot = self.frame.caseframe.slots[i]
            fillers = self.frame.filler_set[i]
            for node in fillers.nodes:
                node.add_up_cable(self, slot)

    def has_frame(self, frame: Frame) -> bool:
        """ Returns if this node has a frame identical to the one provided.
        (Not necessarily the same object) """
        return frame == self.frame

    def __eq__(self, other) -> bool:
        """ Molecular Nodes unique by frame. """
        return isinstance(other, Molecular) and self.has_frame(other.frame)

    def __hash__(self) -> int:
        return id(self)

    def follow_down_cable(self, slot):
        """ Returns all the nodes arrived at by following the down cables formed by some particular slot. """
        return self.frame.get_filler_set(slot)

    def has_constituent(self, constituent, visited=None):
        """ Recursively checks this node and all nodes to which it has down cables,
        looking for a given Node (constituent) """
        # Checks if self the constituent
        if super().has_constituent(constituent):
            return True
        if visited is None:
            visited = set()

        # Stops infinite recursion
        visited.add(self)

        # Checks if fillers have the constituent
        for filler in self.frame.filler_set:
            for node in filler.nodes:
                if node not in visited and node.has_constituent(constituent, visited):
                    return True
        return False

    def wft_rep(self, simplify=None) -> str:
        """ String representation """
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            ret = self.frame.caseframe.name + "("
            for i in range(len(self.frame.filler_set)):
                if i > 0:
                    ret += ", "
                fillers_str = ", ".join([node.wft_rep(simplify.copy()) for node in self.frame.filler_set[i].nodes])
                if len(self.frame.filler_set[i].nodes) > 1:
                    ret += "[{}]".format(fillers_str)
                else:
                    ret += "{}".format(fillers_str)
            ret += ")"
        return ret

    def new_unique_rep(self) -> UniqueRep:
        """ UniqueRep objects help the system ensure variable uniquness. """
        children = []
        for fillers in self.frame.filler_set:
            child = []
            for filler in fillers.nodes:
                child.append(filler.get_unique_rep())
            children.append(child)
        return UniqueRep(caseframe_name=self.frame.caseframe.name, children=children)

class MinMaxOpNode(Molecular):
    """ thresh/andor with two values serving as numeric limits to truth for fillers """

    def __init__(self, frame, min, max) -> None:
        super().__init__(frame)
        self.min = min
        self.max = max

    def num_constituents(self):
        """ Total number of fillers for the given caseframe's single slot (max=None) """
        return len(self.frame.filler_set[0])

    def has_min_max(self, min: int, max: int) -> bool:
        """ Used to check equality """
        return self.min == min and self.max == max

    def __eq__(self, other) -> bool:
        """ MinMaxOp Nodes are unique by tuple of (frame, min, max) """
        return super.__eq__(other) and (self.min, self.max) == (other.min, other.max)

    def __hash__(self) -> int:
        return id(self)

    def wft_rep(self, simplify=None) -> str:
        """ String representation """
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            if self.frame.caseframe.name == "thresh" or self.frame.caseframe.name == "andor":
                ret = "{}{{{}, {}}}(".format(self.frame.caseframe.name, self.min, self.max)
            else:
                name = self.frame.caseframe.name
                if name == "nor" and len(self.frame.filler_set[0]) == 1:
                    name = "not"
                ret = "{}(".format(name)
            for i in range(len(self.frame.filler_set)):
                if i > 0:
                    ret += ", "
                ret += "{}".format( \
                    ", ".join([node.wft_rep(simplify.copy()) for node in self.frame.filler_set[i].nodes]))
            ret += ")"
        return ret

    def new_unique_rep(self) -> UniqueRep:
        """ UniqueRep objects help the system ensure variable uniquness. """
        children = []
        for fillers in self.frame.filler_set:
            child = []
            for filler in fillers.nodes:
                child.append(filler.get_unique_rep())
            children.append(child)

        return UniqueRep(caseframe_name=self.frame.caseframe.name, children=children, min=self.min, max=self.max)

class ThreshNode(MinMaxOpNode):
    """ Thresh with two values """
    pass

class AndOrNode(MinMaxOpNode):
    """ AndOr with two values """
    pass

class ImplNode(Molecular):
    """ if/=> with bound value serving as numeric threshold to truth for antecedents """

    def __init__(self, frame, bound) -> None:
        super().__init__(frame)
        self.bound = bound

    def has_bound(self, bound: int) -> bool:
        """ Used to check equality """
        return self.bound == bound

    def __eq__(self, other) -> bool:
        """ ImplNode Nodes are unique by tuple of (frame, bound) """
        return super.__eq__(other) and self.bound == other.bound

    def __hash__(self) -> int:
        return id(self)

    def antecedents(self):
        """ Returns a set of the node's frame's antecedents """
        return self.follow_down_cable(self.frame.caseframe.slots[0])

    def consequents(self):
        """ Returns a set of the node's frame's consequents """
        return self.follow_down_cable(self.frame.caseframe.slots[1])

    def wft_rep(self, simplify=None) -> str:
        """ String representation """
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)

            antecedents = self.antecedents()
            consequents = self.consequents()

            impl_type = self.bound
            if impl_type == 1:
                impl_type = "v"
            elif impl_type == len(antecedents):
                impl_type = "&"
            ret = "{}=>(".format(impl_type)

            ant_str = ", ".join([ant.wft_rep(simplify.copy()) for ant in antecedents])
            if len(antecedents) > 1:
                ret += "[{}]".format(ant_str)
            else:
                ret += "{}".format(ant_str)

            ret += ", "

            cq_str = ", ".join([cq.wft_rep(simplify.copy()) for cq in consequents])
            if len(consequents) > 1:
                ret += "[{}]".format(cq_str)
            else:
                ret += "{}".format(cq_str)

            ret += ")"
            return ret

    def new_unique_rep(self) -> UniqueRep:
        """ UniqueRep objects help the system ensure variable uniquness. """
        return UniqueRep(caseframe_name=self.frame.caseframe.name, bound=self.bound)

# =====================================
# -------------- UP CABLE -------------
# =====================================

class UpCable:
    """ Tuple containing node and slot """
    def __init__(self, node: Node, slot: Slot):
        self.node = node
        self.slot = slot
        self.name = slot.name

# =====================================
# --------------- MIXIN ---------------
# =====================================

class NodeMixin:
    """ Provides functions related to nodes to Network """

    def __init__(self) -> None:
        if type(self) is NodeMixin:
            raise NotImplementedError("Mixins can't be instantiated.")
        self.nodes = {}

    def define_term(self, name, sem_type_name="Entity") -> None:
        """ Creates a base node by the given name and semantic type. """

        if match(r'^(arb|ind)\d+$', name) or not match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
            raise NodeError("ERROR: The term name '{}' is not allowed".format(name))

        if name in self.nodes:
            # Respecification of existing node
            node = self.nodes[name]
            current_type = node.sem_type
            new_type = self.sem_hierarchy.get_type(sem_type_name)
            node.sem_type = self.sem_hierarchy.respecify(name, current_type, new_type)
        else:
            # Creation of new node
            sem_type = self.sem_hierarchy.get_type(sem_type_name)
            self.nodes[name] = Base(name, sem_type)

    def list_terms(self) -> None:
        """ Prints representations of each Node in the Network """
        for term in self.nodes:
            node = self.nodes[term]
            print("<{}>{}:".format(node.name, '!' if node in self.current_context else ''))
            print("\t{}".format(node))

    def find_term(self, name: str) -> Node:
        """ Returns the Node object with the given name in the network """
        if name in self.nodes:
            return self.nodes[name]
        else:
            raise NodeError('ERROR: Term "' + name + '" not defined.')
