from .Caseframe import Frame
from .Error import SNError
from re import match

class NodeError(SNError):
    pass

class Node:
    """ Root of syntactic hierarchy """
    def __init__(self, name, sem_type, docstring=""):
        self.name = name
        self.docstring = docstring
        self.up_cableset = {} # References to frames that point to this node
        self.sem_type = sem_type
        if type(self) in (Node, Atomic, Variable):
            raise NotImplementedError("Bad syntactic type - see syntax tree in wiki")

    def add_up_cable(self, frame):
        self.up_cableset[frame.name] = frame

    def __str__(self):
        return "<{}>: {} ({})".format(self.name, self.sem_type.name, self.docstring)

    def molecular(self):
        return False

# =====================================
# ---------- ATOMIC NODES -------------
# =====================================

class Atomic(Node):
    """ Node that is a leaf in a graph. (An abstract class) """
    def has_frame(self, frame):
        """ Atomics don't have frames, so this always returns False. """
        return False

class Base(Atomic):
    """ A constant. (An abstract class) """
    pass

class Variable(Atomic):
    """ A variable term ranging over a restricted domain. """
    counter = 1
    def __init__(self, name):
        super().__init__(name) # This needs a semantic types. This will be an error.
        self.restriction_set = {}
        Variable.counter += 1

    def add_restriction(self, restriction):
        self.restriction_set[restriction.name] = restriction

class Arbitrary(Variable):
    """ An arbitaray individual. """
    def __init__(self):
        self.name = 'V' + str(super().counter)
        super().__init__(self.name) # These need semantic types. This will be an error.

class Indefinite(Variable):
    """ An indefinite object. """
    def __init__(self):
        self.name = 'V' + str(super().counter)
        super().__init__(self.name) # These need semantic types. This will be an error.
        self.dependency_set = {}

    def add_dependency(self, dependency):
        self.dependency_set[dependency.name] = dependency

# =====================================
# --------- MOLECULAR NODES -----------
# =====================================

class Molecular(Node):
    counter = 1
    # Non-leaf nodes
    def __init__(self, frame):
        name = "wft" + str(Molecular.counter)
        Molecular.counter += 1
        self.frame = frame
        super().__init__(name, frame.caseframe.sem_type)

    def has_frame(self, frame):
        return frame == self.frame

    def __str__(self):
        return super().__str__() + "\n\t" + str(self.frame)


class MinMaxOpNode(Molecular):
    """ Thresh/andor with two values """
    def __init__(self, frame, min=1, max=1):
        super().__init__(frame)
        self.min = min
        self.max = max

    def has_min_max(self, min, max):
        return self.min == min and self.max == max

    def __str__(self):
        return Node.__str__(self) + " {}, {}".format(self.min, self.max) + "\n\t" + str(self.frame)


# =====================================
# --------------- MIXIN ---------------
# =====================================

class NodeMixin:
    """ Provides functions related to nodes to Network """

    def __init__(self):
        if type(self) is NodeMixin:
            raise NotImplementedError("Mixins can't be instantiated.")
        self.nodes = {}

    def define_term(self, name, sem_type_name="Entity", docstring=""):
        # Creates base atomic node

        if self.enforce_name_syntax and not match(r'[A-Za-z_][A-Za-z0-9_]*', name):
            raise CaseframeError("ERROR: The term name '{}' is not allowed".format(name))

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

    def list_terms(self):
        for term in self.nodes:
            print(self.nodes[term])

    def find_term(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            raise NodeError('ERROR: Term "' + name + '" not defined.')
