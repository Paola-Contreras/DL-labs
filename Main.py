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
from LabC import ValidacionC as vc
#from AFN import *
from Direct import *


stack = []
# ingreso de archivo 
doc = 'ArchivosYALex/slr-3.yal'
cadena = 'ab'#input("Ingrese la cadena que desea evaluar: ")
# Apertura del archivo y generacion de expresion 
read_doc ='(" "|\t|\n)?+#|(0|1|2|3|4|5|6|7|8|9)?+("."(0|1|2|3|4|5|6|7|8|9)?+)?(E(">"|"-")??(0|1|2|3|4|5|6|7|8|9)?+)?#|">"#|"<"#|"("#|")"#'
for key,value in y.dic_rules.items():
    
    if not key.isalpha():
        read_doc += f'|"{key}"#'

#expresion = '(1|2)(1|2)*12(3|ε)#'
#print(read_doc)
expresion_compuesta = p.fix_expression(read_doc)
#print(expresion_compuesta,'esta')
#expresion_compuesta = p.fix_expression(expresion)
# Realizar posfix y componerla para poder correr el algoritmo de AFD Directo 
posfix = p.convert_postfix(expresion_compuesta)


# Mostrar postfix en un formato mas amigable
pos = ''
for i in posfix:
    pos += f" {i}"
print("\n\033[1m Expresion Postfix \033[0m")
print('-> ',pos)

# Hacer arbol y subarboles
tree, treeLF= a.maked_tree(posfix)
print(treeLF)
print(len(treeLF),'LARGO')
dot = tree.to_dot()
graph = graphviz.Source(dot)
graph.render("tree",format='png')

print(tree)
print(treeLF)
#print(tree.postorder_traversal())
#print(treeLF)
d=Direct(tree,treeLF)
obj = d.construct()

with open('test.txt', 'r') as archivo:
    datos_binarios = archivo.read()
    datos_texto = datos_binarios
    print(datos_texto)
d.simulation(datos_texto)



# direct_dict = d.to_dict()
# direct_str = str(direct_dict)
# with open('AFD_Direct.py', 'w', encoding='utf-8') as f:
#     f.write("atributos = " + direct_str)

