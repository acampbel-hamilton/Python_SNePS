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
            for arg in self.findto(source, "nor"):
                if (arg.getClass() == 'Conjunction' and
                    self.findto(arg, "and").issubset(
                    self.findto(targe, "andorargs"))):
                        return target
        if isinstance(source, Implication) and isinstance(target, Implication):
            src_ant = source.down_cableset[0]
            src_cq  = source.down_cableset[1]
            tgt_ant = target.down_cableset[0]
            tgt_cq  = target.down_cableset[1]
            if src_ant.issubset(tgt_ant) and tgt_cq.issubset(src_cq):
                return target
        if isinstance(source, AndOr) and isinstance(target, AndOr):
            i = source.min
            j = source.max
            src_set = source.down_cableset[0]
            tgt_set = source.down_cableset[0]
            k = len(src_set) - len(tgt_set)
            if (k >= 0 and tgt_set.issubset(src_set) and
                max(i-k, 0) == target.min and
                min(j, len(tgt_set)) == target.max) or
                (src_set.issubset(tgt_set) and i == targett.min
                and j-k == target.max):
                return target
        if isinstance(source, Thresh) and isinstance(target, Thresh):
            i = source.min
            j = source.max
            src_set = source.down_cableset[0]
            tgt_set = target.down_cableset[0]
            k = len(src_set) - len(tgt_set)
            if (k >= 0 and tgt_set.issubset(src_set) and
                min(i, len(tgt_set)) == target.min and
                max(j-k, i) == target.max) or (src_set.issubset(tgt_set) and
                i-k == target.min and j == target.max):
                return target
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

    def slot_based_derivable(self, target, context, termstack):
        """If the term "target" is entailed in the given context, assert it and
        return set([target]), else return set(). The termstack is a stack of
        propositions that this goal is a subgoal of."""
        for term in target.caseframe.terms:
            if sb_derivable_test(trm, target, context, termstack):
                return set(list(target))
        for cf in target.caseframe.adj_from:
            for trm in cf.terms:
                if sb-sb_derivable_test(trm, target, context, termstack):
                    return set(list(target))
        return set()

    def sb_derivable_test(self, term, target, context, termstack):
        """True if: target is slot-based-entailed by term, and if term is
        asserted in the current context. Else: False"""
        return (term != target and
            term not in termstack and
            self.slotBasedEntails(term, target) and
            self.askif(term, contec, termstack + [target]))
