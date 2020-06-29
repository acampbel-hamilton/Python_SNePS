from .Error import SNError
from re import match

class ContextError(SNError):
    pass

class Context:
    def __init__(self, name: str, docstring="", parent=None) -> None:
        self.name = name
        self.parent = parent # Another context object
        self.docstring = docstring
        self.hyps = {} # Hypothetical beliefs
        self.ders = {} # Derived beliefs

    def __contains__(self, term: str) -> bool:
        """ Overloads the 'in' operator for use on contexts.
        checks if the given term object is asserted in the context,
        i.e. that term in in either hyps or ders """
        return term in self.hyps or term in self.ders

    def __repr__(self) -> str:
        return "<Context {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self) -> str:
        s = ""
        for k,v in sorted(self.__dict__.items()):
            s += "{:<16}: {:>20}\n".format(str(k), str(v))
        return s

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def add_hypothesis(self, node):
        self.hyps[node.name] = node

    def is_asserted(self, node):
        return node.name in self.hyps or node.name in self.ders

class ContextMixin:
    """ Provides functions related to contexts to network. """

    def __init__(self) -> None:
        if type(self) is ContextMixin:
            raise NotImplementedError("Mixins can't be instantiated.")

        self.contexts = {}
        self.default_context = Context("_default", docstring="The default context")
        self.current_context = self.default_context

    def define_context(self, name: str, docstring="", parent="_default") -> None:
        if self.enforce_name_syntax and not match(r'^[A-Za-z_][A-Za-z0-9_]*$', name):
            raise ContextError("ERROR: The context name '{}' is not allowed".format(name))

        if name in self.contexts:
            raise ContextError("ERROR: You cannot define contexts with the same name.")
        else:
            self.contexts[name] = Context(name, docstring, self.contexts[parent], hyps, ders)

    def list_contexts(self) -> None:
        """ Prints out all the contexts in the network """
        for context_name in self.contexts:
            print(self.contexts[context_name])
