#SNePS3 Slot Based Inference Methods

class SlotInference:
	"""contains methods for slot based inference for use in SNePS class in Network"""

	def slotBasedEntails(self, source, target):
        """Slot based inference on the given source and target"""
        assert(isinstance(source, Term))
        assert(isinstance(target, Term))

        if isinstance(source, Atom) or isinstance(target, Atom):
            return
        if isinstance(source, Negation) and isinstance(target, Nand):
            return
        if isinstance(source, Implication) and isinstance(target, Implication):
            return
        if isinstance(source, AndOr) and isinstance(target, AndOr):
            return
        if isinstance(source, thresh) and isinstance(target, Thresh):
            return
        if isinstance(source, Negation) and isinstance(target, Negation):
            return
        if isinstance(source, Molecular) and isinstance(target, Molecular):
            # if self.adjustable(source.caseframe, target.caseframe) and \
            #     all(map(lambda s : self.validAdjust(x.pos_adj, x.min, x.max, )))
            return
        raise TypeError("Inappropriate syntactic type for slot-based inference.")
