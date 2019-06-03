#SNePs3 slot class definition

class Slot:
	def __init__(self, name, type, pos_adj="reduce", neg_adj="expand",
	 min=1, max=None, path=None, f_path_fn=None, b_path_fn=None):
		self.name = name
		self.type = type
		self.pos_adj = pos_adj
		self.neg_adj = ned_adj
		self.min = min
		self.max = max
		self.path = path
		self.f_path_fn = f_path_fn
		self.b_path_fn = b_path_fn

	def __str__(self):
		return "<{}, {}, pos: {}, neg: {}, {}>".format(self.name, self.type,
		 		self.pos_adj, self.neg_adj, self.min)
