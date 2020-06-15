class CaseFrame:
	def __init__(self, name, sem_type, docstring="", slots=[]):
        self.name = name
        self.docstring = docstring
        self.sem_type = type
        self.slots = slots

class Frame:
	def __init__(self, caseframe, fillers=[]):
        self.caseframe = caseframe
		self.fillers = fillers

		if len(self.fillers) != len(self.caseframe.slots):
			raise Exception("Wrong number of fillers")

		fill_slots()

	def fill_slots(self):
		# Check fillers correspond to slots
		# Fillers are entered as a list of lists:
		#     - Each list correspond to one slot
		#     - Remember one slot might have multiple fillers

		for i in range(len(self.fillers) - 1):
			slot = self.caseframe.slots[i]

			# Check if filler legal(given limit, adjustment rule)
			for filler in self.fillers[i]:
				if not filler.sem_type.compatible(slot.sem_type):
					raise Exception('Incompatible filler provided for slot:\n' \
					+ 'Slot has type: ' + slot.sem_type + ', and filler has type: ' + filler.type)

class Fillers:
	def __init__(self, nodes=[]):
