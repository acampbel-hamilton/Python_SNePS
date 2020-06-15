from SemanticHierarchy import *
from Context import *

class Network:
    def __init__(self):
        self.nodes = {}
        self.caseframes = {}
		self.slots = {} # AKA Relations
        self.sem_hierarchy = SemanticHierarchy()
        self.contexts = {}
        self.defaultContext = Context("_default", docstring="The default context", \
            hyps={}, ders={})

    
