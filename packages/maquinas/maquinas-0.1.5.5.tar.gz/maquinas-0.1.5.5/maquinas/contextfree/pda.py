# Base class for Finite Machines
from maquinas.exceptions import *
from collections import defaultdict
from ordered_set import OrderedSet
import re
import tempfile
import os

from PIL import Image
from IPython.core.display import display, HTML
from graphviz import Digraph

re_queque=re.compile(r'(Z\d+|epsilon|_[^_]+_|\w)')

class PushDownAutomaton():
    """Class for finite automaton"""

    def __init__(self, Q=[], sigma=[], gamma=[], q_0=None,Z_0=None,A=[], delta={}, force=False):
        self.sigma=OrderedSet()
        self.sigma.add('ε')
        self.gamma=OrderedSet()
        self.gamma.add('ε')
        Z_0=self.set_initial_qsymbol(Z_0)
        self.gamma.add(Z_0)
        self.sigma.update(sigma)
        self.gamma.update([self._filter(g) for g in gamma])
        self.Q=OrderedSet(Q)
        self.set_initial_state(q_0)
        self.set_aceptors(A,force=force)
        self.ttable={}
        for (q_i,a,z),qs in delta:
            # Replace Z_0 or Z0 by Z₀ or epsilon for ε
            self.add_transition(q_i,self._filter(a),self._filter(z),[(q,(self._filter(t) for t in self.tokens(r))) for (q,r) in qs])

    def __getitem__(self,key):
        q,a,z=key
        return self.get_transition(q,a,z)

    def _nstate(self,q):
        return self.Q.index(q)

    def _nsymbol(self,a):
        return self.sigma.index(a)

    def _filter(self,z):
        if z in ['Z0','Z_0']:
            z='Z₀'
        if z in ['epsilon']:
            z='ε'
        return z

    def _nqsymbol(self,z):
        return self.gamma.index(self._filter(z))

    def _state(self,nq):
        return self.Q.items[nq]

    def _symbol(self,na):
        return self.sigma.items[na]

    def _qsymbol(self,nz):
        return self.gamma.items[nz]

    def _status(self,status,states={},symbols={}):
        return "|".join(f"{states.get(self._state(s),self._state(s))},\
            {''.join(symbols.get(self._qsymbol(q),self._qsymbol(q)) for q in qs)}]" for (s,qs) in status)

    def states(self):
        return list(self.Q)

    def symbols(self):
        return list(self.sigma)

    def qsymbols(self):
        return list(self.gamma)

    def tokens(self,r):
        return re_queque.findall(r)

    def _transition(self,nq_i,na,nz,nq_f,nq):
        return (self._state(nq_i),self._symbol(na),self._qsymbol(nz)),(self._state(nq_f),[self._qsymbol(nr) for nr in nq])

    def __setitem__(self,key,value):
        q,a,z=key
        queue,q_f=value
        return self.add_transition(q,a,z,q_f,queue)

    def _get_transition(self,nq,na,nz):
        try:
            return self.ttable[nq][na][nz]
        except KeyError:
            return set()

    def expansion_epsilon(self,qs):
        qs__=defaultdict(set)
        qs__.update(qs)
        change=True
        expanded=False
        while change:
            qs_=defaultdict(set)
            qs_.update(qs__)
            qs_.update(self.delta(qs__,'ε'))
            if len(set(qs__.keys()) ^ set(qs_.keys()))==0:
                change=False
            else:
                expanded=True
            qs__=qs_
        return qs__,expanded

    def delta_extended(self,states,w):
        if states is None:
            states=defaultdict(set)
            states[(self._nstate(self.q_0),(1,))]=()
        if len(w)==0:
            res,_=self.expansion_epsilon(states)
            return res
        else:
            *w_,a=w
            q_u=defaultdict(set)
            for k,v in self.delta_extended(states,w_).items():
                r_={k:v}
                q_u.update(self.delta(r_,a))
            res,_ = self.expansion_epsilon(q_u)
            return res

    def delta(self,states,a):
        states_=defaultdict(set)
        for nq,nstack in states:
            na=self._nsymbol(a)
            nz=nstack[0]
            stack=nstack[1:]
            qs=self._get_transition(nq,na,nz)
            for nq_f,r in qs:
                # pop
                if len(r)==1 and r[0]==0:
                    states_[(nq_f,stack)].add(nz)
                # push
                else:
                    states_[(nq_f,r+stack)].add(nz)
        return states_

    def delta_stepwise(self,w,q=None,mark_finished=False):
        if q is None:
            states=defaultdict(set)
            states[(self._nstate(self.q_0),(1,))]=()
        if mark_finished:
            yield states,"",w,len(w)==0
        else:
            yield states,"",w
        for ix,a in enumerate(w):
            states=self.delta(states,a)
            if len(w[ix+1:])>0:
                states,expanded=self.expansion_epsilon(states)
                if mark_finished:
                    yield states,a,w[ix+1:],False
                else:
                    yield states,a,w[ix+1:]
            else:
                epsilon_states=self.delta(states,'ε')
                if mark_finished:
                    yield states,a,w[ix+1:],len(epsilon_states)==0
                else:
                    yield states,a,w[ix+1:]
                if len(epsilon_states)>0:
                    if mark_finished:
                        yield epsilon_states,'ε',w[ix+1:],True
                    else:
                        yield epsilon_states,'ε',w[ix+1:]


    def items(self):
        for nq_i,t_ in self.ttable.items():
            for na,t__ in t_.items():
                for nz,nq_fs in t__.items():
                    for (nq_f,nr) in nq_fs:
                        yield self._transition(nq_i,na,nz,nq_f,nr)

    def step(self,states,a):
        res,_=self.expansion_epsilon(self.delta(states,a))
        return res

    def get_transition(self,q,a,z):
        return self._state(self._get_transition(self._nstate(q),self._nsymbol(a),self._nqsymbol(z)))

    def add_transition(self,q_i,a,z,qs):
        nq_i=self.add_state(q_i)
        na=self.add_symbol(a)
        nz=self.add_qsymbol(z)
        nqs=[(self._nstate(q_f),tuple([self._nqsymbol(s) for s in r])) for q_f,r in qs ]
        if not nq_i in self.ttable:
            self.ttable[nq_i]={}
        if not na in self.ttable[nq_i]:
            self.ttable[nq_i][na]={}
        if not nz in self.ttable[nq_i][na]:
            self.ttable[nq_i][na][nz]=set()
        self.ttable[nq_i][na][nz].update(nqs)

    def valitate(self):
        pass

    def add_state(self,q,initial=False):
        if initial:
            self.q_0=q
        if isinstance(q,(set,list)):
            return set(self.Q.add(q_) for q_ in q)
        else:
            return self.Q.add(q)

    def add_next_state(self,initial=False):
        max_ix=len(self.Q)
        while f"q_{max_ix}" in self.Q:
            max_ix+=1
        q=f"q_{max_ix}"
        self.Q.add(q)
        if initial:
            self.q_0=q
        return q,max_ix

    def add_symbol(self,a):
        return self.sigma.add(a)

    def add_qsymbol(self,z):
        return self.gamma.add(z)

    def set_initial_state(self,q,force=False):
        if q is None:
            self.q_0=None
            return None
        if force and not q in self.Q:
            self.add_state(q)
        self.q_0=q

    def set_initial_qsymbol(self,z,force=False):
        if z is None:
            self.Z_0='Z₀'
        else:
            if force and not z in self.gamma:
                self.gamma.add(z)
            self.Z_0=z
        return self.Z_0

    def get_initial_state(self):
        return self.q_0

    def autorename(self,start=0,avoid=[],copy=True):
        replacements=[(q,f'q_{start+ix}') for q,ix in self.Q.map.items()]
        ix=len(self.Q)+start
        new_A=set()
        while len(replacements)>0:
            old,new=replacements.pop(0)
            if new == old:
                if old in self.A:
                    new_A.add(new)
                if old == self.q_0:
                    self.q_0=new
                continue
            elif new in self.Q or new in avoid:
                replacements.append((old,f'q_{ix}'))
                ix+=1
            else:
                self.replace_state(old,new)
                if old in self.A:
                    new_A.add(new)
                if old == self.q_0:
                    self.q_0=new
        self.A=new_A

    def remove_states(self,states):
        Q_=OrderedSet()
        ttable_={}
        for q in self.Q:
            if not q in states:
                Q_.add(q)

        ttable_={}
        for nq_i,tt in self.ttable.items():
            q_i=self.Q.items[nq_i]
            if q_i in states:
                continue
            nq_i_=Q_.map[q_i]
            for na,nqs in tt.items():
                if isinstance(nqs,set):
                    qs=[self.Q.items[q] for q in nqs ]
                    res=set([Q_.index(q) for q in qs if not q in states])
                else:
                    q=self.Q.items[nqs]
                    if q in states:
                        continue
                    res=Q_.index(q)
                try:
                    ttable_[nq_i_][na]=res
                except KeyError:
                    ttable_[nq_i_]={}
                    ttable_[nq_i_][na]=res
        self.Q=Q_
        self.ttable=ttable_

    def remove_sink_states(self):
        Q_=OrderedSet()
        idx_remove=set()
        for nq,q in enumerate(self.Q):
            if not q in self.A:
                if not nq in self.ttable:
                    idx_remove.add(nq)
                    continue
            destination=set()
            # If state is loopy
            for na,a in enumerate(self.sigma):
                try:
                    res=self.ttable[nq][na]
                except KeyError:
                    continue
                if isinstance(res,set):
                    destination=destination | res
                else:
                    destination.add(res)
            if len(destination)==1 and nq in destination and q not in self.A:
                idx_remove.add(nq)
                continue
            Q_.add(q)

        ttable_={}
        for nq_i_,q_i in enumerate(Q_):
            nq_i=self.Q.map[q_i]
            for na,a in enumerate(self.sigma):
                try:
                    res=self.ttable[nq_i][na]
                except KeyError:
                    continue
                if isinstance(res,set):
                    qs=[self.Q.items[nq] for nq in res if not nq in idx_remove]
                    res=set([Q_.index(q) for q in qs])
                else:
                    if res in idx_remove:
                        continue
                    q=self.Q.items[res]
                    res=Q_.index(q)
                try:
                    ttable_[nq_i_][na]=res
                except KeyError:
                    ttable_[nq_i_]={}
                    ttable_[nq_i_][na]=res
        self.Q=Q_
        self.ttable=ttable_

    def get_initial_state(self):
        return self._get_state_label(self._get_initial_state())

    def set_aceptors(self,A,force=False):
        if force:
            self.add_state(A)
        self.A=set(A)

    def stepStatus(self,status):
        if status.state is None:
            states=set([(self._nstate(self.q_0),(1,))])
        else:
            states=status.state

        a=status.get_symbol_tape()
        states=self.step(states,a)
        status.position+=1
        status.step+=1
        status.state=states

    def accept(self,states):
        final=set([self._state(q) for q,s in states])
        if bool(final.intersection(self.A)):
            return True
        return False

    def replace_symbol(self,old,new):
        ix=self.sigma.index(old)
        del self.sigma.map[old]
        self.sigma.map[new]=ix
        self.sigma.items[ix]=new

    def replace_state(self,old,new):
        if new in self.Q:
            raise AlreadyExistsState(new)
        ix=self.Q.index(old)
        del self.Q.map[old]
        self.Q.map[new]=ix
        self.Q.items[ix]=new
        if old == self.q_0:
            self.q_0=new

    def add_error_state(self,e_label="q_E"):
        self.add_state(e_label)
        ne=self.Q.index(e_label)
        for nq,q in enumerate(self.Q):
            for na,a in enumerate(self.sigma):
                if not nq in self.ttable:
                    self.ttable[nq]={}
                    self.ttable[nq][na]=ne
                elif not na in self.ttable[nq]:
                    self.ttable[nq][na]=ne

    def reachable_states(self):
        # https://en.wikipedia.org/wiki/DFA_minimization#Unreachable_states
        reachable=set([self.q_0])
        new=set([self.q_0])
        while len(new)>0:
            temp=set()
            for q in new:
                for a in self.sigma:
                    try:
                        states=self.get_transition(q,a)
                        if isinstance(states,set):
                            temp.update(states)
                        else:
                            temp.add(states)
                    except DoesNotExistsTransition:
                        pass
            new=temp.difference(reachable)
            reachable=reachable.union(new)
        return reachable

    def unreachable_states(self):
        return set(self.Q.difference(self.reachable_states()))

    def remove_unreachable(self):
        self.remove_states(self.unreachable_states())


    def save_img(self,filename,q_c=set(),a_c=set(),q_prev=set(),symbols={},states={},format='svg',dpi="90.0",string=None,finished=False):
        dot=self.graph(q_c=q_c,a_c=a_c,q_prev=q_prev,symbols=symbols,states=states,format=format,dpi=dpi,string=string,finished=finished)
        dot.render(filename,format="png",cleanup=True)

    def states2string(self,states):
        return " | ".join(["{}, {}]".format(self._state(s), "".join([ self._qsymbol(q) for q in qs])) for s,qs in states ])

    def summary(self):
        info= [
         "States  : "+", ".join(self.states()),
         "Sigma   : "+", ".join(self.symbols()),
         "Gamma   : "+", ".join(self.qsymbols()),
         "Initial : "+self.q_0,
         "Aceptors: "+", ".join(self.A),
         "Transitions:\n"+"\n".join(f" {q_i},{a},{z}/{''.join(r)} → {q_f}" for (q_i,a,z),(q_f,r) in self.items())]
        return "\n".join(info) 

    def graph(self,q_c=set(),a_c=set(),q_prev=set(),states={},symbols={},format="svg",dpi="60.0",string=None,stack=[],status=None,one_arc=True,finished=False):
        if len(q_c)==0:
            states_=defaultdict(set)
            states_[(self._nstate(self.q_0),(1,))]=()
        else:
            states_=q_c

        f=Digraph(comment="PDAs",format=format)
        f.attr(rankdir='LR',dpi=dpi)
        for i,((q_c_,stack),zetas) in enumerate(states_.items()):
            stack=[self._qsymbol(s) for s in stack]
            q_c_=set([self._state(q_c_)])
            with f.subgraph(name=f'cluster_{i}') as f_:
                self._graph(f_,
                    i=i,
                    q_c=q_c_,
                    a_c=a_c,
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    dpi=dpi,
                    format=format,
                    stack=stack,
                    zetas=zetas,
                    finished=finished,
                    status=status,
                    string=string,
                    one_arc=one_arc)
        return f

    def _graph(self,f,i=0,q_c=set(),a_c=set(),q_prev=set(),states={},symbols={},format="svg",dpi="60.0",string=None,stack=[],status=None,one_arc=True,zetas=[],finished=False):
        label_string=None
        label_stack=None
        if status==None:
            color_state="lightblue2"
        elif status and len(self.A.intersection(q_c))>0:
            color_state="limegreen"
        else:
            color_state="orangered"

        if string:
            l,c,r=string
            label_string=f"<TR><TD>{l}</TD> <TD><B>{c}</B></TD> <TD>{r}</TD></TR>"
            if finished and len(r)==0:
                if len(self.A.intersection(q_c))>0:
                    color_state="limegreen"
                else:
                    color_state="orangered"
        if stack:
            label_middle="".join([symbols.get(r_,r_) for r_ in stack])
            label_stack=f"<TR><TD ALIGN='RIGHT'>{label_middle}</TD></TR>"

        f.attr(style='invis',labelloc="b")
        if label_string and label_stack:
            f.attr(label=f"< <TABLE BORDER='0' ><TR><TD><TABLE BORDER='1' CELLBORDER='0' SIDES='TBR'>{label_stack}</TABLE></TD></TR><TR><TD><TABLE BORDER='0'>{label_string}</TABLE></TD></TR></TABLE>>")
        elif label_stack:
            f.attr(label=f"< <TABLE BORDER='1' CELLBORDER='0' SIDES='TBR'>{label_stack}</TABLE>>")

        for q,_ in self.Q.map.items():
            if q in self.A:
                shape="doublecircle"
            else:
                shape="circle"
            if q in q_c:
                f.node(name=f'{q}_{i}',label=states.get(q,q),shape=shape,color=color_state,style="filled")
            else:
                f.node(name=f'{q}_{i}',label=states.get(q,q),shape=shape)

        edges=defaultdict(list)
        for e,info in enumerate(self.items()):
            (q_i,a,z),(q_f,r) = info
            r_=[symbols.get(r_,r_) for r_ in r]
            if (q_f in q_c and q_i in q_prev) and (a in a_c or a=="ε") and (self._nqsymbol(z) in zetas):
                edges[(f'{q_i}_{i}',f'{q_f}_{i}')].append((f'{symbols.get(a,a)},{symbols.get(z,z)}/{"".join(r_)}',True))
            else:
                edges[(f'{q_i}_{i}',f'{q_f}_{i}')].append((f'{symbols.get(a,a)},{symbols.get(z,z)}/{"".join(r_)}',False))

        for (q_i,q_f),labels in edges.items():
            if one_arc:
                tags=[]
                colored_=False
                for label,colored in labels:
                    if colored:
                        colored_=True
                        tags.append(f'<FONT color="{color_state}">{label}</FONT>')
                    else:
                        tags.append(f'{label}')
                tags=f'< {"<BR/>".join(tags)} >'
                if colored_:
                    f.edge(q_i,q_f,label=tags,labelloc='b',color=color_state)
                else:
                    f.edge(q_i,q_f,label=tags,labelloc='b')
            elif not one_arc:
                for label,colored in labels:
                    if colored:
                        f.edge(q_i,q_f,label=label,labelloc='b',color=color_state,fontcolor=color_state)
                    else:
                        f.edge(q_i,q_f,label=label,labelloc='b')
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
                    labels=[]
                    for z,info in self.ttable[self._nstate(q_i)][self._nsymbol(a)].items():
                        for q_f,r in info:
                            r_=[symbols.get(self._qsymbol(r_),self._qsymbol(r_)) for r_ in r]
                            labels.append(f'{symbols.get(self._qsymbol(z),self._qsymbol(z))}/{"".join(r_)}→{self._state(q_f)}')
                    vals.append("<br/>".join(labels))
                except KeyError:
                    vals.append(empty_symbol)
            row="</td><td>".join(vals)
            table+=f"<tr><td {final}>{row}</td></tr>"
        table+="</table>"
        return display(HTML(table))

    def save_gif(self,w,filename="pda.gif",symbols={},states={},dpi="300",show=True,loop=0,duration=500):
        dirpath = tempfile.mkdtemp()
        i=0
        images=[]
        q_prev=set()
        max_images_height=1
        for q,a,w_,finished in self.delta_stepwise(w,mark_finished=True):
            filename_=os.path.join(dirpath,f'{i}')
            fin=len(w)-len(w_)
            if fin:
                processed=w[:fin-1]
            else:
                processed=" "
            a = a if a else " "
            g=self.save_img(filename_,q_c=q,a_c=set([a]),q_prev=q_prev,finished=finished,
                    symbols=symbols,states=states,
                    dpi=dpi,string=(processed,a,w_))
            q_prev=set([self._state(q_c) for q_c,_ in q])
            im=Image.open(filename_+".png")
            width, height = im.size
            max_images_height=max(max_images_height,height)
            images.append(im)
            i+=1
            filename_=os.path.join(dirpath,f'{i}')
            g=self.save_img(filename_,q_c=q,
                    symbols=symbols,dpi=dpi,string=(processed,a,w_),finished=finished)
            im=Image.open(filename_+".png")
            if i==0 or finished:
                images.append(im)
                images.append(im)
                images.append(im)
                images.append(im)
            images.append(im)
            i+=1
        for i,im in enumerate(images):
            im2 = Image.new('RGB', (width, max_images_height), (255, 255, 255))
            width, height = im.size
            im2.paste(im)
            images[i]=im2

        images[0].save(filename,
                save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=loop)
        if show:
            return HTML(f'<img src="{filename}">')
        else:
            return

