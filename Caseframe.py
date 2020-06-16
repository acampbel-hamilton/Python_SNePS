from Slot import *
from SemanticType import SemanticType

class CaseFrame:
    def __init__(self, name, sem_type, docstring="", slots=[]):
        self.name = name
        self.docstring = docstring
        self.sem_type = type
        self.slots = slots

class Frame:
    def __init__(self, caseframe, filler_set=[]):
        self.caseframe = caseframe
        self.filler_set = filler_set

        if len(self.fillers) != len(self.caseframe.slots):
        raise Exception("Wrong number of fillers")

        verify_slots()

    def verify_slots(self):
        """ Check fillers correspond to slots
            Fillers are entered as a list of type Fillers:
            - Each Fillers instance corresponds to one slot
            - One slot might have multiple nodes """

    for i in range(len(self.filler_set))):
        slot = self.caseframe.slots[i]
        fillers = self.filler_set[i]

    # Check if filler is legal (given limit, adjustment rule)
        for sem_type in fillers.sem_types:
            if not sem_type.compatible(slot.sem_type):
                raise Exception("Incompatible filler provided for " + slot.name + ".\n" + \
                                "Slot has type: " + slot.sem_type + ", " + \
                                "and filler has type: " + sem_type

        # Ensures within min/max of slots
        if len(fillers) < slot.min and slot.neg_adj != AdjRule.INF_REDUCE:
            raise Exception('Fewer than minimum required slots provided for ' + slot.name)
        if len(fillers) > slot.max and slot.neg_adj != AdjRule.INF_EXPAND:
            raise Exception('Greater than maximum slots provided for ' + slot.name)

# Forms "cables"/"cablesets"
class Fillers:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.sem_types = [node.sem_type for node in nodes]

    def __len__(self):
        return len(nodes)
