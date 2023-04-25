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
    