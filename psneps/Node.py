from .Caseframe import Frame
from .Slot import Slot
from .Error import SNError
from .SemanticType import SemanticType
from re import match
from .vars.UniqueRep import *

class NodeError(SNError):
    pass

class Node:
    """ Root of syntactic hierarchy """
    def __init__(self, name: str, sem_type: SemanticType) -> None:
        self.name = name # This is unique to each wft (eg. wft1)
        self.up_cableset = set() # Set of UpCable objects that point to this node
        self.sem_type = sem_type
        self.unique_rep = None
        if type(self) in (Node, Atomic, Variable, MinMaxOpNode): # These are all abstract classes.
            raise NotImplementedError("Bad syntactic type - see syntax tree in wiki")

    def add_up_cable(self, node, slot: Slot) -> None:
        """ Adds an up cable to this node. (Up cables contain a node and a slot.) """
        self.up_cableset.add(UpCable(node, slot))

    def has_upcable(self, name: str) -> bool:
        """ True if this node has an up cable with the provided name. """
        for up_cable in self.up_cableset:
            if up_cable.name == name:
                return True
        return False

    def follow_down_cable(self, slot) -> set:
        """ Since vanilla Nodes have no down cables, this returns an empty set. """
        return set()

    def follow_up_cable(self, slot: Slot) -> set:
        """ Returns the set of nodes that  """
        return set(up_cable.node for up_cable in self.up_cableset if up_cable.slot is slot)

    def __str__(self) -> str:
        return self.wft_rep()

    def __repr__(self) -> str:
        return self.wft_rep()

    def wft_rep(self, simplify=None) -> str:
        """ This exists because many classes have wft_rep methods. In some classes,
            these are distinct from __str__. Thus, we're stuck with both in this case. """
        return self.name

    def has_constituent(self, constituent, visited=None):
        return self is constituent

    def get_unique_rep(self) -> UniqueRep:
        if self.unique_rep is None:
            self.unique_rep = self.new_unique_rep()
        return self.unique_rep

    def new_unique_rep(self) -> UniqueRep:
        return UniqueRep(name=self.name)

# =====================================
# ---------- ATOMIC NODES -------------
# =====================================

class Atomic(Node):
    """ Node that is a leaf in a graph. (An abstract class) """
    def has_frame(self, frame: Frame) -> bool:
        """ Atomics don't have frames, so this always returns False. """
        return False

class Base(Atomic):
    """ A constant. (An abstract class) """
    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return id(self)

class Variable(Atomic):
    """ A variable term ranging over a restricted domain. """
    def __init__(self, name: str, sem_type: SemanticType) -> None:
        super().__init__(name, sem_type)
        self.restriction_set = set()
        self.var_rep = VarRep()

    def add_restriction(self, restriction) -> None:
        self.restriction_set.add(restriction)

    def wft_rep(self, simplify=None) -> str:
        return super().wft_rep()

    def __eq__(self, other) -> bool:
        return self.var_rep == other.var_rep

    def __hash__(self):
        return id(self)

    def new_unique_rep(self) -> UniqueRep:
        return UniqueRep(name=self.var_rep.name)

