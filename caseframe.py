#SNePS3 caseframe

#the folowing is a link to historic SNePS caseframes:
#https://cse.buffalo.edu/sneps/Manuals/dictionary.pdf

from Symbol import Sym, _reduce, _expand, _none

class CaseFrame:
	def __init__(self, name, _type, docstring="", slots=None, adj_to=None, adj_from=None, terms=None):
		self.name = Sym(name)
		self.type = _type #must be either obj or class itself
		self.docstring = docstring
		self.slots = [] if slots is None else slots #list of slot names
		self.adj_to = set() if adj_to is None else adj_to
		self.adj_from = set() if adj_from is None else adj_from
		self.terms = set() if terms is None else terms #set of term names

	def __eq__(self, other):
		"""Returns true if both arguments are equivalent caseframes.
			Two caseframes are equivalent when:
				1. They have the same type
				2. They have the same slots (disregarding order)"""
		return not other is None and self.type is other.type and\
		 		set(self.slots) - set(other.slots) == set([])

	def __repr__(self):
		return "Caseframe {} id: {}".format(self.name, hex(id(self)))

	def __str__(self):
		"""Creates a string representation of a CaseFrame"""
		return "{} <{}>\nSlots: {}".format(self.name, self.type.getClass(),
		 			(str([repr(s) for s in self.slots])[1:-1]))

class CaseFrame_Mixin:
	"""contains caseframe related methods for Network class"""

	def listCaseframe(self):
		print(*(sorted(self.caseframes.keys())), sep='\n')

	def find_frame(self, name):
		"""Returns the caseframe associated with the given function symbol"""
		assert isinstance(name, str) or isinstance(name, CaseFrame)
		return self.caseframes.get(Sym(name)) if isinstance(name, str) else name

	def defineCaseframe(self, name, type, slots, docstring=""):
		assert isinstance(name, str)
		assert self.findSemanticType(type) in\
			self.subtypes(self.semanticRoot).union(set([self.semanticRoot]))
		assert self.checkNewCaseframe(type, slots)
		assert isinstance(docstring, str)

		self.caseframes[Sym(name)] = CaseFrame(Sym(name),
					self.findSemanticType(type)(), docstring, slots)
		newCF = self.caseframes[Sym(name)]
		# Look at all existing caseframes, check whether they are adjustable to
		# or from this one. If so, store that information in the frames.
		for case in self.caseframes.values():
			if not case == newCF:
				if self.adjustable(newCF, case):
					newCF.adj_to.add(case)
					case.adj_from.add(newCF)
				if self.adjustable(case, newCF):
					case.adj_to.add(newCF)
					newCF.adj_from.add(case)

	def checkNewCaseframe(self, newType, slots):
		"""If there is already a caseframe with the given type and slots
		   (order doesn't matter), then raises error, else returns"""
		for oldCF in self.caseframes.values():
			if oldCF.type == newType and (set(oldCF.slots) - set(slots) == set()):
				return False
		return True

	def add_caseframe_term(self, term, cf = None):
		"""Adds a term to a caseframe's list of terms that use it.
		If the caseframe cf is given, add the term to that caseframe.
		Else, add the term to the caseframe that term uses."""
		if not(cf): cf = term.CaseFrame
		cf.terms.add(term)

	def adjustable(self, srcframe, tgtframe):
		"""returns true if srcframe is a caseframe which is
			adjustable to the caseframe tgtframe"""
		return  self.pos_adj(srcframe, tgtframe) or\
				self.neg_adj(srcframe, tgtframe) or\
				self.pseudo_adjustable(srcframe, tgtframe)

	def pseudo_adjustable(self, srcFrame, tgtFrame):
		"""Returns t if srcframe is 'pseudo-adjustable' to tgtframe.
		   Pseudo-adjustability allows slot-based inference to operate on frames
		   that are not actually adjustable, e.g. nor and andor"""
		return srcFrame == self.find_frame("Nor") and tgtFrame == self.find_frame("AndOr")
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
				all([(s.pos_adj is _reduce and s.min == 0)
					for s in map(self.findSlot,
						set(srcframe.slots) - set(tgtframe.slots))]) and \
				all([(s.pos_adj is _expand and s.min == 0)
					for s in map(self.findSlot,
						set(tgtframe.slots) - set(srcframe.slots))])

	def neg_adj(self, srcframe, tgtframe):
		"""returns true if srcframe is a caseframe that is neg_adj to the caseframe
			tgtframe. Caseframe <C_src, R_src> is neg_adj to caseframe
			<C_tgt, R_tgt> if:
				1. C_src is the same, or a subtype of C_tgt
				2. Every slot in R_src - R_tgt is neg_adj reducible and min = 0
				3. Every slot in R_tgt - R_src is neg_adj expandable and min = 0"""
		return (srcframe.type is tgtframe.type or
					isinstance(srcframe.type, tgtframe.type.__class__)) and \
				all([(s.neg_adj is _reduce and s.min == 0)
					for s in map(self.findSlot,
						set(srcframe.slots) - set(tgtframe.slots))]) and \
				all([(s.neg_adj is _expand and s.min == 0)
					for s in map(self.findSlot,
						set(tgtframe.slots) - set(srcframe.slots))])
