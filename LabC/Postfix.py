'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

'''
Esta funcion es utilizada para convertir una expresion regular infix en una expresion de tipo 
posfix, es importante destacar que para esta se utilizo el algoritmo de Shunting Yard
'''
def convert_postfix(expresion):
    dentro_de_comillas = False
    es_un_slash =  False
    expresion3 = ''
    # Diccionario con los operadores a utilizar y su precedencia 
    operadores_orden ={'*':2,'+':2,'?':2,'·':1,'|':0}
    
    # Listas que se utilizan para recrear un stack de operadores y al mismo tiempo la cadena postfix 
    stack_operadores = []
    postfix =[]

    # Ciclo para recorrer cada elemento de la cadena ingresada 
    for i in expresion:
        # Condicional que se encarga del manejo de los parentesis dentro del stack de operadores  
        if i == '(' and dentro_de_comillas == False:
            stack_operadores.append(i) 
        elif i == ')' and dentro_de_comillas == False:
            # Ciclo que se recorre hasta encontrar un parentesis cerrado y al mismo tiempo recorre la cadena de izquierda a derecha
            while stack_operadores[-1] != '(':
                # Se añade al la lista de postfix cada elemento que se encuentre de por medio de los parentesis
                postfix.append(stack_operadores.pop())
            # Se eliminan del stak el parentesis de apertura 
            stack_operadores.pop()

        # Condicional que evalua cada caracter y corrobora si estos se encuentran dentro de los operadores validos
        elif i in operadores_orden:
            # Ciclo que se encarga de validad la importancia de cada signo y evalua si este es de mayor o mismo valor  y verifica si esta no es es un parentesis 
            # de apertura para poder sacarlo del stack de operadores para añanadirlo al stack de postfix. Cabe resaltar que el recorrido es de izquierda a derecha
            while (stack_operadores and stack_operadores[-1] != '(' and operadores_orden[i] <= operadores_orden[stack_operadores[-1]]):
                postfix.append(stack_operadores.pop())
            # Se añade al stack el operador luego de verificar su valor, precedencia, dentro de la expresion 
            stack_operadores.append(i)
        
        # Parte de la condicion que aprendea el valor de i si este no es un operador 
        else:
            if i =='"' and not dentro_de_comillas:
                dentro_de_comillas = True
            elif i == '"' and dentro_de_comillas:
                dentro_de_comillas = False
                postfix.append(expresion3)
                expresion3 = ''
            elif dentro_de_comillas:
                expresion3 += i
            elif dentro_de_comillas == True:
                pass
            elif i == '\\' and not es_un_slash:
                es_un_slash = True
                expresion3 += i
            elif es_un_slash:
                expresion3 += i
                postfix.append(expresion3)
                expresion3 = ''
                es_un_slash = False
            else:
                postfix.append(i)

    # Ciclo que apendea los valores restantes del stack de operadores a postfix siempre y cuando este no sea null 
    while stack_operadores:
        postfix.append(stack_operadores.pop())

    return postfix

'''
Esta funcion es utilizada para agregar la concatenacion en los espacios correspondientes para tener esta con todos
los operadores necesarios para seguidamente poder convertirlo a posfix
'''

def fix_expression(expresion):
    dentro_de_comillas = False
    #Coloca un . sobre cada caracter de la cadena 
    expresion = "·".join(expresion)
    #Variable que sera utilizada para almacenar la nueva expresion 
    expresion2 =''
    expresion3 =''

    #Ciclo que enumera cada caracter de la expresion original 
    for i, char in enumerate(expresion):
        if char == '"' and not dentro_de_comillas:
            dentro_de_comillas = True
            expresion3 += char
        #Condicional para detectar el final de una cadena entre comillas
        elif char == '"' and dentro_de_comillas:
            expresion3 += char
            dentro_de_comillas = False
            expresion2 += expresion3
            expresion3 = ''
        #Condicional para omitir el punto dentro de una cadena entre comillas
        elif dentro_de_comillas and char != '·':
            expresion3 += char

        elif dentro_de_comillas == True:
            pass
        #Condicional que agrega a la expresion 2 los operadores
        elif char in '*|+()?':
            expresion2 += char
        # Condicional que si el . esta despues de uno de los caracteres 
        # espesifico omite el punto en la nueva expresion 
        elif char == '·' and expresion[i+1] in '*+|?)':
            continue
        # Condicional que si el . esta antes de uno de los caracteres 
        # espesifico omite el punto en la nueva expresion 
        elif char == '·' and expresion[i-1] in '(|\\':
            continue
        # Si el caracter no es un . despues o antes de un operador se añade a la nueva expresion 
        else:
            expresion2 += char

    
    return expresion2
