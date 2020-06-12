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
			raise Exception("Wrojng number of fillers")
