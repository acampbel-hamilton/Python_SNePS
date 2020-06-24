"""
This is the main file of the package. In here, we define the Network class.
Authors: Seamus Wiseman, John Madigan, Ben Kallus
"""

from .SemanticType import SemanticMixin
from .Context import ContextMixin
from .Slot import SlotMixin, AdjRule
from .Node import NodeMixin
from .Caseframe import CaseframeMixin
from .WftParse import wft_parser
from sys import stderr

class Network(SlotMixin, CaseframeMixin, SemanticMixin, NodeMixin, ContextMixin):
    def __init__(self):
        for cls in type(self).__bases__:
            cls.__init__(self)

        # self.nodes = {} (defined in Node.py)
        # self.caseframes = {} (defined in Caseframe.py)
        # self.slots = {} (defined in Slot.py)
        # self.sem_hierarchy = SemanticHierarchy() (defined in SemanticType.py)
        # self.contexts = {} (defined in Context.py)
        # self.default_context = Context(docstring="The default context", hyps={}, ders={}) (defined in Context.py,_default",
        self._build_default()

    def _build_default(self):
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

        # Slots
        # =====

        # Propositions
        self.define_slot("class", "Category", docstring="Points to a Category that some Entity is a member of.",
                         neg_adj=AdjRule.REDUCE)
        self.define_slot("member", "Entity", docstring="Points to the Entity that is a member of some Category.",
                         neg_adj=AdjRule.REDUCE)
        self.define_slot("equiv", "Entity", docstring="All fillers are coreferential.",
                         neg_adj=AdjRule.REDUCE, min=2, path=None)
        self.define_slot("closedvar", "Entity", docstring="Points to a variable in a closure.")
        self.define_slot("proposition", "Propositional", docstring="Points to a proposition.")

        # Rules
        self.define_slot('and', 'Proposition', docstring='Fillers are arguments of a conjuction',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=2)
        self.define_slot('or', 'Proposition', docstring='Fillers are arguments of a disjunction',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=2)
        self.define_slot('nor', 'Proposition', docstring='Fillers are arguments of a nor',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=1)
        self.define_slot('andorargs', 'Proposition', docstring='Fillers are arguments of an andor',
                         pos_adj=AdjRule.NONE, neg_adj=AdjRule.NONE, min=2)
        self.define_slot('threshargs', 'Proposition', docstring='Fillers are arguments of a thresh',
                         pos_adj=AdjRule.NONE, neg_adj=AdjRule.NONE, min=2)
        self.define_slot('thnor', 'Proposition', docstring='Fillers are arguments of a thnor',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.REDUCE, min=1)
        self.define_slot('ant', 'Proposition', docstring='antecedent for a set',
                         pos_adj=AdjRule.EXPAND, neg_adj=AdjRule.REDUCE, min=1)
        self.define_slot('cq', 'Proposition', docstring='consequent for a set',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=1)

        self.define_slot('xor', 'Proposition', docstring='exclusive or',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=2)
        self.define_slot('nand', 'Proposition', docstring='not and',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=2)
        self.define_slot('iff', 'Proposition', docstring='double implication',
                         pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=2)

        # SNeRE
        self.define_slot("action", "Action", docstring="The actions of an act.",
                         neg_adj=AdjRule.NONE, pos_adj=AdjRule.NONE, min=1, max=1)


        # Condition-Action Rules
        self.define_slot("condition", "Propositional", docstring="Conditions for a rule.",
            neg_adj=AdjRule.REDUCE, pos_adj=AdjRule.EXPAND, min=1)
        self.define_slot("rulename", "Thing", docstring="The name of a rule.",
            neg_adj=AdjRule.NONE, pos_adj=AdjRule.NONE, min=1, max=1)
        self.define_slot("subrule", "Policy", docstring="Subrules for a rule.",
            neg_adj=AdjRule.REDUCE, pos_adj=AdjRule.EXPAND, min=0)

        # Caseframes
        self.define_caseframe('Isa', 'Propositional', docstring="[member] is a [class]",
                              slot_names=["member", "class"])
        self.define_caseframe('Equiv', 'Propositional', docstring="[equiv] are all co-referential",
                              slot_names=["equiv"])
        self.define_caseframe('and', 'Propositional', docstring="it is the case that [and]",
                              slot_names=["and"])
        self.define_caseframe('or', 'Propositional', docstring="it is the case that [or]",
                              slot_names=["or"])
        self.define_caseframe('nor', 'Propositional', docstring="it is not the case that [nor]",
                              slot_names=["nor"])
        self.define_caseframe('thnor', 'Propositional', docstring="I don't know that it is the case that [thnor]",
                              slot_names=["thnor"])
        self.define_caseframe('andor', 'Propositional',
                              slot_names=["andorargs"])
        self.define_caseframe('thresh', 'Propositional',
                              slot_names=["threshargs"])
        self.define_caseframe('if', 'Propositional', docstring="if [ant] then [cq]",
                              slot_names=["ant", "cq"])
        self.define_caseframe('close', 'Propositional', docstring="[proposition] is closed over [closedvar]",
                              slot_names=["proposition", "closedvar"])
        self.define_caseframe('rule', 'Policy', docstring="for the rule [name] to fire, [condition] must be matched, then [action] may occur, and [subrule] may be matched.",
                              slot_names=["rulename", "condition", "action", "subrule"])

        self.define_caseframe('nand', 'Propositional', docstring='it is the case that [nand]',
                               slot_names=['nand'])
        self.define_caseframe('xor', 'Propositional', docstring='it is the case that [xor]',
                               slot_names=['xor'])
        self.define_caseframe('iff', 'Propositional', docstring='it is the case that [doubimpl]',
                               slot_names=['iff'])

        # Aliases
        self.caseframes["nor"].add_alias("not")
        self.caseframes["thnor"].add_alias("thnot")


    def assert_wft(self, wft_str, value="hyp"):
        if value != "hyp" and value != "true":
            print("ERROR: Invalid parameters on assertion. Must be either true or hyp.", file=stderr)
            return

        wft_parser(wft_str, self)

    def print_graph(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()
        for node in self.nodes.values():
            G.add_node(node.name)
            if node.molecular():
                for i in range(0, len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name
                    for filler in fillers.nodes:
                        G.add_edge(node.name, filler.name)
                        # Add edge label

        nx.draw_networkx(G)
        plt.show()
