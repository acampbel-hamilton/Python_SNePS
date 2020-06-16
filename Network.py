from SemanticType import *
from Context import *
import Node

class Network:
    def __init__(self):
        self.nodes = {}
        self.caseframes = {}
        self.slots = {} # AKA Relations
        self.sem_hierarchy = SemanticHierarchy()
        self.contexts = {}
        self.default_context = Context("_default", docstring="The default context", hyps={}, ders={})

    def define_type(self, name, parent_names=[]):
        # Adds term to hierarchy
        self.sem_hierarchy.add_type(name, parent_names)

    def define_term(self, name, docstring="", sem_type_name="Entity"):
        # Creates base atomic node

        if name in self.nodes:
            # Respecification
            node = self.nodes[name]
            current_type = node.sem_type
            new_type = self.sem_hierarchy[sem_type_name]
            node.sem_type = self.sem_hierarchy.respecify(name, current_type, new_type)
        else:
            # Creation
            sem_type = self.sem_hierarchy.get_type(sem_type_name)
            self.nodes[name] = Node.Base(name, sem_type, docstring)

    def all_terms(self):
        for term in self.nodes:
            print(term)

    def show_types(self):
        print(self.sem_hierarchy)

    def define_caseframe():
        pass

    def define_context():
        pass

    def define_slot():
        pass
