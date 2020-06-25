from enum import Enum
from sys import stderr
from .Error import SNError
from re import match

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
        try:
            self.pos_adj = AdjRule.__dict__[pos_adj.upper()] # Positive adjustment rule (i.e. "NONE")
            self.neg_adj = AdjRule.__dict__[neg_adj.upper()] # Negative adjustment
        except KeyError:
            raise SlotError("Invalid adjustment rule string provided. Valid options are \"NONE\", \"REDUCE\", and \"EXPAND\"")
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

class SlotMixin:
    """ Provides functions related to slots to Network """

    def __init__(self):
        if type(self) is SlotMixin:
            raise NotImplementedError("Mixins can't be instantiated.")
        self.slots = {} # AKA Relations

    def define_slot(self, name, sem_type_str, docstring="", pos_adj="NONE",
                    neg_adj="NONE", min=1, max=0, path=None):
        """ Adds new slot to network """

        if self.enforce_name_syntax and not match(r'[A-Za-z_][A-Za-z0-9_]*', name):
            raise SlotError("ERROR: The slot name '{}' is not allowed".format(name))

        if name in self.slots:
            raise SlotError("ERROR: Slot " + name + " already defined.")

        sem_type = self.sem_hierarchy.get_type(sem_type_str)

        self.slots[name] = Slot(name, sem_type, docstring, pos_adj, neg_adj, min, max, path)

    def list_slots(self):
        """ Lists all slots in network """
        for slot_name in self.slots:
            print(self.slots[slot_name])
