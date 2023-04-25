'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''
# ------ Clase automata ------
class Automata():
    def __init__(self, states, start, end, transitions, alphabet):
        self.alfabet = alphabet
        self.states = states
        self.start_state = start
        self.end_state = end
        self.transitions = transitions
    '''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

from Automata import *
# ------ Clase AFD ------
class AFD(Automata):
    def __init__(self,states, start, end, transitions, alphabet, getIdToken, tokenhash):
        super().__init__(states, start, end, transitions, alphabet)
        self.getIdToken = getIdToken
        self.tokenhash = tokenhash

    def fix_cadena(self,cadena):
        cadenas = []
        string = ''
        for i in cadena:
            if i not in ['\n', ' ']:
                string +=i
            if i in ['\n', ' ']:
                if string == '':
                    continue
                else:
                    cadenas.append(string.strip())
                    string = ''
                    cadenas.append(i)
        if string:
            cadenas.append(string.strip())

        return cadenas

    def simulation(self,cadena):
        transiciones = self.transitions
        estado_actual = self.start_state
        cadena=self.fix_cadena(cadena)
        token = []
        ID = []
        self.getIdToken['error'] = 0
        print("\033[1m Simulacion de Palabras \033[0m")
        for palabra in cadena:
            for simbolo in palabra:
                if simbolo == '\n':
                    simbolo ='\\n'
                    if simbolo in tuple(transiciones[tuple(estado_actual)]):
                        estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
                    else:
                        print(f"-> No se encontraron transiciones para '{simbolo}")
                        token.append({0})
                        break
                elif simbolo == '\t':
                    simbolo ='\\t'
                    if simbolo in tuple(transiciones[tuple(estado_actual)]):
                        estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
                    else:
                        print(f"-> No se encontraron transiciones para '{simbolo}")
                        token.append({0})
                        break
                elif simbolo == '+':
                    simbolo ='&'
                    if simbolo in tuple(transiciones[tuple(estado_actual)]):
                        estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
                    else:
                        print(f"-> No se encontraron transiciones para '{simbolo}")
                        token.append({0})
                        break
                elif simbolo == '*':
                    simbolo ='^'
                    if simbolo in tuple(transiciones[tuple(estado_actual)]):
                        estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
                    else:
                        print(f"-> No se encontraron transiciones para '{simbolo}")
                        token.append({0})
                        break
                else:
                    if simbolo in tuple(transiciones[tuple(estado_actual)]):
                        estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
                    
                    else:
                        print(f"» La cadena '\033[1m{palabra}\033[0m' no es aceptada por el autómata")
                        print(f"-> No se encontraron transiciones para '{simbolo}")
                        token.append({0})
                        break
            else:
                if estado_actual in self.end_state[0]:
                    print(f"» La cadena '\033[1m{palabra}\033[0m' es aceptada por el autómata")
                    token_num = set(estado_actual) & set(self.tokenhash)
                    token.append(token_num)
                else:
                    print(f"» La cadena '\033[1m{palabra}\033[0m' no es aceptada por el autómata")

            estado_actual = self.start_state
        
        # --- OBTENER TOKENS ---
        #print(token)
        token = [x for conjunto in token for x in conjunto]
        
        for num in token:
            for k,v in self.getIdToken.items():
                if num == v:
                    ID.append(k)
        print(ID)
        return ID
    
#--------------------------- MAIN -------------------------------
afd = AFD(
            states = [(1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 44, 46, 48, 50), (16,), (17, 45, 5, 43, 29), (4,), (51,), (47,), (49,), (5,), (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 30, 31), (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28), (28,), (43, 29), (42,), (43,), (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42), (17, 43, 29)],
            start = {1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 44, 46, 48, 50},
            end = [[(17, 45, 5, 43, 29), (51,), (47,), (49,), (5,), (43, 29), (43,), (17, 43, 29)]],
            transitions = {(1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 44, 46, 48, 50): {'4': (16,), '&': (17, 45, 5, 43, 29), '\\t': (4,), '9': (16,), ' ': (4,), '8': (16,), '1': (16,), '7': (16,), ')': (51,), '5': (16,), '^': (47,), '(': (49,), '6': (16,), '\\n': (4,), '3': (16,), '2': (16,), '0': (16,)}, (4,): {'&': (5,)}, (17, 45, 5, 43, 29): {'E': (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 30, 31), '.': (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28)}, (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28): {'4': (28,), '&': (43, 29), '9': (28,), '8': (28,), '1': (28,), '7': (28,), '5': (28,), '6': (28,), '3': (28,), '2': (28,), '0': (28,)}, (43, 29): {'E': (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 30, 31)}, (28,): {'&': (43, 29)}, (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 30, 31): {'4': (42,), '&': (43,), '>': (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42), '9': (42,), '8': (42,), '1': (42,), '7': (42,), '5': (42,), '-': (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42), '6': (42,), '3': (42,), '2': (42,), '0': (42,)}, (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42): {'4': (42,), '&': (43,), '9': (42,), '8': (42,), '1': (42,), '7': (42,), '5': (42,), '6': (42,), '3': (42,), '2': (42,), '0': (42,)}, (42,): {'&': (43,)}, (16,): {'&': (17, 43, 29)}, (17, 43, 29): {'E': (32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 30, 31), '.': (18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28)}}, 
            alphabet = {'4', '&', '\\t', '>', '9', ' ', '8', '1', '7', ')', '5', 'E', '^', '-', '(', '6', '\\n', '3', '2', '.', '0'},
            tokenhash= [5, 43, 45, 47, 49, 51],
            getIdToken = {'ws': 5, 'number': 43, '&': 45, '^': 47, '(': 49, ')': 51}
        )
        
from Scanner import *
# ------ SIMUATION -------

# Archivo con palabras a simular
with open('test.txt', 'r') as archivo:
    contenido = archivo.read()

Tokens = afd.simulation(contenido)

from Scanner import *

with open('ReconizedToken.txt', 'w') as archivo:
    archivo.write('--- TOKENS RECONOCIDOS ---\n')
    for i in Tokens:
        findToken=scanner(i)
        archivo.write(f'{findToken}\n')        
    