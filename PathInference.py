#SNePS3 Path Based Inference Methods
# A mix-in
class PathInference:
	"""contains methods for path based inference for use in Network"""

	def assertedMembers(self, termSet, ctxt):
		"""Given a set of terms, returns the set of terms asserted in the context"""
		return filter(lambda term: term in (ctxt.hyps + ctxt.der), termSet)

	def definePath(self, slotname, pathexpr):
		"""Given a slot name and a path expression, generate the functions that
		will compute that path and its converse, and store them in the slot."""
		aslot = self.findSlot(slotname)

		aslot.path = pathexpr
		aslot.b_path_fn = self.buildPathFn(self.converse(pathexpr))
		aslot.f_path_fn = self.buildPathFn(pathexpr)

	def buildPathFn(self, path):
		"""Given a path expression, returns the function that will traverse that path"""

		if isinstance(path, list):
			if path[0] == "compose":
				return "(lambda x: {})".format(self.composeHelper(list(reversed(path[1:]))))
			elif path[0] == "or":
				return "(lambda x: reduce(lambda a,b: a|b, map(lambda fn: set(fn(x)), {})))".format(map(lambda elt: self.buildPathFn(elt), pathElts[1:]))
			elif path[0] == "and":
				return "(lambda x: reduce(lambda a,b: a&b, map(lambda fn: set(fn(x)), {})))".format(map(lambda elt: self.buildPathFn(elt), pathElts[1:]))
			elif path[0] == "kstar":
				assert path[1:][1:] == [], "kstar must have only one path argument in {}".format(path)
				return "(lambda x: fStar(x, {}))".format(self.buildPathFn(path[1]))
			elif path[0] == "kplus":
				assert path[1:][1:] == [], "kplus must have only one path argument in {}".format(path)
				return "(lambda x: fplus(x, {}))".format(self.buildPathFn(path[1]))
			elif path[0] == "converse":
				return (self.buildPathFn(self.converse(path[1])))
			elif path[0] == "irreflexive-restrict":
				# If P is a path from node x to node y, and x != y, then (irreflexive-restrict P) is a path from x to y.
				return "(lambda x: set(({})(x)) - set(x))".format(self.buildPathFn(path[1]))
			elif path[0] == "restrict":
				assert len(path) == 3, "restrict must have two arguments, a path, and an atomicwft in {}".format(path)
				return "(lambda x: set(filter(lambda trm: self.memberOrVar(path[2], {}([trm])), x)))".format(buildPathFn(path[1]))
			else:
				assert False, ("Unrecognized path expression operator: {}".format(path[0]))
		elif path == "!":
			return "(lambda trms: self.assertedMembers(trms, self.currentContext))"
		else:
			# If a backwards slot: getFroms of the forward version of the slot
			if len(path) > 0 and path[-1] == "-":
				return "(lambda x: self.getFroms(x, {}))".format(path[:-1])
			# Else, is a forward slot: getTos of the slot
			return "(lambda x: self.getTos(x, {}))".format(path)

	def composeHelper(self, pathElts):
		"""Given a list of path element in reverse order, return a function which
		 will traverse a path in the original order"""
		if pathElts[1:] != []:
			return "{}({})".format(self.buildPathFn(pathElts[0]), self.composeHelper(pathElts[1:]))
		return "{}(x)".format(self.buildPathFn(pathElts[0]))

	def fPlus(self, nodeset, fn):
		"""Given a nodeset and a function, return the nodeset that results
		from repeately applying the function to the nodeset one or more times"""
		res = fn(nodeset)
		retval = set()
		while res:
			retvel.add(res)
			res = fn(res) - retval
		return retvalue

	def fStar(self, nodeset, fn):
		"""Given a nodeset and a funciton, returns the nodeset that results from
		applying the function to the nodeset zero or more times"""
		return set(nodeset) | set(self.fplus(nodeset, fn))

	def memberOrVar(self, sym, termSet):
		""" True if : sym is "?" and termSet not empty, OR
					  the term named sym is in the termSet """
		return (sym == "?" and termSet) or (self.findTerm(sym) in termSet)

	def converse(self, path):
		"""Given a path expression, returns its converse"""

		if self.isPathKeyword(path[0]):
			return [path[0]] + list(reversed(list(map(lambda elt: self.converse(elt), path[1:]))))
		elif path == "!":
			return "!"
		elif path[-1] == "-":
			return path[:-1]
		else:
			return path + "-"

	def isPathKeyword(self, word):
		"""returns False if the argument is not a path keyword"""
		return word in ["or", "and", "compose", "kstar", "kplus", "not",
		"relative-complement", "irreflexive-restrict", "restrict", "converse"]
