#SNePS3 Contexts

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


class Context_Mixin:
	"""contains context related methods for SnePS class in Network.py"""

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

	#psuedo adjustability should be added here once it is understood
    def adjustable(srcframe, tgtframe):
        """returns true if srcframe is a caseframe which is
            adjustable to the caseframe tgtframe"""
        return pos_adj(srcframe, tgtframe) or\
                neg_adj(srcframe, tgtframe)

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
