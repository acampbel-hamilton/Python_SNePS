#SNePS3 Contexts

from SyntacticTypes import Term

class Context:
	def __init__(self, name, parents=None, docstring="",
					hyps=set(), ders=set(), kinconsistent=False):
		self.name = Sym(name) #symbol
		self.parents = parents #list of context objects
		self.docstring = docstring #string
		self.hyps = hyps #set term objects
		self.ders = ders #set of term objects
		self.kinconsistent = kinconsistent #boolean

	def __contains__(self, term):
		"""overloads the 'in' operator for use on contexts.
		checks if the given term object asserted in the context,
		i.e. that term in in either hyps or ders"""
		assert isinstance(term, Term)
		return term in self.hyps or term in self.ders

	def __repr__(self):
		return "<Context {} id: {}>".format(self.name, hex(id(self)))

	def __str__(self):
		s = ""
		for k,v in sorted(self.__dict__.items()):
			s += "{:<16}: {:>20}\n".format(str(k), str(v))
		return s


class Context_Mixin:
	"""contains context related methods for Network"""

	def findContext(self, ctx):
		"""if ctx is a context obj, returns it.
		Otherwise returns the context named ctx, or none if such DNE"""
		if isinstance(ctx, Context):
			return ctx
		return self.contexts.get(Sym(ctx))

	def currentContext(self):
		return currentContext

	def setCurrentContext(self, ctx):
		"""if ctx is either a context obj or a context name, sets the current
		context to that context, otherwise raises a type error"""
		c = self.findContext(ctx)
		if c is None:
			raise TypeError("Given context was neither a " +
			 "context object nor a context name.")
		self.currentContext = ctx

	def listContexts(self):
		"""prints list of all context names"""
		print(*self.contexts.keys(), sep="\n")

	#this should be reviewed to ensure this has been properly understood and implemented
	def addToContext(self, mol, ctx):
		"""adds a given molecular term to the given context"""
		assert isinstance(mol, Molecular)
		assert isinstance(ctx, Context)

		ctx.hyps.add(mol)


	def removeFromContext(self, mol, ctx):
		"""removes the molecular term from the given context"""
		assert isinstance(mol, Molecular) #must be an object
		assert isinstance(ctx, Context) #must be an object

		ctx.hyps.discard(mol)
		ctx.ders.discard(mol)
