#SNePS Find Methods
from slots import *
from caseframe import *
from contexts import *
from SemanticTypes import *
from SyntacticTypes import *

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
						filter((lambda s: not s is None),
							map((lambda n: self.findTerm(n)), names))))

	def findto(self, n, r):
		"""returns the set of nodes which a slot r goes to from a node n, possibly the empty set"""
		if isinstance(r, Slot):
			r = r.name
		if isinstance(n, str):
			n = self.terms.get(n)
			if n is None:
				return set()

		assert isinstance(r, str)
		assert isinstance(n, Molecular)
		return set(map((lambda k: self.terms[k]), set(n.down_cableset.get(r))))

	def findfrom(self, m, r):
		"""returns the set of nodes from which a slot r goes to m"""
		if isinstance(r, Slot):
			r = r.name
		m = self.findTerm(m)
		if m is None:
			return set()

		assert isinstance(r, str)
		assert isinstance(m, Term)

		if not(m.up_cableset.get(r)):
			return set()
		return set(map(lambda k: self.terms[k], set(m.up_cableset.get(r))))

	def eqfillersets (self, set1, set2):
		"""True if corresponding elements of sets are non-sets or same size"""
		for i in range(len(set1)):
			if isinstance(set1[i], set) and isinstance(set2[i], set) and len(set[i]) != len(set[i]):
				return False
			elif isinstance(set1[i], set) or isinstance(set2[i], set):
				return False
		return True