class Arbitrary(Variable):
    """ An arbitrary individual. Originates from an Every statement. """
    counter = 1
    def __init__(self, name, sem_type: SemanticType) -> None:
        super().__init__(name, sem_type) # These need semantic types. This will be an error.

    def store_in(self, current_network):
        self.name = 'arb' + str(self.counter)
        Arbitrary.counter += 1
        current_network.nodes[self.name] = self

    def wft_rep(self, simplify=None) -> str:
        if simplify is None:
            simplify = set()
        if self in simplify:
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
        super().__init__(name, sem_type) # These need semantic types. This will be an error.

    def add_dependency(self, dependency) -> None: # These need type definitions, since we don't know what restrictions/dependencies are.
        self.dependency_set.add(dependency)

    def store_in(self, current_network: Network):
        self.name = 'ind' + str(self.counter)
        Indefinite.counter += 1
        current_network.nodes[self.name] = self

    def wft_rep(self, simplify=None) -> str:
        if simplify is None:
            simplify = set()
        if self in simplify:
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
    counter = 1
    # Non-leaf nodes
    def __init__(self, frame: Frame) -> None:
        name = "wft" + str(Molecular.counter)
        Molecular.counter += 1
        self.frame = frame
        super().__init__(name, frame.caseframe.sem_type)

        for i in range(len(self.frame.filler_set)):
            slot = self.frame.caseframe.slots[i]
            fillers = self.frame.filler_set[i]
            for node in fillers.nodes:
                node.add_up_cable(self, slot)

    def has_frame(self, frame: Frame) -> bool:
        return frame == self.frame

    def __eq__(self, other) -> bool:
        return isinstance(other, Molecular) and self.has_frame(other.frame)

    def __hash__(self):
        return id(self)

    def follow_down_cable(self, slot):
        return self.frame.get_filler_set(slot)

    def has_constituent(self, constituent, visited=None):
        if visited is None:
            visited = set()
        visited.add(self)
        for filler in self.frame.filler_set:
            for node in filler.nodes:
                if node not in visited and node.has_constituent(constituent, visited):
                    return True
        return False

    def wft_rep(self, simplify=None) -> str:
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            ret = "{}(".format(self.frame.caseframe.name)
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
        children = []
        for fillers in self.frame.filler_set:
            child = []
            for filler in fillers.nodes:
                child.append(filler.get_unique_rep())
            children.append(child)

        return UniqueRep(caseframe_name=self.frame.caseframe.name, children=children)

class MinMaxOpNode(Molecular):
    """ Thresh/andor with two values """
    def __init__(self, frame, min, max) -> None:
        super().__init__(frame)
        self.min = min
        self.max = max

    def num_constituents(self):
        """ All of the propositions to which this and, or, thresh, etc. has wires """
        return len(self.frame.filler_set[0])

    def has_min_max(self, min: int, max: int) -> bool:
        return self.min == min and self.max == max

    def __eq__(self, other) -> bool:
        return super.__eq__(other) and \
            self.min == other.min and self.max == other.max

    def __hash__(self):
        return id(self)

    def wft_rep(self, simplify=None) -> str:
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
        children = []
        for fillers in self.frame.filler_set:
            child = []
            for filler in fillers.nodes:
                child.append(filler.get_unique_rep())
            children.append(child)

        return UniqueRep(caseframe_name=self.frame.caseframe.name, children=children, min=self.min, max=self.max)

### What are these here for?
class ThreshNode(MinMaxOpNode):
    """ Thresh with two values """
    pass

### What are these here for?
class AndOrNode(MinMaxOpNode):
    """ AndOr with two values """
    pass

class ImplNode(Molecular):
    def __init__(self, frame, bound) -> None:
        super().__init__(frame)
        self.bound = bound

    def has_bound(self, bound: int) -> bool:
        return self.bound == bound

    def antecedents(self):
        return self.follow_down_cable(self.frame.caseframe.slots[0])

    def consequents(self):
        return self.follow_down_cable(self.frame.caseframe.slots[1])

    def __eq__(self, other) -> bool:
        return super.__eq__(other) and \
            self.bound == other.bound

    def __hash__(self):
        return id(self)

    def wft_rep(self, simplify=None) -> str:
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
        # Creates base atomic node

        if match(r'^(arb|ind)\d+$', name) or self.enforce_name_syntax and not match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
            raise NodeError("ERROR: The term name '{}' is not allowed".format(name))

        if name in self.nodes:
            node = self.nodes[name]

            # Respecification
            current_type = node.sem_type
            new_type = self.sem_hierarchy.get_type(sem_type_name)
            node.sem_type = self.sem_hierarchy.respecify(name, current_type, new_type)
        else:
            # Creation
            sem_type = self.sem_hierarchy.get_type(sem_type_name)
            self.nodes[name] = Base(name, sem_type)

    def list_terms(self) -> None:
        for term in self.nodes:
            print(self.nodes[term])

    def find_term(self, name: str) -> Node:
        if name in self.nodes:
            return self.nodes[name]
        else:
            raise NodeError('ERROR: Term "' + name + '" not defined.')
