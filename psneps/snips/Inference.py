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
        print(self.ask_if(wft_str))
        print(self.ask_if_not(wft_str))

    def ask_if(self, wft_str: str):
        print("Checking if <{}> . . .".format(wft_str), end='\n\t')

        wft = wft_parser(wft_str, self.net)
        if wft is None:
            print(False)
            return False
        try:
            self.net.sem_hierarchy.assert_proposition(wft)
        except SemError as e:
            print(e)

        truth_value = self._ask_if(wft)
        print(truth_value)
        return truth_value

    def ask_if_not(self, wft_str: str):
        print("Checking if <not({})> . . .".format(wft_str), end='\n\t')

        wft = wft_parser('not({})'.format(wft_str), self.net)
        if wft is None:
            print(False)
            return False

        truth_value = self._ask_if(wft)
        print(truth_value)
        return truth_value

    def _ask_if(self, wft: Node, ignore=None):

        # Prevents recursion
        if ignore is None:
             ignore = set()
        if wft in ignore:
            return False
        ignore.add(wft)

        if self.net.current_context.is_asserted(wft):
            return True
        elif self._slot_based(wft, ignore.copy()):
            return True
        return False

    def _slot_based(self, wft: Node, ignore):
        """ AKA Wire-Based """

        # First special case, binary operations/implication
        # Return true if a certain number of antecedents are true
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

        andOrNodes = set()
        for slot_name in SLOT_NAMES:
            andOrNodes.update(wft.follow_up_cable(self.net.slots[slot_name]))
        for andOr in andOrNodes:
            if self._ask_if(andOr, ignore.copy()):
                total_num = 0
                num_true = 0
                for constituent in andOr.constituents():
                    total_num += 1
                    if self._ask_if(constituent, ignore.copy()):
                        num_true += 1
                if andOr.min >= total_num - num_true:
                    self.net.current_context.add_derived(wft)
                    return True
                if num_true >= andOr.max:
                    return False

        return False
