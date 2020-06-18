class Context:
    def __init__(self, name, docstring="", parent=None, hyps={}, ders={}):
        self.name = name
        self.parent = parent
        self.docstring = docstring
        self.hyps = {} # Hypothetical beliefs
        self.ders = {} # Derived beliefs

    def __contains__(self, term):
        """ overloads the 'in' operator for use on contexts.
        checks if the given term object is asserted in the context,
        i.e. that term in in either hyps or ders """
        return term in self.hyps or term in self.ders

    def __repr__(self):
        return "<Context {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self):
        s = ""
        for k,v in sorted(self.__dict__.items()):
            s += "{:<16}: {:>20}\n".format(str(k), str(v))
        return s

    def __eq__(self, other):
        return self.name == other.name

class ContextMixIn:
    """ Provides functions related to contexts to network """

    def __init__(self):
        if type(self) == ContextMixIn:
            raise NotImplementedError

        self.contexts = {}
        self.default_context = Context("_default", docstring="The default context", hyps={}, ders={})

    def define_context(self, name, docstring="", parent="_default", hyps={}, ders={}):
        new_context = Context(name, docstring, parent, hyps, ders)

        if self == new_context:
            print("You cannot define contexts with the same name.", file=stderr)
            return

        self.contexts[new_context.name] = new_context


    def list_contexts(self):
        """ Prints out all the contexts in the network """
        for context_name in self.contexts:
            print(self.contexts[context_name])

    def build_default(self):
        Context("_default", docstring="The default context", hyps={}, ders={})
