'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

from Arbol import * 
from Validacion import*
from Postfix import *

from AFN import *
from AFD import *
from DirectAFD import *
from Minimization import *

# ingreso de expresion y conversion
expresion_original = "a(a?b*|c+)b|baa"
expresion_compuesta = fix_expression(expresion_original)
check = validate(expresion_compuesta)

if check == 0:
    expresion = convert_postfix(expresion_compuesta)
    print(expresion,'post')

# Hacer arbol y subarboles
tree = make_tree(expresion)
subtrees_list = tree.postorder_traversal()

print('\n --- THOMPSHON --- ')
AFN = thompson(subtrees_list)

# print ('\n --- AFD SUBCONJUNTOS --- ')
# AFD, Final_states = convertToAFD(AFN)

# print('\n --- AFD DIRECTO --- ')
# AFD_D = direct(expresion_original)

# print('\n --- Minimization --- ')
# MIN = main_minimization(AFD, Final_states)
