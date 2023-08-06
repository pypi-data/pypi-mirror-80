# Base class for Finite Machines
from maquinas.exceptions import *
from ordered_set import OrderedSet
import tempfile
import os
from PIL import Image
from IPython.core.display import display, HTML, Markdown, clear_output

class FiniteAutomaton():
    """Class for finite automaton"""

    def __init__(self, Q=[], sigma=[], q_0=None, A=[], delta={}, force=False, epsilon=False):
        self.sigma=OrderedSet()
        if epsilon:
            self.sigma.add('ε')
        self.sigma.update(sigma)
        self.Q=OrderedSet(Q)
        self.set_initial_state(q_0)
        self.set_aceptors(A,force=force)
        self.ttable={}
        for (q_i,a),q_f in delta:
            self.add_transition(q_i,a,q_f)

    def __getitem__(self,key):
        q,a=key
        return self.get_transition(q,a)

    def _nstate(self,q):
        if isinstance(q,set):
            return set(self.Q.index(n) for n in q)
        if q is None:
            return set()
        else:
            return self.Q.index(q)

    def _nsymbol(self,a):
        return self.sigma.index(a)

    def _state(self,nq):
        if isinstance(nq,set):
            return set(self.Q.items[n] for n in nq)
        else:
            return self.Q.items[nq]

    def _symbol(self,na):
        return self.sigma.items[na]

    def states(self):
        return list(self.Q)

    def symbols(self):
        return list(self.sigma)

    def _transition(self,nq_i,na,nq_f):
        return (self._state(nq_i),self._symbol(na)),self._state(nq_f)

    def __setitem__(self,key,value):
        q,a=key
        return self.add_transition(q,a,value)

    def _get_transition(self,nq,na):
        if isinstance(nq,set):
                new=set()
                for nq_ in nq:
                    try:
                        new=new|self.ttable[nq_][na]
                    except KeyError:
                        pass
                return new
        else:
            try:
                return self.ttable[nq][na]
            except KeyError:
                raise DoesNotExistsTransition(nq,na)

    def items(self):
        for nq_i,t_ in self.ttable.items():
            for na,nq_f in t_.items():
                yield self._transition(nq_i,na,nq_f)

    def get_transition(self,q,a):
        return self._state(self._get_transition(self._nstate(q),self._nsymbol(a)))

    def add_transition(self,q_i,a,q_f):
        nq_i=self.add_state(q_i)
        nq_f=self.add_state(q_f)
        na=self.add_symbol(a)
        try:
            self.ttable[nq_i][na]=nq_f
        except KeyError:
            self.ttable[nq_i]={}
            self.ttable[nq_i][na]=nq_f

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

    def set_initial_state(self,q,force=False):
        if q is None:
            self.q_0=None
            return None
        if force and not q in self.Q:
            self.add_state(q)
        self.q_0=q

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

    def _status(self,status,states={},symbols={}):
        return status

    def stepStatus(self,status):
        if status.state is None:
            q_c=self.q_0
        else:
            q_c=status.state

        a=status.get_symbol_tape()
        q_c=self.step(q_c,a)
        status.position+=1
        status.step+=1
        status.state=q_c

    def accept(self,q):
        if isinstance(q,set):
            if bool(q.intersection(self.A)):
                return True
        else:
            if q in self.A:
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

    def save_img(self,filename,q_c=set(),a_c=set(),q_prev=set(),symbols={},states={},format='svg',dpi="90.0",string=None):
        dot=self.graph(q_c=q_c,a_c=a_c,q_prev=q_prev,symbols=symbols,states=states,format=format,dpi=dpi,string=string)
        dot.render(filename,format="png",cleanup=True)

    def summary(self,symbols={},states={}):
        info= [
         "States  : "+", ".join([symbols.get(q,q) for q in self.states()]),
         "Sigma   : "+", ".join([symbols.get(a,a) for a in self.symbols()]),
         "Initial : "+symbols.get(self.q_0,self.q_0),
         "Aceptors: "+", ".join([symbols.get(q,q) for q in self.A]),
         "Transitions:\n"+"\n".join(f" {states.get(q_i,q_i)},{symbols.get(a,a)} → {tuple(states.get(q_f,q_f) for q_f in q_fs)}" for (q_i,a),q_fs in self.items())]
        return "\n".join(info)

    def print_summary(self,symbols={},states={}):
        print(self.summary(symbols=symbols,states=states))

    def print_transitions(self,w):
        for q,a,w_ in self.delta_stepwise(w):
            if a:
                print(f"{a} → {q}", end=",\n ")
            else:
                print(f"{q}",end=",\n ")

    def save_gif(self,w,filename="maquina.gif",symbols={},states={},dpi="300",show=True,loop=0):
        dirpath = tempfile.mkdtemp()
        i=0
        images=[]
        q_prev=set()
        for q,a,w_ in self.delta_stepwise(w):
            filename_=os.path.join(dirpath,f'{i}')
            fin=len(w)-len(w_)
            if fin:
                processed=w[:fin-1]
            else:
                processed=" "
            a = a if a else " "
            if isinstance(q,set):
                g=self.save_img(filename_,q_c=q,a_c=set([a]),q_prev=q_prev,
                        symbols=symbols,states=states,
                        dpi=dpi,string=(processed,a,w_))
                q_prev=q
            else:
                g=self.save_img(filename_,q_c=set([q]),a_c=set([a]),q_prev=q_prev,
                        symbols=symbols,states=states,
                        dpi=dpi,string=(processed,a,w_))
                q_prev=set([q])
            im=Image.open(filename_+".png")
            images.append(im)
            i+=1
            filename_=os.path.join(dirpath,f'{i}')
            if isinstance(q,set):
                g=self.save_img(filename_,q_c=q,
                        symbols=symbols,dpi=dpi,string=(processed,a,w_))
            else:
                g=self.save_img(filename_,q_c=set([q]),
                        symbols=symbols,dpi=dpi,string=(processed,a,w_))
            im=Image.open(filename_+".png")
            if i==0 or len(w_)==0:
                images.append(im)
                images.append(im)
                images.append(im)
                images.append(im)
            images.append(im)
            i+=1

        images[0].save(filename,
                save_all=True, append_images=images[1:], optimize=False, duration=500, loop=loop)
        if show:
            return HTML(f'<img src="{filename}">')
        else:
            return

