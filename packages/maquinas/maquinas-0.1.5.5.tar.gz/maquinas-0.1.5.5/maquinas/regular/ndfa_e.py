# Código para Autómata Finito No Determinístico con transición epsilon

from maquinas.regular.fa import FiniteAutomaton
from maquinas.exceptions import *

from IPython.core.display import display, HTML
from graphviz import Digraph

epsilon='ε'

## TODO allow no strict
## TODO loaders
## TODO compress links in one
class NonDeterministicFiniteAutomaton_epsilon(FiniteAutomaton):
    def __init__(self, Q=[], sigma=[], q_0=None, A=[], delta=[], force=False):
        super().__init__(Q,sigma,q_0,A,delta,epsilon=True)
        self.e='ε'

    def expansion_epsilon(self,qs):
        qs__=set(q for q in qs)
        change=True
        while change:
            qs_=set()
            for q in qs__:
                qs_.add(q)
                try:
                    qs_.update(self.get_transition(q,self.e))
                except DoesNotExistsTransition:
                    pass
            if len(qs__ ^ qs_)==0:
                change=False
            qs__=qs_
        return qs__

    def delta(self,q,a):
        try:
            return self.get_transition(q,a)
        except DoesNotExistsTransition:
            return set()

    def delta_extended(self,q,w):
        if q is None:
            q=set([self.q_0])
        if len(w)==0:
            return self.expansion_epsilon(q)
        else:
            *w_,a=w
            q_u=set()
            for r in self.delta_extended(q,w_):
                q_u.update(self.delta(r,a))
            return self.expansion_epsilon(q_u)

    def step(self,q,a):
        return self.expansion_epsilon(self.delta(q,a))

    def delta_stepwise(self,w,q=None):
        if q is None:
            q_c=set([self.q_0])
        yield q_c,"",w
        for ix,a in enumerate(w):
            q_c=self.delta(q_c,a)
            q_c=self.expansion_epsilon(q_c)
            yield q_c,a,w[ix+1:]

    def graph(self,q_c=set(),a_c=set(),q_prev=set(),states={},symbols={},format="svg",dpi="60.0",string=None,status=None):
        f=Digraph(comment="af",format=format)
        f.attr(rankdir='LR',dpi=dpi)
        color_state="lightblue2"
        if string:
            l,c,r=string
            f.attr(label=f"<{l} <B>{c}</B> {r}>")
            if len(r)==0:
                if len(self.A.intersection(q_c))>0:
                    color_state="limegreen"
                else:
                    color_state="orangered"
        f.node(name="__initial__",label="",shape="none",height=".0",width=".0")
        for q,q_ in self.Q.map.items():
            if q in self.A:
                shape="doublecircle"
            else:
                shape="circle"
            if q in q_c:
                f.node(name=q,label=states.get(q,q),shape=shape,color=color_state,style="filled")
            else:
                f.node(name=q,label=states.get(q,q),shape=shape)

        f.edge("__initial__",self.q_0)
        for e,info in enumerate(self.items()):
            (q_i,a),q_fs = info
            for q_f in q_fs:
                if (q_i in q_prev and a in a_c) or (q_prev and q_i in q_c and a == 'ε'):
                    f.edge(q_i,q_f,label=symbols.get(a,a),color=color_state,fontcolor=color_state)
                else:
                    f.edge(q_i,q_f,label=symbols.get(a,a))
        return f

    def table(self,symbols={},states={},q_order=None,s_order=None,color_final="#32a852",empty_symbol="∅"):
        if not s_order:
            s_order=list(self.sigma)
            s_order.sort()
        if not q_order:
            q_order=list(self.Q)
            q_order.sort()
        symbs_h="</strong></td><td><strong>".join([symbols.get(q,q) for q in s_order])
        table=f"<table><tr><td></td><td><strong>{symbs_h}</strong></td></tr>"
        for q_i in q_order:
            vals=[]
            initial="⟶" if q_i == self.q_0 else "" 
            final=f'bgcolor="{color_final}"' if q_i in self.A else ""
            vals.append(f"<strong>{initial}{states.get(q_i,q_i)}</strong>")
            for a in s_order:
                try:
                    q_fs=set(states.get(q_f,q_f) for q_f in self[q_i,a])
                    if len(q_fs)>0:
                        vals.append(",".join(q_fs))
                    else:
                        vals.append(empty_symbol)
                except DoesNotExistsTransition:
                    vals.append(empty_symbol)
            row="</td><td>".join(vals)
            table+=f"<tr><td {final}>{row}</td></tr>"
        table+="</table>"
        return display(HTML(table))

    def union(self,other,label_a="ᴬ",label_b="ᴮ"):
        new=NonDeterministicFiniteAutomaton_epsilon()
        new.add_state('q_0',initial=True)
        new.sigma=self.sigma.union(other.sigma)
        new.A=set()
        for q in self.Q:
            name=f"{q}{label_a}"
            new.Q.add(name)
            if q in self.A:
                new.A.add(name)
        for q in other.Q:
            name=f"{q}{label_b}"
            new.Q.add(name)
            if q in other.A:
                new.A.add(name)

        skip=1
        for nq_i,t_ in self.ttable.items():
            for na,nqs_f in t_.items():
                a=self.sigma.items[na]
                na=new.sigma.index(a)
                try:
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i+skip]={}
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])

        skip=len(self.Q)+1
        for nq_i,t_ in other.ttable.items():
            for na,nqs_f in t_.items():
                a=other.sigma.items[na]
                na=new.sigma.index(a)
                try:
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i+skip]={}
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
        new.ttable[0]={}
        new.ttable[0][0]=set([1,skip])
        return new

    def concat(self,other,label_a="ᴬ",label_b="ᴮ",):
        new=NonDeterministicFiniteAutomaton_epsilon()
        new.sigma=self.sigma.union(other.sigma)
        new.A=set()
        for q in self.Q:
            name=f"{q}{label_a}"
            if q==self.q_0:
                new.set_initial_state(name)
            new.Q.add(name)
        for q in other.Q:
            name=f"{q}{label_b}"
            new.Q.add(name)
            if q in other.A:
                new.A.add(name)

        skip=0
        for nq_i,t_ in self.ttable.items():
            for na,nqs_f in t_.items():
                a=self.sigma.items[na]
                na=new.sigma.index(a)
                try:
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i+skip]={}
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])

        skip=len(self.Q)
        for nq_i,t_ in other.ttable.items():
            for na,nqs_f in t_.items():
                a=other.sigma.items[na]
                na=new.sigma.index(a)
                try:
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i+skip]={}
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])

        for q in self.A:
            nq=self.Q.index(q)
            if nq in new.ttable:
                if 0 in new.ttable[nq]:
                    new.ttable[nq][0].add(skip)
                else:
                    new.ttable[nq][0]=set([skip])
            else:
                new.ttable[nq]={}
                new.ttable[nq][0]=set([skip])
        return new

    def kleene(self,label_a="ᴬ"):
        new=NonDeterministicFiniteAutomaton_epsilon()
        new.add_state('q_0',initial=True)
        new.sigma=self.sigma 
        new.A=set()
        for q in self.Q:
            name=f"{q}{label_a}"
            new.Q.add(name)
        new.add_state('q_f')
        new.A.add('q_f')
        nq_f=len(new.Q)-1

        skip=1
        for nq_i,t_ in self.ttable.items():
            for na,nqs_f in t_.items():
                a=self.sigma.items[na]
                na=new.sigma.index(a)
                try:
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
                except KeyError:
                    new.ttable[nq_i+skip]={}
                    new.ttable[nq_i+skip][na]=set([nq+skip for nq in nqs_f])
        
        new.ttable[0]={}
        new.ttable[0][0]=set([1,nq_f])
        new.ttable[nq_f]={}
        new.ttable[nq_f][0]=set([0])

        for q in self.A:
            nq=self.Q.index(q)
            if nq+skip in new.ttable:
                if 0 in new.ttable[nq+skip]:
                    new.ttable[nq+skip][0].add(nq_f)
                else:
                    new.ttable[nq+skip][0]=set([nq_f])
            else:
                new.ttable[nq+skip]={}
                new.ttable[nq+skip][0]=set([nq_f])

        return new



def ndfa_e_single_symbol(symbol):
    fa=NonDeterministicFiniteAutomaton_epsilon()
    fa.add_transition("q_0",symbol,["q_1"])
    fa.set_initial_state("q_0")
    fa.set_aceptors(['q_1'])
    return fa

def ndfa_e_epsilon():
    fa=NonDeterministicFiniteAutomaton_epsilon()
    fa.add_transition("q_0",epsilon,["q_0"])
    fa.set_initial_state("q_0")
    fa.set_aceptors(['q_0'])
    return fa

def ndfa_e_empty(symbol):
    fa=NonDeterministicFiniteAutomaton_epsilon()
    fa.set_initial_state("q_0")
    fa.set_aceptors([])
    return fa
