# SNePS3 Syntactics Types
#currently only a skeleton

import re

class Term:
    """root of the syntactic type class hierarchy"""
    def __init__(self):
        pass

#consider replacing the following 3 functions with a dictionary which
#traces the entirety of the inheritance hierarchy for the syntactic types
    def classStrip(self, s):
        r = re.compile('(\()?\<class\s*\'SyntacticTypes\.' + \
        '(?P<C>[A-Z][A-z]*)\'\>(,\))?')
        m = r.match(str(s))
        return m and m.group('C')

    def getParent(self):
        """returns the parent class of the given node instance"""
        return self.classStrip(self.__class__.__bases__)

    def getClass(self):
        return self.classStrip(self.__class__)

class Atom(Term):
    """Named terms containing up cablesets and no structure"""
    def __init__(self):
        pass

class Base(Atom):
    """an individual constant"""
    def __init__(self):
        pass

class Variable(Atom):
    """a variable term ranging over a restricted domain"""
    def __init__(self):
        pass

class Indefinite(Variable):
    """an indefinite object"""
    def __init__(self):
        pass

class Arbitrary(Variable):
    """an arbitaray individual"""
    def __init__(self):
        pass

class Molecular(Term):
    """a functional term with zero or more arguments
    equivalently a frame with slots and fillers"""
    def __init__(self):
        pass

class Param2Op(Molecular):
    """the andor or thresh of some proposition(s)"""
    def __init__(self):
        pass

class AndOr(Param2Op):
    """the andor of some proposition(s)"""
    def __init__(self):
        pass

class Disjunction(AndOr):
    """the disjunction of some proposition(s)"""
    def __init__(self):
        pass

class Xor(AndOr):
    """the exclusive or of some proposition(s)"""
    def __init__(self):
        pass

class Nand(AndOr):
    """the negation of the conjunction of some proposition(s)"""
    def __init(self):
        pass

class Thresh(Param2Op):
    """the thresh of some proposition(s)"""
    def __init__(self):
        pass

class Equivalence(Thresh):
    """an equivalence proposition"""
    def __init__(self):
        pass

class NumericalEntailment(Molecular):
    """a numerical entailment"""
    def __init__(self):
        pass

class OrEntailment(NumericalEntailment):
    """the consequents are implied by any antecedent"""
    def __init__(self):
        pass

class Implication(NumericalEntailment):
    """a conditional propostion"""
    def __init__(self):
        pass

class Categorization(Molecular):
    """a proposition stating that some Entities
    are instances of some Categories"""
    def __init__(self):
        pass

class NegationByFailure(Molecular):
    """the generalized thnor of some proposition(s)"""
    def __init__(self):
        pass

class Conjunction(Molecular):
    """the conjunction of some propositions"""
    def __init__(self):
        pass

class Negation(Molecular):
    """the generalized nor of some proposition(s)"""
    def __init__(self):
        pass
