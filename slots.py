#SNePs3 slot class definition

class Slot:
    name = None
    type = None
    pos_adj = None
    neg_adj = None
    min = 1
    max = None

    def __init__(self, path, f_path_fn, b_path_fn):
        self.path = path
        self.f_path_fn = f_path_fn
        self.b_path_fn = b_path_fn
