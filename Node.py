from .Caseframe import Frame

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

    def has_frame(self, frame):
        return False

    def __str__(self):
        return "<{}>: {}".format(self.name, self.docstring)

# =====================================
# ---------- ATOMIC NODES -------------
# =====================================

class Atomic(Node):
    """ Node that is a leaf in a graph. """
    pass

class Base(Atomic):
    """ A constant. """
    pass

class Variable(Atomic):
    """ A variable term ranging over a restricted domain. """
    counter = 0
    def __init__(self, name, docstring=""):
        super().__init__(name, docstring) # These need semantic types. This will be an error.
        self.restriction_set = {}

    def add_restriction(self, restriction):
        self.restriction_set[restriction.name] = restriction

class Indefinite(Variable):
    """ An indefinite object """
    def __init__(self, docstring=""):
        self.name = 'V' + str(super().counter)
        super().__init__(self.name, docstring) # These need semantic types. This will be an error.
        self.dependency_set = {}

    def add_dependency(self, dependency):
        self.dependency_set[dependency.name] = dependency

class Arbitrary(Variable):
    """ An arbitaray individual """
    def __init__(self, docstring=""):
        self.name = 'V' + str(super().counter)
        super().__init__(self.name, docstring) # These need semantic types. This will be an error.

# =====================================
# --------- MOLECULAR NODES -----------
# =====================================

class Molecular(Node):
    counter = 1
    # Non-leaf nodes
    def __init__(self, sem_type):
        name = "wft" + str(Molecular.counter)
        Molecular.counter += 1
        super().__init__(name, sem_type)
        self.down_cableset = {} # dictionary of frames

    def add_down_cables(self, frame):
        self.down_cableset[frame.name] = frame # Corresponds to frame

    def has_frame(self, frame):
        return any(frame == current_frame for current_frame in self.down_cableset.values())

    def __str__(self):
        ret = super().__str__()
        for frame in self.down_cableset.values():
            ret += "\n\t" + str(frame)
        return ret


class MinMaxOp(Molecular):
    """ Thresh/andor with two values """
    def __init__(self, name, docstring="", min=1, max=1):
        super().__init__(name, docstring)
        self.min = min
        self.max = max


class NodeMixIn:
    """ Provides functions related to nodes to network """

    def __init__(self):
        if type(self) == NodeMixIn:
            raise NotImplementedError
        self.nodes = {}

    def define_term(self, name, docstring="", sem_type_name="Entity"):
        # Creates base atomic node
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

    def all_terms(self):
        for term in self.nodes:
            print(self.nodes[term])

    def find_term(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            print('ERROR: Term "' + name + '" not defined.', file=stderr)
            return None
