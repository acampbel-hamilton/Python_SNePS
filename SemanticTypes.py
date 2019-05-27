# SNePS3 Semantic Types
# currently a skeleton

import re

class Entity:
    """root of the semantic type hierarchy"""
    def __init__(self):
        pass

    def _classStrip(self, s):
        r = re.compile('(\()?\<class\s*\'SemanticTypes\.' + \
        '(?P<C>[A-Z][A-z]*)\'\>(,\))?')
        m = r.match(str(s))
        return m and m.group('C')

    def getParent(self):
        """returns the parent class of the given node instance"""
        return self._classStrip(self.__class__.__bases__)

    def getClass(self):
        return self._classStrip(self.__class__)

class Proposition(Entity):
    """an entity who can be believed and whose negation can be believed"""
    def __init__(self):
        pass

class Act(Entity):
    """an Entity that can be performed"""
    def __init__(self):
        pass

class Policy(Entity):
    """an Entity that relates Propositions to Acts"""
    def __init__(self):
        pass

class Thing(Entity):
    """everything not a Proposition, Act, or Policy"""
    def __init__(self):
        pass

class Category(Thing):
    """a category of entities"""
    def __init__(self):
        pass

class Action(Thing):
    """an action that can be performed on one or more argument entities"""
    def __init(self):
        pass
