# Código para Autómata Finito [Determinístic]

from maquinas.regular.fa import FiniteAutomaton
from maquinas.exceptions import *
from IPython.core.display import display, HTML
from graphviz import Digraph

class DeterministicFiniteAutomaton(FiniteAutomaton):
    def __init__(self, Q=[], sigma=[], q_0=None, A=[], delta={}, force=False):
        super().__init__(Q,sigma,q_0,A,delta)

    def delta(self,q,a):
        return self.get_transition(q,a)

    def delta_extended(self,q,w):
        if q is None:
            q=self.q_0
        if len(w)==0:
            return q
        else:
            *w_,a=w
            return self.delta(self.delta_extended(q,w_),a)

    def delta_stepwise(self,w,q=None):
        if q is None:
            q_c=self.q_0
        yield q_c,"",w
        for ix,a in enumerate(w):
            q_c=self.delta(q_c,a)
            yield q_c,a,w[ix+1:]

    def step(self,q,a):
        return self.delta(q,a)

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
            (q_i,a),q_f = info
            if q_i in q_prev and a in a_c:
                f.edge(q_i,q_f,label=symbols.get(a,a),color=color_state,fontcolor=color_state)
            else:
                f.edge(q_i,q_f,label=symbols.get(a,a))
        return f

    def table(self,symbols={},states={},q_order=None,s_order=None,color_final="#32a852"):
        if not s_order:
            s_order=list(self.sigma)
            s_order.sort()
        if not q_order:
            q_order=list(self.Q)
            q_order.sort()
        symbs_h="</strong></td><td><strong>".join([states.get(q,q) for q in s_order])
        table=f"<table><tr><td></td><td><strong>{symbs_h}</strong></td></tr>"
        for q_i in q_order:
            vals=[]
            initial="⟶" if q_i == self.q_0 else "" 
            final=f'bgcolor="{color_final}"' if q_i in self.A else ""
            vals.append(f"<strong>{initial}{states.get(q_i,q_i)}</strong>")
            for a in s_order:
                try:
                    q_f=self[q_i,a]
                    vals.append(states.get(q_f,q_f))
                except DoesNotExistsTransition:
                    vals.append("")
            row="</td><td>".join(vals)
            table+=f"<tr><td {final}>{row}</td></tr>"
        table+="</table>"
        return display(HTML(table))
