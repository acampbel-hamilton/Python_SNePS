#SNePS3 caseframe

#the folowing is a link to historic SNePS caseframes:
#https://cse.buffalo.edu/sneps/Manuals/dictionary.pdf

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
		return "<{}, \{{}\} >".format(self.type,
		 			(str(list(map(lambda slot: str(slot), self.slots)))[1:-1]))

class CaseFrame_Mixin:
	"""contains caseframe related methods for Network class"""

	def find_frame(self, frameName):
		"""Returns the caseframe associated with the given function symbol"""
		return self.caseframes[frameName]

	def defineCaseframe (self, typename, slots, frameSymbols, docstring="", print_pattern = None):
		assert isinstance(findSemanticType(typename), self.semanticRoot)
		checkNewCaseframe(type, slots)
		assert isinstance(docstring, str)
		assert isinstance(print_pattern, list)
		assert (isinstance(fsymbols, list) or fsymbols == null)
		newCF = CaseFrame(self.findSemanticType(type), docstring, slots)
		for fs in frameSymbols:
			self.caseframes[fs] = newCF
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

	def checkNewCaseframe (self, newType, slots):
		"""If there is already a caseframe with the given type and slots
		   (order doesn't matter), then raises error, else returns"""
		for key in self.caseframes:
			oldCF = self.caseframes[key]
			if oldCF.type == newType and (set(oldCF.slots) - set(slots) == set([])):
				error

	def add_caseframe_term(self, term, cf = None):
		"""Adds a term to a caseframe's list of terms that use it.
		If the caseframe cf is given, add the term to that caseframe.
		Else, add the term to the caseframe that term uses."""
		if not(cf): cf = term.CaseFrame
		cf.terms.add(term)

	def adjustable(self, srcframe, tgtframe):
		"""returns true if srcframe is a caseframe which is
			adjustable to the caseframe tgtframe"""
		return  pos_adj(srcframe, tgtframe) or\
				neg_adj(srcframe, tgtframe) or\
				pseudo_adjustable(srcframe, tgtframe)

	def pseudo_adjustable(self, srcFrame, tgtFrame):
		"""Returns t if srcframe is 'pseudo-adjustable' to tgtframe.
		   Pseudo-adjustability allows slot-based inference to operate on frames
		   that are not actually adjustable, e.g. nor and andor"""
		return srcFrame == find_frame("Nor") and tgtFrame == find_frame("AndOr")
		# NOR does not exist until defined in initialization

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
