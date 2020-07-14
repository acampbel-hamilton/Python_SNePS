from ...Error import SNError

class SNePSVarError(SNError):
    pass

class UniqueRep:
    """ Unique set-like representation for variables """
    def __init__(self, name=None, caseframe_name=None, min=None, max=None, bound=None, children=None):
        self.name = name
        self.caseframe_name = caseframe_name
        self.min = min
        self.max = max
        self.bound = bound
        # Children should be an ordered list of UniqueRep objects
        self.children = [] if children is None else children

        # Ensure min, max, bound are within bounds
        if self.min is not None or self.max is not None or self.bound is not None:
            size = len(self.children[0])
            if self.min is not None and self.min > size:
                raise SNePSVarError("The min must be between 0 and {}".format(size))
            if self.max is not None and self.max > size:
                raise SNePSVarError("The max must be between 0 and {}".format(size))
            if self.bound is not None and self.bound > size:
                raise SNePSVarError("The bound must be between 0 and {}".format(size))

    def equivalent_structure(self, other, self_name: str = None, other_name: str = None):

        if not ((self.name == other.name or (self.name == self_name and other.name == other_name)) and \
            self.caseframe_name == other.caseframe_name and \
            self.min == other.min and \
            self.max == other.max and \
            self.bound == other.bound and \
            len(self.children) == len(other.children)):
                return False

        for i in range(len(self.children)):
            self_children = self.children[i].copy()
            other_children = other.children[i].copy()

            for self_child in self_children:
                for other_child in other.children[i]:
                    if self_child.equivalent_structure(other_child, self_name, other_name):
                        other_children.remove(other_child)
                        break
                else:
                    return False
            if len(other_children) != 0:
                return False

        return True

    def includes_var(var_name: str):
        """ Returns whether this UniqueRep or any of its children contains the given var. """
        return name == var_name or any(child.includes_var(var_name) for child in self.children)

    def __str__(self) -> str:
        return self.to_str()

    def to_str(self, depth=None) -> str:
        depth = 1 if depth is None else depth
        ret = "\t" * depth
        ret += self.name if self.name is not None else self.caseframe_name
        ret += " ({}, {})".format(self.min, self.max) if self.min is not None else ''
        ret += " ({})".format(self.bound) if self.bound is not None else ''
        for child in self.children:
            for subchild in child:
                ret += "\n" + subchild.to_str(depth=depth+1)
            ret += "\n"
        return ret

class VarRep:
    var_num = 1
    def __init__(self):
        self.name = '_' + str(VarRep.var_num)
        VarRep.var_num += 1
        # Restrictions should be an unordered set of UniqueRep objects
        self.restriction_reps = set()
        # Dependencies should be an unordered set of VarRep objects
        self.dependency_reps = set()

    def add_restriction(self, restriction: UniqueRep):
        for rest_rep in self.restriction_reps:
            if rest_rep.equivalent_structure(restriction):
                return
        self.restriction_reps.add(restriction)

    def add_dependency(self, dependency: UniqueRep):
        self.dependency_reps.add(dependency)

    def __eq__(self, other):
        if len(self.dependency_reps) != len(other.dependency_reps) \
            or len(self.restriction_reps) != len(other.restriction_reps):
                return False

        # Ensure every dependency on self on other
        if not self.dependency_reps == other.dependency_reps:
            return False

        # Ensure every restriction on self on other
        self_rest_reps = self.restriction_reps.copy()
        other_rest_reps = other.restriction_reps.copy()
        for rep in self_rest_reps:
            located = False
            for other_rep in other.restriction_reps:
                if other_rep.equivalent_structure(rep, other.name, self.name):
                    located = True
                    other_rest_reps.remove(other_rep)
                    break
            if not located:
                return False

        return True

    def __str__(self) -> str:
        ret = self.name + ":"
        for restriction in self.restriction_reps:
            ret += "\n" + str(restriction)

        return ret
