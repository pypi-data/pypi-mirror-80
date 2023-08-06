# Código para Autómata Finito [Determinístic]

from maquinas.exceptions import *
from maquinas.regular.ndfa_e import * 
from maquinas.regular.REParser import REParser

parser=REParser()

class RE:
    def __init__(self, er_string):
        self.original=er_string
        self.ast=parser.parse(er_string,rulne_name="start")

    def __str__(self):
        return self.original

    def _ndfa_e(self, ast):
        if isinstance(ast,list):
            if len(ast)==3:
                fst=self._ndfa_e(ast[0])
                snd=self._ndfa_e(ast[2])
                fa=fst.union(snd)
            elif len(ast)==2:
                if not ast[1]=='*':
                    fst=self._ndfa_e(ast[0])
                    snd=self._ndfa_e(ast[1])
                    fa=fst.concat(snd)
                else:
                    fst=self._ndfa_e(ast[0])
                    fa=fst.kleene()
        else:
            if ast.startswith('"'):
                name=ast[1:-1]
            else:
                name=ast
            if name in ['empty','∅']:
                fa=ndfa_e_empty()
            elif name in ['epsilon','ε']:
                fa=ndfa_e_epsilon()
            else:
                fa=ndfa_e_single_symbol(name)
        return fa

    def ndfa_e(self):
        return self._ndfa_e(self.ast)

