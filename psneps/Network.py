"""
This is the main file of the package. In here, we define the Network class.
Authors: Seamus Wiseman, John Madigan, Ben Kallus
"""

from .SemanticType import SemanticMixin
from .Context import ContextMixin
from .Slot import SlotMixin, AdjRule
from .Node import NodeMixin, Molecular, MinMaxOpNode
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
                         neg_adj='reduce')
        self.define_slot("member", "Entity", docstring="Points to the Entity that is a member of some Category.",
                         neg_adj='reduce')
        self.define_slot("equiv", "Entity", docstring="All fillers are coreferential.",
                         neg_adj='reduce', min=2, path=None)
        self.define_slot("closedvar", "Entity", docstring="Points to a variable in a closure.")
        self.define_slot("proposition", "Propositional", docstring="Points to a proposition.")

        # Rules
        self.define_slot('and', 'Proposition', docstring='Fillers are arguments of a conjuction',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('or', 'Proposition', docstring='Fillers are arguments of a disjunction',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('nor', 'Proposition', docstring='Fillers are arguments of a nor',
                         pos_adj='reduce', neg_adj='expand', min=1)
        self.define_slot('andorargs', 'Proposition', docstring='Fillers are arguments of an andor',
                         pos_adj='none', neg_adj='none', min=2)
        self.define_slot('threshargs', 'Proposition', docstring='Fillers are arguments of a thresh',
                         pos_adj='none', neg_adj='none', min=2)
        self.define_slot('thnor', 'Proposition', docstring='Fillers are arguments of a thnor',
                         pos_adj='reduce', neg_adj='reduce', min=1)
        self.define_slot('ant', 'Proposition', docstring='antecedent for a set',
                         pos_adj='expand', neg_adj='reduce', min=1)
        self.define_slot('cq', 'Proposition', docstring='consequent for a set',
                         pos_adj='reduce', neg_adj='expand', min=1)

        self.define_slot('xor', 'Proposition', docstring='exclusive or',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('nand', 'Proposition', docstring='not and',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('equivalence', 'Proposition', docstring='double implication',
                         pos_adj='reduce', neg_adj='expand', min=2)

        # SNeRE
        self.define_slot("action", "Action", docstring="The actions of an act.",
                         neg_adj='none', pos_adj='none', min=1, max=1)


        # Condition-Action Rules
        self.define_slot("condition", "Propositional", docstring="Conditions for a rule.",
            neg_adj='reduce', pos_adj='expand', min=1)
        self.define_slot("rulename", "Thing", docstring="The name of a rule.",
            neg_adj='none', pos_adj='none', min=1, max=1)
        self.define_slot("subrule", "Policy", docstring="Subrules for a rule.",
            neg_adj='reduce', pos_adj='expand', min=0)

        # Caseframes
        self.define_caseframe('Isa', 'Propositional', slot_names=["member", "class"],
                                docstring="[member] is a [class]")
        self.define_caseframe('Equiv', 'Propositional', slot_names=["equiv"],
                                docstring="[equiv] are all co-referential")
        self.define_caseframe('and', 'Propositional', slot_names=["and"],
                                docstring="it is the case that [and]")
        self.define_caseframe('or', 'Propositional', slot_names=["or"],
                                docstring="it is the case that [or]")
        self.define_caseframe('nor', 'Propositional', slot_names=["nor"],
                                docstring="it is not the case that [nor]")
        self.define_caseframe('thnor', 'Propositional', slot_names=["thnor"],
                                docstring="I don't know that it is the case that [thnor]")
        self.define_caseframe('andor', 'Propositional', slot_names=["andorargs"],
                                docstring="I don't know that it is the case that [thnor]")
        self.define_caseframe('thresh', 'Propositional', slot_names=["threshargs"],
                                docstring="I don't know that it is the case that [thnor]")
        self.define_caseframe('if', 'Propositional', slot_names=["ant", "cq"],
                                docstring="if [ant] then [cq]")
        self.define_caseframe('close', 'Propositional', slot_names=["proposition", "closedvar"],
                                docstring="[proposition] is closed over [closedvar]")
        self.define_caseframe('rule', 'Policy', slot_names=["rulename", "condition", "action", "subrule"],
                                docstring="for the rule [name] to fire, [condition] must be matched, then [action] may occur, and [subrule] may be matched.")

        self.define_caseframe('nand', 'Propositional', slot_names=['nand'],
                               docstring='it is the case that [nand]')
        self.define_caseframe('xor', 'Propositional', slot_names=['xor'],
                               docstring='it is the case that [xor]')
        self.define_caseframe('iff', 'Propositional', slot_names=['equivalence'],
                               docstring='it is the case that [doubimpl]')

        # Aliases
        self.caseframes["nor"].add_alias("not")
        self.caseframes["thnor"].add_alias("thnot")


    def assert_wft(self, wft_str, value="hyp"):
        if value != "hyp" and value != "true":
            print("ERROR: Invalid parameters on assertion. Must be either true or hyp.", file=stderr)
            return

        wft_parser(wft_str, self)

    def print_graph(self):
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
        except ModuleNotFoundError:
            print("You need to pip install networkx and matplotlib in order to draw graphs.", file=stderr)
            return

        label_dictionary = {}

        G = nx.DiGraph()
        for node in self.nodes.values():
            G.add_node(node.name)
            if isinstance(node, Molecular):
                for i in range(len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name
                    if isinstance(node, MinMaxOpNode):
                        name += " ({}, {})".format(node.min, node.max)
                    if name == "nor" and len(fillers) == 1:
                        name = "not"
                    for filler in fillers.nodes:
                        G.add_edge(node.name, filler.name)
                        label_dictionary[(node.name, filler.name)] = name

        pos = nx.circular_layout(G)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=label_dictionary, font_color='black')
        nx.draw_networkx(G, pos)
        plt.show()
