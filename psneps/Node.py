from .Caseframe import Frame
from .Slot import Slot
from .Error import SNError
from .SemanticType import SemanticType
from re import match

class NodeError(SNError):
    pass

class Node:
    """ Root of syntactic hierarchy """
    def __init__(self, name: str, sem_type: SemanticType) -> None:
        self.name = name
        self.up_cableset = set() # References to frames that point to this node
        self.sem_type = sem_type
        if type(self) in (Node, Atomic, Variable, MinMaxOpNode):
            raise NotImplementedError("Bad syntactic type - see syntax tree in wiki")

    def add_up_cable(self, node, slot: Slot) -> None:
        self.up_cableset.add(UpCable(node, slot))

    def has_upcable(self, name):
        return any(up_cable.name == name for up_cable in self.up_cableset)

    def follow_down_cable(self, slot):
        return set()

    def follow_up_cable(self, slot):
        return set(up_cable.node for up_cable in self.up_cableset if up_cable.slot is slot)

    def __str__(self) -> str:
        return self.wft_rep()

    def wft_rep(self, simplify=None):
        return self.name

    def has_constituent(self, constituent, visited=None):
        return self is constituent

    def replace_var(self, old, new):
        return

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
    pass

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return id(self)

class Variable(Atomic):
    """ A variable term ranging over a restricted domain. """
    def __init__(self, name: str, sem_type: SemanticType) -> None:
        super().__init__(name, sem_type) # This needs a semantic types. This will be an error.
        self.char_name = name
        self.restriction_set = set()

    def add_restriction(self, restriction) -> None: # These need type definitions, since we don't know what restrictions/dependencies are.
        self.restriction_set.add(restriction)

    def replace_var(self, old, new):
        temp_restriction_set = set()
        for restriction in self.restriction_set:
            if restriction is old:
                temp_restriction_set.add(new)
            else:
                temp_restriction_set.add(restriction)
        self.restriction_set = temp_restriction_set

    def wft_rep(self, simplify=None):
        return self.char_name

class Arbitrary(Variable):
    """ An arbitaray individual. """
    counter = 1
    def __init__(self, name, sem_type: SemanticType) -> None:
        super().__init__(name, sem_type) # These need semantic types. This will be an error.

    def store_in(self, current_network):
        self.name = 'arb' + str(self.counter)
        Arbitrary.counter += 1
        current_network.nodes[self.name] = self

    def wft_rep(self, simplify=None):
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            return "every({} {})".format( \
                self.char_name, \
                ", ".join([restriction.wft_rep(simplify.copy()) for restriction in self.restriction_set]))

class Indefinite(Variable):
    """ An indefinite object. """
    counter = 1
    def __init__(self, name, sem_type: SemanticType) -> None:
        self.dependency_set = set()
        super().__init__(name, sem_type) # These need semantic types. This will be an error.

    def add_dependency(self, dependency) -> None: # These need type definitions, since we don't know what restrictions/dependencies are.
        self.dependency_set.add(dependency)

    def store_in(self, current_network):
        self.name = 'ind' + str(self.counter)
        Indefinite.counter += 1
        current_network.nodes[self.name] = self

    def replace_var(self, old, new):
        super().replace_var(old, new)
        temp_dependency_set = set()
        for dependency in self.dependency_set:
            if dependency is old:
                temp_dependency_set.add(new)
            else:
                temp_dependency_set.add(dependency)
        self.dependency_set = temp_dependency_set

    def wft_rep(self, simplify=None):
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep(simplify)
        else:
            simplify.add(self)
            return "some({} ({}) {})".format( \
                self.char_name, \
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

    def __eq__(self, other):
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

    def replace_var(self, old, new):
        temp_filler_nodes = set()
        for i in range(0, len(self.frame.filler_set)):
            slot = self.frame.caseframe.slots[i]
            fillers = self.frame.filler_set[i]
            for node in fillers.nodes:
                if node is old:
                    temp_filler_nodes.add(new)
                    new.add_up_cable(self, slot)
                else:
                    temp_fillers.add(node)
            fillers.nodes = temp_filler_nodes
            temp_filler_nodes = set()

    def wft_rep(self, simplify=None):
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            ret = "{}(".format(self.frame.caseframe.name)
            for i in range(len(self.caseframe.filler_set)):
                if i > 0:
                    ret += ", "
                ret += "["
                filler = self.caseframe.filler_set[i]
                for j in len(filler.nodes):
                    if j > 0:
                        ret += ", "
                    ret += filler.nodes[j].wft_rep(simplify.copy())
                ret += "]"
            ret += ")"
        return ret


class MinMaxOpNode(Molecular):
    """ Thresh/andor with two values """
    def __init__(self, frame, min, max) -> None:
        super().__init__(frame)
        self.min = min
        self.max = max

    def num_constituents(self):
        # All of the propositions to which this and, or, thresh, etc. has wires
        return len(self.frame.filler_set[0])

    def has_min_max(self, min: int, max: int) -> bool:
        return self.min == min and self.max == max

    def __eq__(self, other):
        return super.__eq__(other) and \
            self.min == other.min and self.max == other.max

    def __hash__(self):
        return id(self)

    def wft_rep(self, simplify=None):
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            if self.frame.caseframe.name == "thresh" or self.frame.caseframe.name == "andor":
                ret = "{}\{{}, {}\}(".format(self.frame.caseframe.name, self.min, self.max)
            else:
                ret = "{}(".format(self.frame.caseframe.name)
            for i in range(len(self.caseframe.filler_set)):
                if i > 0:
                    ret += ", "
                ret += "["
                filler = self.caseframe.filler_set[i]
                for j in len(filler.nodes):
                    if j > 0:
                        ret += ", "
                    ret += filler.nodes[j].wft_rep(simplify.copy())
                ret += "]"
            ret += ")"
        return ret

class ThreshNode(MinMaxOpNode):
    """ Thresh with two values """
    pass

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

    def __eq__(self, other):
        return super.__eq__(other) and \
            self.bound == other.bound

    def __hash__(self):
        return id(self)

    def wft_rep(self, simplify=None):
        if simplify is None:
            simplify = set()
        if self in simplify:
            return super().wft_rep()
        else:
            simplify.add(self)
            return "{}=>([{}], [{}])".format(self.bound, \
            ", ".join([ant.wft_rep(simplify.copy()) for ant in self.antecedents]),
            ", ".join([cq.wft_rep(simplify.copy()) for cq in self.antecedents]))


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
