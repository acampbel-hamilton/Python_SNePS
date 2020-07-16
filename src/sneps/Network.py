"""
This is the main file of the SNePS module. In here, we define the Network class.
Authors: Ben Kallus, John Madigan, and Seamus Wiseman
"""

from .Visualization import VisualizationMixin
from .SemanticType import SemanticMixin
from .Context import ContextMixin
from .Slot import SlotMixin, AdjRule
from .Node import NodeMixin
from .Path import PathMixin
from .Caseframe import CaseframeMixin
from .wft.WftParse import wft_parser

# =====================================
# -------------- NETWORK --------------
# =====================================

class Network(SlotMixin, CaseframeMixin, SemanticMixin, NodeMixin, ContextMixin, VisualizationMixin, PathMixin):
    def __init__(self) -> None:
        for cls in type(self).__bases__:
            cls.__init__(self)

        # THE FOLLOWING INSTANCE VARIABLES ARE DEFINED IN MIXINS
        # self.nodes = {} (defined in Node.py)
        # self.caseframes = {} (defined in Caseframe.py)
        # self.slots = {} (defined in Slot.py)
        # self.sem_hierarchy = SemanticHierarchy() (defined in SemanticType.py)
        # self.contexts = {} (defined in Context.py)
        # self.default_context = Context(docstring="The default context") (defined in Context.py,_default",
        # self.default_context = self.default_context
        self._build_default()

    def _build_default(self) -> None:
        """ Builds the default context """

        # Types
        # =====

        # Entities
        self.define_type('Act')
        self.define_type('Propositional')
        self.define_type('Thing')
        self.define_type('Policy')

        # Propositional
        self.define_type('Proposition', ['Propositional'])
        self.define_type('WhQuestion', ['Propositional'])

        # Things
        self.define_type('Category', ['Thing'])
        self.define_type('Action', ['Thing'])

        # Slots
        # =====

        # Propositions
        self.define_slot('class', 'Category', neg_adj='reduce')
        self.define_slot('member', 'Entity', neg_adj='reduce')
        self.define_slot('equiv', 'Entity', neg_adj='reduce', min=2, path='compose(!, equiv, kstar(compose(equiv-, !, equiv)))')
        self.define_slot('closedvar', 'Entity')
        self.define_slot('proposition', 'Propositional')

        # AndOr Rules
        self.define_slot('and', 'Proposition', pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('or', 'Proposition', pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('nor', 'Proposition', pos_adj='reduce', neg_adj='expand', min=1)
        self.define_slot('xor', 'Proposition', pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('nand', 'Proposition', pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('andorargs', 'Proposition', pos_adj='none', neg_adj='none', min=2)

        # Thresh Rules
        self.define_slot('equivalence', 'Proposition', pos_adj='reduce', neg_adj='expand', min=2)
        # self.define_slot('thnor', 'Proposition', pos_adj='reduce', neg_adj='reduce', min=1)
        self.define_slot('threshargs', 'Proposition', pos_adj='none', neg_adj='none', min=2)

        # Impl rules
        self.define_slot('ant', 'Proposition', pos_adj='expand', neg_adj='reduce', min=1)
        self.define_slot('cq', 'Proposition', pos_adj='reduce', neg_adj='expand', min=1)

        # SNeRE
        self.define_slot('action', 'Action', neg_adj='none', pos_adj='none', min=1, max=1)

        # Condition-Action Rules
        self.define_slot('condition', 'Propositional', neg_adj='reduce', pos_adj='expand', min=1)
        self.define_slot('rulename', 'Thing', neg_adj='none', pos_adj='none', min=1, max=1)
        self.define_slot('subrule', 'Policy', neg_adj='reduce', pos_adj='expand', min=0)

        # Caseframes
        # ==========

        self.define_caseframe('Isa', 'Propositional', slot_names=['member', 'class'])
        self.define_caseframe('Equiv', 'Propositional', slot_names=['equiv'])
        self.define_caseframe('and', 'Propositional', slot_names=['and'])
        self.define_caseframe('or', 'Propositional', slot_names=['or'])
        self.define_caseframe('nor', 'Propositional', slot_names=['nor'])
        # self.define_caseframe('thnor', 'Propositional', slot_names=['thnor'])
        self.define_caseframe('andor', 'Propositional', slot_names=['andorargs'])
        self.define_caseframe('thresh', 'Propositional', slot_names=['threshargs'])
        self.define_caseframe('if', 'Propositional', slot_names=['ant', 'cq'])
        self.define_caseframe('close', 'Propositional', slot_names=['proposition', 'closedvar'])
        self.define_caseframe('rule', 'Policy', slot_names=['rulename', 'condition', 'action', 'subrule'])
        self.define_caseframe('nand', 'Propositional', slot_names=['nand'])
        self.define_caseframe('xor', 'Propositional', slot_names=['xor'])
        self.define_caseframe('iff', 'Propositional', slot_names=['equivalence'])

        # Aliases
        self.caseframes['nor'].add_alias('not')
        # self.caseframes['thnor'].add_alias('thnot')


    def assert_wft(self, wft_str: str, inf: bool = False) -> None:
        """ Asserts a provided. This is one of the main ways to interact with the sneps system. """
        # NOTE: Currently inf does nothing. In the future, perhaps it can be used to trigger
        # forward inference from a queue of unsolved SNIPS queries

        # Parses string and returns node
        wft = wft_parser(wft_str, self)

        # Adds wft as asserted hypothesis in current context
        if wft is not None:
            print(wft.name + "! :", wft)
            self.current_context.add_hypothesis(wft)
