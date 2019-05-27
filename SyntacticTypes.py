# SNePS3 Syntactics Types
#currently only a partial skeleton

import re

class Term:
    """root of the syntactic type class hierarchy"""
    def __init__(self, name, activation_value=0, fired=None,
     recorded_firing=None, activation_marker=None, up_cableset={}):
        self.name = name
        self.activation_value = activation_value
        self.fired = fired
        self.recorded_firing = recorded_firing
        self.activation_marker = activation_marker
        self.up_cableset = up_cableset

#consider replacing the following 3 functions with a dictionary which
#traces the entirety of the inheritance hierarchy for the syntactic types
    def _classStrip(self, s):
        r = re.compile('(\()?\<class\s*\'SyntacticTypes\.' + \
        '(?P<C>[A-Z][A-z]*)\'\>(,\))?')
        m = r.match(str(s))
        return m and m.group('C')

    def getParent(self):
        """returns the parent class of the given node instance"""
        return self._classStrip(self.__class__.__bases__)

    def getClass(self):
        return self._classStrip(self.__class__)

class Atom(Term):
    """Named terms containing up cablesets and no structure"""

class Base(Atom):
    """an individual constant"""

class Variable(Atom):
    """a variable term ranging over a restricted domain"""
    def __init__(self, restriction_set=set(), var_label=None):
        self.restriction_set = restriction_set
        self.var_label = var_label

class Indefinite(Variable):
    """an indefinite object"""
    def __init__(self, ind_counter=1, dependencies=set()):
        self.ind_counter = ind_counter
        self.dependencies = dependencies

class Arbitrary(Variable):
    """an arbitaray individual"""
    def __init__(self, arb_counter=1):
        self.arb_counter = arb_counter

class Molecular(Term):
    """a functional term with zero or more arguments
    equivalently a frame with slots and fillers"""
    wftcounter = 0
    def __init__(self, caseframe, down_cableset, down_weights):
        self.caseframe = caseframe
        self.down_cableset = down_cableset
        self.down_weights = down_weights

class Param2Op(Molecular):
    """the andor or thresh of some proposition(s)"""
    def __init__(self, min, max):
        self.min = min
        self.max = max

class AndOr(Param2Op):
    """the andor of some proposition(s)"""

class Disjunction(AndOr):
    """the disjunction of some proposition(s)"""

class Xor(AndOr):
    """the exclusive or of some proposition(s)"""

class Nand(AndOr):
    """the negation of the conjunction of some proposition(s)"""


class Thresh(Param2Op):
    """the thresh of some proposition(s)"""


class Equivalence(Thresh):
    """an equivalence proposition"""


class NumericalEntailment(Molecular):
    """a numerical entailment"""
    def __init__(self, min):
        self.min = min

class OrEntailment(NumericalEntailment):
    """the consequents are implied by any antecedent"""


class Implication(NumericalEntailment):
    """a conditional propostion"""


class Categorization(Molecular):
    """a proposition stating that some Entities
    are instances of some Categories"""


class NegationByFailure(Molecular):
    """the generalized thnor of some proposition(s)"""


class Conjunction(Molecular):
    """the conjunction of some propositions"""


class Negation(Molecular):
    """the generalized nor of some proposition(s)"""
