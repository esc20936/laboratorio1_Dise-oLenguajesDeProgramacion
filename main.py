#  Laboratorio 1
#  Universidad del Valle de Guatemala
#  Diseño de lenguajes de programacion

#  Autor:
# - Pablo Escobar 20936

from algorithms import Thompson, subsetConstruction
from utils import graphAutomata
import pandas as pd


# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
# basado en el algoritmo de Shunting-yard
def parseRegexToPostfix(regex):
    outputQueue = []
    operatorStack = []
    operatorPrecedence = {
        '*': 3,
        '%': 2,
        '|': 1,
        '+': 3,
        '(': 0,
        ')': 0
    }

    for char in regex:
        if char == '(':
            operatorStack.append(char)
        elif char == ')':
            while operatorStack[-1] != '(':
                outputQueue.append(operatorStack.pop())
            operatorStack.pop()
        elif char in operatorPrecedence:
            while operatorStack and operatorPrecedence[char] <= operatorPrecedence[operatorStack[-1]]:
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
    caracteres = ["(", ")", "|", "*", "%", "+", "?","&"]
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
            if (regex[i].isalnum() and regex[i + 1].isalnum()) or (regex[i].isalnum() and regex[i + 1] == "(") or (regex[i] == ")" and regex[i + 1].isalnum()) or (regex[i] == ")" and regex[i + 1] == "(") or (regex[i] == "*" and regex[i + 1].isalnum()) or (regex[i] == "*" and regex[i + 1] == "(") or (regex[i] == "+" and regex[i + 1].isalnum()) or (regex[i] == "+" and regex[i + 1] == "(") or (regex[i] == "%" and regex[i + 1].isalnum()) or (regex[i] == "%" and regex[i + 1] == "(") or (regex[i] == "?" and regex[i + 1].isalnum()) or (regex[i] == "?" and regex[i + 1] == "(") or (regex[i] == "&" and regex[i + 1].isalnum()) or (regex[i] == "&" and regex[i + 1] == "(") or (regex[i].isalnum() and regex[i+1]=="&") or (regex[i] == ")" and regex[i+1]=="&"):
                newRegex += regex[i] + "%"
            else:
                newRegex += regex[i]
    newRegex += regex[len(regex) - 1]
    return newRegex


def start(expresion):
    if validarExpresionRegular(expresion):
        regex = expresion
        expresion = createFixedRegex(expresion)
        expresion = parseRegexToPostfix(expresion)
        print(expresion)

        nfa = Thompson(expresion)
        if nfa[1] == None:
            print(regex)
            exit()
        
        nfa = nfa[1]


        nfa.setNameToAllStates()
        print("Tabla de transiciones NFA\n")
        nfa.show()
        print("\n")
        listaEstados = nfa.getAllStatesNamesInOrder()
        transiciones = nfa.getAllTransitions()
        graphAutomata(listaEstados, transiciones)

        
        # subset = subsetConstruction(nfa, expresion)

        # estadosSubset = []
        # transicionesSubset = {}
        # for i in range(len(subset['Estados'])):
        #     ESTADO = subset['Estados'][i]
        #     estadosSubset.append(subset['Estados'][i])
        #     for transicion in subset.keys():
        #         if transicion != 'Estados':
        #             diccionarioSimbolo = {}
        #             if subset[transicion][i] != 'NONE':
        #                 diccionarioSimbolo[transicion] = [subset[transicion][i]]
                        
        #                 if ESTADO in transicionesSubset:
        #                     transicionesSubset[ESTADO].update(diccionarioSimbolo)
        #                 else:
        #                     transicionesSubset[ESTADO] = diccionarioSimbolo
        #     # estadosSubset.append(subset['Estados'][i])

        # print(transicionesSubset)
        # print(estadosSubset)
        # graphAutomata(estadosSubset, transicionesSubset,"subsetConstruction.gv")
        # print("Tabla de transiciones Subset Construction\n")
        # df = pd.DataFrame(subset)
        # print(df)
        # print("\n")

    else:
        print("Expresion regular no valida")




if __name__ == "__main__":

    expresiones = [
        "*a",
        "a||",
        "|ba",
        "ab|&|",
        "(a|b",
        "(a|b))",
    ]

    expresion = expresiones[0]

    start(expresion)

    


   