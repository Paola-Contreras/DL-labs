'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

value = []
dic_prod = {}
dic_rules = {}
new_expresion ={}
get_changed_values = {} 
updated_proddictionary = {}


def openFile (doc):
    with open(doc, 'r') as archivo:
        #print("-> Reading file......")
        content = archivo.read() 
        #print(f"-> File read '\033[1m {doc} \033[0m'\n")
        content = content.replace('\t', '')
    return content

def convert_prod_to_dic(prod):
    #Vuelve la lista de producciones en un diccionario 
    for el in prod:
        key = ""
        string1 = ""
        for char in el:
            if char != "=" and char!= "'" :
                string1 += char
                if string1 == "let ":
                    string1 = ""
            if char == "=":
                while string1 and string1[-1] == ' ':
                    string1 = string1[:-1]
                    
                key = string1
                string1 = "" 

        #Se genera diccionario sin vacios 
       
        if string1:
            while string1 and string1[0] == ' ':
                string1 = string1[1:]
            if '[' in string1:
                change = ''
                if ' ' in string1: 
                    for letter in string1:
                        if letter == ' ':
                            change +='"" "'
                        else:
                            change += letter
                    string1 = change
            else:
                string1 = string1.replace(" ", "")
            dic_prod[key] = string1
    
    return dic_prod

def convert_rules_to_dic(rules):
    for el in rules:
        key = ""
        vall = ""
        string2 = ""
        for char in el:
            if char != "|"and char != "{" and char != "}" and char != "'" and char != '"':
                string2+= char
                if string2 == "rule tokens =":
                    string2 = ""
            if char == "{":
                key = string2.strip()
                string2 = ""
            if char == "}":
                vall = string2
                output =""
                #Ciclo para ponerle espacios entre return y resto
                for letter in vall:
                    output += letter
                    if output == "return":
                        output += " "

                vall = output.strip()
                string2 = ""

        if string2:
            # Agrega al diccionario los valores que no tienen return en el archivo y les asigna el return de su llave
            dic_rules[string2] = f"return {string2}"

        else:
            if key !="" and vall !="":
                if key == '+':
                    key = '&'
                    dic_rules[key] = vall
                elif key == '*':
                    key = '^'
                    dic_rules[key] = vall
                else:
                
                    dic_rules[key] = vall


    return dic_rules

def handle_data(contenido):
    prod = []
    rules = []
    string = ""
    is_a_comment = False
    is_in_llaves = False
    temp_string = ""

    # Este se encarga de por cada dato del archivo almacenarlo en una lista omitiendo los comentarios
    for i in range(len(contenido)):
        data = contenido[i]
        if not is_a_comment:
            if data == "(" and contenido[i+1] == "*":
                is_a_comment = True
            elif data != "\n":
                if is_in_llaves:
                    temp_string += data

                else:   
                    string += data

                if data == '{':
                    is_in_llaves = True
                    temp_string = string

                elif data == '}':
                    is_in_llaves = False
                    if temp_string != "":
                        string += temp_string
                        temp_string = ""
                


            elif string:
                if is_in_llaves is True:
                    pass
                else:
                    value.append(string.strip())
                    string = ""
    
        elif data == ")" and contenido[i-1] == "*":
            is_a_comment = False
            if i < len(contenido) - 1:
                i += 1
    
    # En base a la lista general este ciclo genera una lista de producciones y otra de reglas 
    for val in value:
        if "let" in val:
            prod.append(val)
        else:
            rules.append(val)

    #Vuelve la lista a un diccionario    
    convert_prod_to_dic(prod)
    convert_rules_to_dic(rules)
    #print(dic_rules)
    return dic_prod, dic_rules

def add_or (prod):
    expresion = ''
    caracteres = ''
    found_quote = False

    for k, v in prod.items():
        exp2 = ''
        if '[' in v and ']' in v:
            if k == 'delim':
                if 'ε' in v:
                    expresion = "|".join(v)
                    for j in expresion:
                        if j != '\\' and j != '|':
                            caracteres += j

                    for i, char in enumerate(expresion):
                        if char == '[' or char == ']':
                            continue
                        if char in f"{v}":
                            exp2 += char
                        elif char == '|' and expresion[i+1] in caracteres:
                            continue
                        else:
                            exp2 += char
                    dic_prod[k] = f'({exp2})?'

                elif '\\' in v and 'ε' not in v:
                    expresion = "|".join(v)
                    for j in expresion:
                        if j != '\\' and j != '|':
                            caracteres += j

                    for i, char in enumerate(expresion):
                        if char == '[' or char == ']':
                            continue
                        if char in f"{v}":
                            exp2 += char
                        elif char == '|' and expresion[i+1] in caracteres:
                            continue
                        else:
                            exp2 += char

                    exp2 = exp2[1:]
                    dic_prod[k] = f'({exp2})'

            elif k == 'letter':    
                for i, char in enumerate(v):
                    if char == '-':
                        start = ord(v[i-1])
                        end = ord(v[i+1])

                        for letter in range(start,end+1):
                            if letter == start:
                                exp2 += f'{chr(letter)}'
                            else:
                                exp2 += f'|{chr(letter)}'
                        new_string = ''

                        for i in range(len(exp2)):
                            if exp2[i] != '|' and i != len(exp2):
                                new_string += exp2[i] + '|'
                       
                        if new_string[-1] == '|':
                            new_string = new_string[:-1]
                        exp2 = new_string                    

                dic_prod[k] = f'({exp2})'
        
            elif k == 'digit':
                for i, char in enumerate(v):
                        if char == '-':
                            start =int(v[i-1])
                            end = int(v[i+1])
                            for num in range(start,end+1):
                                if num == start:
                                    exp2 += f'{num}'
                                else:
                                    exp2 += f'|{num}'
                        elif char == '"':
                            if not found_quote:
                                found_quote = True
                                start =int(v[2])
                                end = int(v[-3])
                                for num in range(start,end+1):
                                    if num == start:
                                        exp2 += f'{num}'
                                    else:
                                        exp2 += f'|{num}'
                
                dic_prod[k] = f'({exp2})'
        else:
            pass
    return dic_prod

