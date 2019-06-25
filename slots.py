#SNePs3 slot class definition

from Symbol import *

class Slot:
	def __init__(self, name, type, docstring="", pos_adj=Sym("reduce"), neg_adj=Sym("expand"),
	 min=1, max=None, path=None, f_path_fn=None, b_path_fn=None):
		self.name = name
		self.type = type
		self.docstring = docstring
		self.pos_adj = pos_adj
		self.neg_adj = neg_adj
		self.min = min
		self.max = max
		self.path = path
		self.f_path_fn = f_path_fn
		self.b_path_fn = b_path_fn

	def __repr__(self):
		return "<Slot {} id: {}>".format(self.name, hex(id(self)))

	def __str__(self):
		return "<{}, {}, pos: {}, neg: {}, min: {}>\nDesc: {}".format(self.name, self.type,
		 		self.pos_adj, self.neg_adj, self.min, self.docstring)

class Slot_Mixin:
	def findSlot(self, slot):
		if isinstance(slot, Slot):
			return slot
		if isinstance(slot, str) and Sym(slot) in self.slots.keys():
			return self.slots[Sym(slot)]
		raise TypeError("Inappropriate type passed to findSlot function.")

	def listSlots(self):
		"""prints all slots for the user"""
		print(*sorted(self.slots.keys()), sep="\n")
