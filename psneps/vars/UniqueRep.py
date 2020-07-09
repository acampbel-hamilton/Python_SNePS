class UniqueRep:
    """ Unique set-like representation for variables """
    var_num = 1
    def __init__(self, name=None, min=None, max=None, bound=None, children=None):
        self.name = name
        if self.name == '_':
            self.name = '_' + UniqueRep.var_num
            UniqueRep.var_num += 1
        self.min = min
        self.max = max
        self.bound = bound
        # Children should be an ordered list of UniqueRep objects
        self.children = [] if children is None else children

    def __eq__(self, other):
        return self.name == other.name and \
               self.min == other.min and \
               self.max == other.max and \
               self.bound == other.bound and \
               self.children == other.children

    def includes_var(var_name : str):
        if name == var_name:
            return True
        for child in self.children:
            if child.includes_var(var_name):
                return True
        return False

    def __hash__(self):
        return hash((self.name, self.min, self.max, self.bound, tuple(self.children)))

class VarRep:
    def __init__(self, name):
        # Restrictions should be an unordered set of UniqueRep objects
        self.restrictions = set()
        # Dependencies should be an unordered set of UniqueRep objects
        self.dependencies = set()

    def add_restriction(self, restriction : UniqueRep):
        self.restrictions.add(restriction)

    def add_dependency(self, dependency : UniqueRep):
        self.dependen.add(dependency)

    def __eq__(self, other):
        return self.dependencies == other.dependencies and \
               self.restrictions == other.restrictions