def generate_scanner(dic):
    with open('Scanner.py', 'w') as archivo:
        archivo.write(f'def scanner (rule):\n')
        for k,v in dic.items():
            if ':' in v:
                new_parte1 = ""
                archivo.write(f'\tif rule == {k!r}:\n')
                indice = v.index(":")
                parte1 = v[:indice+1]
                parte2 = v[indice+1:]

                # Separar segunda parte del codigo 
                inicio = parte2.index(':')
                sub2 = parte2[inicio+1:]
                sub21 = parte2[:inicio+1]            
                i = sub2.index(' ')
                sub2_s = sub2[i+1:]
                sub2_r = sub2[:i+1]
                ultima_letra_mayuscula = None

                for letra in reversed(sub21):
                    if letra.isupper():
                        ultima_letra_mayuscula = letra
                        break

                fin = sub21.index(ultima_letra_mayuscula)
                sub2_1 = sub21[:fin+1]
                sub2_2 = sub21[fin+1:]
                sub2_1s = sub2_1[i+1:]
                sub2_1r = sub2_1[:i+1]

                # Manejo de la primera parte del codigo 
                if '=' in parte1:
                    inicio = parte1.index('=')+2
                    fin= parte1.index(':')
                    subcadena2 = parte1[inicio:fin]
                    
                    if subcadena2.isdigit():
                        archivo.write(f'\t\t{parte1} {sub2_1r} {sub2_1s!r}\n')
                    else:
                        
                        inicio = parte1.index('=')
                        subcadena3 = parte1[:inicio]
                        new_parte1 += f'{subcadena3}= {subcadena2!r}:'
                        archivo.write(f'\t\t{new_parte1} {sub2_1r} {sub2_1s!r}\n')
                        
                archivo.write(f'\t\t{sub2_2} {sub2_r} {sub2_s!r}\n')
                
            else:
                i = v.index(' ')
                subcadena = v[i+1:]
                subcadena1 = v[:i+1]
                archivo.write(f'\tif rule == {k!r}: {subcadena1}{subcadena!r}\n')
        archivo.write(f"\tif rule == 'error': return 'ERROR LEXICO'")

def generate_expresion(prod1):
    temp ={}

    string = ''
    data_in =''
    dentro_corchetes = False

    #Ciclo para cambiar los valores que tambien se encuentran como llaves 
    for key, value in prod1.items():
        # Reemplazar la key en el valor con su correspondiente valor
        for k in reversed(list(prod1.keys())):
            v = prod1[k]
            value = value.replace(k, v)

        updated_proddictionary[key] = value

    #cambio usando corchetes 
    for k,v in updated_proddictionary.items():
        for j in v:
            if j == '[':
                dentro_corchetes = True
                data_in += j
            elif j == ']':
                data_in += j
                dentro_corchetes = False
            elif j == '"' and dentro_corchetes is True:
                pass
            elif j == '+'and dentro_corchetes is True:
                data_in += '&'
                string += f'|"&"'
            elif j == '*'and dentro_corchetes is True:
                data_in += '^'   
            elif dentro_corchetes:
                string += f'|"{j}"'
                data_in += j

    string = string[1:]
    if string:
        string = f'({string})?'

    exp = ''
    key=''
    for k,v in updated_proddictionary.items():
        for j in v:
            if '[' in v and ']' in v :
                if j == '[':
                    dentro_corchetes = True
                    exp += string
                elif j == ']':
                    dentro_corchetes = False
                    pass
                elif dentro_corchetes:
                    pass
                else:
                    exp += j
                key = k
        # print(key)
        # print(exp)
    updated_proddictionary[key]=exp
                

    #Generar expresion fianl 
    expresion_key = ''
    expresion_final =''
    
    for key in updated_proddictionary.keys():
        if key in dic_rules.keys():
            value = updated_proddictionary[key]
            temp[key]=value
            value += '#'
            get_changed_values[key]=value

    for k,v in get_changed_values.items(): 
        new_expresion[k]=v

    for k,v in dic_rules.items(): 
        if not k.isalpha(): 
            new_expresion[k]= f'"{k}"#'

    for k,v in new_expresion.items():
        expresion_key += f'|{k}'
        expresion_final += f'|{v}'

    #print(expresion_final)
    #print(updated_proddictionary)
    #print(get_changed_values,'hh')
    #print(dic_rules)
    #print(dic_prod)
 

    expresion_key = expresion_key[1:]
    expresion_final = expresion_final[1:]
   
    # print("\033[1m Expresion Resumida \033[0m")
    # print('-> ', expresion_key,'\n')
    
    # print("\033[1m Expresion Extendida \033[0m")
    # print('-> ', expresion_final,'\n')

    return expresion_final

def mainYalex(doc):
    contenido =openFile(doc) 
    prod , rule  = handle_data(contenido) 
    prod1 = add_or(prod)
    maked_expresion = generate_expresion(prod1)
    generate_scanner(rule)

    return maked_expresion
