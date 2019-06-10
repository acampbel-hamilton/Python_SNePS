# Python SNePS3 class

import inspect, re, sys
from slots import *
from caseframe import *
from contexts import *
from SemanticTypes import *
from SyntacticTypes import *
from SlotInference import *
from PathInference import *
from Find import *

class Network(Context_Mixin, SlotInference, PathInference, CaseFrame_Mixin, Slot_Mixin, Find):
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

	def __str__(self):
		"""returns a string representation of the network"""
		s = ""
		for k,v in sorted(self.__dict__.items()):
			if isinstance(v, dict):
				s += "\n{:<}:\n".format(str(k))
				for p,q in v.items():
					s += "\t{:<16}: {:>40}\n".format(str(p), repr(q))
			elif isinstance(v, list) or isinstance(v, set):
				s += "\n{:<}:\n".format(str(k))
				for i in v:
					s += "\t{:>24}\n".format(str(i))
			else:
				s += "\n{:<16}: {:>40}\n".format(str(k), repr(v))
		return s

	def initialize(self):
		"""this function will set up the default state for a SNePS object once
		implemented, including default contexts, slots, and caseframes."""
#################### Default Context Definitions ####################
		#declares BaseCT (base context) as the root of the context hierarchy and properly stores it
		self.contextRoot = Context("BaseCT", parents=None, docstring="The root of all contexts")
		self.contextHierachy[self.contextRoot.name] = self.contextRoot.parents
		self.contexts[self.contextRoot.name] = self.contextRoot

		DefaultCT = self.defineContext("DefaultCT", docstring="The default current context")
		self.currentContext = DefaultCT
#################### Default Slot Definitions ####################
	## Slots for built in propositions
		self.defineSlot("class", type="Category",
				docstring="Points to a Category that some Entity is a member of.",
				neg_adj="reduce")
		self.defineSlot("member",
				docstring="Points to the Entity that is a member of some Category",
				neg_adj="reduce")
		#equiv slot is missing a path init from initialize.cl
		self.defineSlot("equiv", docstring="All fillers are coreferential", neg_adj="reduce")

	## Slots for Rules
		self.defineSlot("and", type="Proposition",
		 				docstring="Fillers are arguments of a conjunction",
						min=2, pos_adj="reduce", neg_adj="expand")
		self.defineSlot("nor", type="Proposition", docstring="Fillers are arguments of a nor")
		self.defineSlot("andorargs", type="Proposition",
						docstring="Fillers are arguments of an andor",
						min=2, pos_adj=None, neg_adj=None)
		self.defineSlot("threshargs", type="Proposition",
						docstring="Fillers are arguments of a thresh",
						min=2, pos_adj=None, neg_adj=None)
		self.defineSlot("thnor", type="Proposition", docstring="Fillers are arguments of a thnor",
						pos_adj="reduce", neg_adj="reduce")
		self.defineSlot("ant", type="Proposition", docstring="Antecedent for a set",
						pos_adj="expand", neg_adj="reduce")
		self.defineSlot("cq", type="Proposition", docstring="Consequent for a set")

	## Slots for SNeRE (currently SNeRE is not implemented)
		self.defineSlot("actions", type="Action", docstring="The actions of an act",
						max=1, pos_adj=None, neg_adj=None)

#################### Default Caseframe Definitions ####################
		# self.defineCaseframe("Isa", "Proposition", ["member", "class"])
		#implementation of defineCaseframe needs to be checked concerning print_pattern

	def listSemanticTypes(self):
		"""Prints all semantic types for the user"""
		print(*([cls.__name__ for cls in self.semanticRoot.__subclasses__()]
				.append(self.semanticRoot.type_name)), sep="\n")

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

	def supertypes(self, type):
		"""returns the list of all supertypes of the given type"""
		return type.mro()[:-1]

	def subtypes(self, type):
		"""returns the list of all subtypes of the given type"""
		return (set(type.__subclasses__()).union(
						[s for c in type.__subclasses__() for s in self.subtypes(c)]))

	#currently requires self.initialize to be called (this decision should be revisited)
	def defineContext(self, name, docstring="", parents=None, hyps=set()):
		"""allows a user defined contexts within a context hierarchy rooted at self.contextRoot"""
		if parents is None:
			parents = set([self.contextRoot.name])
		assert isinstance(name, str)
		assert name not in self.contexts.keys(), "A context {} already exists".format(name)
		assert isinstance(docstring, str)
		assert isinstance(parents, set)
		#parents is a set of strings denoting the names of contexts
		assert all(map((lambda c: c in self.contexts.keys()), parents))
		assert isinstance(hyps, set)
		#hyps is a set of strings denoting the names of terms
		assert all(map((lambda t: t in self.terms.keys()), hyps))

		self.contexts[name] = Context(name, docstring=docstring,
								parents=set(map((lambda n: self.contexts[n]), parents)),
								hyps=set(map((lambda t: self.terms[t]), hyps)))
		self.contextHierachy[name] = parents
		return self.contexts[name]

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
		assert isinstance(name, str)
		cls = getattr(sys.modules[__name__], type)
		assert cls is self.semanticRoot or cls in self.subtypes(self.semanticRoot)
		assert isinstance(docstring, str)
		assert pos_adj in self._adjustments
		assert neg_adj in self._adjustments
		assert isinstance(min, int)
		assert isinstance(max, int) or max is None

		self.slots[name] = Slot(name, type, docstring, pos_adj, neg_adj, min, max, path)
		return self.slots[name]
