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
		print (aslot.b_path_fn)
		print (aslot.f_path_fn)

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
				# print(path)
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

	def getFroms(self, nodes, slotname):
		"""Given a nodeset and slot name,
		returns all nodes with an arc to 1+ of the input nodes"""
		retValue = set()
		for node in nodeset:
			retValue.update(self.findfrom(node, slotname))
		return retValue

	def getTos(self, nodeset, slotname):
		"""Given a nodeset and slot name,
		returns all nodes with an arc from 1+ of the input nodes"""
		retValue = set()
		for node in nodeset:
			retValue.update(self.findfrom(node, slotname))
		return retValue

	def pb_findfroms (terms, slot):
		"""Returns the nodeset pointed to by the given slot/path"""
		# TODO: add the other cases of pb_findfroms
		if slot.b_path_fn:
			(slot.b_path_fn)(terms)
		else:
			getFroms(terms, slot)

	def path_based_derivable (self, prop, context):
		"""If proposition prop is derivable given context by path-based-inference
		return set([prop]), else return set([])"""
		if prop.type_name == 'Molecular':
			cf = prop.caseframe
			dcs = prop.down_cableset
			firstTime = True
			results = set()

			for slot in dcs:
				if firstTime:
					results.add(pb_findfroms(dcs[slot], slot))
					# TODO: figure out if this pb_findfroms call is good
					firstTime = False
				else:
					results = results & pb_findfroms(dcs[slot], slot)

			results = filter(lambda term: self.assertedProp(term, context), results)
			if results and some(map(lambda result: self.eqfillersets(result.down_cableset, dcs), results)):
				return set([prop])
		return set()

	# If we make an "assert" file, move this there.
	def assertedProp (self, prop, context=None):
		"""Returns first context that the proposition is asserted in, else None"""
		# TODO: the lisp implementation used "resource-value" and "build",
		# which I didn't understand/seemed overly complicated. Not sure if this works:
		if not(context):
			context = self.currentContext
		if prop.type_name == 'Proposition':
			for ctxt in ([context] + context.parents):
				if prop in (ctxt.hyps + ctxt.ders):
					return ctxt
		return None

	# Move to an "ask" file, if one is created
	def askif(self, prop, context, termstack):
		""" If prop is derivable in the context, return set([prop]), else set().
		Termstack is a stack of propositions that this goal is a subset of. """
		if self.assertedProp(prop, context):
			return set([prop])
		#TODO: update this when natural-deducation, slot-based, sort-based are done
		return self.path_based_derivable(prop, context)


















#
