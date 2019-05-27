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
