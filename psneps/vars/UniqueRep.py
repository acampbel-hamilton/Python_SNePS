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

    def equivalent_structure(self, other, self_name : str, other_name : str):

        if not ((self.name == other.name or (self.name == self_name and other.name == other_name)) and \
            self.caseframe_name == other.caseframe_name and \
            self.min == other.min and \
            self.max == other.max and \
            self.bound == other.bound):
                return False

        try:
            for i in range(len(self.children)):
                for j in range(len(self.children[i])):
                    if not self.children[i][j].equivalent_structure(other.children[i][j], self_name, other_name):
                        return False
        except Exception:
            return False

        return True

    def includes_var(var_name : str):
        if name == var_name:
            return True
        for child in self.children:
            if child.includes_var(var_name):
                return True
        return False

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

    def add_restriction(self, restriction : UniqueRep):
        self.restriction_reps.add(restriction)

    def add_dependency(self, dependency : UniqueRep):
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
            for other_rep in other_rest_reps:
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
