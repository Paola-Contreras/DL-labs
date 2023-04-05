'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

from Arbol import * 
from Validacion import*
from Postfix import *
from Yalex import *

# ingreso de expresion y conversion
doc = 'ArchivosYALex/slr-2.yal'
read_doc = mainYalex(doc)
expresion_compuesta = fix_expression(read_doc)
posfix = convert_postfix(expresion_compuesta)

# Hacer arbol y subarboles
tree = make_tree(posfix)
subtrees_list = tree.postorder_traversal()
print(subtrees_list)