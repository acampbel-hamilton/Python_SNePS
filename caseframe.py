#SNePS3 caseframe

#the folowing is a link to historic SNePS caseframes:
#https://cse.buffalo.edu/sneps/Manuals/dictionary.pdf

import inspect

class CaseFrame:
    def __init__(self, type, slots=[], adj_to=set(), adj_from=set(), terms=set()):
        self.type = type #must be either obj or class itself
        self.slots = slots
        self.adj_to = adj_to
        self.adj_from = adj_from
        self.terms = terms

    def __eq__(self, other):
        """Returns true if both arguments are equivalent caseframes.
            Two caseframes are equivalent when:
                1. They have the same type
                2. They have the same slots (disregarding order)"""
        return self.type is other.type and self.slots == other.slots
