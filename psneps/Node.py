from .Caseframe import Frame
from .Slot import Slot
from .Error import SNError
from .SemanticType import SemanticType
from re import match

class NodeError(SNError):
    pass

class Node:
    """ Root of syntactic hierarchy """
    def __init__(self, name: str, sem_type: SemanticType, docstring="") -> None:
        self.name = name
        self.docstring = docstring
        self.up_cableset = set() # References to frames that point to this node
        self.sem_type = sem_type
        if type(self) in (Node, Atomic, Variable):
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
        return "<{}>: {} ({})".format(self.name, self.sem_type.name, self.docstring)

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
        self.restriction_set = set()

    def add_restriction(self, restriction) -> None: # These need type definitions, since we don't know what restrictions/dependencies are.
        self.restriction_set.add(restriction)

class Arbitrary(Variable):
    """ An arbitaray individual. """
    counter = 1
    def __init__(self, sem_type: SemanticType) -> None:
        self.name = 'arb' + str(self.counter)
        self.counter += 1
        super().__init__(self.name, sem_type) # These need semantic types. This will be an error.

class Indefinite(Variable):
    """ An indefinite object. """
    counter = 1
    def __init__(self, sem_type: SemanticType) -> None:
        self.name = 'ind' + str(self.counter)
        self.counter += 1
        self.dependency_set = set()
        super().__init__(self.name, sem_type) # These need semantic types. This will be an error.

    def add_dependency(self, dependency) -> None: # These need type definitions, since we don't know what restrictions/dependencies are.
        self.dependency_set.add(dependency)

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

        for i in range(0, len(self.frame.filler_set)):
            slot = self.frame.caseframe.slots[i]
            fillers = self.frame.filler_set[i]
            for node in fillers.nodes:
                node.add_up_cable(self, slot)

    def has_frame(self, frame: Frame) -> bool:
        return frame == self.frame

    def __eq__(self, other):
        return self.has_frame(other.frame)

    def __str__(self) -> str:
        return super().__str__() + "\n\t" + str(self.frame)

    def __hash__(self):
        return id(self)

    def follow_down_cable(self, slot):
        return self.frame.get_filler_set(slot)


class MinMaxOpNode(Molecular):
    """ Thresh/andor with two values """
    def __init__(self, frame, min=1, max=1) -> None:
        super().__init__(frame)
        self.min = min
        self.max = max

    def has_min_max(self, min: int, max: int) -> bool:
        return self.min == min and self.max == max

    def __eq__(self, other):
        return super.__eq__(other) and \
            self.min == other.min and self.max == other.max

    def __hash__(self):
        return id(self)

    def __str__(self) -> str:
        return Node.__str__(self) + " {}, {}".format(self.min, self.max) + "\n\t" + str(self.frame)

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

    def define_term(self, name, sem_type_name="Entity", docstring="") -> None:
        # Creates base atomic node

        if self.enforce_name_syntax and not match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
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
            self.nodes[name] = Base(name, sem_type, docstring)

    def list_terms(self) -> None:
        for term in self.nodes:
            print(self.nodes[term])

    def find_term(self, name: str) -> Node:
        if name in self.nodes:
            return self.nodes[name]
        else:
            raise NodeError('ERROR: Term "' + name + '" not defined.')
