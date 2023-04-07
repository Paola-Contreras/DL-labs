'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

from Arbol import * 
from Validacion import*
from Postfix import *
from Yalex import *
import graphviz

# ingreso de expresion y conversion
doc = 'ArchivosYALex/slr-1.yal'
read_doc = mainYalex(doc)
expresion_compuesta = fix_expression(read_doc)
posfix = convert_postfix(expresion_compuesta)

# Hacer arbol y subarboles
tree = make_tree(posfix)


# Obtener la representación y crear una imagen 
dot = tree.to_dot()
graph = graphviz.Source(dot)
graph.render('expresion_regular',format='png')

