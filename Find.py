#SNePS Find Methods


class Find:
	def findTerm(self, name):
		"""returns the term named name or name if it is a term and None otherwise"""
		if isinstance(name, Term):
			return name
		if isinstance(name, str):
			return self.terms.get(name)
		return None

	def findTerms(self, names):
		"""returns all terms specified by a valid name in names and the empty set if none exist"""
		assert isinstance(names, list)
		return set(reduce((lambda a,b: union(a, b)),
						filter((lambda s: s not is None),
							map((lambda n: self.findTerm(n)), names))))
