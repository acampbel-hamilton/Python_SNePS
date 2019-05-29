# Python SNePS3 class

import inspect, re
from caseframe import CaseFrame
from contexts import Context
from SemanticTypes import *
from SyntacticTypes import *

class SNePS:
    def __init__(self):
        self.terms = {} #maps term names to term objs

        #stores all arbitary (universally quantified) terms
        self.arbitraries = set()

        #stores all indifinite (existentially quantified) terms
        self.indefinites = set()
        self.syntacticTypeRoot = Term #root of the syntatic class hierarchy
        self.semanticTypeRoot = Entity #root of the semantic class hierarchy
        self.caseframes = set() #stores all caseframes
        self.slots = {} # maps slot names to slot objs
        self.contexts = {} #maps context names to context objs
        self.currentContext = None #stores the current context

        #determine whether inferences are traced
        self.goaltrace = None
        self.trace = False

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
