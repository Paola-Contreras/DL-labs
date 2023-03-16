import graphviz


def makeDic(transiciones):
    afd = {}
    for transicion in transiciones:
        inicio, fin, simbolo = transicion
        if inicio not in afd:
            afd[inicio] = {}
        if fin not in afd:
            afd[fin] ={}
        afd[inicio][simbolo] = fin
    return afd

def getdifferentiate(sate, state2, afd, end):
    if (sate in end and state2 not in end) or (state2 in end and sate not in end):
        return True
    
    for simbolo in afd[sate]:
            if simbolo not in afd[state2]:
                continue
            if afd[sate][simbolo] != afd[state2][simbolo]:
                return True
            
    return False

def makeSets(conjuntos, afd, estados_finales):
    new_sets = []
    for conjunto in conjuntos:
        if len(conjunto) == 1:
            new_sets.append(conjunto)
            continue
        particiones = []
        for estado in sorted(conjunto):
            particion = None
            for i, p in enumerate(particiones):
                if getdifferentiate(estado, p[0], afd, estados_finales):
                    continue
                particion = i
                break
            if particion is None:
                particiones.append([estado])
            else:
                particiones[particion].append(estado)
        new_sets.extend(particiones)
    return new_sets

def maketran(afd_min,end):
    tran =[]
    final_state = []
    for clave, valor in afd_min.items():
        if isinstance(valor, dict):
            for clave2, valor2 in valor.items():
                tran.append((clave, valor2,clave2))
        
        if clave in end:
            final_state.append(clave)

    print(tran)
    return tran, final_state

def graph_min(afd,end,start):
    graph = graphviz.Digraph('AFD Minimization', filename='Minimization', format= 'png')
    graph.attr(rankdir='LR')

    start_state = start
    print(start,'aa')
    end_state = end

    for inicio,fin,label in afd:
        if inicio == start_state:
            graph.node(str(start_state), style= 'filled', fillcolor = '#87CEEB', shape= 'circle', rank = 'same')
            
        for i in end_state:
            graph.node(str(i), shape= 'doublecircle', rank = 'same')
             
        graph.attr('node', shape='circle')
        graph.edge(str(inicio), str(fin), label= str(label))

    graph.view()

def minimizar_afd(afd, estados_finales):
    
    estados_no_finales = set(afd.keys()) - estados_finales
    conjuntos = [estados_finales, estados_no_finales]

    if len(estados_no_finales) == 0:
        start_state = next(iter(estados_finales))
    else:
        start_state = next(iter(estados_no_finales))

    while True:
        nuevos_conjuntos = makeSets(conjuntos, afd, estados_finales)
        if nuevos_conjuntos == conjuntos:
            break
        conjuntos = nuevos_conjuntos
    afd_min = {}
    for conjunto in conjuntos:
        estado = list(conjunto)[0]
        afd_min[estado] = {}
        for simbolo in afd[estado]:
            estado_destino = afd[estado][simbolo]
            for c in conjuntos:
                if estado_destino in c:
                    afd_min[estado][simbolo] = list(c)[0]
                    break

    tran_min, final_state= maketran(afd_min,estados_finales)
    
    graph_min(tran_min,final_state,start_state)
    return afd_min

def main_minimization(lista_transiciones,estados_finales):
    afd = makeDic(lista_transiciones)
    afd_min = minimizar_afd(afd, estados_finales)
    return(afd_min)

