# Clase que nos ayudara a crear un NFA
# Atributos:
#   start - Estado inicial
#   end - Estado final
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    # Funcion para mostrar el NFA
    def show(self):
        self.start.show()
    # Funcion para obtener todos los estados
    def getAllStates(self):
        return list(self.start.getAllStates())
    # Funcion para obtener todos los estados en orden
    def getAllStatesInOrder(self):
        return self.start.getAllStatesInOrder()

    def getAllStatesNamesInOrder(self):
        return [state.name for state in self.getAllStatesInOrder()]
    # Funcion para obtener todos los simbolos
    # NO USAR ESTA FUNCION mejor obtener los simbolos de la expresion regular
    def getAllSymbols(self):
        return list(self.start.getAllSymbols())
    # Funcion para asginar nombre a todos los estados
    def setNameToAllStates(self, name=0):
        for state in self.getAllStatesInOrder():
            state.setName(f"q{name}")
            name += 1
    
    def getAllTransitions(self):
        transitions = {}
        for state in self.getAllStatesInOrder():
            transitions[state.name] = state.getAllTransitionsWithNames()
        return transitions
    
    def getAcceptanceState(self):
        return self.end.name



# Clase que nos ayudara a representar un estado
# Atributos:
#   transitions - Diccionario que contiene las transiciones del estado
class State:
    def __init__(self, transitions=None, name=None):
        self.transitions = transitions if transitions else {}
        self.name = name

    # Funcion para agregar una transicion
    # Parametros:
    #  symbol - Simbolo de la transicion
    #  state - Estado al que se llega
    def addTransition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

    # Funcion para agregar un nombre al estado
    # Parametros:
    #  name - Nombre del estado
    def setName(self, name):
        self.name = name

    # Clase que nos ayudara a mostrar el NFA 
    def show(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)   
        statesNames = []
        clave = ""
        for key in self.transitions:
            clave = key
            for state in self.transitions[key]:
                statesNames.append(state.name)
        print(f"{self.name} -- {clave} -> {statesNames}")
        for key in self.transitions:
            for state in self.transitions[key]:
                state.show(visited)

    # Funcion para obtener todos los estados en orden
    def getAllStatesInOrder(self, visited=None):
        if visited is None:
            visited = []
        if self in visited:
            return
        visited.append(self)
        for key in self.transitions:
            for state in self.transitions[key]:
                state.getAllStatesInOrder(visited)
        return visited

    # Funcion para obtener todos los estados
    def getAllStates(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        for key in self.transitions:
            for state in self.transitions[key]:
                state.getAllStates(visited)
        return visited
    
    
    def getAllTransitionsWithNames(self):
        transitions = {}
        for key in self.transitions:
            transitions[key] = [state.name for state in self.transitions[key]]
        return transitions

    # Funcion para obtener todos los simbolos de la transiciones del estado
    # Parametros:
    # symbol - Simbolo de la transicion
    def getTransition(self, symbol):
        if symbol in self.transitions:
            return self.transitions[symbol]
        return None

    # Funcion para obtener todos los simbolos
    # NO USAR ESTA FUNCION mejor obtener los simbolos de la expresion regular
    def getAllSymbols(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        for key in self.transitions:
            visited.add(key)
            for state in self.transitions[key]:
                state.getAllSymbols(visited)
        return visited
       
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





# Funcion para obtener todos los estados alcanzables desde un estado a través de epsilon
def epsilonClosure(state):
    if state is None:
        return set()
    closure = set()
    closure.add(state)
    if '&' in state.transitions:
        for state in state.transitions['&']:
            closure = closure.union(epsilonClosure(state))
    return closure

# Funcion para obtener todos los estados alcanzables desde un conjunto de estados a través de epsilon
def epsilonClosureOfSet(states):
    closure = set()
    for state in states:
        closure = closure.union(epsilonClosure(state))
    return closure

# Funcion para obtener los nombres de los estados en string
def getFixedName(states):
    newName =""
    numbers = []
    for state in states:
        numbers.append(int(state.name[1:]))

    numbers.sort()
    for number in numbers:
        newName += f"{number},"

    return newName[:-1]

# Funcion para obtener todos los estados alcanzables desde un conjunto de estados a través de un simbolo
def getTransions(states,symbol):
    transiciones = set()
    for state in states:
        if symbol in state.transitions:
            for state in state.transitions[symbol]:
                transiciones.add(state)
    return transiciones

# Funcion para obtener todos los estados por nombre
# Parametros:
#  states - Conjunto de estados
#  names - Nombres de los estados en lista
def getStatesByName(states, names):
    statesByName = set()
    nNames = []
    for name in names:
        nNames.append(f"q{name}")
    for state in states:
        if state.name in nNames:
            statesByName.add(state)
    return statesByName

# Function that is going to take a dictionary where the keys are the states and the values are the subStates, also receives a subState
# and returns an array with the states that contain the subState
def getStatesBySubState(states, subState):
    statesBySubState = []
    for state in states:
        if subState in states[state]:
            statesBySubState.append(state)
    return statesBySubState


# Algoritmo de subconjuntos para convertir un NFA a un DFA
# VIDEOS DE APOYO
# https://www.youtube.com/watch?v=WikU-ujoCqg
# https://www.youtube.com/watch?v=vt2x0W_jcPU
# https://www.youtube.com/watch?v=DjH7K7MZRAw&t=1427s

def subsetConstruction(NFA,expression):
    DFA = {}
    start = NFA.start
    newStates = {}
    simbolos = []
    for c in expression:
        if c not in simbolos and c not in ['|','%','*','+', '?']:
            simbolos.append(c)

    DFA = {"Estados":[],}
    for s in simbolos:
        if s != '&':
            DFA[s]=[]

    # epsilon closure del estado inicial
    data = epsilonClosure(start)
    # Creamos el estado inicial del DFA
    valor = f"S{len(newStates)}"
    newStates[valor] = getFixedName(data)

    DFA['Estados']= [valor]
    for STATE in enumerate(DFA['Estados']):
        ndata = getStatesByName(NFA.getAllStates(),newStates[STATE[1]].split(','))
        newSet = set()
        for state in ndata:
            newSet = newSet.union(epsilonClosure(state))
        data = ndata
        for s in simbolos:
            if s != '&':
                transiciones = getTransions(data,s)
                nData =set()
                for state in transiciones:
                    nData = nData.union(epsilonClosure(state))  
                # print("nData",nData)
                nName = getFixedName(nData)
                # print(nName)
                if nName != "":
                    if nName not in newStates.values():
                        valor = f"S{len(newStates)}"
                    
                        newStates[valor] = nName
                        DFA['Estados'].append(valor)
                        DFA[s].append(valor)
                    else:
                        for key in newStates:
                            if newStates[key] == nName:
                                DFA[s].append(key)
                else:
                    DFA[s].append("NONE")
    # print(newStates)
    return (DFA, newStates)
