#PySNePS Symbols

class Symbol(str):
    """a representation of symbols"""
    pass

def Sym(s, sym_tab={}):
    """return a symbol of the given string s if Symbol(s) DNE in sym_tab"""
    if s not in sym_tab:
        sym_tab[s] = Symbol(s)
    return sym_tab[s]

_reduce, _expand, _none = map(Sym, "reduce expand none".split())
