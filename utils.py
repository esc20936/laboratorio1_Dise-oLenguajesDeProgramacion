import matplotlib.pyplot as plt
import networkx as nx
from graphviz import Digraph

def graphAutomata(states, transitions):
    g = Digraph('G', filename='automata.gv', format='png')
    g.attr(rankdir='LR', size='8,5')
    g.attr('node', shape='doublecircle')
    g.attr('node', shape='circle')
    for state in states:
        g.node(state)

    for state, transitions in transitions.items():
        for symbol, states in transitions.items():
            for state2 in states:
                g.edge(state, state2, label=symbol)
    g.view()
      