from .Slot import *
from .SemanticType import SemanticType
from .Error import SNError
from sys import stderr

class CaseframeError(SNError):
    pass

class Caseframe:
    def __init__(self, name, sem_type, docstring="", slots=None):
        self.name = name
        self.docstring = docstring
        self.sem_type = sem_type
        self.slots = [] if slots is None else slots # see https://effbot.org/zone/default-values.htm for why this is necessary
        self.aliases = [self.name]

    def add_alias(self, alias):
        # Adds new alias to array
        self.aliases.append(alias)

    def has_alias(self, alias):
        # Checks if string in aliases
        return alias in self.aliases

    def __eq__(self, other):
        """ Returns true if both arguments are equivalent caseframes.
            Two caseframes are equivalent when:
                1. They have the same type
                2. They have the same slots (disregarding order) """
        return other is not None and self.sem_type is other.sem_type and \
               set(self.slots) == set(other.slots)

    def __str__(self):
        return "<{}>: {}\n".format(self.name, self.docstring) + \
               "\tSemantic Type: {}\n".format(self.sem_type.name) + \
               "\tAliases: [" + ", ".join(self.aliases) + "]"


class Frame:
    def __init__(self, caseframe, filler_set=None):
        self.name = caseframe.name
        self.caseframe = caseframe
        self.filler_set = [] if filler_set is None else filler_set # see https://effbot.org/zone/default-values.htm for why this is necessary

        if len(self.filler_set) != len(self.caseframe.slots):
            raise CaseframeError('ERROR: Wrong number of fillers. "' + self.caseframe.name + '" takes ' + \
                                 str(len(self.caseframe.slots)) + ' fillers.')

        self.verify_slots()

    def verify_slots(self):
        """ Check fillers correspond to slots
            Fillers are entered as a list of type Fillers:
                - Each Fillers instance corresponds to one slot
                - One slot might have multiple nodes """

        for i in range(len(self.filler_set)):
            slot = self.caseframe.slots[i]
            fillers = self.filler_set[i]

            # Check if filler is legal (given limit, adjustment rule)
            for sem_type in fillers.sem_types:
                if not sem_type.compatible(slot.sem_type):
                    raise CaseframeError("ERROR: Incompatible filler provided for " + slot.name + ".\n" + \
                                         "Slot has type: " + slot.sem_type + ", " + \
                                         "and filler has type: " + sem_type)

            # Ensures within min/max of slots
            if len(fillers) < slot.min:
                raise CaseframeError('ERROR: Fewer than minimum required slots provided for "' + slot.name + '"')

            if slot.max is not None and len(fillers) > slot.max:
                raise CaseframeError('ERROR: Greater than maximum slots provided for "' + slot.name + '"')

    def __eq__(self, other):
        return self.caseframe == other.caseframe and self.filler_set == other.filler_set

    def __str__(self):
        ret = self.name
        for i in range(0, len(self.filler_set)):
            ret += self.filler_set[i].__str__(self.caseframe.slots[i].name)
        return ret


class Fillers:
    """ Forms 'cables'/'cablesets' """

    def __init__(self, nodes=None):
        self.nodes = [] if nodes is None else nodes # see https://effbot.org/zone/default-values.htm for why this is necessary
        self.sem_types = [node.sem_type for node in self.nodes]

    def __len__(self):
        return len(self.nodes)

    def __str__(self, slot_name):
        return "\n\t  " + slot_name + ":" + "".join("\n\t    " + str(node) for node in self.nodes)


class CaseframeMixin:
    """ Provides functions related to caseframes to network """

    def __init__(self):
        if type(self) is CaseframeMixin:
            raise NotImplementedError("Mixins can't be instantiated.")

        self.caseframes = {}

    def find_caseframe(self, name):
        for caseframe in self.caseframes.values():
            if caseframe.has_alias(name):
                return caseframe
        else:
            raise CaseframeError('ERROR: Caseframe "' + name + '" not defined.')

    def list_caseframes(self):
        for caseframe in self.caseframes:
            print(self.caseframes[caseframe])

    def define_caseframe(self, name, sem_type_name, docstring="", slot_names=None):
        """ Defines a new caseframe. """
        # see https://effbot.org/zone/default-values.htm for why this is necessary
        if slot_names is None:
            slot_names = []

        # Checks provided slots names are valid
        frame_slots = []
        for slot_name in slot_names:
            if slot_name not in self.slots:
                raise CaseframeError("ERROR: The slot '{}' does not exist".format(slot_name))
            frame_slots.append(self.slots[slot_name])

        # Checks provided type is valid
        sem_type = self.sem_hierarchy.get_type(sem_type_name)
        if sem_type is None:
            raise CaseframeError("ERROR: The semantic type '{}' does not exist".format(sem_type_name))

        # Builds new caseframe with given parameters
        new_caseframe = Caseframe(name, sem_type, docstring, frame_slots)

        # Checks if identical to existing caseframe
        for caseframe in self.caseframes.values():
            if caseframe.has_alias(name):
                raise CaseframeError("ERROR: Caseframe name '{}' is already taken".format(name))

            if new_caseframe == caseframe:
                print('Your caseframe "' + new_caseframe.name + '" is identical to "' + caseframe.name + '".')

                while True:
                    response = input('Would you like to add an alias to "' + caseframe.name + '"? (y/N)')
                    if "YES".startswith(response.upper()):
                        caseframe.add_alias(name)
                        break
                    elif "NO".startswith(response.upper()):
                        break

                while True:
                    response = input('Would you like to override the docstring for "'+ caseframe.name + '"? (y/N)')
                    if "YES".startswith(response.upper()):
                        caseframe.docstring = docstring
                        break
                    elif "NO".startswith(response.upper()):
                        break

                return

        # If new/unique, adds to dictionary
        self.caseframes[new_caseframe.name] = new_caseframe