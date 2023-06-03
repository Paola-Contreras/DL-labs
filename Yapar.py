'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

import Read_Yapar as yapar
from prettytable import PrettyTable
import graphviz

prod = yapar.dic_productions
tok = yapar.token_dic

class Tokens():
    def __init__(self,tok):
        self.Ignored =[]
        self.FTokens ={}
        self.tempTok = tok
        self.T = []
        self.Read_Tokens = self.get_Tokens()

        
    def get_Tokens(self):
        tempT =[]
        for k,v in self.tempTok.items():
            if k == 'IGNORE':
                self.Ignored.append(v)
            else:
                self.FTokens[k]=v
        
        for k,v in self.FTokens.items():
            temp = ''
            #print(v)
            for char in v:
                if char == '&':
                    temp += '+'
                elif char == '^':
                    temp += '*'
                else:
                    temp += char
            tempT.append(temp)
        self.T = tempT
        return self.FTokens
        
class Productions():
    def __init__(self,prod):
        self.nonTerminals = {}
        self.Terminals = []
        self.tempProd = prod
        self.productions = self.get_nonT_and_T()
    
    def get_nonT_and_T(self):
        termTemp =[]
        nontermTemp =[]
        palabra = ''

        for val in self.tempProd.values():
            palabra = '' 
            #print(val)
            char = list(val)
            for let in char:
                if let != ' ' and let !="|":
                    palabra += let
                    #print(palabra)
                elif let == ' ': 
                    if palabra.isupper():
                        #print(palabra,'MAY')
                        if palabra not in termTemp:
                            termTemp.append(palabra )
                        palabra = ''
                    elif palabra.islower():
                        #print(palabra,'low')
                        if palabra not in nontermTemp:
                            nontermTemp.append(palabra )
                        palabra = ''
            if palabra:
                #print(palabra,'AQUI')
                if palabra.isupper():
                        #print(palabra,'MAY')
                        if palabra not in termTemp:
                            termTemp.append(palabra )
                        palabra = ''
                elif palabra.islower():
                    #print(palabra,'low')
                    if palabra not in nontermTemp:
                        nontermTemp.append(palabra )
                    palabra = ''
        for k,v in self.tempProd.items():
            if k not in nontermTemp:
                nontermTemp.append(k)
        
        for val in nontermTemp:
            first_let = val[0].upper()
            self.nonTerminals[val]=(first_let)

        for k,v in self.nonTerminals.items():
            for prod_key, prod_value in self.tempProd.items():
                self.tempProd[prod_key] = prod_value.replace(k, v)
        
        self.Terminals = termTemp
        #print(self.nonTerminals)

        return self.tempProd
    
class Gramatica():
    def __init__(self, tok, prod):
        self.production = Productions(prod)
        self.tokens = Tokens(tok)
        self.SLR_Grammar = self.get_grammar()

    def get_grammar(self):
        grammar = {}
        tempGrammar = {}
        actual_productions = self.production.tempProd
        actual_tokens = self.tokens.FTokens
        no_terminals = self.production.nonTerminals
        #print(actual_productions)
        #print(actual_tokens)

        for key, value in actual_productions.items():
            for token, token_value in actual_tokens.items():
                value = value.replace(token, token_value)
            tempGrammar[key] = value

        for k, v in tempGrammar.items():
            temp =''
            for char in v:
                if char == '&':
                    temp += '+'
                elif char == '^':
                    temp += '*'
                else:
                    temp += char
            tempGrammar[k] = temp

        for ke, val in tempGrammar.items():
            for kee , vall in no_terminals.items():
                if ke == kee:
                    grammar[vall]= val
        #print(no_terminals)
        #print(tempGrammar)
        #print(grammar)

        print(f"---\033[1m Gramatica SLR \033[0m---")
        for k,v in grammar.items():
            print(k,'->',v)
        print()
        
        return grammar
 
