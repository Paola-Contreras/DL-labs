'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

import traceback


doc = 'ArchivosYALex/slr-4.yal'
def openFile (doc):
    with open(doc, 'r') as archivo:
        print("-> Reading file......")
        content = archivo.read() 
        print(f"-> File read '\033[1m {doc} \033[0m'\n")
        #print(content)
    return content


'''
Esta función es utilizada para corroborar que la exprsión ingresada no cuente con errores
ya sea con balanceo de parentesis o con elementos los cuales no son aceptados
'''
def validate (expresion):
    # BALANCEO DE PARENTESIS
    # Contador de parantesis 
    count = 0
    val = 0 
    #Ciclo que recorre la expresion 
    for i in expresion:
        #Condicional que verifica la cantidad de parentesis
        if i == '(':
            count +=1
        else:
            val +=1
        if i == ')':
            count +=1
    # Si el modulo de count no es  1 se muestra un error 
    if count % 2 == 1 or val ==0:
        raise ValueError('Tu expresión no se encuentra bien escrita, revisa parentesis')

    # VALIDACION DE EXPRESIONES
    # Lista de los caracteres y operadores que se aceptan en la expresion  
    caracteres = 'abcdefghijklmnñopqrstuvwxyz0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZε#E-'
    operadores = '*|+().?'
    # Ciclo for recorrer cada caracter de la expresion
    for caracter in expresion:
        # Condicional que verifica si un caracter se encuentra dentro de los caracteres permitidos, de lo contrario muestra un error
        if caracter not in caracteres and caracter not in operadores:
            raise ValueError('Tu expresión no se encuentra bien escrita, caracteres invalidos')

    # VALIDACIÓN DE OPERADORES
    # Ciclo utilizado para brindarle un valor numerico a cada elemento de la cadena y realizado con el fin de corroborar la cadena
    # i = numero brindado a cada elemento de la cadena, char = elemento de la cadena 
    for i, char in enumerate(expresion):
        # Condicional que en base a un operador verifica que este cuente con todos los caracteres permitdos para validar la cadena de lo contrario retorna un error 
        if char == '.':
            if ((i < len(expresion) - 1 and expresion[i+1] in '.|*+') or (i > 0 and expresion[i-1] == '.|') or (i == 0 or i == len(expresion)-1)):
                raise ValueError ('El operador cuenta con un elemento invalido antes o despues del operador .')
        elif char == '|':
            if ((i < len(expresion) - 1 and expresion[i+1] in '.|*+') or (i > 0 and expresion[i-1] == '.|') or (i == 0 or i == len(expresion)-1)):
                raise ValueError ('El operador cuenta con un elemento invalido antes o despues del operador |')
        elif char == '(':
            if (i < len(expresion) - 1 and expresion[i+1] == '.|*+') or (i > 0 and expresion[i-1] == '.|'):
                raise ValueError ('El operador cuenta con un elemento invalido antes o despues del parentesis de apertura')
        elif char == ')':
            if (i < len(expresion) - 1 and expresion[i+1] == '.|') or (i > 0 and expresion[i-1] == '('):
                raise ValueError ('El operador puede que cuente con un elemento invalido antes o despues del parentesis de cierre o no cuente con ninguno')
        elif char == '+':
            if ((i < len(expresion) - 1 and expresion[i+1] in '+|*') or (i > 0 and expresion[i-1] == '.|*(ε')):
                raise ValueError ('El operador cuenta con un elemento invalido antes o despues del operador +')
    
    if (expresion.startswith('+')) or (expresion.startswith('*')):
        raise ValueError('La cadena no puede comenzar con cerraduras kleen')
        
    return 0


def count(contenido,char,char2):
    num = 0
    num = contenido.count(char) + contenido.count(char2)
    return num 

def validate_doc(contenido):
    parentesis = count(contenido,'(',')')
    asterisco = count(contenido,'*','*')
    coment = count(contenido,'(*','*)')
    llaves = count(contenido,'{','}')
    brackets = count(contenido,'[',']')
    comillas = count(contenido,"'","'")

    if parentesis % 2 == 1:
        line = traceback.extract_stack()[-1][1]
        message = f'Hace falta un patentesis de apertura o cierre, error ocurrio en la linea {line}'
        raise ValueError(message)
    
    elif coment %2 ==1:
        line = traceback.extract_stack()[-1][1]
        message = f'Hace falta un *, error ocurrio en la linea {line}'
        raise ValueError(message)
    
    elif asterisco == 0:
        line = traceback.extract_stack()[-1][1]
        message = f'Hace falta un parentesis en un comentario, error ocurrio en la linea {line}'
        raise ValueError(message)
    
    elif parentesis == 0:
        line = traceback.extract_stack()[-1][1]
        message = f'Hace falta un asterisco en un comentario, error ocurrio en la linea {line}'
        raise ValueError(message)

    elif llaves %2 ==1:
        line = traceback.extract_stack()[-1][1]
        message = f'Error de llaves de apertura o cierre, error ocurrio en la linea {line}'
        raise ValueError(message)
    
    elif brackets %2 ==1:
        line = traceback.extract_stack()[-1][1]
        message = f'Error de brackets de apertura o cierre, error ocurrio en la linea {line}'
        raise ValueError(message)
    
    elif comillas %2 ==1:
        line = traceback.extract_stack()[-1][1]
        message = f'Error de comillas de apertura o cierre, error ocurrio en la linea {line}'
        raise ValueError(message)
    
    return 0
