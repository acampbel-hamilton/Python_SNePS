class CaseFrame:
	def __init__(self, name, docstring="", sem_type, slots=[]):
        self.name = name
        self.docstring = docstring
        self.sem_type = type
        self.slots = slots

class Frame:
	def __init__(self, caseframe, fillers=[]):
        self.caseframe = caseframe
		self.fillers = fillers

		# Check fillers correspond to slots
		# Fillers are entered as a list of lists:
		#     - Each list correspond to one slot
		#     - Remember one slot might have multiple fillers
		if len(self.fillers) != len(self.caseframe.slots):
			raise Exception("Wrong number of fillers")

		for i in range(0, len(self.fillers) - 1):
			slot = self.caseframe.slots[i]

			# Check if filler legal(given limit, adjustment rule)
			

			for filler in self.fillers[i]:
				if not (filler.sem_type.compatible(slot.sem_type)):
					raise Exception('Incompatible filler provided for slot:\n' \
					+ 'Slot has type: ' + slot.sem_type + ' while Filler has type: '\
					+ filler.type)
