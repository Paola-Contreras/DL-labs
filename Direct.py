'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

import graphviz
from Automata import *
from AFD import *

followpos_dict = {}

class Direct:
    def __init__(self,tree, treeLF,hash_dic):
        self.tree = tree
        self.nodes = treeLF
        self.alfabeto = self.alphabet(tree)
        self.states = None
        self.start_state = None
        self.end_state = None
        self.transitions = None
        self.getIdToken = hash_dic

    def alphabet(self, tree):
        alfa = []
        traversal_result = tree.postorder_traversal()
       
        for i in range(len(traversal_result)):
            node_name = traversal_result[i][0]
            node_value= traversal_result[i][1]
            if node_value == '#' or node_value == 'ε':
                pass
            else:
                if node_name == 'Simbolo':
                    node_value = traversal_result[i][1]
                    alfa.append(node_value)

        return set(alfa)
    
    def flatten(self,l):
        for el in l:
            if isinstance(el, list) or isinstance(el, tuple):
                yield from self.flatten(el)
            else:
                yield el
        
    def nullable(self, node=None):
        #calculo de nullable en base a las reglas y procedencia de los operadores
        if node.left == None and node.right == None:
            #return node.value == "ε"
            if node.value == "ε":
                return True
        elif node.value == "*" or node.value == "?":
            return True
        elif node.value == "+":
            return self.nullable(node.left)
        elif node.value == "·":
            return (self.nullable(node.left) and self.nullable(node.right))
        elif node.value == "|":
            return (self.nullable(node.left) or self.nullable(node.right))
        #return False

    def firstpos(self,node):        
        if node.left == None and node.right == None:
            if node.value == "ε":
                return ()
            else:
                return node.position
        else:
            if node.value == "*" or node.value == "?" or  node.value == "+":
                return self.firstpos(node.left)
            elif node.value == "ε":
                return ()
            elif node.value == "·":
                if node.left.label['nullable'] is True:
                    return (self.firstpos(node.left) , self.firstpos(node.right))
                else:
                    return self.firstpos(node.left)
            elif node.value == "|":
                return (self.firstpos(node.left) , self.firstpos(node.right))

    def lastpos(self, node):
        if node.left == None and node.right == None:
            if node.value == "ε":
                return ()
            else:
                return node.position
        else:
            if node.value == "ε":
                return ()
            elif node.value == "*" or node.value == "?" or  node.value == "+":
                return self.lastpos(node.left)
            elif node.value == "·":
                if node.right.label['nullable'] is True:
                    return (self.lastpos(node.left) , self.lastpos(node.right))
                else:
                    return self.lastpos(node.right)
            elif node.value == "|":
                return (self.lastpos(node.left) , self.lastpos(node.right))
        
    def followpos(self,node):
        if node.value == "·":
            if node.left.value is not None:
                for i in node.left.label["lastpos"]:
                    if i in followpos_dict:
                        if type(followpos_dict[i]) is set and type(node.right.label["firstpos"]) is set:
                            followpos_dict[i] |= node.right.label["firstpos"]
                        else:
                            #print(i)
                            followpos_dict[i].update({node.right.label["firstpos"]})
                    else:
                        followpos_dict[i] = node.right.label["firstpos"]
                return followpos_dict
           
        elif node.value == "*" or node.value == "+":
            for i in node.label["lastpos"]:
                if i in followpos_dict:
                    if type(followpos_dict[i]) is set and type(node.label["firstpos"]) is set:
                            followpos_dict[i] |= node.label["firstpos"]
                    else:
                        followpos_dict[i].update({node.label["firstpos"]})
                else:
                    followpos_dict[i] = node.label["firstpos"]
            return followpos_dict
        else:
            pass

    def convert(self,tuplas,end,start):
        diccionario = {}
        endstates = []
        startstates = ''
        letra = 'A'
        for tupla in tuplas:
            lista1, lista2, letra_tupla = tupla
            if tuple(lista1)not in diccionario:
                diccionario[tuple(lista1)] = letra
                letra = chr(ord(letra) + 1)
            if tuple(lista2) not in diccionario:
                diccionario[tuple(lista2)] = letra
                letra = chr(ord(letra) + 1)
        
        for val in diccionario.keys():
            for num in end[0]:
                valor = diccionario[num]
                if valor not in endstates:
                    endstates.append(valor)
            if tuple(start) == val:
                startstates = diccionario[val]

        tuplas_nuevas = []
        for tupla in tuplas:
            lista1, lista2, letra_tupla = tupla
            nueva_lista1 = diccionario[tuple(lista1)]
            nueva_lista2 = diccionario[tuple(lista2)]
            tupla_nueva = (nueva_lista1, nueva_lista2, letra_tupla)
            tuplas_nuevas.append(tupla_nueva)
        #print(endstates,"fin")
        return tuplas_nuevas,endstates,startstates
    
    def graph_afd(self,afd,end=None,start=None):
        graph = graphviz.Digraph('AFD Directo', filename='AFD_Dir', format= 'png')
        graph.attr(rankdir='LR',labelloc="t",)

        start_state = start
        end_state = end

        for inicio,fin,label in afd:
            if inicio == start_state:
                graph.node(str(start_state), style= 'filled', fillcolor = '#87CEEB', shape= 'circle', rank = 'same')
                
            for i in end_state:
                graph.node(str(i), shape= 'doublecircle', rank = 'same')
                
            graph.attr('node', shape='circle')
            graph.edge(str(inicio), str(fin), label= str(label))

        
        #graph.view()

    def construct(self):
        follow_tables = []
        final = []
        for i in self.nodes:
            i.label["nullable"] = self.nullable(i)
            tupla =  self.firstpos(i)
            if type(tupla) is tuple:
                conjunto = set(self.flatten(tupla))
            elif type(tupla) is int:
                conjunto = [tupla]
                conjunto2 = set(conjunto)
                conjunto = conjunto2
            else:
                conjunto = tupla

            i.label["firstpos"] = conjunto
            

            tuplafn =  self.lastpos(i)
            if type(tuplafn) is tuple:
                conjuntofn = set(self.flatten(tuplafn))
            elif type(tuplafn) is int:
                conjuntofn = [tuplafn]
                conjuntofn2 = set(conjuntofn)
                conjuntofn = conjuntofn2
            else:
                conjuntofn = tuplafn

            i.label["lastpos"] = conjuntofn

            tuplafoll =  self.followpos(i)
            if type(tuplafoll) is tuple:
                conjuntofoll = set(self.flatten(tuplafoll))
            elif type(tuplafoll) is int:
                conjuntofoll = [tuplafoll]
                conjuntofoll2 = set(conjuntofoll)
                conjuntofoll = conjuntofoll2
            else:
                conjuntofoll = tuplafoll
            i.label["followpos"] = conjuntofoll

            # print (i.label["nullable"],  i.value,'null','\n')
            #print (i.label["firstpos"],  i.value,'first','\n')
            # print (i.label["lastpos"],  i.value,'last','\n')
            # #if i.label["followpos"] != {}:
            #print (i.label["followpos"], i.value,'follow','\n')
       
        for j in self.nodes:
            if j.position != None:
                    if j.value != '#':
                        follow_tables.append([j.position,j.value,followpos_dict[j.position]])
                    else:
                        final.append(j.position)
        #print(followpos_dict)

        alfabe = {}
        for sublst in follow_tables:
            key = sublst[0]
            if key not in alfabe:
                alfabe[key] = {}
            if sublst[1] not in alfabe[key]:
                alfabe[key][sublst[1]] = set()
            alfabe[key][sublst[1]].update(sublst[2])

        #print(alfabe)
                
        # ------------ Transitions -------------
        visited =[]
        states = []
        transitions = []
        end=[]
        start =(self.tree.label['firstpos'])
        #print(start,'inicio')
        
        states.append(tuple(start))
        visited.append(tuple(start))
        #print(final)
        while len(states)>0:
            temp ={}
            temp2 = {}
            actual_state = states.pop()
            for char in self.alfabeto:
                for state in actual_state:
                    if state in final:
                        continue
                    else:
                        get_subkey = alfabe[state]
                        if state in alfabe.keys():
                            if char in get_subkey.keys():
                                new_state = alfabe[state]
                                temp[state]= new_state
            #print(temp,'DICCIONARIO TEMPORAL')
            for el in temp.values():
                for keys, val in el.items():
                    if keys not in temp2:
                        temp2[keys] =val.copy()
                    else:
                        temp2[keys].update(val)
                
            for k, v in temp2.items():
                #print(temp2,'tamos')
                if tuple(v) not in visited:
                    visited.append(tuple(v))
                    states.append(tuple(v))
                    transitions.append([actual_state,tuple(v),k])
                else:
                    is_added = False
                    for t in transitions:
                        if t[0] == actual_state and t[1] == tuple(v) and t[2] == k:
                            is_added = True
                            break
                    if not is_added:
                        transitions.append([actual_state, tuple(v), k])
        
        filtrada = [tupla for tupla in visited if any(elem in final for elem in tupla)]
        end.append(filtrada)
        
        #print('\n',transitions)
        #print(visited,'VISITED')
        #print(end)
        trans, end_s, start_s= self.convert(transitions,end,start)
        # print(end_s)
        # print(trans)
        self.graph_afd( trans, end_s, start_s)
        trans_dic = {}

        for tupla in transitions:
            clave, valor, letra = tupla
            if clave not in trans_dic:
                trans_dic[clave] = {}
            trans_dic[clave][letra] = valor
            
        #print(trans_dic)
        self.states = visited
        self.transitions = trans_dic
        self.end_state = end
        self.start_state = start
        self.tokenhash = final 
        #print(self.tokenhash)
        # Crear una instancia de la clase Automata y asignar valores a sus atributos
        self.afd = AFD(states=self.states, start=self.start_state, end=self.end_state, transitions=self.transitions, alphabet=self.alfabeto, tokenhash = self.tokenhash,getIdToken=self.getIdToken)
        return  self.states,self.start_state, self.end_state, self.transitions, self.alfabeto,self.tokenhash, self.getIdToken
    
    # def fix_cadena(self,cadena):
    #     cadenas = []
    #     string = ''
    #     for i in cadena:
    #         if i not in ['\n', ' ']:
    #             string +=i
    #         if i in ['\n', ' ']:
    #             if string == '':
    #                 continue
    #             else:
    #                 # if i == '\n':
    #                 #     cadenas.append(string.strip())
    #                 #     string = ''
    #                 #     cadenas.append('\\n')
    #                 # else:
    #                     cadenas.append(string.strip())
    #                     string = ''
    #                     cadenas.append(i)
    #     if string:
    #         cadenas.append(string.strip())

    #     return cadenas

    # def simulation(self,cadena):
    #     transiciones = self.transitions
    #     estado_actual = self.start_state
    #     cadena=self.fix_cadena(cadena)
    #     token = []
    #     ID = []
    #     self.getIdToken['error'] = 0
    #     print("\033[1m Simulacion de Palabras \033[0m")
    #     for palabra in cadena:
    #         for simbolo in palabra:
    #             if simbolo == '\n':
    #                 simbolo ='\\n'
    #                 if simbolo in tuple(transiciones[tuple(estado_actual)]):
    #                     estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
    #                 else:
    #                     print(f"-> No se encontraron transiciones para '{simbolo}")
    #                     token.append({0})
    #                     break
    #             elif simbolo == '\t':
    #                 simbolo ='\\t'
    #                 if simbolo in tuple(transiciones[tuple(estado_actual)]):
    #                     estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
    #                 else:
    #                     print(f"-> No se encontraron transiciones para '{simbolo}")
    #                     token.append({0})
    #                     break
    #             else:
    #                 if simbolo in tuple(transiciones[tuple(estado_actual)]):
    #                     estado_actual = tuple(transiciones[tuple(estado_actual)][simbolo])
                    
    #                 else:
    #                     print(f"» La cadena '\033[1m{palabra}\033[0m' no es aceptada por el autómata")
    #                     print(f"-> No se encontraron transiciones para '{simbolo}")
    #                     token.append({0})
    #                     break
    #         else:
    #             if estado_actual in self.end_state[0]:
    #                 print(f"» La cadena '\033[1m{palabra}\033[0m' es aceptada por el autómata")
    #                 token_num = set(estado_actual) & set(self.tokenhash)
    #                 token.append(token_num)
    #             else:
    #                 print(f"» La cadena '\033[1m{palabra}\033[0m' no es aceptada por el autómata")

    #         estado_actual = self.start_state
        
    #     # --- OBTENER TOKENS ---
    #     #print(token)
    #     token = [x for conjunto in token for x in conjunto]
        
    #     for num in token:
    #         for k,v in self.getIdToken.items():
    #             if num == v:
    #                 ID.append(k)
    #     print(ID)
    #     print(self.end_state[0])
    # #     return ID
