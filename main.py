#  Laboratorio 1
#  Universidad del Valle de Guatemala
#  Diseño de lenguajes de programacion

#  Autor:
# - Pablo Escobar 20936

from algorithms import Thompson, subsetConstruction
import matplotlib.pyplot as plt
import networkx as nx
from utils import graphAutomat



# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
# basado en el algoritmo de Shunting-yard 
def parseRegexToPostfix(regex):
    outputQueue = []
    operatorStack = []
    operatorPrecedence = {
        '*': 3,
        '?': 2,
        '|': 1,
        '+': 1,
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
    count= 0  
    ans=False  
    for i in cadena:  
        if i == "(":  
            count += 1  
        elif i == ")":  
            count-= 1  
        if count < 0:  
            return ans  
    if count==0:  
        return not ans  
    return ans  

# Funcion para valida que la expresion regular es valida
# param - expresion regular 
def validarExpresionRegular(expresion):
    bandera = False
    caracteres = ["(", ")", "|", "*", "?","+"]
    for caracter in expresion:
        if caracter.isalnum() or caracter in caracteres:
            bandera = True
    return bandera and revisarParentesis(expresion)

   
# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
def createFixedRegex(regex):
    newRegex = ""
    for i in range(len(regex)):
        if i < len(regex) - 1:
            if (regex[i].isalnum() and regex[i + 1].isalnum()) or (regex[i].isalnum() and regex[i + 1] == "(") or (regex[i] == ")" and regex[i + 1].isalnum()) or (regex[i] == ")" and regex[i + 1] == "(") or (regex[i] == "*" and regex[i + 1].isalnum()) or (regex[i] == "*" and regex[i + 1] == "("):
                newRegex += regex[i]  + "?"
            else:
                newRegex += regex[i]
    newRegex += regex[len(regex) - 1]
    return newRegex


if __name__ == "__main__":
    # expresion = input("Ingrese la expresion regular: ")
    # cadena = input("Ingrese la cadena a evaluar: ")

    # Expresion prueba
    expresion = "(a|b)*abbc"

    OPERATORS = {
        '|': 1,
        '^': 2,
        '*': 3,
        '?': 2,
        '+': 1
    }
    EPSILON = '&'
    

    if validarExpresionRegular(expresion):
        expresion = createFixedRegex(expresion)
        expresion = parseRegexToPostfix(expresion)
        nfa = Thompson(expresion)
        nfa.setNameToAllStates()
        print("Tabla de transiciones NFA\n")
        nfa.show()

        listaEstados = nfa.getAllStatesNamesInOrder()
        transiciones = nfa.getAllTransitions()

        # G = nx.Graph()

        # G.add_nodes_from(listaEstados)
        # nx.draw_networkx(G)
        # plt.show()

        # print("Estados: ", listaEstados)
        # print("Transiciones: ", transiciones)

        edges=[]
        edgeLabels = {}
        for estado in transiciones:
            for simbolo in transiciones[estado]:
                for estadoDestino in transiciones[estado][simbolo]:
                    edges.append((estado,estadoDestino))
                    edgeLabels[(estado,estadoDestino)] = simbolo
        print("edges:",edges)
        print("\n")

        graphAutomat(edges,edgeLabels,nfa.getAcceptanceState(),'q0')

        # G = nx.Graph()
        # G.add_edges_from(edges)
        # pos = nx.spring_layout(G)
        # plt.figure()
        # colores = []
        # estadoAcepatacion = nfa.getAcceptanceState()


        # for nodo in G.nodes:
        #     # print(nodo)
        #     colores.append('lightgreen' if nodo == 'q0' else  "pink" if nodo== estadoAcepatacion else   'lightblue')
            

        # nx.draw(
        #     G, pos, edge_color='black', width=1, linewidths=1, node_color=colores,
        #     node_size=500, alpha=0.9,
        #     labels={node: node for node in G.nodes()}
        # )
        # # nx.draw_networkx(G, node_color=colores, with_labels=True)

        # nx.draw_networkx_edge_labels(
        #     G, pos,
        #     edge_labels=edgeLabels,
        #     font_color='red'
        # )

        # plt.show()


        # print("edges:",edges)
        print("\n")
        # print("Tabla de transiciones DFA\n")
        # print(subsetConstruction(nfa,expresion))
        
    else:
        print("Expresion regular no valida")
 


        
     
        


        



