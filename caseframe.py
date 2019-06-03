#SNePS3 caseframe

#the folowing is a link to historic SNePS caseframes:
#https://cse.buffalo.edu/sneps/Manuals/dictionary.pdf

from SyntacticTypes import AndOr, Nor

class CaseFrame:
	def __init__(self, type, docstring="", slots=[], adj_to=set(), adj_from=set(), terms=set()):
		self.type = type #must be either obj or class itself
        self.docstring = docstring
		self.slots = slots
		self.adj_to = adj_to
		self.adj_from = adj_from
		self.terms = terms

	def __eq__(self, other):
		"""Returns true if both arguments are equivalent caseframes.
			Two caseframes are equivalent when:
				1. They have the same type
				2. They have the same slots (disregarding order)"""
		return self.type is other.type and set(self.slots) - set(other.slots) == set([])

	def __str__(self):
		"""Creates a string representation of a CaseFrame"""
		return "<{}, \{{}\} >".format(self.type, (str(list(map(lambda slot: slot.__str__(), self.slots)))[1:-1]))

class CaseFrame_Mixin:
	"""contains caseframe related methods for Network class"""

    def find_frame(self, frameName):
        """Returns the caseframe associated with the given function symbol"""
        return self.caseframes[frameName]

    def defineCaseframe (typename, slots, docstring="", print_pattern, frameSymbols):
        assert some(map (lambda x: x.type_name == typename) (set(self.semanticRoot) + set(self.semanticRoot.__subclasses__())))
        # assert that the CaseFrame doesn't already exist
        assert isinstance(docstring, str)
        assert isinstance(print_pattern, list)
        assert (isinstance(fsymbols, list) or fsymbols == null)
        newCF = CaseFrame(self.findSemanticType(type), docstring, slots)
        map (self.caseframes[fs] = newCF) frameSymbols
        # Look at all existing caseframes, check whether they are adjustable to
        # or from this one. If so, store that information in the frames.
        for case in self.caseframes:
            if case != newCF:
                if adjustable(newCF, case):
                    newCF.adj_to.add(case)
                    case.adj_from.add(newCF)
                if adjustable(case, newCF):
                    case.adj_to.add(newCF)
                    newCF.adj_from.add(case)


    def adjustable(self, srcframe, tgtframe):
		"""returns true if srcframe is a caseframe which is
			adjustable to the caseframe tgtframe"""
		return pos_adj(srcframe, tgtframe) or\
				neg_adj(srcframe, tgtframe)
				# the CL inplementation also has a psudeo-adjustable (Add this later?)

    # def pseudo_adjustable(self, srcFrame, tgtFrame):
    #       """Returns t if srcframe is 'pseudo-adjustable' to tgtframe.
    #            Pseudo-adjustability allows slot-based inference to operate on frames
    #            that are not actually adjustable, e.g. nor and andor"""
    #     return

#isinstance check for C_src subtype of C_tgt may be incorrect (see caseframes.cl ln 368)
	def pos_adj(self, srcframe, tgtframe):
		"""returns true if srcframe is a caseframe that is pos_adj to the caseframe
			tgtframe. Caseframe <C_src, R_src> is pos_adj to caseframe
			<C_tgt, R_tgt> if:
				1. C_src is the same, or a subtype of C_tgt
				2. Every slot in R_src - R_tgt is pos_adj reducible and min = 0
				3. Every slot in R_tgt - R_src is pos_adj expandable and min = 0"""
		return (srcframe.type is tgtframe.type or
				isinstance(srcframe.type, tgtframe.type.__class__)) and \
				all(s.pos_adj is "reduce" and s.min == 0
					for s in (set(srcframe.slots) - set(tgtframe.slots))) and \
				all(s.pos_adj is "expand" and s.min == 0
					for s in (set(tgtframe.slots) - set(srcframe.slots)))

	def neg_adj(self, srcframe, tgtframe):
		"""returns true if srcframe is a caseframe that is neg_adj to the caseframe
			tgtframe. Caseframe <C_src, R_src> is neg_adj to caseframe
			<C_tgt, R_tgt> if:
				1. C_src is the same, or a subtype of C_tgt
				2. Every slot in R_src - R_tgt is neg_adj reducible and min = 0
				3. Every slot in R_tgt - R_src is neg_adj expandable and min = 0"""
		return (srcframe.type is tgtframe.type or
					isinstance(srcframe.type, tgtframe.type.__class__)) and \
				all(s.neg_adj is "reduce" and s.min == 0
					for s in (set(srcframe.slots) - set(tgtframe.slots))) and \
				all(s.neg_adj is "expand" and s.min == 0
					for s in (set(tgtframe.slots) - set(srcframe.slots)))
