'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

from Arbol import * 
from Validacion import*
from Postfix import *

# ingreso de expresion y conversion
expresion_original = "(b|b)*abb(a|b)*"
expresion_compuesta = fix_expression(expresion_original)
check = validate(expresion_compuesta)

if check == 0:
    expresion = convert_postfix(expresion_compuesta)
    print(expresion,'post')

# Hacer arbol y subarboles
tree = make_tree(expresion)
subtrees_list = tree.postorder_traversal()