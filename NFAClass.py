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

