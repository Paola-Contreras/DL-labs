# ------ Clase automata ------ 
'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

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
        #print(ID)
        return ID
    
#--------------------------- MAIN -------------------------------
afd = AFD(
            states = [(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 26, 39, 40, 42, 44, 46), (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), (1, 2, 3, 4), (43,), (47,), (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), (45,), (41,), (32, 33, 34, 35, 36, 37, 38, 39, 27, 28, 29, 30, 31), (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31)],
            start = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 26, 39, 40, 42, 44, 46},
            end = [[(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 26, 39, 40, 42, 44, 46), (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), (1, 2, 3, 4), (43,), (47,), (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), (45,), (41,), (32, 33, 34, 35, 36, 37, 38, 39, 27, 28, 29, 30, 31), (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31)]],
            transitions = {(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 26, 39, 40, 42, 44, 46): {'3': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), ' ': (1, 2, 3, 4), '9': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '<': (43,), '0': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), ')': (47,), '1': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '7': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '\\n': (1, 2, 3, 4), '\\t': (1, 2, 3, 4), '2': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '.': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '(': (45,), '4': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '8': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '6': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '>': (41,), '5': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), 'E': (32, 33, 34, 35, 36, 37, 38, 39, 27, 28, 29, 30, 31)}, (32, 33, 34, 35, 36, 37, 38, 39, 27, 28, 29, 30, 31): {'3': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '9': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '0': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '1': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '7': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '2': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '4': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '8': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '6': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '>': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '5': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '-': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31)}, (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31): {'3': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '9': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '0': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '1': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '7': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '2': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '4': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '8': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '6': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31), '5': (32, 33, 34, 35, 36, 37, 38, 39, 29, 30, 31)}, (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26): {'3': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '9': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '0': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '1': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '7': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '2': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '4': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '8': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '6': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '5': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), 'E': (32, 33, 34, 35, 36, 37, 38, 39, 27, 28, 29, 30, 31)}, (1, 2, 3, 4): {' ': (1, 2, 3, 4), '\\n': (1, 2, 3, 4), '\\t': (1, 2, 3, 4)}, (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26): {'3': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '9': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '0': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '1': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '7': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '2': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '.': (39, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26), '4': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '8': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '6': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), '5': (5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 39, 26), 'E': (32, 33, 34, 35, 36, 37, 38, 39, 27, 28, 29, 30, 31)}}, 
            alphabet = {'3', ' ', '9', '<', '0', ')', '1', '7', '\\n', '\\t', '2', '.', '(', '4', '8', '6', '>', '5', 'E', '-'},
            tokenhash= [4, 39, 41, 43, 45, 47],
            getIdToken = {'ws': 4, 'number': 39, '>': 41, '<': 43, '(': 45, ')': 47}
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
    