from .SNError import SNError
from re import match

# =====================================
# -------------- GLOBALS --------------
# =====================================

class ContextError(SNError):
    pass

# =====================================
# -------------- CONTEXT --------------
# =====================================

class Context:
    def __init__(self, name: str, docstring="", parent=None) -> None:
        self.name = name
        self.parent = parent # Another context object
        self.docstring = docstring
        self.hyps = set() # Hypothetical beliefs
        self.ders = set() # Derived beliefs

    def __contains__(self, term: str) -> bool:
        """ Overloads the 'in' operator for use on contexts.
            Checks if the given term object is asserted in the context,
            i.e. that term in in either hyps or ders """
        return term in self.hyps or term in self.ders

    def __repr__(self) -> str:
        return "<Context {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self) -> str:
        return "<{}>:\n\tparent : {}\n\tdocstring : {}\n\thyps : [{}]\n\tders : [{}]\n\t".format(
            self.name, self.parent.name if self.parent is not None else '', self.docstring,
            ", ".join([hyp.name for hyp in self.hyps]), ", ".join([der.name for der in self.ders]))

    def add_hypothesis(self, node):
        self.hyps.add(node)

    def add_derived(self, node):
        self.ders.add(node)

    def all_asserted(self):
        return self.hyps | self.ders

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __hash__(self):
        return id(self) # Contexts are unique

# =====================================
# --------------- MIXIN ---------------
# =====================================

class ContextMixin:
    """ Provides functions related to contexts to network. """

    def __init__(self) -> None:
        if type(self) is ContextMixin:
            raise NotImplementedError("Mixins can't be instantiated.")

        self.contexts = {}
        self.default_context = Context("default", docstring="The default context")
        self.current_context = self.default_context
        self.contexts[self.current_context.name] = self.current_context

    def define_context(self, name: str, docstring: str = "", parent: str = "default") -> None:
        """ Defines a new context. """

        if self.enforce_name_syntax and not match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
            raise ContextError("ERROR: The context name '{}' is not allowed".format(name))

        # Ensures uniqueness
        if name in self.contexts:
            raise ContextError("ERROR: Context {} already defined.".format(parent))

        # Parent must exist
        elif parent not in self.contexts:
            raise ContextError("ERROR: Parent context {} does not exist.")

        # Builds new Context object and stores in Network
        else:
            self.contexts[name] = Context(name, docstring, self.contexts[parent])

    def set_current_context(self, context_name: str) -> None:
        """ Sets the current context. """
        if context_name in self.contexts:
            self.current_context = self.contexts[context_name]
        else:
            raise ContextError("ERROR: Context \"{}\" does not exist.".format(context_name))

    def list_contexts(self) -> None:
        """ Prints out representations for all the contexts in the network """
        for context_name in self.contexts:
            print(self.contexts[context_name])
