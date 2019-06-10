#SNePS3 Path Based Inference Methods
# A mix-in
class PathInference:
	"""contains methods for path based inference for use in Network"""

	def buildPathFn(self, path):
		"""Given a path expr, returns a function which will traverse that path"""
		if path[0] == "compose":
			return lambda x : composeHelper(reverse(path[1:]))
			#return function that doesnt depend on input?!?

	def composeHelper(self, pathElts):
		"""Given a list of path element in reverse order, return a function which
		 will traverse a path in the original order"""
		if pathElts[1:] != []:
			return buildPathFn(pathElts[0])(composeHelper(pathElts[1:]))
		return buildPathFn(pathElts[0])

	def asserted_members(termSet, ctxt):
		"""Given a set of terms, returns the set of terms asserted in the context"""
		return filter(lambda term: term in (ctxt.hyps + ctxt.der), termSet)

	def definePath(self, slotname, pathexpr):
		"""Given a slot name and a path expression, generate the functions that
		will compute that path and its converse, and store them in the slot."""
		aslot = self.findSlot(slotname)

		aslot.path = pathexpr
		aslot.b_path_fn = build_path_fn(converse(pathexpr))
		aslot.f_path_fn = build_path_fn(pathexpr)

	def build_path_fn(self, path):
		"""Given a path expression, returns the function that will traverse that path"""

		# if isinstance(path, list):
		# 	switch = {
		# 		compose: 	`(lambda (x) ,(compose-helper (reverse (rest path))))
		# 		or:			`(lambda (x) ,(or-helper (rest path)))
		# 		and: 		`(lambda (x) ,(and-helper (rest path)))
		# 		kstar:		(assert (null (cddr path)) (path)
		# 	    			"kstar must have only one path argument in ~S" path)
		# 	  				`(lambda (x) (f* x ,(build-path-fn (second path))))
		# 		kplus:		(assert (null (cddr path)) (path)
		# 				    "kplus must have only one path argument in ~S" path)
		# 					`(lambda (x) (f+ x ,(build-path-fn (second path)))))
		# 		converse:	(build-path-fn (converse (second path)))
		# 		irreflexive-restrict:
		# 					 `(lambda (x) (set:difference  (funcall ,(build-path-fn (second path)) x) x))
		# 		restrict:
		# 					(assert (and (= (length path) 3)) (path)
		# 				    "restrict must have two arguments, a path, and an atomicwft in ~S" path)
		# 					`(lambda (x)
		# 				     (set:new-set
		# 				      :items
		# 				      (set:loopset for trm in x
		# 						   if (memberOrVar ',(third path)
		# 								   (funcall ,(build-path-fn (second path))
		# 									    (set:singleton trm)))
		# 						   collect trm))))
		# 	}
		# 	switch.get( (intern (first path) :snip),  (error "Unrecognized path expression operator: ~S" (first path))  )
		# elif (equal '! (intern path :snip):
		# 	`(lambda (x) (asserted-members x (ct::currentContext)))
		# else:
		# 	rev = rev-slotname(path)
		# 	if rev:
		# 		 `(lambda (x) (get-froms x (quote ,rev)))
		# 	 else:
		# 		 `(lambda (x) (get-tos x (quote ,path)))









		# compile name &optional definition => function, warnings-p, failure-p
			# name: nil
			# definition: a lambda expression or a function
			# function: the function-name, or a compiled function

		# intern string &optional package => symbol
			# enters a symbol named string into package
