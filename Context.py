class Context:
    def __init__(self, name, docstring="", parent=None, hyps={}, ders={}):
        self.name = name
        self.parent = parent
        self.docstring = docstring
        self.hyps = {} # Hypothetical beliefs
        self.ders = {} # Derived beliefs

    def __contains__(self, term):
        """ overloads the 'in' operator for use on contexts.
        checks if the given term object asserted in the context,
        i.e. that term in in either hyps or ders """
        return term in self.hyps or term in self.ders

    def __repr__(self):
        return "<Context {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self):
        s = ""
        for k,v in sorted(self.__dict__.items()):
            s += "{:<16}: {:>20}\n".format(str(k), str(v))
        return s
