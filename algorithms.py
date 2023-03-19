from NFAClass import NFA
from StateClass import State
from SubsetConstruction import epsilonClosure, epsilonClosureOfSet


def belongsToLanguage(nfa, string, acceptanceStates):
    # Obtener el conjunto de estados alcanzables desde el estado inicial
    currentStates = epsilonClosure(nfa.start)
    # Iterar por cada simbolo en la cadena de entrada
    for symbol in string:
        nextStates = set()
        # Obtener el conjunto de estados alcanzables desde los estados actuales usando el simbolo actual
        for state in currentStates:
            if symbol in state.transitions:
                nextStates = nextStates.union(set(state.transitions[symbol]))
        # Obtener el conjunto de estados alcanzables desde los estados actuales usando epsilon
        currentStates = epsilonClosureOfSet(nextStates)
    # Verificar si el conjunto de estados actuales contiene un estado final
    for state in currentStates:
        if state.name in acceptanceStates:
            return True
    return False


# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
# basado en el algoritmo de Shunting-yard
def parseRegexToPostfix(regex):
    outputQueue = []
    operatorStack = []
    operatorPrecedence = {"*": 3, "%": 2, "|": 1, "+": 3, "(": 0, ")": 0}

    for char in regex:
        if char == "(":
            operatorStack.append(char)
        elif char == ")":
            while operatorStack[-1] != "(":
                outputQueue.append(operatorStack.pop())
            operatorStack.pop()
        elif char in operatorPrecedence:
            while (
                operatorStack
                and operatorPrecedence[char] <= operatorPrecedence[operatorStack[-1]]
            ):
                outputQueue.append(operatorStack.pop())
            operatorStack.append(char)
        else:
            outputQueue.append(char)

    while operatorStack:
        outputQueue.append(operatorStack.pop())

    return outputQueue


# Funcion para revisar que los parentesis esten balanceados
# param - cadena de caracteres
def revisarParentesis(cadena):
    count = 0
    ans = False
    for i in cadena:
        if i == "(":
            count += 1
        elif i == ")":
            count -= 1
        if count < 0:
            print("Error: Regex invalido\t" + cadena)
            print("Parentesis no balanceados")
            return ans
    if count == 0:
        return not ans
    else:
        print("Error: Regex invalido\t" + cadena)
        print("Parentesis no balanceados")
        return ans


# Funcion para valida que la expresion regular es valida
# param - expresion regular


def validarExpresionRegular(expresion):
    bandera = False
    caracteres = ["(", ")", "|", "*", "%", "+", "?", "&"]
    for caracter in expresion:
        if caracter.isalnum() or caracter in caracteres:
            bandera = True
        else:
            bandera = False
            print(f"Error: Regex invalido\t{expresion}")
            if caracter == " ":
                print("Caracter invalido: (whitespace)")
            else:
                print("Caracter invalido: " + caracter)
            break
    return bandera and revisarParentesis(expresion)


# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
def createFixedRegex(regex):
    newRegex = ""
    for i in range(len(regex)):
        if i < len(regex) - 1:
            if (
                (regex[i].isalnum() and regex[i + 1].isalnum())
                or (regex[i].isalnum() and regex[i + 1] == "(")
                or (regex[i] == ")" and regex[i + 1].isalnum())
                or (regex[i] == ")" and regex[i + 1] == "(")
                or (regex[i] == "*" and regex[i + 1].isalnum())
                or (regex[i] == "*" and regex[i + 1] == "(")
                or (regex[i] == "+" and regex[i + 1].isalnum())
                or (regex[i] == "+" and regex[i + 1] == "(")
                or (regex[i] == "%" and regex[i + 1].isalnum())
                or (regex[i] == "%" and regex[i + 1] == "(")
                or (regex[i] == "?" and regex[i + 1].isalnum())
                or (regex[i] == "?" and regex[i + 1] == "(")
                or (regex[i] == "&" and regex[i + 1].isalnum())
                or (regex[i] == "&" and regex[i + 1] == "(")
                or (regex[i].isalnum() and regex[i + 1] == "&")
                or (regex[i] == ")" and regex[i + 1] == "&")
            ):
                newRegex += regex[i] + "%"
            else:
                newRegex += regex[i]
    newRegex += regex[len(regex) - 1]
    return newRegex
