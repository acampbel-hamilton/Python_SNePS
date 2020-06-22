from enum import Enum
from sys import stderr
from .Error import SNError

class SlotError(SNError):
    pass

class AdjRule(Enum):
    NONE = 0
    REDUCE = 1
    EXPAND = 2

class Slot:
    def __init__(self, name, sem_type, docstring, pos_adj, neg_adj, min, max, path):
        self.name = name
        self.docstring = docstring
        self.sem_type = sem_type # Semantic type
        self.pos_adj = pos_adj # Positive adjustment
        self.neg_adj = neg_adj # Negative adjustment
        self.min = min
        self.max = max
        self.path = path

    def __repr__(self):
        return "<Slot {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self):
        return "<{}>: {}\n".format(self.name, self.docstring) + \
               "\tSemantic Type: {}\n".format(self.sem_type) + \
               "\tPositive Adjust: {}\n".format(self.pos_adj) + \
               "\tNegative Adjust: {}\n".format(self.neg_adj) + \
               "\tMinimum Fillers: {}\n".format(self.min) + \
               "\tMaximum Fillers: {}\n".format(self.max) + \
               "\tPath: {}".format(self.path)

class SlotMixIn:
    """ Provides functions related to slots to Network """

    def __init__(self):
        if type(self) == SlotMixIn:
            raise NotImplementedError("Mixins can't be instantiated.")
        self.slots = {} # AKA Relations

    def define_slot(self, name, sem_type_str, docstring="", pos_adj=AdjRule.NONE,
                    neg_adj=AdjRule.NONE, min=1, max=None, path=None):
        """ Adds new slot to network """
        if name in self.slots:
            raise SlotError("ERROR: Slot " + name + " already defined. Doing nothing instead.")

        sem_type = self.sem_hierarchy.get_type(sem_type_str)
        if sem_type is not None:
            self.slots[name] = Slot(name, sem_type, docstring, pos_adj, neg_adj, min, max, path)

    def list_slots(self):
        """ Lists all slots in network """
        for slot_name in self.slots:
            print(self.slots[slot_name])
