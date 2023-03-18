from NFAClass import NFA
from StateClass import State
# simbolo de epsilon = &
# Algoritmo de Thompson para convertir una expresion regular a un NFA
# Parametros:
#   Regex - Expresion regular
# Retorno:
# Tupla si existe error y el NFA (ERROR, NFA)
def Thompson(Regex):
    NFAstack = []
    for char in Regex:
        if char == '|':
            if(len(NFAstack) < 2):
                print("No hay suficientes NFA para realizar la operacion | (or)\nDescripcion: Deben existir simbolos de ambos lados del operador | (or)\n Formato esperado a|b \n Formato recibido:")
                return ({"Error": "No hay suficientes NFA para realizar la operacion |"}, None)
            nfa2 = NFAstack.pop()
            nfa1 = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa1.start)
            start.addTransition('&', nfa2.start)
            nfa1.end.addTransition('&', end)
            nfa2.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '%':
            nfa2 = NFAstack.pop()
            nfa1 = NFAstack.pop()
            nfa1.end.transitions = {**nfa1.end.transitions,** nfa2.start.transitions}
            NFAstack.append(NFA(nfa1.start, nfa2.end))

        elif char == '*':
            if len(NFAstack) < 1:
                print("Error: No hay suficientes NFA para realizar la operacion * (cerradura de kleene)\n Formato esperado a* \n Formato recibido:")
                return ({"Error": "No hay suficientes NFA para realizar la operacion *"}, None)
            nfa = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa.start)
            start.addTransition('&', end)
            nfa.end.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '+':
            if len(NFAstack) < 1:
                print("Error: No hay suficientes NFA para realizar la operacion + (cerradura positiva)\n Formato esperado a+ \n Formato recibido:")
                return ({"Error": "No hay suficientes NFA para realizar la operacion +"}, None)
            nfa = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa.start)
            nfa.end.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '?':
            if len(NFAstack) < 1:
                print("Error: No hay suficientes NFA para realizar la operacion ? (opcional)\n Formato esperado a? \n Formato recibido:")
                return ({"Error": "No hay suficientes NFA para realizar la operacion ?"}, None)
            start = State()
            nfa = NFAstack.pop()
            end = State()
            subStart = State()
            subEnd = State()

            subStart.addTransition('&', subEnd)
            subEnd.addTransition('&', end)

            start.addTransition('&', subStart)
            start.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)

            NFAstack.append(NFA(start, end))
  
        else:
            end = State()
            start = State(transitions={char: [end]})
            NFAstack.append(NFA(start, end))
            
    return (False, NFAstack.pop())

