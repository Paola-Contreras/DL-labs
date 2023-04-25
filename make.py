'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

def make_automata(states, start, end, transitions, alphabet, tokenhash, getIdToken):
    
    with open('Automata.py') as archivo:
        Automata = archivo.read()

    with open('AFD.py') as archivo:
        AFD = archivo.read()
    
    with open('Scan2.py', 'w') as archivo:
        archivo.write(Automata)
        archivo.write(AFD)
        instance = f'''
#--------------------------- MAIN -------------------------------
afd = AFD(
            states = {states},
            start = {start},
            end = {end},
            transitions = {transitions}, 
            alphabet = {alphabet},
            tokenhash= {tokenhash},
            getIdToken = {getIdToken}
        )
        '''
    
        simular = '''
from Scanner import *
# ------ SIMUATION -------

# Archivo con palabras a simular
with open('test.txt', 'r') as archivo:
    contenido = archivo.read()

Tokens = afd.simulation(contenido)

from Scanner import *

with open('ReconizedToken.txt', 'w') as archivo:
    archivo.write('--- TOKENS RECONOCIDOS ---\\n')
    for i in Tokens:
        findToken=scanner(i)
        archivo.write(f'{findToken}\\n')        
    '''
    
        archivo.write(instance)
        archivo.write(simular)
