# SNePS3 Semantic Types
#currently a copy of the corresponding Allegro lisp implementation file
import re

class Entity:
	"""root of the semantic type hierarchy"""
	def __init__(self):
		self.type_name = self.getClass()

	def _classStrip(self, s):
		r = re.compile('(\()?\<class\s*\'SemanticTypes\.' + \
		'(?P<C>[A-Z][A-z]*)\'\>(,\))?')
		m = r.match(str(s))
		return m and m.group('C')

	def getParent(self):
		"""returns the parent class of the given node instance"""
		return self._classStrip(self.__class__.__bases__)

	def getClass(self):
		"""returns the class name as a string"""
		return self._classStrip(self.__class__)

	def __str__(self):
		"""represents the class as a string"""
		return str(self.type_name)

class Proposition(Entity):
	"""an entity who can be believed and whose negation can be believed"""
	def __init__(self, support_set=None, supported_nodes=None):
		Entity.__init__(self)
		self.support_set = set() if support_set is None else support_set
		self.supported_nodes = set() if supported_nodes is None else supported_nodes

class Act(Entity):
	"""an Entity that can be performed"""
	def __init__(self, primaction=None):
		Entity.__init__(self)
		self.primaction = primaction

class Policy(Entity):
	"""an Entity that relates Propositions to Acts"""

class Thing(Entity):
	"""everything not a Proposition, Act, or Policy"""

class Category(Thing):
	"""a category of entities"""

class Action(Thing):
	"""an action that can be performed on one or more argument entities"""
	def __init(self, primaction=None):
		Thing.__init__(self)
		self.primaction = primaction
