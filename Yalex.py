'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

doc = 'ArchivosYALex/slr-4.yal'
value = []
dic_prod = {}
dic_rules = {}

def openFile (doc):
    with open(doc, 'r') as archivo:
        print("-> Reading file......")
        content = archivo.read() 
        print(f"-> File read '\033[1m' {doc} '\033[0m'\n")
        #print(content)
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
            change = ''
            if ' ' in string1: 
                for letter in string1:
                    if letter == ' ':
                        change += 'ε'
                    else:
                        change += letter
                string1 = change
            dic_prod[key] = string1
    
    return dic_prod

def convert_rules_to_dic(rules):
    for el in rules:
        key = ""
        vall = ""
        string2 = ""
        for char in el:
            if char != " " and char != "|"and char != "{" and char != "}" and char != "'":
                string2+= char
                if string2 == "ruletokens=":
                    string2 = ""
            if char == "{":
                key = string2
                string2 = ""
            if char == "}":
                vall = string2
                output =""

                #Ciclo para ponerle espacios entre return y resto
                for letter in vall:
                    output += letter
                    if output == "return":
                        output += " "

                vall = output
                string2 = ""
        
        if string2:
            # Agrega al diccionario los valores que no tienen return en el archivo y les asigna el return de su llave
            dic_rules[string2] = f"return {string2}"
        else:
            if key !="" and vall !="":
                dic_rules[key] = vall

    return dic_rules

def handle_data(contenido):
    prod = []
    rules = []
    string = ""
    is_a_comment = False
    # Este se encarga de por cada dato del archivo almacenarlo en una lista omitiendo los comentarios
    for i in range(len(contenido)):
        data = contenido[i]
        if not is_a_comment:
            if data == "(" and contenido[i+1] == "*":
                is_a_comment = True
            elif data != "\n":
                string += data
            elif string:
                value.append(string)
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
        
    return dic_prod, dic_rules

def add_or (prod):
    expresion = ''
    caracteres = ''

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
                    dic_prod[k] = f'({exp2})'

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
                dic_prod[k] = f'({exp2})'
        else:
            pass
    return dic_prod

def generate_expresion(prod1):

    updated_proddictionary = {}
    get_changed_values = {}

    #Ciclo para cambiar los valores que tambien se encuentran como llaves 
    for key, value in prod1.items():
        # Reemplazar la key en el valor con su correspondiente valor
        for k in reversed(list(prod1.keys())):
            v = prod1[k]
            value = value.replace(k, v)

        updated_proddictionary[key] = value

    #Ciclo para ver que valores han cambiado en el diccionario actualizado vs el diccionario original
    for key in prod1.keys():
        if key in updated_proddictionary.keys():
            if prod1[key] != updated_proddictionary[key]:
                get_changed_values[key] = (updated_proddictionary[key])

    #Generar expresion fianl 
    expresion_key = ''
    expresion_final =''
    for k,v in get_changed_values.items():
        expresion_key += f'|{k}'
        expresion_final += f'|{v}'

    expresion_key = expresion_key[1:]
    expresion_final = expresion_final[1:]


    print(expresion_key,'\n')
    print(expresion_final)

    return expresion_key , expresion_final


contenido =openFile(doc) 
prod , rule = handle_data(contenido) 
prod1 = add_or(prod)
expresion = generate_expresion(prod1)