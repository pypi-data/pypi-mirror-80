# Base class for Finite Machines
from maquinas.exceptions import *
from ordered_set import OrderedSet
import re
import tempfile
import os
from collections import defaultdict

from PIL import Image
from IPython.core.display import display, HTML
from graphviz import Digraph

re_tape=re.compile(r'(\[B\]|epsilon|"[^"]+"|\w)')

class TuringMachine():
    """Turing machine"""

    def __init__(self, Q=[], sigma=[], gamma=[], B='𝖁',q_0=None,A=[], delta={}, force=False):
        self.sigma=OrderedSet()
        self.sigma.add('ε')
        self.B=B
        self.i=0
        self.gamma=OrderedSet()
        self.gamma.add(self.B)
        self.gamma.update([self._filter(g) for g in gamma])
        self.gamma.update(sigma)
        self.sigma.update(sigma)
        self.Q=OrderedSet(Q)
        self.set_initial_state(q_0)
        self.set_aceptors(A,force=force)
        self.ttable={}
        for (q_i,a),qs in delta:
            self.add_transition(q_i,self._filter(a),[(q_f,self._filter(a),self._ndir(Dir)) for q_f,a,Dir in qs])
        self.curr=0
        self.tape=((),(self.B))

    def __getitem__(self,key):
        q,a=key
        return self.get_transition(q,a)

    def _nstate(self,q):
        return self.Q.index(q)

    def _nsymbol(self,a):
        return self.sigma.index(a)

    def _filter(self,t):
        if t == '[B]':
            return self.B
        elif t.lower() == 'blank':
            return self.B

        return t

    def _dir(self,d):
        if d == 1:
            return 'R'
        elif d == -1:
            return 'L'
        else:
            return 'N'

    def _ndir(self,d):
        if d == 'R':
            return 1
        elif d == 'L':
            return -1
        else:
            return 0

    def _ntsymbol(self,t):
        return self.gamma.index(self._filter(t))

    def _state(self,nq):
        return self.Q.items[nq]

    def _symbol(self,na):
        return self.sigma.items[na]

    def _tsymbol(self,nz):
        return self.gamma.items[nz]

    def _status(self,status,states={},symbols={}):
        return "|".join(f"{states.get(self._state(s),self._state(s))}" for s,_,_,_ in status)

    def states(self):
        return list(self.Q)

    def symbols(self):
        return list(self.sigma)

    def tsymbols(self):
        return list(self.gamma)

    def tokens(self,r):
        return re_tape.findall(r)

    def _transition(self,nq_i,nt,nq_f,nt_,Dir):
        return (self._state(nq_i),self._tsymbol(nt)),(self._state(nq_f),self._tsymbol(nt_),Dir)

    def __setitem__(self,key,value):
        q,t=key
        q_f,t_,Dir=value
        return self.add_transition(q,t,q_f,t_,Dir)

    def _get_transition(self,nq,nt):
        try:
            return self.ttable[nq][nt]
        except KeyError:
            return set()

    def delta(self,states):
        states_=set()
        for nq,tn,tp,(c,a) in states:
            if c<0:
                try:
                    na=tn[-c]
                except IndexError:
                    tn=tn+tuple(self.B for _ in range(len(tn),1-c))
                    na=tn[-c]
            else:
                try:
                    na=tp[c]
                except IndexError:
                    tp=tp+tuple(self.B for _ in range(len(tp),c+1))
                    na=tp[c]
            qs=self._get_transition(nq,na)
            for nq_f,t_,Dir in qs:
                if c<0:
                    tn=list(tn)
                    tn[c]=t_
                elif c>=0:
                    tp=list(tp)
                    tp[c]=t_
                c=c+Dir
                if c<0 and len(tn)<=abs(c):
                    tn.append(self._ntsymbol(self.B))
                if c>=0 and len(tp)<=abs(c):
                    tp.append(self._ntsymbol(self.B))
                states_.add((nq_f,tuple(tn),tuple(tp),(len(tn)+c,self._tsymbol(na))))
        return states_

    def _tape(self,nt,pt):
        return [t for t in reversed(nt)]+[t for t in pt]

    def delta_stepwise(self,w,q=None,max_steps=0):
        if q is None:
            states=set([(self._nstate(self.q_0),(),tuple(self._ntsymbol(a) for a in w),(0,""))])
            yield states
        steps=0
        while len(states)>0 and len(set([q for q,_,_,_ in states]).intersection(self.A))==0:
            states=self.delta(states)
            steps+=1
            yield states
            if max_steps and steps>=max_steps:
                break

    def delta_extended(self,states,w,max_steps=None):
        if states is None:
            states=set([(self._nstate(self.q_0),(),tuple(self._ntsymbol(a) for a in w),(0,""))])
        steps=0
        while len(states)>0 and len(set([self._state(q) for q,_,_,_ in states]).intersection(self.A))==0:
            states=self.delta(states)
            steps+=1
            res=[(q,tn,tp,c) for q,tn,tp,c in states]
            if max_steps and steps>=max_steps:
                return []
        return res

    def items(self):
        for nq_i,val in self.ttable.items():
            for nt,nq_fs in val.items():
                for (nq_f,nt_,Dir) in nq_fs:
                    yield self._transition(nq_i,nt,nq_f,nt_,Dir)

    def step(self,states):
        return self.delta(states)

    def get_transition(self,q,a):
        return self._state(self._get_transition(self._nstate(q),self._nsymbol(a)))

    def add_transition(self,q_i,t,qs):
        nq_i=self.add_state(q_i)
        nt=self.add_tsymbol(t)
        qs=[(self._nstate(q),self._ntsymbol(t),Dir) for q,t,Dir in qs]
        if not nq_i in self.ttable:
            self.ttable[nq_i]={}
        if not nt in self.ttable[nq_i]:
            self.ttable[nq_i][nt]=set()
        self.ttable[nq_i][nt].update(qs)

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
        return self.gamma.add(a)

    def add_tsymbol(self,t):
        return self.gamma.add(t)

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
            states=set([(self._nstate(self.q_0),(),(),0,"")])
        else:
            states=status.state

        states=self.step(states)
        status.position+=1
        status.step+=1
        status.state=states

    def accept(self,states):
        final=set([self._state(q) for q,_,_,_ in states])
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


    def save_img(self,filename,q_c=set(),a_c=set(),q_prev=set(),symbols={},states={},format='svg',dpi="90.0",string=None,status=None):
        dot=self.graph(q_c=q_c,a_c=a_c,q_prev=q_prev,symbols=symbols,states=states,format=format,dpi=dpi,string=string,status=status)
        dot.render(filename,format="png",cleanup=True)

    def states2string(self,states):
        res=[]
        for q,nt,pt,(c,a) in states:
            tape=self._tape(nt,pt)
            res.append("{}, … {} _{}_ {} …".format(self._state(q),\
                "".join([ self._tsymbol(t) for t in tape[:c]]),\
                self._tsymbol(tape[c]),\
                "".join([ self._tsymbol(t) for t in tape[c+1:]])))
        return "|".join(res)

    def summary(self):
        info= [
         "States  : "+", ".join(self.states()),
         "Sigma   : "+", ".join(self.symbols()),
         "Gamma   : "+", ".join(self.tsymbols()),
         "Initial : "+self.q_0,
         "Aceptors: "+", ".join(self.A),
         "Transitions:\n"+"\n".join(f" {q_i},{t}/{t_} → {q_f},{Dir}" for (q_i,t),(q_f,t_,Dir) in self.items())]
        return "\n".join(info) 

    def graph(self,q_c=set(),a_c=set(),q_prev=set(),states={},symbols={},format="svg",dpi="60.0",string=None,stack=[],status=None,one_arc=True,finished=False):
        if len(q_c)==0:
            states_=[(self._nstate(self.q_0),(),(),(0,""))]
        else:
            states_=q_c

        f=Digraph(comment="PDAs",format=format)
        f.attr(rankdir='LR',dpi=dpi)
        for i,(q_c_,nt,pt,(c,a)) in enumerate(states_):
            if len(q_c)>0:
                q_c_=set([self._state(q_c_)])
            else:
                q_c_=[]
            with f.subgraph(name=f'cluster_{i}') as f_:
                self._graph(f_,
                    i=i,
                    q_c=q_c_,
                    a_c=set([a]),
                    q_prev=q_prev,
                    symbols=symbols,
                    states=states,
                    tape=self._tape(nt,pt),
                    pos=c+len(nt),
                    dpi=dpi,
                    format=format,
                    status=status,
                    string=string,
                    one_arc=one_arc)
        return f

    def _graph(self,f,i=0,q_c=set(),a_c=set(),q_prev=set(),states={},symbols={},format="svg",dpi="60.0",string=None,tape=None,status=None,one_arc=True,pos=None,finished=False):
        label_tape=None
        if len(self.A.intersection(q_c))>0:
            color_state="limegreen"
        else:
            if status==None:
                color_state="lightblue2"
            else:
                color_state="orangered"

        f.attr(style='invis',labelloc="b")

        if tape:
            cells=[]
            for i,c in enumerate(tape):
                if i==pos:
                    cells.append(f'<TD BGCOLOR="{color_state}">{symbols.get(self._tsymbol(c),self._tsymbol(c))}</TD>')
                else:
                    cells.append(f'<TD>{symbols.get(self._tsymbol(c),self._tsymbol(c))}</TD>')
            label_tape=f"< <TABLE BORDER='0' CELLBORDER='1' SIDES='TBRL'><TR>{' '.join(cells)}</TR></TABLE> >"

        if label_tape:
            f.attr(label=label_tape)

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
            (q_i,a),(q_f,a_,Dir) = info
            if (q_f in q_c and q_i in q_prev) and (a in a_c):
                edges[(f'{q_i}_{i}',f'{q_f}_{i}')].append((f'{symbols.get(a,a)}/{symbols.get(a_,a_)},{self._dir(Dir)}',True))
            else:
                edges[(f'{q_i}_{i}',f'{q_f}_{i}')].append((f'{symbols.get(a,a)}/{symbols.get(a_,a_)},{self._dir(Dir)}',False))

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
            s_order=list(self.gamma)
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
                    for q_f,r,Dir in self.ttable[self._nstate(q_i)][self._ntsymbol(a)]:
                        labels.append(f'/{symbols.get(self._tsymbol(r),self._tsymbol(r))}→{self._state(q_f)},{self._dir(Dir)}')
                    vals.append("<br/>".join(labels))
                except KeyError:
                    vals.append(empty_symbol)
            row="</td><td>".join(vals)
            table+=f"<tr><td {final}>{row}</td></tr>"
        table+="</table>"
        return display(HTML(table))

    def save_gif(self,w,filename="tm.gif",symbols={},states={},dpi="300",show=True,loop=0,max_steps=1000):
        dirpath = tempfile.mkdtemp()
        i=0
        images=[]
        q_prev=set()
        max_images_height=1
        status=None
        for ii,q in enumerate(self.delta_stepwise(w)):
            if len(q)==0:
                status=self.accept(q_prev)
                if status:
                    break
                q=q_prev
                q_prev=set()
            if ii>=max_steps:
                break
            filename_=os.path.join(dirpath,f'{i}')
            g=self.save_img(filename_,q_c=q,q_prev=set([self._state(q_c) for q_c,_,_,_ in q]),
                    symbols=symbols,states=states,status=status,
                    dpi=dpi)
            q_prev=q
            im=Image.open(filename_+".png")
            width, height = im.size
            max_images_height=max(max_images_height,height)
            images.append(im)
            i+=1
            filename_=os.path.join(dirpath,f'{i}')
            if isinstance(q,set):
                g=self.save_img(filename_,q_c=q,status=status,
                        symbols=symbols,states=states,dpi=dpi)
            else:
                g=self.save_img(filename_,q_c=set([q]),status=status,
                        symbols=symbols,states=states,dpi=dpi)
            im=Image.open(filename_+".png")
            images.append(im)
            i+=1
        images.append(im)
        images.append(im)
        images.append(im)
        images.append(im)

        for i,im in enumerate(images):
            im2 = Image.new('RGB', (width, max_images_height), (255, 255, 255))
            width, height = im.size
            im2.paste(im)
            images[i]=im2

        images[0].save(filename,
                save_all=True, append_images=images[1:], optimize=False, duration=500, loop=loop)
        if show:
            return HTML(f'<img src="{filename}">')
        else:
            return

