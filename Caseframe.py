from Slot import *
from SemanticType import SemanticType
from sys import stderr

class Caseframe:
	counter = 0
	def __init__(self, name, sem_type, docstring="", slots=[]):
		self.name = name
		self.docstring = docstring
		self.sem_type = type
		self.slots = slots
		self.aliases = [self.name]

	def add_alias(self, alias):
		# Adds new alias to array
		self.aliases.append(alias)

	def has_alias(self, alias):
		# Checks if string in aliases
		return alias in self.aliases

	def __eq__(self, other):
		"""Returns true if both arguments are equivalent caseframes.
			Two caseframes are equivalent when:
				1. They have the same type
				2. They have the same slots (disregarding order)"""
		return not other is None and self.sem_type is other.sem_type and \
			set(self.slots) - set(other.slots) == set([])

class Frame:
	def __init__(self, caseframe, filler_set=[]):
		self.caseframe = caseframe
		self.filler_set = filler_set

		if len(self.fillers) != len(self.caseframe.slots):
			print('Wrong number of fillers. "' + self.caseframe.name + '" takes' + \
					len(self.caseframe.slots)+' fillers.', file=stderr)
			return

		verify_slots()

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
					print("Incompatible filler provided for " + slot.name + ".\n" + \
						"Slot has type: " + slot.sem_type + ", " + \
						"and filler has type: " + sem_type, file=stderr)
					return

			# Ensures within min/max of slots
			if len(fillers) < slot.min and slot.neg_adj != AdjRule.INF_REDUCE:
				print('Fewer than minimum required slots provided for ' + slot.name, file=stderr)
				return
			if len(fillers) > slot.max and slot.neg_adj != AdjRule.INF_EXPAND:
				print('Greater than maximum slots provided for ' + slot.name, file=stderr)
				return

# Forms "cables"/"cablesets"
class Fillers:
	def __init__(self, nodes=[]):
		self.nodes = nodes
		self.sem_types = [node.sem_type for node in nodes]

	def __len__(self):
		return len(nodes)
