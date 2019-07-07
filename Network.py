# Python SNePS3 class

import inspect, sys, re
from Symbol import Symbol, Sym, _reduce, _expand, _none
from slots import *
from caseframe import *
from contexts import *
from SemanticTypes import *
from SyntacticTypes import *
# from SlotInference import *
from PathInference import * #add this back once the file is finished being written
from Find import *

class Network(Context_Mixin, CaseFrame_Mixin, Slot_Mixin, Find, PathInference):
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
		self._adjustments = [_reduce, _expand, _none]

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
				neg_adj=_reduce)
		self.defineSlot("member",
				docstring="Points to the Entity that is a member of some Category",
				neg_adj=_reduce)
		#equiv slot is missing a path init from initialize.cl
		self.defineSlot("equiv", docstring="All fillers are coreferential", neg_adj=_reduce)
		self.defineSlot("subclass", docstring="Subcategories of some category/ies.", neg_adj=_reduce)
		self.defineSlot("superclass", docstring="Supercategories of some category/ies.", neg_adj=_reduce)

		## Slots for Rules
		self.defineSlot("and", type="Proposition",
		 				docstring="Fillers are arguments of a conjunction",
						min=2, pos_adj=_reduce, neg_adj=_expand)
		self.defineSlot("nor", type="Proposition", docstring="Fillers are arguments of a nor")
		self.defineSlot("andorargs", type="Proposition",
						docstring="Fillers are arguments of an andor",
						min=2, pos_adj=_none, neg_adj=_none)
		self.defineSlot("threshargs", type="Proposition",
						docstring="Fillers are arguments of a thresh",
						min=2, pos_adj=_none, neg_adj=_none)
		self.defineSlot("thnor", type="Proposition", docstring="Fillers are arguments of a thnor",
						pos_adj=_reduce, neg_adj=_reduce)
		self.defineSlot("ant", type="Proposition", docstring="Antecedent for a set",
						pos_adj=_expand, neg_adj=_reduce)
		self.defineSlot("cq", type="Proposition", docstring="Consequent for a set")

		## Slots for SNeRE (currently SNeRE is not implemented)
		self.defineSlot("actions", type="Action", docstring="The actions of an act",
						max=1, pos_adj=_none, neg_adj=_none)

		#################### Default Caseframe Definitions ####################
		self.defineCaseframe("isa", "Proposition", ["member", "class"],
							docstring="[member] is a [class]")
		self.defineCaseframe("equiv", "Proposition", ["equiv"],
							docstring="[equiv] are all coreferential")
		self.defineCaseframe("and", "Proposition", ["and"],
							docstring="it is the case that [and]")
		self.defineCaseframe("nor", "Proposition", ['nor'],
							"it is not the case that [nor]")
		self.defineCaseframe("thnor", "Proposition", ["thnor"],
							"I don't know that it is the case that [thnor]")
		self.defineCaseframe("andor", "Proposition", ["andorargs"])
		self.defineCaseframe("thresh", "Proposition", ["threshargs"])
		self.defineCaseframe("if", "Proposition", ["ant", "cq"],
							"if [ant] then [cq]")
		self.defineCaseframe("ako", "Proposition", ["subclass", "superclass"],
							docstring="every [subclass] is a kind of [superclass]s")

	def listSemanticTypes(self):
		"""Prints all semantic types for the user"""
		print(*sorted([cls.__name__ for cls in self.semanticRoot.__subclasses__()] +
		 			[self.semanticRoot.__name__]), sep='\n')

	def findSemanticType(self, typeName):
		"""Returns the semantic object for the type name"""
		for type in (list(self.subtypes(self.semanticRoot)) + [self.semanticRoot]):
			if typeName == type.__name__:
				return type
		return object

	def assertedMembers(self, terms, ctx):
		"""returns all and only the asserted members of the given set of terms"""
		assert isinstance(terms, set), 'The given terms must be a set object'
		assert all(map((lambda t: isinstance(t, self.syntaticRoot)), terms)),\
				"Every term in the given set must be an instantiation of a term object"
		assert isinstance(ctx, Context), "the given context is a context"

		return list(filter((lambda t: t in ctx), terms))

	def supertypes(self, type):
		"""returns the list of all supertypes of the given type"""
		return type.mro()[:-1]

	def subtypes(self, type):
		"""returns the list of all subtypes of the given type"""
		return (set(type.__subclasses__()).union(
						[s for c in type.__subclasses__() for s in self.subtypes(c)]))

	#currently requires self.initialize to be called (this decision should be revisited)
	def defineContext(self, name, docstring="", parents=None, hyps=None):
		"""allows a user defined contexts within a context hierarchy rooted at self.contextRoot"""
		if parents is None:
			parents = set([self.contextRoot.name])
		if hyps is None:
			hyps = set()
		assert isinstance(name, str)
		assert Sym(name) not in self.contexts.keys(), "A context {} already exists".format(name)
		assert isinstance(docstring, str)
		assert isinstance(parents, set)
		#parents is a set of strings denoting the names of contexts
		assert all(map((lambda c: c in self.contexts.keys()), parents)),\
				"A proposed parent is not a context"
		assert isinstance(hyps, set)
		#hyps is a set of strings denoting the names of terms
		assert all(map((lambda t: t in self.terms.keys()), hyps)),\
				"A proposed hypothesis does not exist"

		self.contexts[Sym(name)] = Context(Sym(name), docstring=docstring,
								parents=set(map((lambda n: self.contexts[n]), parents)),
								hyps=set(map((lambda t: self.terms[t]), hyps)))
		self.contextHierachy[Sym(name)] = map(Sym, parents)
		return self.contexts[Sym(name)]

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

	def defineSlot(self, name, type="Entity", docstring="", pos_adj=_reduce, neg_adj=_expand,
					min=1, max=None, path=None):
		"""Defines a slot"""
		assert isinstance(name, str)
		assert getattr(sys.modules[__name__], type) in\
			(self.subtypes(self.semanticRoot).union(set([self.semanticRoot]))),\
			"The specified type must exist"
		assert isinstance(docstring, str)
		pos_adj, neg_adj = Sym(pos_adj), Sym(neg_adj)
		assert pos_adj is _reduce or pos_adj is _expand or pos_adj is _none,\
				"positive adjust must be \"reduce\", \"expand\", or \"none\""
		assert neg_adj is _reduce or neg_adj is _expand or neg_adj is _none,\
				"negative adjust must be \"reduce\", \"expand\", or \"none\""
		assert isinstance(min, int)
		assert isinstance(max, int) or max is None

		#insert check for duplicate slot

		self.slots[Sym(name)] = Slot(Sym(name), type, docstring, pos_adj,
										neg_adj, min, max, path)
		return self.slots[Sym(name)]

	def construct(self, caseframe, fillers, SynType=Molecular, OutOfContext=None):
		"""builds a given term and returns the term object"""
		assert isinstance(caseframe, CaseFrame), "Given caseframe must exist"
		assert isinstance(fillers, list) #fillers should be a list of lists of strings
		assert all([isinstance(s, str) for s in [i for sl in fillers for i in sl]])
		OutOfContext = [] if OutOfContext is None else OutOfContext
		for name in set([i for sl in fillers for i in sl]):
			if name not in self.terms.keys() and\
					name not in map((lambda t: t.name), OutOfContext):
				OutOfContext += [Term(name)]
		return (SynType("_", caseframe, down_cableset=dict(zip(caseframe.slots, fillers))), OutOfContext)

	def build(self, caseframe, fillers, SynType=Molecular, uassert=False):
		"""build a molecular node based on the given caseframe
		 and list of fillers"""
		assert isinstance(caseframe, CaseFrame), "Given caseframe must exist"
		assert isinstance(fillers, list) #fillers should be a list of lists of strings
		assert all([isinstance(s, str) for s in [i for sl in fillers for i in sl]])

		term, newBT = self.construct(caseframe, fillers)

		for t in newBT: #add created base terms
			self.terms[Sym(t.name)] = t
		for t in self.terms.values(): #check for identical term
			if term == t:
				raise AssertionError("Identical term {} already exists".format(t.name))
		#make appropriate changes to the network
		Molecular.counter += 1
		term.name = Sym("M{}".format(Molecular.counter))
		print(term.name)
		self.terms[term.name] = term
		caseframe.terms.add(term.name)
		for i in range(len(caseframe.slots)):
			for node in fillers[i]:
				self.terms[node].up_cableset.update({Sym(caseframe.slots[i]):
					self.terms[node].up_cableset.get(Sym(caseframe.slots[i]), [])
					+ [term.name]})
		if uassert:
			self.currentContext.hyps.add(term)
		return term

	# def primbuild(self, rfstr):
	# 	"""parses a string containing relations and fillers and validates
	# 	the result as input"""
	# 	assert isinstance(rfstr, str)
	#
	# 	rfregex = re.compile("^\s*(?P<rel>\w+)\s+\((?P<fill>(\s*\w+)+)\)")
	# 	rfdict = {}
	# 	while not rfstr == '':
	# 		m = rfregex.match(rfstr)
	# 		if m is not None:
	# 			rfdict.update({m.group('rel'):
	# 				m.group('fill').split() + rfdict.get(m.group('rel'), [])})
	# 			rfstr = rfstr[len(m.group(0)):]
	# 		else:
	# 			break
	# 	for r in rfdict.keys():
	# 		if not r in self.slots.keys():
	# 			raise AssertionError("Use of undefined slot {}".format(r))
	# 	cf = None
	# 	for c in self.caseframes.values:
	# 		if set(c.slots) == set(rfdict.keys()):
	# 			cf = c
	# 			break
	# 	if cf is None:
	# 		raise AssertionError('No caseframe with given slots <{}> is defined'
	# 				.format(str(rfdict.keys())[1:-1]))
	# 		return
	# 	return self.build(cf, [rfdict[r] for r in cf.slots])

	def casebuild(self, casename, fillers):
		"""parses a string of fillers and associates them with the appropriate
		slots from the designated caseframe"""
		assert casename in self.caseframes.keys()
		assert isinstance(fillers, str)

		fillregex = re.compile('^\s*(?:(?P<sing>\w+)|\((?P<mult>(?:\s*\w+)+)\))')
		lst = []
		while not fillers == '':
			m = fillregex.match(fillers)
			if not m:
				break
			if m.group('sing'):
				lst += [[m.group('sing')]]
			if m.group('mult'):
				lst += [m.group('mult').split()]
			fillers = fillers[len(m.group(0)):]
		if not len(self.caseframes[casename].slots) == len(lst):
			raise AssertionError("Insufficient fillers for the given caseframe {}"
				.format(casename))
		return self.build(self.caseframes[casename], lst)
