# Python SNePS3 class

import inspect, re
from caseframe import CaseFrame
from contexts import Context, Context_Mixin
from SemanticTypes import Entity, Proposition, Act, Policy, Thing, Category, Action
from SyntacticTypes import Term, Atom, Base, Variable, Indefinite, Arbitrary, \
    Molecular, Param2Op, AndOr, Disjunction, Xor, Nand, Thresh, Equivalence, \
    NumericalEntailment, OrEntailment, Implication, Categorization, \
    NegationByFailure, Conjunction, Negation

class Network(Context_Mixin, SlotInference, PathInference):
    def __init__(self):
        self.terms = {} #maps term names to term objs

        #stores all arbitary (universally quantified) terms
        self.arbitraries = set()

        #stores all indifinite (existentially quantified) terms
        self.indefinites = set()

        #root of the syntatic class hierarchy
        self.syntacticTypeRoot = Term

        #root of the semantic class hierarchy
        self.semanticTypeRoot = Entity
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
        print(*[cls.__name__ for cls in self.semanticTypeRoot.__subclasses__()], sep="\n")
