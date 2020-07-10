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

    def equivalent_structure(self, other, var_name : str):
        return (self.name == other.name or self.name == var_name) and \
               self.caseframe_name == other.caseframe_name and \
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

class VarRep:
    var_num = 1
    def __init__(self):
        self.name = '_' + VarRep.var_num
        VarRep.var_num += 1
        # Restrictions should be an unordered set of UniqueRep objects
        self.restriction_reps = set()
        # Dependencies should be an unordered set of UniqueRep objects
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
        self_dep_reps = self.dependency_reps.copy()
        other_dep_reps = other.dependency_reps.copy()
        for rep in self_dep_reps:
            located = False
            for other_rep in other_dep_reps:
                if other_rep.equivalent_structure(rep, other.name):
                    located = True
                    other_dep_reps.remove(other_rep)
                    break
                if not located:
                    return False

        # Ensure every restriction on self on other
        self_rest_reps = self.restriction_reps.copy()
        other_rest_reps = other.restriction_reps.copy()
        for rep in self_rest_reps:
            located = False
            for other_rep in other_rest_reps:
                if other_rep.equivalent_structure(rep, other.name):
                    located = True
                    other_rest_reps.remove(other_rep)
                    break
                if not located:
                    return False

        return True
