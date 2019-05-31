#SNePS3 caseframe

#the folowing is a link to historic SNePS caseframes:
#https://cse.buffalo.edu/sneps/Manuals/dictionary.pdf

class CaseFrame:
    def __init__(self, type, slots=[], adj_to=set(), adj_from=set(), terms=set()):
        self.type = type #must be either obj or class itself
        self.slots = slots
        self.adj_to = adj_to
        self.adj_from = adj_from
        self.terms = terms

    def __eq__(self, other):
        """Returns true if both arguments are equivalent caseframes.
            Two caseframes are equivalent when:
                1. They have the same type
                2. They have the same slots (disregarding order)"""
        return self.type is other.type and self.slots == other.slots

    def __str__(self):
        """Creates a string representation of a CaseFrame"""
        return "<{}, \{{}\} >".format(self.type, (str(list(map(lambda slot: slot.__str__(), self.slots)))[1:-1]))

class CaseFrame_Mixin:
	"""contains caseframe related methods for Network class"""
		#psuedo adjustability should be added here once it is understood
	    def adjustable(srcframe, tgtframe):
	        """returns true if srcframe is a caseframe which is
	            adjustable to the caseframe tgtframe"""
	        return pos_adj(srcframe, tgtframe) or\
	                neg_adj(srcframe, tgtframe)    # the CL inplementation also has a psudeo-adjustable (Add this later?)

	#isinstance check for C_src subtype of C_tgt may be incorrect (see caseframes.cl ln 368)
	    def pos_adj(srcframe, tgtframe):
	        """returns true if srcframe is a caseframe that is pos_adj to the caseframe
	            tgtframe. Caseframe <C_src, R_src> is pos_adj to caseframe
	            <C_tgt, R_tgt> if:
	                1. C_src is the same, or a subtype of C_tgt
	                2. Every slot in R_src - R_tgt is pos_adj reducible and min = 0
	                3. Every slot in R_tgt - R_src is pos_adj expandable and min = 0"""
	        return (srcframe.type is tgtframe.type or
	                isinstance(srcframe.type, tgtframe.type.__class__)) and \
	                all(s.pos_adj is "reduce" and s.min == 0
	                    for s in (srcframe.slots - tgtframe.slots)) and \
	                all(s.pos_adj is "expand" and s.min == 0
	                    for s in (tgtframe.slots - srcframe.slots))

	    def neg_adj(srcframe, tgtframe):
	        """returns true if srcframe is a caseframe that is neg_adj to the caseframe
	            tgtframe. Caseframe <C_src, R_src> is neg_adj to caseframe
	            <C_tgt, R_tgt> if:
	                1. C_src is the same, or a subtype of C_tgt
	                2. Every slot in R_src - R_tgt is neg_adj reducible and min = 0
	                3. Every slot in R_tgt - R_src is neg_adj expandable and min = 0"""
	        return (srcframe.type is tgtframe.type or
	                    isinstance(srcframe.type, tgtframe.type.__class__)) and \
	                all(s.neg_adj is "reduce" and s.min == 0
	                    for s in (srcframe.slots - tgtframe.slots)) and \
	                all(s.neg_adj is "expand" and s.min == 0
	                    for s in (tgtframe.slots - srcframe.slots))
