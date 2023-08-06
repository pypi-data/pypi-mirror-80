# Excepciones para máquinas

class AlreadyExistsState(Exception):
    """El estado ya existe en la máquina"""
    def __init__(self, q):
        self.q = q
        msg= f"El estado '{q}' existe en estados de Máquina"
        super().__init__(msg)

class AlreadyExistsSymbol(Exception):
    """El estado ya existe en la máquina"""
    def __init__(self, a):
        self.a = a
        msg= f"El símbolo '{a}' existe en sigma de Máquina"
        super().__init__(msg)

class AlreadyExistsTransition(Exception):
    """La transacción ya existe en la máquina"""
    def __init__(self, q_i, a,m):
        self.a = a
        self.q_i = q_i
        self.m = m
        msg= f"La transicion ({q_i},{a}) ya existe con destino a {m[q_i,a]}"
        super().__init__(msg)

class DoesNotExistsTransition(Exception):
    """No existe la transacción"""
    def __init__(self, q_i, a):
        self.a = a
        self.q_i = q_i
        msg= f"La transición ({q_i},{a}) no existe en la Máquina"
        super().__init__(msg)

class DoesNotExistsState(Exception):
    """No existe el estado"""
    def __init__(self, q):
        self.q = q
        msg= f"El estado {q} no existe en la Máquina"
        super().__init__(msg)

class DoesNotExistsSymbol(Exception):
    """No existe el símbilo"""
    def __init__(self, a):
        self.a = a
        msg= f"El símbolo '{a}' no existe en la Máquina"
        super().__init__(msg)

class NoIntitialStateDefined(Exception):
    """No se ha definido el estado inicial"""
    def __init__(self):
        msg= f"No se ha definido el estado inicial"
        super().__init__(msg)


