import matplotlib.pyplot as plt
import networkx as nx
from graphviz import Digraph

def graphAutomata(states, transitions, name="automata.gv"):
    g = Digraph('G', filename=name, format='png')
    g.attr(rankdir='LR', size='20,5')
    print(transitions)
    cont = 0
    for state in states:
        if cont == 0:
            g.attr('node', shape='doublecircle')
            cont += 1
        else:
            g.attr('node', shape='circle')
        g.node(state)

    for state, transitions in transitions.items():
        for symbol, states in transitions.items():
            for state2 in states:
                g.edge(state, state2, label=symbol)
    g.view()
      