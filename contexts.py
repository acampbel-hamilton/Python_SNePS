#SNePS3 Contexts

class Context:
    hierarchy = {}

    def __init__(self, name, parents=[],
                    hyps=set(), ders=set(), kinconsistent=False):
        self.name = name
        self.parents = parents
        self.hyps = hyps
        self.ders = ders
        self.kinconsistent = kinconsistent

    def addToContext(self, molecular):
        """adds a given molecular term to the context"""
        pass

    def removeFromContext(self, mol):
        """removes the molecular term from the context"""
        pass
