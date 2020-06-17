from SemanticType import Semantic_Mixin
from Context import Context_Mixin
from Slot import Slot_Mixin
from Node import Node_Mixin
from Caseframe import Caseframe_Mixin
from WftParse import wft_parser
from sys import stderr

class Network(Slot_Mixin, Caseframe_Mixin, Semantic_Mixin, Node_Mixin, Context_Mixin):
    def __init__(self):
        self.nodes = {}
        self.caseframes = {}
        self.slots = {} # AKA Relations
        self.sem_hierarchy = new_hierarchy()
        self.contexts = {}
        self.default_context = build_default()

    def assert_wft(self, wft_str, value="hyp"):
        if value != "hyp" and value != "true":
            print("Invalid parameters on assertion. Must be either true or hyp.", file=stderr)
            return

        wft_parser(wft_str, self)
