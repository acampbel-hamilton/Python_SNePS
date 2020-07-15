from ..sneps.Network import *
from ..sneps.SemanticType import SemError
from ..sneps.Node import Node, ImplNode, AndOrNode
from .SNIPSError import SNIPSError

ANDOR_SLOT_NAMES = ['and', 'or', 'nor', 'xor', 'nand', 'andorargs']
THRESH_SLOT_NAMES = ['equivalence', 'threshargs']

"""
This is the main file of the SNIPS package. In here, we define the Inference class.
Authors: Ben Kallus, John Madigan, and Seamus Wiseman
"""

class Inference:
    def __init__(self, net: Network):
        self.net = net
        self.debug = False

    def toggle_debug(self):
        self.debug = not self.debug

    def _print_wft(self, wft: Node):
        print("\tI know that {}! : {}".format(wft.name, wft))

    def ask(self, wft_str: str):
        results = self.ask_if(wft_str, complete_ask=True)
        not_results = self.ask_if_not(wft_str, complete_ask=True)
        results.update(not_results)
        print("{}!") if results == set() else print(results, "!", sep='')
        return results

    def ask_if(self, wft_str: str, complete_ask :bool=False):
        print("Checking if {} . . .".format(wft_str))

        wft = wft_parser(wft_str, self.net)
        if wft is None:
            return set()
        try:
            self.net.sem_hierarchy.assert_proposition(wft)
        except SemError as e:
            print(e)
            return set()

        true = self._ask_if(wft)

        results = set()
        if true:
            results.add(wft)
        if not complete_ask:
            print("{}!") if results == set() else print(results, "!", sep='')
        return results

    def ask_if_not(self, wft_str: str, complete_ask: bool = False):
        return self.ask_if("not({})".format(wft_str), complete_ask)

    def _ask_if(self, wft: Node, ignore=None):
        # Prevents recursion
        if ignore is None:
             ignore = set()
        if wft in ignore:
            return False
        ignore.add(wft)

        # Check using different inference methods
        derived = self.net.current_context.is_asserted(wft) or \
                  self._slot_based(wft, ignore.copy()) or \
                  self._by_binary_op(wft, ignore.copy()) or \
                  self._by_nary_op(wft, ignore.copy())

        if derived:
            self.net.current_context.add_derived(wft)
            if self.debug:
                self._print_wft(wft)
        return derived

    def _slot_based(self, wft: Node, ignore):
        """ AKA Wire-Based """

        # 1. Check if not(and()) and treat as nand
        if isinstance(wft, AndOrNode) and wft.frame.caseframe is self.net.caseframes['nor']:
            notNodes = wft.follow_down_cable(self.net.slots['nor'])
            for notNode in notNodes:
                if isinstance(notNode, AndOrNode) and \
                   (notNode.frame.caseframe is self.net.caseframes['and'] or \
                   notNode.frame.caseframe is self.net.caseframes['andor'] and \
                   notNode.min == notNode.num_constituents() and \
                   notNode.max == notNode.num_constituents()):

                        # TODO - evaluate and as nand . . .
                        pass

        return False

    def _by_binary_op(self, wft: Node, ignore):
        """ Follows up cq arc to a binary operator
        Returns true if the binary operator itself is asserted and
        the bound is hit by the number of true antecedents """

        implNodes = wft.follow_up_cable(self.net.slots['cq'])
        for impl in implNodes:
            if self._ask_if(impl, ignore.copy()):
                bound = impl.bound
                for ant in impl.antecedents():
                    if self._ask_if(ant, ignore.copy()):
                        bound -= 1
                        if bound < 1:
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
                return True

        threshNodes = set()
        for thresh_slot_name in THRESH_SLOT_NAMES:
            threshNodes.update(wft.follow_up_cable(self.net.slots[thresh_slot_name]))
        for thresh in threshNodes:
            if self._ask_if(thresh, ignore.copy()) and thresh.min >= thresh.num_constituents():
                return True

        return False
