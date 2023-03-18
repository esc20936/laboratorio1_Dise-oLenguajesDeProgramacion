class Node(object):

    
    #Una clase nodo, almacena información de un nodo en un árbol binario.
    
   # Params:
    # parent (Node): nodo padre (si no tiene es un nodo raíz)
    # left (Node): nodo hijo del lado izquierdo
    # right (Node): nodo hijo del lado derecho
    # data (string): símbolo u operador que el nodo almacena

    def __init__(self, data, parent=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        
        self.lastpos = []
        self.firstpos = []
        self.followpos = []
        self.nullable = False
        self.pos = None
