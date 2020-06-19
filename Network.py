from .SemanticType import SemanticMixIn
from .Context import ContextMixIn
from .Slot import SlotMixIn
from .Node import NodeMixIn
from .Caseframe import CaseframeMixIn
from .WftParse import wft_parser
from sys import stderr

class Network(SlotMixIn, CaseframeMixIn, SemanticMixIn, NodeMixIn, ContextMixIn):
    def __init__(self):
        for cls in type(self).__bases__:
            cls.__init__(self)

        # self.nodes = {} (defined in Node.py)
        # self.caseframes = {} (defined in Caseframe.py)
        # self.slots = {} (defined in Slot.py)
        # self.sem_hierarchy = SemanticHierarchy() (defined in SemanticType.py)
        # self.contexts = {} (defined in Context.py)
        # self.default_context = Context("_default", docstring="The default context", hyps={}, ders={}) (defined in Context.py)
        self.build_default()

    def build_default(self):
        """ Builds the default context """

        # Types
        # =====

        # Entities
        self.define_type("Act")
        self.define_type("Propositional")
        self.define_type("Thing")
        self.define_type("Policy")

        # Propositional
        self.define_type("Proposition", ["Propositional"])
        self.define_type("WhQuestion", ["Propositional"])

        # Things
        self.define_type("Category", ["Thing"])
        self.define_type("Action", ["Thing"])

        self.define_caseframe("and", "Proposition", )


        # Slots
        # =====

        # Propositions

        # Rules
        self.define_slot('and', 'Proposition', 'Fillers are arguemnts of a conjuction',\
                            AdjRule.REDUCE, AdjRule.EXPAND, 2)

        self.define_slot('nor', 'Proposition', 'Fillers are arguemnts of a nor',\
                            AdjRule.REDUCE, AdjRule.EXPAND, 1)

        self.define_slot('andorargs', 'Proposition', 'Fillers are arguemnts of an andor',\
                            AdjRule.NONE, AdjRule.NONE, 2)
        
        self.define_slot('threshargs', 'Proposition', 'Fillers are arguemnts of a thresh',\
                            AdjRule.NONE, AdjRule.NONE, 2)

        self.define_slot('thnor', 'Proposition', 'Fillers are arguemnts of a thnor',\
                            AdjRule.REDUCE, AdjRule.REDUCE, 1)

        self.define_slot('ant', 'Proposition', 'antecedent for a set',\
                            AdjRule.EXPAND, AdjRule.REDUCE, 1)

        self.define_slot('cq', 'Proposition', 'consequent for a set',\
                            AdjRule.REDUCE, AdjRule.EXPAND, 1)

        # SNeRE
        self.define_slot("action", "Action", docstring="The actions of an act.",
            neg_adj=AdjRule.NONE, pos_adj=AdjRule.NONE, min=1, max=1)

        # Condition-Action Rules
        # self.define_slot("condition", "Propositional", docstring="Conditions for a rule.",
        #     neg_adj=AdjRule.REDUCE, pos_adj=AdjRule.EXPAND, min=1)
        # self.define_slot("rulename", "Thing", docstring="The name of a rule.",
        #     neg_adj=AdjRule.NONE, pos_adj=AdjRule.NONE, min=1, max=1)
        # self.define_slot("subrule", "Policy", docstring="Subrules for a rule.",
        #     neg_adj=AdjRule.REDUCE, pos_adj=AdjRule.EXPAND, min=0)

        # Caseframes
        # ==========

    def assert_wft(self, wft_str, value="hyp"):
        if value != "hyp" and value != "true":
            print("Invalid parameters on assertion. Must be either true or hyp.", file=stderr)
            return

        wft_parser(wft_str, self)
