# Clase que nos ayudara a representar un estado
# Atributos:
#   transitions - Diccionario que contiene las transiciones del estado
class State:
    def __init__(self, transitions=None, name=None):
        self.transitions = transitions if transitions else {}
        self.name = name
        self.isAcceptanceState = False

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
  