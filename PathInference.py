#SNePS3 Path Based Inference Methods
# A mix-in
from SyntacticTypes import Molecular
from caseframe import *
import inspect, sys, re
from Symbol import Symbol, Sym, _reduce, _expand, _none
from slots import *
from caseframe import *
from contexts import *

class PathInference:
	"""contains methods for path based inference for use in Network"""

	def definePath(self, slotname, pathexpr):
		"""Given a slot name, stores the forward and backward path expr for it"""
		aslot = self.findSlot(slotname)

		aslot.f_path = pathexpr
		aslot.b_path = self.converse(pathexpr)

	def isPathKeyword(self, word):
		"""returns False if the argument is not a path keyword"""
		# do not have compose, relative-complement, irreflexive-restrict, restrict,  or converse
		return word in ["or", "and", "kstar", "kplus", "not"]

	def converse(self, p):
		"""Given a path expression, returns its converse"""
		path = p.copy() if self.isPathKeyword(p[0]) else list(reversed(p))
		for i in range(len(path)):
			if isinstance(path[i], str):
				if path[i] == '!':
					pass
				elif path[i][-1] == "-":
					path[i] = path[i][:-1]
				elif not(self.isPathKeyword(path[i])):
					path[i] = path[i] + "-"
			if isinstance(path[i], list):
				path[i] = self.converse(path[i])
		return path

	def pb_buildProp(self, caseframe, fillers, SynType=Molecular, uassert=False):
		"""Builds a molecular node based on the given caseframe
		 and list of fillers. Does not add the node to the network."""
		assert isinstance(caseframe, CaseFrame), "Given caseframe must exist"
		assert isinstance(fillers, list) #fillers should be a list of lists of strings
		assert all([isinstance(s, str) for s in [i for sl in fillers for i in sl]])

		#all base terms  must exist
		for name in set([i for sl in fillers for i in sl]):
			if name not in self.terms.keys():
				self.terms[Sym(name)] = Term(name)
		for term in self.terms.values(): #no identical term exists
			if isinstance(term, Molecular) and term.caseframe == caseframe and \
				[sorted(sl) for sl in sorted(term.down_cableset.values())] == \
				[sorted(sl) for sl in sorted(fillers)]:
				raise AssertionError("Identical term {} already exists".format(term.name))

		term = SynType(Sym("M?"), caseframe,
		 			down_cableset=dict(zip(caseframe.slots, fillers)))
		return (term)

	def isAsserted(self, proposition, context):
		"""Return true if an asserted prop's caseframe and fillers match the given prop"""
		# TODO: make sure this works for if fillers of a slot are in different order
		for prop in (context.hyps | context.ders):
			if proposition.down_cableset == prop.down_cableset:
				return True
		return False

	# Move to an "ask" file, if one is created
	def askif(self, prop, context=None):
		""" If prop is derivable in the context, return set([prop]), else set()"""

		# Prints for debugging...
		print ("\nASK IF: ")
		print ("prop: {}".format(prop))
		input("waiting...")

		# default to the currentContext
		context = self.currentContext if context == None else context

		# return True if the proposition is asserted in the context
		if self.isAsserted(prop, context):
			return True

		nodes = self.pb_derivable(prop, context)

	def pb_findfrom(self, prop, context):
		"""Returns the set of nodes from which the given slot,
		or a path for the slot, goes to term."""

		results = self.findfrom(filler, slot)
		if slot.f_path:
			pass

	def pb_derivable(self, prop, context):
		dcs = prop.down_cableset
		# for each slot
		for slot in dcs:
			# for each filler of the slot
			for filler in dcs[slot]:
				# for the nodes that point to filler with the arc name slot, or
				# that point to filler via the defined path for the slot
				for node in self.pb_findfrom(filler, slot, context):
					pass

	def traverse(self, node, path, context = None):
		"""Takes a node, a path. Reads the next direction given by the path,
		performs the direction, and recursively calls traverse on the next node
		with the rest of the path. Returns a set of nodes led to by the path"""
		# Got rid of compose and converse
		# Still don't know what the restricts do...
		# Maybe instead of expecting a node, it should be a node set...
		# that way we can combine traverse() and traverseFromNodes().

		# make node string into node
		if isinstance(node, str):
			node = self.terms[node]

		# default to the currentContext
		context = self.currentContext if context == None else context

		#Debug info:
		# print("\nTRAVERSE\n  node: {}\n  path: {}".format(node.name, path))
		# input("")

		# At the end of the path:
		if not(path):
			return set([node])

		# If a string
		elif isinstance(path[0], str):
			# Asserted Node
			if path[0] == "!":
				if self.isAsserted(node, context):
					return self.traverse(node, path[1:])
				return set()

			# Backward Arc
			elif path[0][-1] == "-":
				# for node n along the backwards slot listed in path
				nextNodes = node.up_cableset.get(path[0][:-1], set())
				return self.traverseFromNodes(nextNodes, path[1:])

			# Forward Arc
			else:
				# for node n along the next slot in path
				nextNodes = node.down_cableset[path[0]]
				return self.traverseFromNodes(nextNodes, path[1:])
		elif isinstance(path[0], list):
			if path[0][0] == "and":
				assert len(path[0]) >= 2, "Incomplete AND statement"

				# get initial value for nextNodes from evaluating first path in the and
				nextNodes = self.traverse(node, path[0][1])

				# for the rest of the paths in the and statement:
				for p in path[0][2:]:
					# short cicuit out of AND if nextNodes is empty
					if nextNodes == set():
						return set()

					# Intersect/And together nextNodes and nodes returned from
					# traversing from current node along path p
					nextNodes.intersection(self.traverse(node, p))

				# From each node in nextNodes, evaluate the rest of the path
				return self.traverseFromNodes(nextNodes, path[1:])

			elif path[0][0] == "or":
				assert len(path[0]) >= 2, "Incomplete OR statement"
				nextNodes = set()

				# for paths in the or statement:
				for p in path[0][1:]:
					# traverse from current node, using that path
					nextNodes.update(self.traverse(node, p))

				# From each node in nextNodes, evaluate the rest of the path
				return self.traverseFromNodes(nextNodes, path[1:])

			elif path[0][0] == "kstar":
				assert len(path[0]) == 2, "Improper kstar format"
				nextNodes = self.traverseKplus(set([node]), path[0][1])
				return (set([node]) | self.traverseFromNodes(nextNodes, path[1:]))

			elif path[0][0] == "kplus":
				assert len(path[0]) == 2, "Improper kplus format"
				nextNodes = self.traverseKplus(set([node]), path[0][1])
				return self.traverseFromNodes(nextNodes, path[1:])

	def traverseFromNodes(self, nodes, path):
		retVals = set()
		if nodes:
			for s in map(lambda n: self.traverse(n, path), nodes):
				if s:
					retVals.update(s)
		return retVals

	def traverseKplus(self, nodes, path):
		nextNodes = set()
		next = nodes

		while True:
			# get nodes from traversing the path another time
			next = self.traverseFromNodes(next, path)
			# add those nodes to nextNodes
			nextNodes.update(next)
			# break case:
			if next == set():
				break
		return nextNodes








#
