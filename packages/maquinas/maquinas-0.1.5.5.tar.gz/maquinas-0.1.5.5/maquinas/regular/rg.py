# Código para Autómata Finito [Determinístic]
from maquinas.exceptions import *
from maquinas.regular.dfa import *
from maquinas.regular.RGParser import RGParser
import maquinas.parser.earley_parser as earley_parser
from ordered_set import OrderedSet
from IPython.core.display import display, HTML
import random
import itertools
import copy
import re

parser=RGParser()

# TODO: Check the left version and the extended

def flat(vals,ini=[]):
    if isinstance(vals,list):
        ini1=flat(vals[0])
        ini2=flat(vals[1])
        return ini1+ini2
    else:
        return [vals]

def flat_tree(tree,acc=[]):
    if len(tree)==2 and tree[-1][-1]==";":
        acc=flat_tree(tree[0])
        acc.append(tree[1])
        return acc
    return [tree]

class RegularGrammar:
    def __init__(self, er_string, S=None, type='right'):
        self.original = er_string
        self.Sigmariginal=er_string
        self.ast=parser.parse(er_string,rule_name="start")
        if len(self.ast)==2:
            self.ast=flat_tree(self.ast[0])+[self.ast[1]]
        else:
            self.ast=flat_tree(self.ast[0])+[self.ast[1],self.ast[2]]
        self.V=set()
        self.sigma=set()
        self.P={}
        replacements={'epsilon':'ε'}
        for p in self.ast:
            head = p[0]
            if head not in self.sigma:
                self.V.add(head.replace('"',''))
        for p in self.ast:
            body=flat(p[2])
            body=[replacements.get(p.replace('"',''),p.replace('"','')) for p in body]
            try:
                self.P[p[0]].append(body)
            except KeyError:
                self.P[p[0]]=[body]
            for val in body:
                if not val in self.V:
                    if not val == "ε":
                        self.sigma.add(val.replace('"',''))
        if S:
            self.S=S
        else:
            self.S=self.ast[0][0]
        for alpha,betas in self.P.items():
            for beta in betas:
                if not alpha in self.V:
                    return "Error"
                if type=="right":
                    if not len(beta)==2 and beta[0] in self.sigma and beta[1] in self.V:
                        return "Error"
                elif type=="left":
                    if not len(beta)==2 and beta[0] in self.sigma and beta[1] in self.V:
                        return "Error"

        tokens=[t for t in self.V]+[t for t in self.sigma]
        tokens.sort(key=len,reverse=True)
        self.re_tokens=re.compile("|".join(["".join([f'[{t_}]' for t_ in t])+"\s*" for t in tokens]))

    def tokenize(self,string):
        return [t.strip() for t in self.re_tokens.findall(string)]

    def parse(self,string):
        tokens=self.tokenize(string)
        if len(tokens) == 0:
            return False,[],{}
        chart=earley_parser.parse(tokens,self.P,self.S,self.sigma)
        forest=earley_parser.extract_forest(self.S,chart,self.sigma,tokens)
        roots=earley_parser.verify_chart(chart,tokens,self.S)
        return roots,chart,forest

    def _reduce_tree(self,tree):
        if len(tree)==1:
            return tree
        head,children=tree
        subtree=[]
        for child in children:
            child_=self._reduce_tree(child)
            if child_[0]['partial']:
                for grandchild in child_[1]:
                    subtree.append(grandchild)
            else:
                subtree.append(child_)
        return (head,subtree)

    def derivation(self,tree):
        tree=self._reduce_tree(tree)
        for i,nodes in enumerate(self.delta_analyse_tree(tree)):
            if i==0:
                string=[("","") for _ in range(nodes[0][1],nodes[0][2])]
            for node in nodes:
                ini,fin=node[1],node[2]
                if ini != fin:
                    pre,label=string[ini]
                    string[ini]=(pre,node[0])
                else:
                    if ini==len(string):
                        string.append(("",""))
                    pre,label=string[ini]
                    string[ini]=(node[0],label)
            yield [l[0]+l[1] for l in string] 

    def print_derivations(self,string,ini=0,fin=None):
        roots,chart,forest=self.parse(string)
        if roots:
            trees=self.extract_trees(forest)
            for i,tree in enumerate(trees):
                if i<=ini:
                    continue
                if i>fin:
                    break
                print("Tree #",ini+i)
                for j,step in enumerate(self.derivation(tree)):
                    if not j:
                        print("".join(step),end="")
                    else:
                        print(" ⇒ ","".join(step),end="\n ")
                print()

    def summary(self):
        info= [
         "No terminal : "+", ".join(self.V),
         "Terminals   : "+", ".join(self.sigma),
         "Start       : "+", ".join(self.S),
         "Productions :\n"+"\n".join(f" {alpha} → {' | '.join(''.join(beta) for beta in betas)}" for alpha,betas in self.P.items())]
        return "\n".join(info) 


    def _delta_analyse_tree(self,tree):
        if len(tree)==2:
            _,children=tree
            children_=[t[0]['label'] for t in children]
            yield children_
            for child in children:
                yield from self._delta_analyse_tree(child)

    def delta_analyse_tree(self,tree):
        tree=self._reduce_tree(tree)
        current,children=tree
        yield [current['label']]
        children_=[t[0]['label'] for t in children]
        yield children_
        for child in children:
            yield from self._delta_analyse_tree(child)

    def print_chart(self,string,chart,pointers=False):
        earley_parser.print_chart(string,chart,pointers=pointers)

    def chart2table(self,string,chart,pointers=False):
        earley_parser.chart2table(string,chart,pointers=pointers)

    def graph_forest(self,forest,**params):
        return earley_parser.graph_forest(forest,**params)

    def extract_forest(self,chart):
        return earley_parser.extract_forest(self.S,chart,self.sigma)

    def extract_trees(self,forest,max_depth=None,max_ancesters=3):
        return earley_parser.extract_trees(forest,self.sigma,max_depth=max_depth,max_ancesters=max_ancesters)

    def graph_tree(self,tree,**params):
        return earley_parser.graph_tree(tree,**params)

    def graph_trees(self,trees,**params):
        return earley_parser.graph_trees(trees,**params)

    def save_trees_img(self,trees,filename,**params):
        dot=self.graph_trees(trees)
        dot.render(filename,format="png",cleanup=True)

    def __str__(self):
        return self.original


