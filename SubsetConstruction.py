# Funcion para guardar como estado de aceptacion basado en los nuevos estadaos
# Parametros:
# - states: estados
# - subState: estado
def getStatesBySubState(states, subState):
    statesBySubState = []
    for state in states:
        if subState in states[state]:
            statesBySubState.append(state)
    return statesBySubState


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


# Funcion para obtener todos los estados alcanzables desde un conjunto de estados a través de un simbolo
def getTransions(states, symbol):
    transiciones = set()
    for state in states:
        if symbol in state.transitions:
            for state in state.transitions[symbol]:
                transiciones.add(state)
    return transiciones


# Funcion para obtener todos los estados alcanzables desde un estado a través de epsilon
def epsilonClosure(state):
    if state is None:
        return set()
    closure = set()
    closure.add(state)
    if "&" in state.transitions:
        for state in state.transitions["&"]:
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
    newName = ""
    numbers = []
    for state in states:
        numbers.append(int(state.name[1:]))

    numbers.sort()
    for number in numbers:
        newName += f"{number},"

    return newName[:-1]


# Algoritmo de subconjuntos para convertir un NFA a un DFA
# VIDEOS DE APOYO
# https://www.youtube.com/watch?v=WikU-ujoCqg
# https://www.youtube.com/watch?v=vt2x0W_jcPU
# https://www.youtube.com/watch?v=DjH7K7MZRAw&t=1427s


def subsetConstruction(NFA, expression):
    DFA = {}
    start = NFA.start
    newStates = {}
    simbolos = []
    for c in expression:
        if c not in simbolos and c not in ["|", "%", "*", "+", "?"]:
            simbolos.append(c)

    DFA = {
        "Estados": [],
    }
    for s in simbolos:
        if s != "&":
            DFA[s] = []

    # epsilon closure del estado inicial
    data = epsilonClosure(start)
    # Creamos el estado inicial del DFA
    valor = f"S{len(newStates)}"
    newStates[valor] = getFixedName(data)

    DFA["Estados"] = [valor]
    for STATE in enumerate(DFA["Estados"]):
        ndata = getStatesByName(NFA.getAllStates(), newStates[STATE[1]].split(","))
        newSet = set()
        for state in ndata:
            newSet = newSet.union(epsilonClosure(state))
        data = ndata
        for s in simbolos:
            if s != "&":
                transiciones = getTransions(data, s)
                nData = set()
                for state in transiciones:
                    nData = nData.union(epsilonClosure(state))
                # print("nData",nData)
                nName = getFixedName(nData)
                # print(nName)
                if nName != "":
                    if nName not in newStates.values():
                        valor = f"S{len(newStates)}"

                        newStates[valor] = nName
                        DFA["Estados"].append(valor)
                        DFA[s].append(valor)
                    else:
                        for key in newStates:
                            if newStates[key] == nName:
                                DFA[s].append(key)
                else:
                    DFA[s].append("NONE")
    # print(newStates)
    return (DFA, newStates)
