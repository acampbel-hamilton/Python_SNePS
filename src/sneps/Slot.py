from enum import Enum
from .SNError import SNError
from .SemanticType import SemanticType
from re import match
from .Path import Path

# =====================================
# ------------- GLOBALS ---------------
# =====================================

class SlotError(SNError):
    pass

class AdjRule(Enum):
    """ Enum allows us to use these names as shorthands in adjustment rules. """
    NONE = 0
    REDUCE = 1
    EXPAND = 2

# =====================================
# --------------- SLOT ----------------
# =====================================

class Slot:
    """ A unique object used in the construction of caseframes and the corresponding nodes.
        Also referred to as relations. """

    def __init__(self, name: str, sem_type: SemanticType,
                 docstring: str, pos_adj: str, neg_adj: str,
                 min: int, max: int) -> None:
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
        self.paths = set()

    def add_path(self, path: Path) -> None:
        """ Adds a new path object on which the slot exists. """
        self.paths.add(path)

    def __repr__(self):
        return "<Slot {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self) -> str:
        return "<{}>: {}\n".format(self.name, self.docstring) + \
               "\tSemantic Type: {}\n".format(self.sem_type) + \
               "\tPositive Adjust: {}\n".format(self.pos_adj.name.lower()) + \
               "\tNegative Adjust: {}\n".format(self.neg_adj.name.lower()) + \
               "\tMinimum Fillers: {}\n".format(self.min) + \
               "\tMaximum Fillers: {}\n".format(self.max) + \
               "\tPaths:{}{}".format(
                    "\n\t  " if len(self.paths) > 0 else '',
                    "\n\t  ".join([str(path) for path in self.paths]))

# =====================================
# -------------- MIXIN ----------------
# =====================================

class SlotMixin:
    """ Provides functions related to slots to Network """

    def __init__(self) -> None:
        if type(self) is SlotMixin:
            raise NotImplementedError("Mixins can't be instantiated.")
        self.slots = {} # AKA Relations

    def find_slot(self, name: str):
        """ Locates a slot with the given name in the Network """
        if name in self.slots:
            return self.slots[name]
        else:
            raise SlotError("ERROR: The slot name '{}' does not exist".format(name))

    def define_slot(self, name: str, sem_type_str: str, docstring="", pos_adj="NONE",
                    neg_adj="NONE", min=1, max=None, path='') -> None:
        """ Adds new slot to network """

        if not match(r'^[A-Za-z][A-Za-z0-9_]*$', name):
            raise SlotError("ERROR: The slot name '{}' is not allowed".format(name))

        if name in self.slots: # Slots are unique
            raise SlotError("ERROR: Slot " + name + " already defined.")

        sem_type = self.sem_hierarchy.get_type(sem_type_str)

        # Creates and stores the slot in the Network
        self.slots[name] = Slot(name, sem_type, docstring, pos_adj, neg_adj, min, max)

        # Adds any path which might have been provided to the slot
        self.define_path(name, path)

    def list_slots(self) -> None:
        """ Prints all slots in network """
        for slot_name in self.slots:
            print(self.slots[slot_name])
