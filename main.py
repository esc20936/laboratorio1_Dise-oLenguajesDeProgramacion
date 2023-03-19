#  Laboratorio 1
#  Universidad del Valle de Guatemala
#  Diseño de lenguajes de programacion

#  Autor:
# - Pablo Escobar 20936

# from algorithms import Thompson, subsetConstruction, getStatesBySubState
from Thompson import Thompson
from SubsetConstruction import subsetConstruction, getStatesBySubState, getStatesByName
from utils import graphAutomata
from algorithms import (
    belongsToLanguage,
    parseRegexToPostfix,
    revisarParentesis,
    validarExpresionRegular,
    createFixedRegex,
)
from minimization import minimize_dfa
from SyntaxTree import SyntaxTree
from DFA import DFA
import pandas as pd


def getDFASubset(nfa, expresion, acceptanceStates):
    subset, newStates = subsetConstruction(nfa, expresion)
    subState = acceptanceStates.split("q")[1]

    acceptanceStatesArray = getStatesBySubState(newStates, str(subState))
    estadosSubset = []
    transicionesSubset = {}
    for i in range(len(subset["Estados"])):
        ESTADO = subset["Estados"][i]
        estadosSubset.append(subset["Estados"][i])
        for transicion in subset.keys():
            if transicion != "Estados":
                diccionarioSimbolo = {}
                if subset[transicion][i] != "NONE":
                    diccionarioSimbolo[transicion] = [subset[transicion][i]]

                    if ESTADO in transicionesSubset:
                        transicionesSubset[ESTADO].update(diccionarioSimbolo)
                    else:
                        transicionesSubset[ESTADO] = diccionarioSimbolo
        estadosSubset.append(subset["Estados"][i])

    print(newStates)
    graphAutomata(
        estadosSubset,
        transicionesSubset,
        "subsetConstruction.gv",
        acceptanceStatesArray,
    )
    print("Tabla de transiciones Subset Construction\n")
    df = pd.DataFrame(subset)
    print(df)
    print("\n")

    # minimizacion
    # print("Tabla de transiciones Minimizacion\n")
    # print("Estados de aceptacion: ", acceptanceStatesArray)
    # # df.set_index('Estados', inplace=True)
    # print(df)
    # minimizacion = minimize_dfa(df, acceptanceStatesArray)
    # print(minimizacion)


def startThompsonSubsetMin(expresion, cadena):
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
        aceptanceState = nfa.getAcceptanceState()
        print("\nSimulacion de cadena en NFA\n")
        res = belongsToLanguage(nfa, cadena, [aceptanceState])
        print("Cadena: ", cadena)
        print("Resultado: ", res)
        if res:
            print("La cadena pertenece al lenguaje")
        else:
            print("La cadena no pertenece al lenguaje")
        graphAutomata(listaEstados, transiciones, "nfa.gv")
        getDFASubset(nfa, expresion, aceptanceState)
    else:
        print("Expresion regular no valida")


if __name__ == "__main__":

    expresion = "(a|x)*b*z+ax"
    cadena = "abzzax"

    operators = {
        "*": 3,
        "%": 2,
        "|": 1,
        "+": 3,
        ".": 2,
        "?": 3,
    }

    startThompsonSubsetMin(expresion, cadena)
    arbol = SyntaxTree(operators, expresion)

    hash_tree = SyntaxTree(operators, expresion + "#", direct=True)

    print(hash_tree.traverse_postorder(hash_tree.root))
    nodes = hash_tree.traverse_postorder(hash_tree.root, full=True)
    direct_dfa = DFA(syntax_tree=hash_tree, direct=True, nodes=nodes)
    direct_dfa.direct()
    direct_dfa.graph_automata(mapping=direct_dfa.state_mapping)
    res = direct_dfa.simulate(cadena)
    print(res)
