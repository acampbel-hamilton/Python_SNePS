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
		if not(p):
			return list()
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

	def isAsserted(self, prop, context):
		"""Return the existing node if it is asserted in the context, else
		return None"""
		# TODO: make sure this works for if fillers of a slot are in different order
		# for prop in (context.hyps | context.ders):
		# 	if proposition.down_cableset == self.terms[prop].down_cableset:
		# 		return True
		# return False
		# return proposition.name in (context.hyps | context.ders)
		for p in [self.terms[p] for p in (context.hyps | context.ders)]:
			if prop == p:
				return p
		return None


	# Move to an "ask" file, if one is created
	def askif(self, prop, context=None):
		""" If already asserted, prints the asserted prop's name and returns it
		If prop is derivable in the context, adds prop to network, prints it's
		new name, and returns it"""

		# default to the currentContext
		context = self.currentContext if context == None else context

		# check if the proposition is asserted in the context
		isAsserted = self.isAsserted(prop, context)
		if isAsserted:
			print (isAsserted.name) 	# print the already asserted prop's name
			return isAsserted


		if self.pb_derivable(prop, context):
			Molecular.counter += 1
			prop.name = Sym("M{}".format(Molecular.counter))
			prop.caseframe.terms.add(prop.name)
			self.terms[prop.name] = prop

			for i in range(len(prop.caseframe.slots)):
				for node in list(prop.down_cableset.values())[i]:
					self.terms[node].up_cableset.update({Sym(prop.caseframe.slots[i]):
						self.terms[node].up_cableset.get(Sym(prop.caseframe.slots[i]), [])
						+ [prop.name]})

			context.ders.add(prop.name)
			print (prop.name)
			return prop
			
		print ("False")

	def pb_findfroms(self, term, slot, context = None):
		"""Returns the list of nodes from which the slot,
		or a path for the slot, goes to term."""

		# default to the currentContext
		context = self.currentContext if context == None else context

		if isinstance(slot, str):
			slot = self.slots[slot]

		if slot.b_path:
			return self.traverse(term, slot.b_path, context)
		return self.findfrom(term, slot)

	def pb_derivable(self, prop, context):
		dcs = prop.down_cableset

		first = True
		nodes = set()

		# for each slot
		for slot in dcs:
			# for each filler of the slot
			for filler in dcs[slot]:
				if first:
					nodes = self.pb_findfroms(filler, slot, context)
					first = False
				else:
					froms = self.pb_findfroms(filler, slot, context)
					nodes = [n for n in froms if n in nodes]
		if nodes:
			return True
		return False

	def traverse(self, node, path, context = None):
		"""Takes a node, a path. Reads the next direction given by the path,
		performs the direction, and recursively calls traverse on the next node
		with the rest of the path. Returns a set of nodes led to by the path"""
		# Got rid of compose and converse, still don't know what the restricts do...

		# make node string into node
		if isinstance(node, str):
			node = self.terms.get(node, node)
			if isinstance(node, str):
				raise AssertionError("term \'{}\' does not exist".format(node))

		# default to the currentContext
		context = self.currentContext if context == None else context

		#Debug info:
		# print("\nTRAVERSE\n  node: {}\n  path: {}".format(node.name, path))
		# input("")

		# At the end of the path:
		if not(path):
			return [node]

		# If a string
		elif isinstance(path[0], str):
			# Asserted Node
			if path[0] == "!":
				if self.isAsserted(node, context):
					return self.traverse(node, path[1:], context)
				return list()

			# Backward Arc
			elif path[0][-1] == "-":
				# for node n along the backwards slot listed in path
				nextNodes = node.up_cableset.get(path[0][:-1], list())
				return self.traverseFromNodes(nextNodes, path[1:], context)

			# Forward Arc
			else:
				# for node n along the next slot in path
				nextNodes = list()
				if isinstance(node, Molecular):
					nextNodes = node.down_cableset[path[0]]
				return self.traverseFromNodes(nextNodes, path[1:], context)
		elif isinstance(path[0], list):
			if path[0][0] == "and":
				assert len(path[0]) >= 2, "Incomplete AND statement"

				# get initial value for nextNodes from evaluating first path in the and
				nextNodes = self.traverse(node, path[0][1], context)

				# for the rest of the paths in the and statement:
				for p in path[0][2:]:
					# short cicuit out of AND if nextNodes is empty
					if not(nextNodes):
						return list()

					# Intersect/And together nextNodes and nodes returned from
					# traversing from current node along path p
					nextNodes = [n for n in nextNodes if n in self.traverse(node, p, context)]

				# From each node in nextNodes, evaluate the rest of the path
				return self.traverseFromNodes(nextNodes, path[1:], context)

			elif path[0][0] == "or":
				assert len(path[0]) >= 2, "Incomplete OR statement"
				nextNodes = list()

				# for paths in the or statement:
				for p in path[0][1:]:
					# traverse from current node, using that path
					nextNodes += [n for n in self.traverse(node, p, context) if n not in nextNodes]

				# From each node in nextNodes, evaluate the rest of the path
				return self.traverseFromNodes(nextNodes, path[1:], context)

			elif path[0][0] == "kstar":
				assert len(path[0]) == 2, "Improper kstar format"

				zeroTimes = self.traverse(node, path[1:], context)

				nextNodes = self.traverseKplus([node], path[0][1], context)
				multTimes = self.traverseFromNodes(nextNodes, path[1:], context)

				return multTimes + [n for n in zeroTimes if n not in multTimes]

			elif path[0][0] == "kplus":
				assert len(path[0]) == 2, "Improper kplus format"
				nextNodes = self.traverseKplus([node], path[0][1], context)
				return self.traverseFromNodes(nextNodes, path[1:], context)

	def traverseFromNodes(self, nodes, path, context):
		retVals = list()
		if nodes:
			for s in map(lambda n: self.traverse(n, path, context), nodes):
				if s:
					retVals += [n for n in s if n not in retVals]
		return retVals

	def traverseKplus(self, nodes, path, context):
		nextNodes = list()
		next = nodes

		while True:
			# get nodes from traversing the path another time
			next = self.traverseFromNodes(next, path, context)
			# add those nodes to nextNodes
			nextNodes += [n for n in next if n not in nextNodes]
			# break case:
			if not(next):
				break
		return nextNodes

# Eample Paths
# defPath member (member (kstar (equiv- ! equiv)))
# defPath member (or member(member (kstar (equiv- ! equiv))))
# defPath class (or class (class (kstar (subclass- superclass))))
# defPath class (class (kstar (subclass- superclass)))






#
