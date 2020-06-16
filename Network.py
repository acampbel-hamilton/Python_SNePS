from SemanticType import *
from Context import *
import Node
import wft

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
        [print(term) for term in self.nodes]

    def show_types(self):
        print(self.sem_hierarchy)

    def define_caseframe(self):
        pass

    def define_context(self):
        pass

    def define_slot(self):
        pass

    def assertWft(wft, value="hyp"):
        if value != "hyp" and value != "true":
            print("Invalid parameters on assertion. Must be either true or hyp.")
            return
