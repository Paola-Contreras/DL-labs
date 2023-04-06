'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''
import graphviz
from Arbol import * 

afn = []
counter = 0

class Automata_partes:
    def __init__(self):
        self.start_state = Handle_states().number
        self.end_state = Handle_states().number

class Handle_states:
    counter =0
    def __init__(self):
        self.number = Handle_states.counter
        Handle_states.counter += 1
        self.transitions = []

def symbol(sym):
    Grafo = Automata_partes()
    states = Handle_states()
    Handle_states.counter -= 1

    states.transitions.append((Grafo.start_state,Grafo.end_state,sym))
    afn.append(states.transitions)
    return Grafo

def kleene (X): 
    Grafo1 = Automata_partes()
    states = Handle_states()
    Handle_states.counter -= 1

    AFN1 = X
    tran = afn.pop()  
    states.transitions.append((Grafo1.start_state,AFN1.start_state, 'ε'))
    states.transitions += tran 
    states.transitions.append((AFN1.end_state, AFN1.start_state, 'ε'))
    states.transitions.append((AFN1.end_state, Grafo1.end_state, 'ε'))
    states.transitions.append((Grafo1.start_state, Grafo1.end_state, 'ε'))

    afn.append(states.transitions)
    return Grafo1

def optional (X):
    Grafo1 = Automata_partes()
    states = Handle_states()
    Handle_states.counter -= 1
    AFN1 = X
    tran = afn.pop()  
    states.transitions.append((Grafo1.start_state,AFN1.start_state, 'ε'))
    states.transitions += tran 
    states.transitions.append((AFN1.end_state, Grafo1.end_state, 'ε'))
    states.transitions.append((Grafo1.start_state, Grafo1.end_state, 'ε'))

    afn.append(states.transitions)
    return Grafo1

def positive(X):
    counter = Handle_states.counter
    Grafo1 = Automata_partes()
    Grafo1.start_state=(X.start_state)
    Grafo1.end_state=(X.end_state)
    states = Handle_states()
    Handle_states.counter = counter

    AFN1 = X
    tran = afn.pop()  

    states.transitions += tran 
    states.transitions.append((AFN1.end_state, AFN1.start_state, 'ε'))

    afn.append(states.transitions)
    return Grafo1

def concatenate (X,Y): 
    AFN1 = X
    AFN2 = Y

    counter = Handle_states.counter
    Grafo = Automata_partes()
    Grafo.start_state=(X.start_state)
    Grafo.end_state=(Y.end_state)
    states = Handle_states()
    Handle_states.counter = counter

    tran1 = afn.pop()
    tran2 = afn.pop()

    states.transitions += tran1
    states.transitions.append((AFN1.end_state, AFN2.start_state, 'ε'))
    states.transitions += tran2

    afn.append(states.transitions)
  
    return Grafo

def union(X,Y):
    AFN1 = X
    AFN2 = Y
    
    Grafo = Automata_partes()
    states = Handle_states()

    tran1 = afn.pop()
    tran2 = afn.pop()

    states.transitions.append((Grafo.start_state, AFN1.start_state, 'ε'))
    states.transitions.append((Grafo.start_state, AFN2.start_state, 'ε'))
    states.transitions += tran1
    states.transitions += tran2
    states.transitions.append((AFN1.end_state, Grafo.end_state, 'ε'))
    states.transitions.append((AFN2.end_state, Grafo.end_state, 'ε'))

    afn.append(states.transitions)
    return Grafo

def graph_afn(afn):
    graph = graphviz.Digraph('Thompson Construction', filename='AFN', format= 'png')
    graph.attr(rankdir='LR', shape= 'circle')

    values = []
    for val in afn[0]:
        for vals in val:
           if isinstance(vals, int) and vals not in values:
                values.append(vals)

    for valor in values:
        contador = 0
        contador1 = 0 
        for tupla in afn[0]:
            if tupla[0] == valor:
                contador += 1
            if tupla[1] == valor:
                contador1 += 1
        if contador1 == 0:
            start_state = valor
            print(start_state)

    end_state = max(values)
        
    for inicio,fin,label in afn[0]:
        if inicio == start_state:
            graph.node(str(start_state), style= 'filled', fillcolor = '#87CEEB', shape= 'circle', rank = 'same')
        if fin == end_state:
             graph.node(str(end_state), shape= 'doublecircle', rank = 'same')
             
        graph.attr('node', shape='circle')
        graph.edge(str(inicio), str(fin), label= str(label))

    graph.view()

def thompson(subtrees_list):
    stack2 =[]

    for i in subtrees_list:
        if i[0] == 'Simbolo':
            stack2.append(symbol(i[1]))
        if i[0] == 'Kleene':
            G = stack2.pop()
            stack2.append(kleene(G))
        if i[0] == 'Opcional':
            G1 = stack2.pop()
            stack2.append(optional(G1))
        if i[0] == 'Kleen Positiva':
            G2 = stack2.pop()
            stack2.append(positive(G2))
        if i[0] == 'Concatenacion':
            G3 = stack2.pop()
            G4 = stack2.pop()
            stack2.append(concatenate(G4,G3))
        if i[0] == 'Union':
            G5 = stack2.pop()
            G6 = stack2.pop()
            stack2.append(union(G6,G5))

    graph_afn(afn)
    print(afn)
    return afn
