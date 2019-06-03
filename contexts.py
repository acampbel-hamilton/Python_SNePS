#SNePS3 Contexts

from SyntacticTypes import Term

class Context:
    hierarchy = {} #is this necessary?

    def __init__(self, name, parents=[],
                    hyps=set(), ders=set(), kinconsistent=False):
        self.name = name
        self.parents = parents
        self.hyps = hyps
        self.ders = ders
        self.kinconsistent = kinconsistent

    def addToContext(self, molecular):
        """adds a given molecular term to the context"""
        pass

    def removeFromContext(self, mol):
        """removes the molecular term from the context"""
        pass

	def __contains__(self, term):
		"""overloads the 'in' operator for use on contexts.
		checks if the given term object asserted in the context,
		i.e. that term in in either hyps or ders"""
		assert isinstance(term, Term)
		return term in self.hyps or term in self.ders


class Context_Mixin:
	"""contains context related methods for Network"""

	def findContext(self, ctx):
        """if ctx is a context obj, returns it.
        Otherwise returns the context named ctx, or none if such DNE"""
        if isinstance(ctx, Context):
            return ctx
        return self.contexts.get(ctx)

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
