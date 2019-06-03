# Python SNePS3 class

import inspect, re, sys
from caseframe import CaseFrame, CaseFrame_Mixin
from contexts import Context, Context_Mixin
from SemanticTypes import Entity, Proposition, Act, Policy, Thing, Category, Action
from SyntacticTypes import Term, Atom, Base, Variable, Indefinite, Arbitrary, \
	Molecular, Param2Op, AndOr, Disjunction, Xor, Nand, Thresh, Equivalence, \
	NumericalEntailment, OrEntailment, Implication, Categorization, \
	NegationByFailure, Conjunction, Negation
from SlotInference import SlotInference
from PathInference import PathInference

class Network(Context_Mixin, SlotInference, PathInference, CaseFrame_Mixin):
	def __init__(self):
		self.terms = {} #maps term names to term objs

		#stores all arbitary (universally quantified) terms
		self.arbitraries = set()

		#stores all indifinite (existentially quantified) terms
		self.indefinites = set()

		#root of the syntatic class hierarchy
		self.syntaticRoot = Term

		#root of the semantic class hierarchy
		self.semanticRoot = Entity

		#root of the context hierarchy
		self.contextRoot = None
		self.contextHierachy = {} #maps context names to lists of parent names

		self.caseframes = {} # maps CaseFrame names to CaseFrame objects
		self.slots = {} # maps slot names to slot objs
		self.contexts = {} #maps context names to context objs
		self.currentContext = None #stores the current context

		#determine whether inferences are traced
		self.goaltrace = None
		self.trace = False

		#contains possible values for pos_adj and neg_adj attributes of slots
		self._adjustments = ["reduce", "expand", None]

	def initialize(self):
		"""this function will set up the default state for a SNePS object once
		implemented, including default contexts, slots, and caseframes."""
		#declares BaseCT (base context) as the root of the context hierarchy and properly stores it
		self.contextRoot = Context("BaseCT", parents=None)
		self.contextHierachy[self.contextRoot.name] = self.contextRoot.parents
		self.contexts[self.contextRoot.name] = self.contextRoot

	def listSemanticTypes(self):
		"""Prints all semantic types for the user"""
		print(*[cls.__name__ for cls in self.semanticRoot.__subclasses__()], sep="\n")

	def findSemanticType(self, typeName):
		"""Returns the semantic object for the type name"""
		for type in (self.semanticRoot.__subclasses__() + self.semanticRoot):
			if typeName == type.getClass(): return type
		return False

	def assertedMembers(self, terms, ctx):
		"""returns all and only the asserted members of the given set of terms"""
		assert isinstance(terms, set)
		assert all(map((lambda t: isinstance(t, self.syntaticRoot)), terms))
		assert isinstance(ctx, Context)

		return list(filter((lambda t: t in ctx), terms))


	#currently requires self.initialize to be called (this decision should be revisited)
	def defineContext(self, name, docstring="", parents=set([self.contextRoot.name]), hyps=set()):
		"""allows a user defined contexts within a context hierarchy rooted at self.contextRoot"""
		assert isinstance(name, str)
		assert name not in self.contexts.keys(), "A context {} already exists".format(name)
		assert isinstance(docstring, str)
		assert isinstance(parents, set)
		#parents is a set of strings denoting the names of contexts
		assert all(map((lambda c: c in self.contexts.keys()), parents))
		assert isinstance(hyps, set)
		#hyps is a set of strings denoting the names of terms
		assert all(map((lambda t: t in self.terms.keys()), hyps))

		self.contexts[name] = Context(name, docstring,
								parents=set(map((lambda n: self.contexts[n]), parents)),
								hyps=set(map((lambda t: self.terms[t]), hyps)))
		self.contextHierachy[name] = parents

	def defineSemanticType(self, newtype, supers, docstring=""):
		"""allows user to defined new semantic types to be added to the semantic type
			hierarchy for the Network"""
		assert isinstance(newtype, str)
		assert isinstance(supers, list)
		assert all(map((lambda s: isinstance(s, str)), supers))
		assert isinstance(docstring, str)
		try:
			getattr(sys.modules[__name__], newtype)
			raise AssertionError("{} already names a SNePS semantic type".format(newtype))
		except AttributeError:
			for super in supers:
				try:
					cls = getattr(sys.modules[__name__], super)
					if not isinstance(cls, self.semanticRoot):
						raise AssertionError("{} is not a SNePS semantic type".format(super))
				except AttributeError:
					raise AssertionError("{} is not a SNePS semantic type".format(super))
		exec("""class {}({}):\n \"\"\"{}\"\"\"""".format(newtype, str(supers)[1:-1], docstring))

	def defineSlot(self, name, type="Entity", docstring="", pos_adj="reduce", neg_adj="expand",
					min=1, max=None, path=None):
		"""Defines a slot"""
		assert type == "Entity" or type in Entity.__subclasses__()
		assert isinstance(docstring, str)
		assert pos_adj in self._adjustments
		assert neg_adj in self._adjustments
		assert isinstance(min, int)
		assert isinstance(max, int) or max is None

		self.slots[name] = Slot(name, type, docstring, pos_adj, neg_adj, min, max, path)
