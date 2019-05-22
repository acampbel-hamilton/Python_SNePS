#Python implementation of SNePS3 version 1.0

# Nodes must:
    # have a unique identifier
    # be given a semantic class

class Node:
    """the most general form of the Node class"""
    def __init__(self, name, upCableSet=[], downCableSet=[]):
        "constructor for node class"
        self._name = name
        self._upCableSet = upCableSet
        self._downCableSet = downCableSet

    def getName(self):
        """returns the name of the node"""
        return self._name

    def getUpCableSet(self):
        """returns the upCableSet of the node"""
        return self._upCableSet

    def getDownCableSet(self):
        """returns the downCableSet of the node"""
        return self._downCableSet

    def getCableSet(self):
        """returns the entire cable set of the node """
        return self._upCableSet + self._downCableSet

class Base(Node):
    """A Base Node represents a node with no arcs amanating from it"""
    # A base node is assumed to represent some entity—individual, object, class,
    # property, etc. It is assumed that no two base nodes represent the same,
    # identical entity.

    # DOES THIS MEAN THAT BASE NODES DO NOT HAVE DOWNCABLE?
    def __init__(self, name, upCableSet=[], downCableSet=[]):
        """base node constructor"""
        Node.__init__(self, name, upCableSet, downCableSet)

    def syntacticType(self):
        """returns the syntactic type of a node"""
        return "Base"

# Molecular nodes have arc emanaing from them
class Molecular(Node):
    """A Molecular node represents a proposition and must have a downCableSet"""
    def __init__(self, name, upCableSet=[], downCableSet):
        """molecular node constructor"""
        Node.__init__(self, name, upCableSet, downCableSet)

    def syntacticType(self):
        """returns the syntactic type of a node"""
        return "Molecular"

class Variable(Node):
    """A variable node represents and arbitrary entity and may be restricted by
    quantifiers and properties"""
    def __init__(self, name, upCableSet=[], downCableSet=[]):
        """variable node constructor"""
        Node.__init__(self, name, upCableSet, downCableSet)

    def syntacticType(self):
        """returns the syntactic type of a node"""
        return "Variable"
