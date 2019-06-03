# Python SNePS3 class

import inspect, re, sys
from caseframe import CaseFrame
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
        self.caseframes = set() #stores all caseframes
        self.slots = {} # maps slot names to slot objs
        self.contexts = {} #maps context names to context objs
        self.currentContext = None #stores the current context

        #determine whether inferences are traced
        self.goaltrace = None
        self.trace = False

    def initialize(self):
        """this function will set up the default state for a SNePS object once
        implemented, including default contexts, slots, and caseframes."""
        pass

    def listSemanticTypes(self):
		"""Prints all semantic types for the user"""
        print(*[cls.__name__ for cls in self.semanticRoot.__subclasses__()], sep="\n")

	def assertedMembers(self, terms, ctx):
		"""returns all and only the asserted members of the given set of terms"""
		assert isinstance(terms set())
		assert all(map((lambda t: isinstance(t, self.syntaticRoot)), terms))
		assert isinstance(ctx, Context)

		return filter((lambda t: t in ctx), terms)

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
		except:
			for super in supers:
				try:
					cls = getattr(sys.modules[__name__], super)
					if not isinstance(cls, self.semanticRoot):
						raise AssertionError("{} is not a SNePS semantic type".format(super))
				except:
					raise AssertionError("{} is not a SNePS semantic type".format(super))
		exec("""class {}({}):\n \"\"\"{}\"\"\"""".format(newtype, str(supers)[1:-1], docstring))
