'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

import graphviz
from LabC.Arbol import ExpressionTree as a
from Validacion import*
from LabC import Postfix as p
from LabC import Yalex as y
from Direct import *
from make import *


doc = 'ArchivosYALex/slr-3.yal'
read_doc = y.mainYalex(doc)
new_expresion = y.new_expresion
pos = 1

stack =[]
treeLFs2 = []
treeLFs3 =[] 
hash_dic  = {}

# Realizar arbol por cada value obtenido 
for k,v in new_expresion.items():
    expresion_compuesta = p.fix_expression(v)
    posfix = p.convert_postfix(expresion_compuesta)
    trees,treeLFs= a.maked_tree(posfix,pos)
    stack.append(trees)
    # print(expresion_compuesta)
    for i in treeLFs:
        if i.value == '#':
            pos = i.position + 1
            hash_dic[k]=i.position
        #print(i.position,i.value)

# Unificar arboles
while len(stack)>1:
    a1 = stack.pop()
    a2 = stack.pop()
    tree, node= a.unir(a2,a1,"|")
    stack.append(tree)
treeLFs2.append(node)

# Obtener lista de nodos para realizar AFD
getl = treeLFs2.pop()
for i in getl:
    for k in i:
        treeLFs3.append(k)

# Mostrar graficamente el arbol obtenido 
dot = tree.to_dot()
graph = graphviz.Source(dot)
graph.render("tree",format='png')

# Simulacion 
d=Direct(tree,treeLFs3,hash_dic)
state,start,end,trans,alphabet,tokenhash,dichash= d.construct()

make_automata(state,start,end,trans,alphabet,tokenhash,dichash)

