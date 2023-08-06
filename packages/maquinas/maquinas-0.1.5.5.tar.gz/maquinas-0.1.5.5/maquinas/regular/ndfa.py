# Código para Non Deterministic Finete Automaton

from maquinas.regular.fa import FiniteAutomaton
from maquinas.exceptions import *
from IPython.core.display import display, HTML
from graphviz import Digraph

class NonDeterministicFiniteAutomaton(FiniteAutomaton):
    def __init__(self, Q=[], sigma=[], q_0=None, A=[], delta={}, force=False):
        super().__init__(Q,sigma,q_0,A,delta)

    def delta(self,q,a):
        try:
            return self.get_transition(q,a)
        except DoesNotExistsTransition:
            return set()

    def delta_extended(self,q,w):
        if q is None:
            q=set([self.q_0])
        if len(w)==0:
            return q
        *w_,a=w
        q_u=set()
        for r in self.delta_extended(q,w_):
            q_u.update(self.delta(r,a))
        return q_u

    def step(self,q,a):
        return self.delta(q,a)

    def delta_stepwise(self,w,q=None):
        if q is None:
            q_c=set([self.q_0])
        yield q_c,"",w
        for ix,a in enumerate(w):
            q_c=self.get_transition(q_c,a)
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
                if q_i in q_prev and a in a_c:
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
