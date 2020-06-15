class Node:
    # Root of syntactic hierarchy
    def __init__(self, name, docstring="", sem_type):
        self.name = name
        self.docstring = docstring
        self.up_cableset = {}
        self.asserted_in = {}
        self.sem_type = sem_type
        if self.type in (Node, Atomic, Variable):
            raise NotImplementedError("Bad syntactic type - see syntax tree in wiki")

    def add_up_cable(self, cable):
        self.up_cableset[cable.name] = cable

class Molecular(Node):
    # Non-leaf nodes
    def __init__(self, name, docstring=""):
        super().__init__(self, name, docstring)
        self.down_cableset = {}

    def add_down_cable(self, cable):
        self.down_cableset[cable.name] = cable

    def __eq__(self, other):
		# determines if two molecular terms are equivalent
		if not isinstance(other, Molecular):
			return False
		self_fill = self.down_cableset.values()
		other_fill = other.down_cableset.values()
		return other.caseframe == self.caseframe and \
				[sorted(sl) for sl in sorted(other_fill)] == \
				[sorted(sl) for sl in sorted(self_fill)]

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

class Param2Op(Molecular):
	# Thresh/andor with two values
	def __init__(self, name, docstring="", min, max):
		super().__init__(self, name, docstring)
		self.min = min
		self.max = max

class Param1Op(Molecular):
    # Thresh with single value
    def __init__(self, name, docstring="", limit):
		super().__init__(self, name, docstring)
		self.limit = limit
