from ..Network import *
from ..SemanticType import SemError
from ..Node import Node, ImplNode
from ..Error import SNError

SLOT_NAMES = ['and', 'or', 'nor', 'xor', 'nand', 'andorargs']

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
        self.ask_if(wft_str)
        self.ask_if_not(wft_str)

    def ask_if(self, wft_str: str):
        wft = wft_parser(wft_str, self.net)
        if wft is None:
            return False
        try:
            self.net.sem_hierarchy.assert_proposition(wft)
        except SemError as e:
            print(e)
        return self._ask_if(wft)

    def ask_if_not(self, wft_str: str):
        wft = wft_parser('not({})'.format(wft_str), self.net)
        if wft is None:
            return False
        return self._ask_if(wft)

    def _ask_if(self, wft: Node, ignore=None):

        # Prevents recursion
        if ignore is None:
             ignore = set()
        if wft in ignore:
            return False
        ignore.add(wft)

        if self.net.current_context.is_asserted(wft):
            return True
        elif self._slot_based(wft, ignore):
            return True
        return False

    def _slot_based(self, wft: Node, ignore):
        """ AKA Wire-Based """

        notNodes = wft.follow_up_cable(self.net.slots['nor'])
        for node in notNodes:
            if self._ask_if(node, ignore):
                return False

        implNodes = wft.follow_up_cable(self.net.slots['cq'])
        for impl in implNodes:
            # First special case, binary operations/implication
            antecedents = impl.antecedents()
            bound = impl.bound
            for ant in antecedents:
                if self._ask_if(ant, ignore):
                    bound -= 1
                    if bound < 1:
                        return True

        andOrNodes = set()
        for slot_name in SLOT_NAMES:
            andOrNodes.update(wft.follow_up_cable(self.net.slots[slot_name]))
        for andOr in andOrNodes:
            if self._ask_if(andOr, ignore):
                total_num = 0
                num_true = 0
                for constituent in andOr.constituents():
                    total_num += 1
                    if self._ask_if(constituent, ignore):
                        num_true += 1
                if andOr.min >= total_num - num_true:
                    return True
                if num_true >= andOr.max:
                    return False

        return False

        ask("if(wft1, wft1)")
