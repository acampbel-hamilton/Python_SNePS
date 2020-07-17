"""
This is the main file of the SNIP package. In here, we define the Inference class.
Authors: Ben Kallus, John Madigan, and Seamus Wiseman
"""

# =====================================
# -------------- IMPORTS --------------
# =====================================

from ..sneps.Network import *
from ..sneps.SemanticType import SemError
from ..sneps.Node import Node, ImplNode, AndOrNode
from .SNIPError import SNIPError

# =====================================
# -------------- GLOBALS --------------
# =====================================

ANDOR_SLOT_NAMES = ['and', 'or', 'nor', 'xor', 'nand', 'andorargs']
THRESH_SLOT_NAMES = ['equivalence', 'threshargs']

# =====================================
# ------------- INFERENCE -------------
# =====================================

class Inference:
    """ The Inference class is the main class of the inference module, and provides this
        functionality to SNePS.
        As it stands, SNIP has not been implemented. The few inference functions
        written so far serve as a demonstration of what inference can be performed
        with a more robust inference module in the future. """

    def __init__(self, net: Network):
        self.net = net
        self.debug = False

    def toggle_debug(self):
        """ In debug mode, SNIP prints the intermediate knowledge it uses while
            attempting to infer a proposition. """
        self.debug = not self.debug

    def _print_wft(self, wft: Node):
        print("\tI know that {}! : {}".format(wft.name, wft))

    def ask(self, wft_str: str):
        """ Checks if either (or both) a statement and the rejection of that statement
            (not(expr)) is asserted or can be derived in the current context. """
        # Positive expression
        results = self.ask_if(wft_str, complete_ask=True)
        # Negative expression
        not_results = self.ask_if_not(wft_str, complete_ask=True)

        # Combine, print, and return results
        results.update(not_results)
        print("{}!") if results == set() else print(results, "!", sep='')
        return results

    def ask_if(self, wft_str: str, complete_ask :bool=False):
        """ Checks if a positive statement is asserted or can be derived in the
            current context. """
        print("Checking if {} . . .".format(wft_str))

        # Parse the statement
        wft = wft_parser(wft_str, self.net)
        if wft is None:
            return set()

        # Ensure the stament is a proposition
        try:
            self.net.sem_hierarchy.assert_proposition(wft)
        except SemError as e:
            print(e)
            return set()

        # Checks if statement true and prints/returns results
        true = self._ask_if(wft)
        results = set()
        if true:
            results.add(wft)
        if not complete_ask:
            print("{}!") if results == set() else print(results, "!", sep='')
        return results

    def ask_if_not(self, wft_str: str, complete_ask: bool = False):
        """ Gets the rejection of the provided term (not(expr)) and checks if it
            is asserted or can be derived in the current context. """
        return self.ask_if("not({})".format(wft_str), complete_ask)

    def _ask_if(self, wft: Node, ignore=None):
        """ Checks if provided node is asserted or can be derived via one of the inference methods. """

        # Prevents recursion
        if ignore is None:
             ignore = set()
        if wft in ignore:
            return False
        ignore.add(wft)

        # Check using different inference methods (many are currently missing)
        derived = wft in self.net.current_context or \
                  self._slot_based(wft, ignore.copy()) or \
                  self._by_binary_op(wft, ignore.copy()) or \
                  self._by_nary_op(wft, ignore.copy())

        # Assert derived propositions
        if derived:
            self.net.current_context.add_derived(wft)

            # Prints intermediate knowledge in debug mode
            if self.debug:
                self._print_wft(wft)

        return derived

    def _slot_based(self, wft: Node, ignore):
        """ Slot based inference. """

        # 1. Check if not(and()) and treat as nand - incomplete function
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
        the bound is hit by the number of asserted antecedents. """

        implNodes = wft.follow_up_cable(self.net.slots['cq'])

        # Follow each consequent up cable
        for impl in implNodes:

            # Check if the binary operation wft is asserted
            if self._ask_if(impl, ignore.copy()):
                bound = impl.bound

                # Only return true if enough of the antecedents are true
                for ant in impl.antecedents():
                    if self._ask_if(ant, ignore.copy()):
                        bound -= 1
                        if bound < 1:
                            return True

        return False

    def _by_nary_op(self, wft: Node, ignore):
        """ Follows up andor and thresh arcs to a minmax (nary) operator
        Returns true if the nary operator itself is asserted and
        the given wft is needed to fall between the min and max values.

        Currently a partial, poor implementation.
        """
        # For andor caseframe (also: and, or, etc.)
        andOrNodes = set()

        # Follow each andorarg up cable
        for andor_slot_name in ANDOR_SLOT_NAMES:
            andOrNodes.update(wft.follow_up_cable(self.net.slots[andor_slot_name]))

        # Check if wft node asserted and given wft is needed to fall between the min and max values
        for andOr in andOrNodes:
            if self._ask_if(andOr, ignore.copy()) and andOr.min >= andOr.num_constituents():
                return True

        # For thresh caseframe (also: iff, etc.)
        threshNodes = set()

        # Follow each thresharg up cable
        for thresh_slot_name in THRESH_SLOT_NAMES:
            threshNodes.update(wft.follow_up_cable(self.net.slots[thresh_slot_name]))

        # Check if wft node asserted and given wft is needed to fall outside the min and max values
        for thresh in threshNodes:
            if self._ask_if(thresh, ignore.copy()) and thresh.min >= thresh.num_constituents():
                return True

        return False
