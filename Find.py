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

	def findTerms(self, names):	# Needs to be re-written to return list instead of set
		"""returns all terms specified by a valid name in names and the empty set if none exist"""
		assert isinstance(names, list)
		return set(reduce((lambda a,b: a | b),
						filter((lambda s: not s is None),
							map((lambda n: self.findTerm(n)), names))))

	def findto(self, n, r):
		"""returns the list of nodes which a slot r goes to from a node n"""
		if isinstance(r, Slot):
			r = r.name
		if isinstance(n, str):
			n = self.terms.get(n)
			if n is None:
				return list()

		assert isinstance(r, str)
		assert isinstance(n, Molecular)
		return list(map((lambda k: self.terms[k]), n.down_cableset.get(r)))

	def findfrom(self, m, r):
		"""returns the list of nodes from which a slot r goes to m"""
		if isinstance(r, Slot):
			r = r.name
		m = self.findTerm(m)
		if m is None:
			return list()

		assert isinstance(r, str)
		assert isinstance(m, Term)

		if not(m.up_cableset.get(r)):
			return list()
		return list(map(lambda k: self.terms[k], m.up_cableset.get(r) ))
