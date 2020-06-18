from .Caseframe import Frame

class Node:
    # Root of syntactic hierarchy
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
        return "<{}>: {}".format(self.name, self.docstring)

# =====================================
# ---------- ATOMIC NODES -------------
# =====================================

class Atomic(Node):
    # Node that is a leaf in a graph
    pass

class Base(Atomic):
    # Constant
    pass

class Variable(Atomic):
    # a variable term ranging over a restricted domain
    counter = 0
    def __init__(self, name, docstring=""):
        super().__init__(self, name, docstring)
        self.restriction_set = {}

    def add_restriction(self, restriction):
        self.restriction_set[restriction.name] = restriction

class Indefinite(Variable):
    # an indefinite object
    def __init__(self, docstring=""):
        self.name = 'V' + str(super().counter)
        super().__init__(self, name, docstring)
        self.dependency_set = {}

    def add_dependency(self, dependency):
        self.dependency_set[dependency.name] = dependency

class Arbitrary(Variable):
    # an arbitaray individual
    def __init__(self, docstring=""):
        self.name = 'V' + str(super().counter)
        super().__init__(self, name, docstring)

# =====================================
# --------- MOLECULAR NODES -----------
# =====================================

class Molecular(Node):
    # Non-leaf nodes
    def __init__(self, name, docstring=""):
        super().__init__(self, name, docstring)
        self.down_cableset = {} # dictionary of frames

    def add_down_cable(self, cable):
        self.down_cableset[cable.name] = cable # Corresponds to frame

    def __eq__(self, other):
        # determines if two molecular terms are equivalent
        if not isinstance(other, Molecular):
            return False
        self_fill = self.down_cableset.values()
        other_fill = other.down_cableset.values()
        return other.caseframe == self.caseframe and \
            [sorted(sl) for sl in sorted(other_fill)] == \
            [sorted(sl) for sl in sorted(self_fill)]

    def __str__(self):
        return super().__str__() + \
        "\t{}".format("\n\t".join(self.up_cableset.keys()))

class MinMaxOp(Molecular):
    # Thresh/andor with two values
    def __init__(self, name, docstring="", min=1, max=1):
        super().__init__(self, name, docstring)
        self.min = min
        self.max = max

# =====================================
# -------------- MIXIN ----------------
# =====================================

class NodeMixIn:
    """ Provides functions related to nodes to network """

    def __init__(self):
        if type(self) == NodeMixIn:
            raise NotImplementedError
        self.nodes = {}

    def define_term(self, name, docstring="", sem_type_name="Entity"):
        # Creates base atomic node

        if name in self.nodes:
            # Respecification
            node = self.nodes[name]
            current_type = node.sem_type
            new_type = self.sem_hierarchy[sem_type_name]
            node.sem_type = self.sem_hierarchy.respecify(name, current_type, new_type)
        else:
            # Creation
            sem_type = self.sem_hierarchy.get_type(sem_type_name)
            self.nodes[name] = Base(name, sem_type, docstring)

    def all_terms(self):
        [print(self.nodes[term]) for term in self.nodes]

    def find_term(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            print("Term ''" + name + "'' not defined.", file=stderr)
