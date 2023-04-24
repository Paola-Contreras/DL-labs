'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

import graphviz

afd = []

def e_Closures(transitions, state):
    closures =[state]
    for states in closures:
        for (first, end, symbol) in transitions:
                if first == states and symbol == 'ε' and end not in closures:
                    closures.append(end)
    return closures

def convert(tuplas,endstate):
    diccionario = {}
    endstates = []
    letra = 'A'

    for tupla in tuplas:
        lista1, lista2, letra_tupla = tupla
        if tuple(lista1)not in diccionario:
            diccionario[tuple(lista1)] = letra
            letra = chr(ord(letra) + 1)
        if tuple(lista2) not in diccionario:
            diccionario[tuple(lista2)] = letra
            letra = chr(ord(letra) + 1)
        
    for val in diccionario.keys():
        if endstate in val:
            valor = diccionario[val]
            endstates.append(valor)
            
    tuplas_nuevas = []
    for tupla in tuplas:
        lista1, lista2, letra_tupla = tupla
        nueva_lista1 = diccionario[tuple(lista1)]
        nueva_lista2 = diccionario[tuple(lista2)]
        tupla_nueva = (nueva_lista1, nueva_lista2, letra_tupla)
        tuplas_nuevas.append(tupla_nueva)
    
    return tuplas_nuevas, endstates

def graph_afd(afd,end):
    graph = graphviz.Digraph('AFD SUBCONSTRUCTION', filename='AFD_Sub', format= 'png')
    graph.attr(rankdir='LR')

    start_state = afd[0][0]
    end_state = end

    for inicio,fin,label in afd:
        if inicio == start_state:
            graph.node(str(start_state), style= 'filled', fillcolor = '#87CEEB', shape= 'circle', rank = 'same')
            
        for i in end_state:
            graph.node(str(i), shape= 'doublecircle', rank = 'same')
             
        graph.attr('node', shape='circle')
        graph.edge(str(inicio), str(fin), label= str(label))

    graph.view()

def convertToAFD(transitions):

    # AFN variables
    afn_transitions = transitions[0]
    start_state = afn_transitions[0][0]
    end_state = afn_transitions[-1][1]
    states_afn = []

    # AFD variables
    alphabet = []
    stack = []
    subgroups =[]
   
    #Get alphabet 
    for i in (transitions):
        for j in i:
            if j[2] not in alphabet and j[2] != 'ε':
                alphabet.append(j[2])

    #Get states used on the AFN
    for g in (transitions):
        for r in g:
            if r[0] not in states_afn:
                states_afn.append(r[0])
            if r[1] not in states_afn:
                states_afn.append(r[1])

    #Get transitions
    initial_closure = e_Closures(afn_transitions,start_state)
    stack.append(initial_closure)
    subgroups.append(initial_closure)
    
    afn_transitions_dict = {}
    for move in afn_transitions:
        if move[2] in alphabet:
            key = (move[0], move[2])
            if key in afn_transitions_dict:
                afn_transitions_dict[key].append(move[1])
            else:
                afn_transitions_dict[key] = [move[1]]

                

    afd_transitions = []
    new = {}
    for subgroup in subgroups:
        for symbol in alphabet:
            new_group = []
            new_subgroup =[]
            for state in subgroup:
                key = (state, symbol)
                if key in afn_transitions_dict:
                    new_group += afn_transitions_dict[key]
            if new_group:
                new_group = list(set(new_group))
                for states in new_group:
                    
                    move_closure = e_Closures(afn_transitions,states) 
                    
                    new[states] = move_closure
                    new_subgroup += new[states]

                    nws = list(set(new_subgroup))
                    
                if nws not in subgroups:
                    subgroups.append(nws)
                
                afd_transitions.append((subgroup, nws,symbol))

    Trans_convert, end =convert(afd_transitions,end_state)
    graph_afd(Trans_convert, end)

    print(Trans_convert,end)
    return Trans_convert , set(end)