class YAPAR():
    def __init__(self,tok,prod):
        self.grammar = Gramatica(tok, prod)
        self.FirstSet = self.First()
        self.FollowSet = self.Follow()
        self.symbols = self.s_grammar()
        self.Aumented_SLRG = self.aument_grammar()
        self.UpdateProd = self.new_grammar()
        self.Move = self.Automata()
        self.S_Table = self.Table(self.Move)

    def s_grammar(self):
        nt = self.grammar.production.nonTerminals
        nt = [value for value in nt.values()]
        t = self.grammar.tokens.T
        grammar_symbols=[]

        for c in nt:
            grammar_symbols.append(c)
        
        for r in t:
            grammar_symbols.append(r)

        return grammar_symbols
        
    def replace_rules(self,grammar):
        changed = True
        while changed:
            changed = False
            for key, val in grammar.items():
                for i in range(len(val)):
                    if val[i] in grammar.keys():
                        grammar[key][i:i+1] = grammar[val[i]]
                        changed = True
        return grammar
    
    def First(self):
        SLRG = self.grammar.SLR_Grammar
        first_post = []
        first_set ={}
        #print(SLRG,'SLRG')
        for k, v in SLRG.items():
            productions = v.split(' | ') 
            for prod in productions:
                symbols = prod.split() 
                if symbols[0] == k:  
                    continue
                elif '|' in symbols: 
                    index = symbols.index('|')
                    if symbols[index + 1] not in first_post:
                        first_post.append(symbols[index + 1])
                else:
                    if symbols[0] not in first_post:
                        first_post.append(symbols[0])
            #print(first_post,'lista')
            first_set[k] = first_post
            first_post =[]
        setF = self.replace_rules(first_set)
        # print('---FIRST---')
        # print(setF)
        return setF
    
    def remove_spaces(self,s):
        new_str = ''
        for char in s:
            if char != ' ':
                new_str += char
        return new_str
    
    def Follow(self):
        SLRG = self.grammar.SLR_Grammar
        label = [key for key in SLRG]
        followed = {k: set() for k in label}
        followed[label[0]].add('$')

        for k,v in SLRG.items():
            each = v.split('|')
            #print(each,'Each')
            for el in each:
                el = el.lstrip()
                #print(el,'el')
                P = el.split()
                #print(P,'P')
                if len(P) == 3:
                    followed[k].add(P[1])
                elif len(P) == 2:
                    followed[P[1]] = followed[P[1]].union(followed[k])
                elif len(P) == 1 and P[0] not in label:
                    index = label.index(k)
                    lab = label[index - 1]
                    followed[lab] = followed[lab].union(followed[k])
                elif  len(P) == 1:
                    followed[P[0]] = followed[P[0]].union(followed[k])
        # print('---FOLLOWED---')
        # print(followed)
        return followed

    def aument_grammar(self):
        SLRG = self.grammar.SLR_Grammar
        label = [key for key in SLRG]
        initial_symbol = label[0]
        new_grammar = {}
        converted_dict = {}
        # Agregar una nueva regla para el símbolo inicial aumentado
        augmented_symbol = f'{initial_symbol}`'
        new_grammar[augmented_symbol] = f'{initial_symbol}'

        # Copiar las reglas originales en la nueva gramática
        for non_terminal, production in SLRG.items():
            new_grammar[non_terminal] = production

        for key, value in new_grammar.items():
            productions = value.split(' | ')
            converted_dict[key] = [prod.strip() for prod in productions]

        return converted_dict
    
    def new_grammar(self):
        produc =[]
        SLRG= self.Aumented_SLRG
        for k ,v in SLRG.items():
            for j in v:
                produc.append(f'{k} -> . {j}')
        return produc

    def Closure(self,production):
        closures = []
        nt = self.grammar.production.nonTerminals
        nt = [value for value in nt.values()]
        t = self.grammar.tokens.T
        label_eval = []
        already = []

        splited = production.split(' ')
        dot_pos = splited.index('.')
        
        #print(production)
        #print(splited)
        # print(self.UpdateProd)
        label_eval.append(splited[dot_pos+1])
        already.append(splited[dot_pos+1])
        closures.append(production)

        while len(label_eval) > 0:
            in_Nt = label_eval.pop()
            if in_Nt in t:
                #print('Es un terminal, se termina')
                continue
            elif in_Nt in nt:
                #print('Es un no terminal')
                #print(in_Nt,'l')
                for P in self.UpdateProd:
                    P = P.split(' -> ')
                    #print(P)
                    if in_Nt == P[0]:
                        new_eval = P[1]
                        #print(P[1],'PROD')  
                        dot_index = new_eval.index('.')
                        next_character = new_eval[dot_index + 2]
                        closures.append(f'{in_Nt} -> {new_eval}')
                        if next_character not in already:
                            already.append(next_character)
                            label_eval.append(next_character)
                        
        #print(closures)
        return closures

    
    def Moved(self,item,simbol):
        nt = self.grammar.production.nonTerminals
        nt = [value for value in nt.values()]
        t = self.grammar.tokens.T
        I_copy = []
        stack = []
        transitions = []
        #print(item)
        for prod in item:
            I = prod.split()
            #print(I)
            dot_pos = I.index('.')
            if dot_pos + 1 < len(I):
                nt_eval = I[dot_pos+1]
               #print(nt_eval)
                if nt_eval == simbol:
                    I_copy.append(I)

        for It in I_copy:
            #print(It)
            dot_new = It.index('.')
            if dot_new + 1 < len(It):
                # Intercambiar los elementos adyacentes al punto
                It[dot_new], It[dot_new + 1] = It[dot_new + 1], It[dot_new]

            dot_new2 = It.index('.')
            if dot_new2 + 1 < len(It):
                new = It[dot_new2+1]
                if new in nt:
                    #print('closure')
                    n = ' '.join(map(str, It))
                    #print(n)
                    n_c =self.Closure(n)
                    #print(n_c)
                    #print('closure')
                    for cl in n_c:
                        stack.append(cl)
                elif new in t:
                    n = ' '.join(map(str, It))
                    #print(n)
                    stack.append(n)
            elif It[-1] == '.':
                n = ' '.join(map(str, It))
                stack.append(n)
                #print(n)

            #print(It,simbol)

        #print(item)
        #print(simbol)
        #print(stack,'stack')

        if len(stack) != 0:
            transitions.append((item,stack,simbol))

        return stack, transitions
    
    def graph_afd(self,trans):
        graph = graphviz.Digraph('AFD Directo', filename='SLR_Automata', format= 'png')
        graph.attr(rankdir='LR',labelloc="t",)
        
        
        for transicion in trans:
            T = transicion[0]
            #print(T,'T')
            inicio, fin, label = T[0], T[1], T[2]
            # print(inicio,'INI')
            # print(fin,'FIN')
            # print(label,'LAB')
            
        
            graph.node(str(inicio), shape='square', rank='same')
            graph.node(str(fin), shape='square', rank='same')
            graph.attr('node', shape='square')
            graph.edge(str(inicio), str(fin), label=str(label))

        graph.view()

    def Automata(self):
        simbol = self.symbols
        temp = []
        trans = []
        evaluated = []

        
        start = self.UpdateProd[0]
        Fc = self.Closure(start)
        temp.append(Fc)

        while len(temp) > 0:
            item = temp.pop(0)
            #print(item,'POP')
            evaluated.append(item)
            for sym in simbol:
                #print(item)
                ss, tran = self.Moved(item,sym)
                if ss != []:
                    if ss not in evaluated and ss not in temp and temp != Fc:
                        temp.append(ss)
                    trans.append(tran)
                    
            #print(len(temp))
            #print(tran)
        #print(temp,'HAVING')
        #print(trans,'FIN')
        #for tt in evaluated:
        fin = [(evaluated[1],"Aceptacion",'$')]
        trans.append(fin)
        #evaluated.append()
        #self.graph_afd(trans)
        self.ADF_TRANS = trans
        #print(evaluated)
        #print(trans)
        return trans, evaluated 

    
    def Table(self, productions):
        prod,states = productions
        #print(states)
        states_num = {}
        table ={}

        label =[]
        nonT =[]
        tok = []

        Individual_prod =[]
        ends_point = []

        #grama = self.grammar.SLR_Grammar
       # print(grama)

        for indice, valor in enumerate(states):
            states_num[valor[0]]= indice
            table[indice] =[]
        #print(states_num) 

        for i in self.grammar.production.nonTerminals:
            label.append(i[0].upper())
            nonT.append(i[0].upper())

        tok.append("$")
        for i in self.grammar.tokens.T:
            label.append(i)
            tok.append(i)
        label.append("$")

        for i in prod:
            if i[0][2] in nonT:
                #print(i[0],'AAA')
                for key in states_num.keys():
                    if key in i[0][1]:
                        #print(i[0][0][0])
                        k = states_num[i[0][0][0]]
                        table.setdefault(k, []).append((i[0][2],states_num[key]))
                        #print(key,'IN')
            elif i[0][2] in tok:
                for key in states_num.keys():
                    if key in i[0][1]:
                        #print(i[0][0][0])
                        k = states_num[i[0][0][0]]
                        table.setdefault(k, []).append((i[0][2],f"s{states_num[key]}"))
                        #print(key,'IN')
                if i[0][2] == '$':
                    k = states_num[i[0][0][0]]
                    #print(k)
                    table.setdefault(k, []).append((i[0][2],"acc"))
            if i[0][0] not in Individual_prod:
                Individual_prod.append(i[0][0])
            elif i[0][1] not in Individual_prod:
                Individual_prod.append(i[0][1])


        for j in Individual_prod:
            #print(j)
            for val in j:
                if val.endswith(" ."):
                    #print(val)
                    if 'E`' in val:
                        pass
                    else:
                        ends_point.append(val)

        #print(self.FollowSet)
        #print(self.grammar.SLR_Grammar)

        Invert_gramar = {}

        for clave, valor in self.grammar.SLR_Grammar.items():
            partes = valor.split("|")
            parte_izquierda = partes[0].strip()
            parte_derecha = partes[1].strip()

            Invert_gramar[parte_izquierda] = clave
            Invert_gramar[parte_derecha] = clave

        #print(Invert_gramar,'aqui')

        end = []
        for i in ends_point:
            indice_flecha = i.index("->")
            parte_izquierda = i[:indice_flecha].strip()
            parte_derecha = i[indice_flecha + 2:].strip()
            #print(parte_izquierda)
            a = self.FollowSet [parte_izquierda]
            end.append([a,parte_izquierda,parte_derecha.rstrip(' .')])
            #print(a,parte_izquierda,'AQUI')
        #print(end)

        num_grammar = {}
        for indice, (clave, valor) in enumerate(Invert_gramar.items() , start=1):
            num_grammar[clave] = indice
            #print(indice, clave, valor)

        #print(num_grammar)

        for el in end:
            # print(el[2])
            # print(num_grammar[el[2]])
            # print(el[0])
            for it in el[0]:
                #print(it)
                if it not in nonT:
                    table.setdefault(num_grammar[el[2]], []).append((it[0],f"r{num_grammar[el[2]]}"))


        # Crear una tabla
        tabla = PrettyTable()
        tabla.field_names = ['States'] + label

        # Agregar los datos a la tabla
        for key, valores in table.items():
            fila = []
            fila.append(key)
            for encabezado in label:
                for tupla in valores:
                    if tupla[0] == encabezado:
                        fila.append(tupla[1])
                        break
                else:
                    fila.append('')
            tabla.add_row(fila)

        print(f"\t\t   ---\033[1m TABLA \033[0m---")
        print(tabla)
        #print(table)
        #print(label)
        #print(Individual_prod)







#print (docs)
YAPAR(tok,prod)
