from ..Network import *
from ..SemanticType import SemError
from ..Node import Node, ImplNode
from ..Error import SNError

ANDOR_SLOT_NAMES = ['and', 'or', 'nor', 'xor', 'nand', 'andorargs']
THRESH_SLOT_NAMES = ['equivalence', 'threshargs']

class SNIPSError(SNError):
    pass

"""
This is the main file of the SNIPS package. In here, we define the Inference class.
Authors: Ben Kallus, John Madigan, and Seamus Wiseman
"""

class Inference:
    def __init__(self, net: Network):
        self.net = net

    def ask(self, wft_str: str):
        truth_value = self.ask_if(wft_str)
        self.ask_if_not(wft_str)
        return truth_value

    def ask_if(self, wft_str: str):
        print("Checking if {} . . .".format(wft_str), end='\n\t')

        wft = wft_parser(wft_str, self.net)
        if wft is None:
            return False
        try:
            self.net.sem_hierarchy.assert_proposition(wft)
        except SemError as e:
            print(e)

        truth_value = self._ask_if(wft)
        if truth_value:
            print("I know that {}".format(wft))
        else:
            print("Unknown")
        return truth_value

    def ask_if_not(self, wft_str: str):
        print("Checking if not({}) . . .".format(wft_str), end='\n\t')

        wft = wft_parser('not({})'.format(wft_str), self.net)
        if wft is None:
            print(False)
            return False

        truth_value = self._ask_if(wft)
        if truth_value:
            print("I know that {}".format(wft))
        else:
            print("Unknown")
        return truth_value

    def _ask_if(self, wft: Node, ignore=None):

        # Prevents recursion
        if ignore is None:
             ignore = set()
        if wft in ignore:
            return False
        ignore.add(wft)

        # Check using different inference methods
        if self.net.current_context.is_asserted(wft):
            return True
        elif self._slot_based(wft, ignore.copy()):
            return True
        elif self._by_binary_op(wft, ignore.copy()):
            return True
        elif self._by_nary_op(wft, ignore.copy()):
            return True
        return False

    def _slot_based(self, wft: Node, ignore):
        """ AKA Wire-Based """
        return False

    def _by_binary_op(self, wft: Node, ignore):
        """ Follows up cq arc to a binary operator
        Returns true if the binary operator itself is asserted and
        the bound is hit by the number of true antecedents """

        implNodes = wft.follow_up_cable(self.net.slots['cq'])
        for impl in implNodes:
            if self._ask_if(impl, ignore.copy()):
                antecedents = impl.antecedents()
                bound = impl.bound
                for ant in antecedents:
                    if self._ask_if(ant, ignore.copy()):
                        bound -= 1
                        if bound < 1:
                            self.net.current_context.add_derived(wft)
                            return True
        return False

    def _by_nary_op(self, wft: Node, ignore):
        """ Follows up andor and thresh arcs to a minmax (nary) operator
        Returns true if the nary operator itself is asserted and
        the wft is needed to fall between the min and max values """

        andOrNodes = set()
        for andor_slot_name in ANDOR_SLOT_NAMES:
            andOrNodes.update(wft.follow_up_cable(self.net.slots[andor_slot_name]))
        for andOr in andOrNodes:
            if self._ask_if(andOr, ignore.copy()) and andOr.min >= andOr.num_constituents():
                self.net.current_context.add_derived(wft)
                return True

        threshNodes = set()
        for thresh_slot_name in THRESH_SLOT_NAMES:
            threshNodes.update(wft.follow_up_cable(self.net.slots[thresh_slot_name]))
        for thresh in threshNodes:
            if self._ask_if(thresh, ignore.copy()) and thresh.min >= thresh.num_constituents():
                self.net.current_context.add_derived(wft)
                return True

        return False
