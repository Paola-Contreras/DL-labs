'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

import graphviz
from LabC import Arbol as ar
from Validacion import*
from LabC import Postfix as p

objects = []
nodes_val =[]

class Direct:
    counter = 1
    def __init__(self):
    
        self.nullable = None
        self.label = Direct.counter
        Direct.counter += 1
        self.firstpos = None
        self.lastpos = None
        self.value = None

def symbol(value):
    val = Direct.counter 
    node = Direct()

    node.firstpos = val 
    node.lastpos = val 
    node.value = value

    objects.append(node)
    nodes_val.append(node.label)
 
    return node

def kleene(c1,value):
    counter = Direct.counter 
    node3 = Direct()

    node3.firstpos = c1.firstpos
    node3.lastpos = c1.lastpos
    node3.nullable = True
    node3.label = 0
    node3.value = value

    Direct.counter = counter
    objects.append(node3)

    return node3

def kleene_plus(c1,value):
    counter = Direct.counter 
    node5 = Direct()

    node5.firstpos = c1.firstpos
    node5.lastpos = c1.lastpos
    node5.label = 0
    node5.value = value

    if c1.nullable is True:
        node5.nullable = True
    else:
        node5.nullable = False

    Direct.counter = counter
    objects.append(node5)

    return node5

def union(c1,c2,value):
    counter = Direct.counter 

    node2 = Direct()

    node2.firstpos = [c1.firstpos, c2.firstpos]
    node2.lastpos = [c1.lastpos,c2.lastpos] if isinstance(c1.lastpos, list) else [c1.lastpos] + [c2.lastpos]
    node2.value = value
    Direct.counter = counter
    node2.label = 0
    
    if c1.nullable == True or c2.nullable == True:
        node2.nullable = True

    objects.append(node2)
    
    return node2

def concat (c1,c2,value):
    counter = Direct.counter 
    node4 = Direct()

    if c1.nullable is True:
        node4.firstpos = [c1.firstpos,c2.firstpos]
    else:
        node4.firstpos = c1.firstpos

    if c2.nullable is True:
        node4.lastpos = [c1.lastpos , c2.lastpos]
    else:
        node4.lastpos = c2.lastpos

    node4.value = value
    Direct.counter = counter

    node4.label = 0
    objects.append(node4)
    return node4, c1, c2

def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

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

def transitions(followpos,objects,alphabet):
    new_followpos = {}
    transitions = []
    for key, value in followpos.items():
        if isinstance(value, list):
            new_followpos[key] = flatten(value)
        else:
            new_followpos[key] = value

    new_followpos = dict(sorted(new_followpos.items()))
   

    for symbol in objects:
        if symbol.value in alphabet:
            valor = symbol.value 
            num = symbol.label
            if num in new_followpos:
                new_followpos[num] = [new_followpos[num], [valor]]

    start = [min(nodes_val)]
    end = max(nodes_val)
    new_followpos[end]=[[],['#']]
    stack = [start]
    

    visited=[]
    while stack:
        start = stack.pop()
        for letter in alphabet:
            temp =[]
            count = 0
            for i in start:
                if i not in new_followpos:
                    followpos[i]= [['#']]
                letter_node = ''.join(new_followpos[i][1])
                count += 1
                if letter_node == letter:
                    if new_followpos[i][0] not in temp:
                        temp.append(new_followpos[i][0])
                        
                if count == len(start): 
                    temp1 = sum(temp,[])
                    if temp1:
                        transitions.append((start,temp1,letter))
                        if temp1 not in visited:
                            visited.append(temp1)    
                            if temp1 not in stack:
                                stack.append(temp1)

    return transitions

def graph_afd(afd,end):
    graph = graphviz.Digraph('AFD Direct', filename='AFD_Direct', format= 'png')
    graph.attr(rankdir='LR')

    start_state = afd[0][0][0]
    end_state = end

    if not isinstance(end_state, list):
        end_state = [end_state]
    else:
        end_state = [elem for lst in end_state for elem in (lst if isinstance(lst, list) else [lst])]

    for inicio,fin,label in afd:
        if inicio == start_state:
            graph.node(str(start_state), style= 'filled', fillcolor = '#87CEEB', shape= 'circle', rank = 'same')
            
        for i in end_state:
            graph.node(str(i), shape= 'doublecircle', rank = 'same')
             
        graph.attr('node', shape='circle')
        graph.edge(str(inicio), str(fin), label= str(label))

    graph.view()

def direct (expresion):
    newexpresion = expresion 
    expresion_compuesta = p.fix_expression(newexpresion)
    print(expresion_compuesta)
    
    posfix = p.convert_postfix(expresion_compuesta)
    print(posfix)   

    tree = ar.ExpressionTree.maked_tree(posfix)
    dot = tree.to_dot()
    graph = graphviz.Source(dot)
    graph.render('expresion_regular_yalex0',format='png')

    subtrees_list = tree.postorder_traversal()
    
    stack = []
    alphabet = []
    followpos = {}
    c1_stack = []
    c2_stack =[]

    for name, value in subtrees_list:
        if name == 'Simbolo' and value not in alphabet:
            alphabet.append(value)

        if value in alphabet:
            stack.append(symbol(value))

        if name == 'Kleene' or name == 'Opcional':
            c1 = stack.pop()
            stack.append(kleene(c1,value))

        if name == 'Kleen Positiva':
            c1 = stack.pop()
            stack.append(kleene_plus(c1,value))

        if name == 'Concatenacion':
            c2 = stack.pop()
            c1 = stack.pop()
            
            node4,c1_val,c2_val = concat(c1,c2,value)

            stack.append(node4)
            c1_stack.append(c1_val)
            c2_stack.append(c2_val)
            objects.append(node4)


        if name == 'Union':
            c2 = stack.pop()
            c1 = stack.pop()
            
            stack.append(union(c1,c2,value))
        
    for nodes in objects:
        if nodes.value == '*':
            lp = nodes.lastpos
            fp = nodes.firstpos

            if not isinstance(lp, list):
                    lp = [lp]
            else:
                    lp = [elem for lst in lp for elem in (lst if isinstance(lst, list) else [lst])]
            for num in lp:
                if num in nodes_val:
                    followpos[num] = [fp]

        if nodes.value == '.':
            if len(c1_stack) > 0 or len(c2_stack) >0:
                eval_c1=c1_stack.pop(0)
                eval_c2 = c2_stack.pop(0)

                lp = eval_c1.lastpos
                fp = eval_c2.firstpos

                if not isinstance(lp, list):
                    lp = [lp]
                else:
                    lp = [elem for lst in lp for elem in (lst if isinstance(lst, list) else [lst])]
                    

                if not isinstance(fp, list):
                    fp =[fp]
                else:
                    fp = [elem for lst in fp for elem in (lst if isinstance(lst, list) else [lst])]

                for num in lp:
                    if num in nodes_val:
                        if num in followpos:
                            if len(followpos[num]) == 0:
                                followpos[num] = fp
                            else:
                                if fp not in followpos[num]:
                                    followpos[num].append(fp)
                        else:
                            followpos[num] = fp

    trans= transitions(followpos, objects, alphabet)
    
    end = max(nodes_val)
    new_trans,end2 = convert(trans, end)
    graph_afd(new_trans,end2)

    print(trans)
    return trans
