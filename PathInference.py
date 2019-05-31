#SNePS3 Path Based Inference Methods

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
