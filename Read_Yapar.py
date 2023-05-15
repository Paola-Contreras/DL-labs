'''
Universidad del Valle de Guatemala
Diseño de lenguajes de programación 
Gabriela Poala Contreras Guerra
'''

from LabC import Yalex as y
token_dic = {}
dic_productions ={}

def openFile (doc):
    with open(doc, 'r') as archivo:
        print("-> Reading file......")
        content = archivo.read() 
        print(f"-> File read '\033[1m {doc} \033[0m'\n")
    return content

def Convert_dic_productions(prod):
    for i, val in enumerate(prod):
        if i % 2 == 0:
            key = val
        
        else:
            value = val.strip(";")
            dic_productions[key] = value

    return dic_productions

def Convert_dic_token(tokens,doc):
    y.mainYalex(doc)
    #print(y.dic_rules)

    upper_tokens = []

    for token in tokens:
        word =''
        for char in token:
            if char.isupper():
                word += char
            elif word and not char.isupper():
                upper_tokens.append(word)
                word = ''  
        if word:            
            upper_tokens.append(word)
    #print(upper_tokens)
   
    for key, value in y.dic_rules.items():
        for token in upper_tokens:
            if token in value:
                token_dic[value.split()[1]] = key

    for element in upper_tokens:
        if element == 'IGNORE':
            index = upper_tokens.index('IGNORE')
            siguiente = upper_tokens[index+1]
            token_dic[element] = siguiente

    return token_dic

def handleData(contenido,yalex):
    string = ''
    temp =''
    content =[]
    tokens =[]
    prod = []
    is_coment = False
    is_production = False 
    
    for i in range(len(contenido)):
        data = contenido[i]
        if not is_coment:
            if data == "/" and contenido[i+1] == "*":
                is_coment = True
                #print('in')

            elif data != "\n":
                if data == ':':
                    is_production = True
                    
                elif data == ';':
                    is_production = False
                    string = temp
                    temp =''
                
                if is_production is True:
                    if data == ':':
                        continue 
                    else:
                        temp += data
                else:
                    if data == ';':
                        continue 
                    string += data
                
            
            elif string:
                content.append(string.strip())
                string = ""

        elif data == "/" and contenido[i-1] == "*":
            #print('out')
            is_coment = False
    #print(content)
    for val in content:
        #print(val)
        if "%token" in val:
            tokens.append(val)
        elif 'IGNORE' in val:
            tokens.append(val)
        else:
            prod.append(val)
    #print(prod,'\n',tokens)
    Convert_dic_productions(prod)
    Convert_dic_token(tokens,yalex)

    return token_dic, dic_productions

def main_read_yapar():
    doc = 'ArchivosYALex/slr-4.yal'
    docs = openFile("ArchivosYapar/slr-4.yalp")
    t,p = handleData(docs,doc)
    return t,p 

main_read_yapar()
