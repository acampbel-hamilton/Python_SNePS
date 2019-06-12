#SNePS3 Slot Based Inference Methods

class SlotInference:
	"""contains methods for slot based inference for use in SNePS class in Network"""

	def slotBasedEntails(self, source, target):
		"""Slot based inference on the given source and target"""
		assert(isinstance(source, Term))
		assert(isinstance(target, Term))

		if isinstance(source, Atom) or isinstance(target, Atom):
			return None
		if isinstance(source, Negation) and isinstance(target, Nand):
			return
		if isinstance(source, Implication) and isinstance(target, Implication):
			return
		if isinstance(source, AndOr) and isinstance(target, AndOr):
			return
		if isinstance(source, Thresh) and isinstance(target, Thresh):
			return
		if isinstance(source, Negation) and isinstance(target, Negation):
			if not source is target:
				srcset = self.findto(source, "nor")
				tgtset = self.findto(target, "nor")
				if len(srcset) == 1 and len(tgtset) == 1:
					src = srcset.pop()
					tgt = tgtset.pop()
					if isinstance(src, Molecular) and isinstance(tgt, Molecular) and \
						self.adjstable(src.caseframe, tgt.caseframe) and \
						all(map((lambda s: self.validAdjust(s.pos_adj, s.min, s.max,
														self.findto(src, s),
														self.findto(tgt, s))),
								src.caseframe.slots)):
						return target #returns tgtset in original code
				if self.covers(srcset, tgtset):
					return target #returns tgtset in original code
			return None
		if isinstance(source, Molecular) and isinstance(target, Molecular):
			if self.adjustable(source.caseframe, target.caseframe) and \
				 all(map(lambda s : self.validAdjust(s.pos_adj, s.min, s.max,
				 							self.findto(source, s),
											self.findto(target, s)),
						source.caseframe.slots)):
				return target
			return None
		raise TypeError("Inappropriate syntactic type for slot-based inference.")

	def validAdjust(self, adj, min, max, srcfill, tgtfill):
		"""returns True if the srcfill can be adjsted via the adjust type to the tgtfill"""
		if srcfill is set() or tgtfill is set():
			return False
		return (min <= len(tgtfill)) and \
				((max is None) or len(tgtfill) <= max) and \
				{"reduce": (lambda s,t: t.issubset(s)),
 				 "expand": (lambda s,t: s.issubset(t)),
				 None: (lambda s,t: s == t)}.get(adj)(srcfill, tgtfill)

	def covers(self, srcset, tgtset):
		"""returns True if every prop in tgtset is identical to or slotBasedEntailed by
		some proposition in srcset"""
		return all(map((lambda t:
						any(map((lambda s:
						 		s is t or self.slotBasedEntails(s, t)),
							srcset))),
					tgtset))
