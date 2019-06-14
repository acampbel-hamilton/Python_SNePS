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
		aslot.b_path_fn = buildPathFn(converse(pathexpr))
		aslot.f_path_fn = buildPathFn(pathexpr)

	def buildPathFn(self, path):
		"""Given a path expression, returns the function that will traverse that path"""

		if isinstance(path, list):
			if path[0] == "compose":
				return f"(lambda x: {composeHelper(list(reversed(path[1:])))})"
			elif path[0] == "or":
				return f"(lambda x: reduce(lambda a,b: a|b, map(lambda fn: set(fn(x)), {(map(lambda elt: buildPathFn(elt), pathElts[1:]))})))"
			elif path[0] == "and":
				return f"(lambda x: reduce(lambda a,b: a&b, map(lambda fn: set(fn(x)), {(map(lambda elt: buildPathFn(elt), pathElts[1:]))})))"
			elif path[0] == "kstar":
				assert path[1:][1:] == [], "kstar must have only one path argument in {}".format(path)
				return f"(lambda x: fStar(x, {(buildPathFn(path[1]))}))"
			elif path[0] == "kplus":
				assert path[1:][1:] == [], "kplus must have only one path argument in {}".format(path)
				return f"(lambda x: fplus(x, {(buildPathFn(path[1]))}))"
			elif path[0] == "converse":
				return (buildPathFn(converse(path[1])))
			elif path[0] == "irreflexive-restrict":
				# If P is a path from node x to node y, and x != y, then (irreflexive-restrict P) is a path from x to y.
				return f"(lambda x: set(({buildPathFn(path[1])})(x)) - set(x))"
			elif path[0] == "restrict":
				assert len(path) == 3, "restrict must have two arguments, a path, and an atomicwft in {}".format(path)
				return f"(lambda x: set(filter(lambda trm: memberOrVar(path[2], ({buildPathFn(path[1])})([trm])), x)))"
			else:
				assert False, ("Unrecognized path expression operator: {}".format(path[0]))
		elif path == "!":
			return "(lambda trms: assertedMembers(trms, self.currentContext))"
		else:
			# If a backwards slot: getFroms of the forward version of the slot
			if path[-1] == "-":
				return f"(lambda x: getFroms(x, {path[:-1]}))"
			# Else, is a forward slot: getTos of the slot
			return f"(lambda x: getTos(x, {path}))"

	def composeHelper(self, pathElts, x):
		"""Given a list of path element in reverse order, return a function which
		 will traverse a path in the original order"""
		if pathElts[1:] != []:
			return f"{buildPathFn(pathElts[0])}({(composeHelper(pathElts[1:]))})"
		return f"{buildPathFn(pathElts[0])}(x)"

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
		return set(nodeset) | set(fplus(nodeset, fn))

	def memberOrVar(self, sym, termSet):
		""" True if : sym is "?" and termSet not empty, OR
					  the term named sym is in the termSet """
		return (sym == "?" and termSet) or (self.findTerm(sym) in termSet)

	def converse(path):
		"""Given a path expression, returns its converse"""

		if isPathKeyword(path[0]):
			return [path[0]] + list(reversed(list(map(lambda elt: converse(elt), path[1:]))))
		elif path == "!":
			return "!"
		elif path[-1] == "-":
			return path[:-1]
		else:
			return path + "-"

	def isPathKeyword(word):
		"""returns False if the argument is not a path keyword"""
		return word in ["or", "and", "compose", "kstar", "kplus", "not",
		"relative-complement", "irreflexive-restrict", "restrict", "converse"]

	# def pathBasedDerivable(prop, context):

		# compile name &optional definition => function, warnings-p, failure-p
			# name: nil
			# definition: a lambda expression or a function
			# function: the function-name, or a compiled function

		# intern string &optional package => symbol
			# enters a symbol named string into package
