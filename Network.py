from SemanticType import *
from Context import *
from Slot import *
from Caseframe import Caseframe
import Node
from WftParse import wft_parser
from sys import stderr

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

    def find_term(self, name):
        if name in self.nodes:
            return self.nodes[name]
        else:
            print("Term ''" + name + "'' not defined.", file=stderr)

    def show_types(self):
        print(self.sem_hierarchy)

    def define_caseframe(self, name, sem_type, docstring="", slot_names=[]):

        frame_slots = []

        for slot_name in slot_names:
            if slot_name not in self.slots:
                print("ERROR: The slot '{}' does not exist".format(slot_name), file=stderr)
                return
            frame_slots.append(self.slots[slot_name])

        new_caseframe = Caseframe(name, sem_type, docstring, frame_slots)

        for caseframe_name in self.caseframes:
            caseframe = self.caseframes[caseframe_name]

            if caseframe.has_alias(name):
                print("Caseframe name '{}' is already taken".format(name), file=stderr)
                return

            if new_caseframe == caseframe:
                print('Your caseframe "' + new_caseframe.name + '" is idential to "' + caseframe.name + '".', file=stderr)

                response = input('Would you like to add an alias to "' + caseframe.name + '"? (y/N)')
                if response == 'y':
                    caseframe.add_alias(name)

                response = input('Would you like to override the docstring for "'+ caseframe.name + '"? (y/N)')
                if response == 'y':
                    caseframe.docstring = docstring

                return

        self.caseframes[new_caseframe.name] = new_caseframe

    def list_caseframes(self):
        pass

    def define_context(self):
        pass

    def list_contexts(self):
        pass

    def define_slot(self, name, sem_type_str, docstring="", pos_adj=AdjRule.REDUCE,
        neg_adj=AdjRule.EXPAND, min=1, max=1, path=None):
        if name in self.slots:
            print("Slot " + name + " already defined. Nothing being changed.", file=stderr)
            return
        sem_type = self.sem_hierarchy.get_type(sem_type_str)
        if sem_type != None:
            self.slots[name] = Slot(name, sem_type, docstring, pos_adj, neg_adj, min, max, path)

    def list_slots(self):
        for slot in self.slots:
            print(self.slots[slot])

    def assert_wft(self, wft_str, value="hyp"):
        if value != "hyp" and value != "true":
            print("Invalid parameters on assertion. Must be either true or hyp.", file=stderr)
            return

        wft_parser(wft_str, self)
