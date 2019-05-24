#SNePS3 caseframe

#the folowing is a link to historic SNePS caseframes:
#https://cse.buffalo.edu/sneps/Manuals/dictionary.pdf

class CaseFrame:
    def __init__(self, type, slots=[], adj_to=set(), adj_from=set(), terms=set()):
        self.type = type
        self.slots = slots
        self.adj_to = adj_to
        self.adj_from = adj_from
        self.terms = terms
