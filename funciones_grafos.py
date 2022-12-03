from grafo import Grafo
import heapq
from collections import deque

def dijkstraMinimos(grafo: Grafo, origen, destino):
    dist = {}
    padre = {}
    for v in grafo.obtener_vertices():
        dist[v]= float("inf")
    dist[origen] = 0
    padre[origen]= None
    q = []
    heapq.heappush(q,(0,origen))
    while not len(q) == 0:
        _,v = heapq.heappop(q)
        if v == destino:
            return padre , dist
        for w in grafo.adyacentes(v):
            nueva_dist = dist[v] + grafo.peso(v,w)
            if nueva_dist < dist[w]:
                dist[w] = nueva_dist
                padre[w] = v
                q.heappush((dist[w], w))
    return padre, dist

def ArbolMinimo_Prim(grafo: Grafo):
    visitados = set()
    q = heapq
    v = grafo.vertice_aleatorio()
    visitados.add(v)
    for w in grafo.adyacentes(v):
        q.heappush((v,w), grafo.peso(v,w))
    arbol = Grafo(False, grafo.obtener_vertices())
    while not len(q) == 0:
        (v,w), peso = q.heappop()
        if w not in visitados:
            arbol.agregar_arista(v,w,peso)
            visitados.add(w)
            for x in grafo.adyacentes(w):
                if x not in visitados:
                    q.heappush((w,x), grafo.peso(w,x))
    return arbol

def obtener_grados(grafo: Grafo):
    grados = {}
    for v in grafo.obtener_vertices():
        grados[v] = 0
        for w in grafo.adyacentes(v):
            grados[v] += 1
    return grados

#       Recorridos        #

def bfs(grafo: Grafo, origen):
    visitados = set()
    padre = {}
    orden = {}
    cola = deque
    cola.append(origen)
    visitados.add(origen)
    padre[origen] = None
    orden[origen] = 0
    while not len(cola) == 0:
        v = cola.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                padre[w]= v
                orden[w] = orden[v]+1
                cola.append(w)
    return padre, orden

def _dfs(grafo: Grafo,v,visitados: set,padre, orden: dict):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            padre[w] = v
            orden[w] = orden.setdefault(v, 0)+1
            visitados.add(w)
            _dfs(grafo,w,visitados,padre,orden)
    

def dfs(grafo: Grafo, origen):
    padre = {}
    visitados = set()
    orden = {}
    padre[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    _dfs(grafo,origen,visitados,padre,orden)
    return padre , orden

def dfs_completo(grafo: Grafo):
    visitados = set()
    padre = {}
    orden = {}
    for v in grafo.obtener_vertices():
        if v not in visitados:
            visitados.add(v)
            padre[v]= None
            orden[v] = 0
            _dfs(grafo, v,visitados,padre, orden)
    return padre, orden

# Verificaciones #

def es_conexo(grafo: Grafo):
    visitados = set()
    v = grafo.vertice_aleatorio()
    visitados.add(v)
    _dfs(grafo, v, visitados, {}, {})
    return len(visitados) == grafo.cant

def vertices_grado_impar(grafo: Grafo):
    grados = obtener_grados(grafo)
    impares = 0
    for v in grafo.obtener_vertices():
        if not (grados[v] % 2) == 0:
            impares += 1
    return impares

#   Ciclo   #

def ciclo_euleriano(grafo):
    ciclo = [] #Capaz hay q cambiar esto
    if es_conexo(grafo) and vertices_grado_impar(grafo) == 0:
        ciclo = hierholzer(grafo)
    elif es_conexo and vertices_grado_impar == 2:
        #ciclo = fleury(grafo)
        return ciclo
    else:
        print("No presenta ciclo Euleriano")
    return ciclo

#            HIERHOLZER            #

def hierholzer(grafo: Grafo):
    camino = []
    aristas_visit = {}
    v = grafo.vertice_aleatorio()
    camino.append(v)
    dfs_hierholzer(grafo, v, aristas_visit, camino)
    i = 0
    while i < len(camino):
        nuevo_camino = [camino[i]]
        if not dfs_hierholzer(grafo, camino[i], aristas_visit, nuevo_camino):
            i += 1
            continue
        
        # ej: i = 2              |
        # camino:       [v1, v2, v3, v4, v5, v6]
        # nuevo_camino:           \ [v3, v8, v9, v3]
        camino = camino[:i] + nuevo_camino + camino[i+1:]
    
def _dfs_hierholzer(grafo: Grafo, v, aristas_visit: dict, camino: list, origen):
    adyacentes_v: set = aristas_visit.setdefault(v, set())
    aristas_adyacentes_sin_visitar = set(grafo.adyacentes(v)).difference(adyacentes_v)
    for w in aristas_adyacentes_sin_visitar:
        adyacentes_w: set = aristas_visit.setdefault(w, set())
        adyacentes_v.add(w)
        adyacentes_w.add(v)

        camino.append(w)
        if w == origen or _dfs_hierholzer(grafo, w, aristas_visit, camino, origen):
            return True
        
        adyacentes_v.remove(w)
        adyacentes_w.remove(v)
        camino.pop()

    return False

def dfs_hierholzer(grafo: Grafo, v, aristas_visit: dict, camino: list):
    """
    Encuentra un ciclo que comienza en v y termina en v sin utilizar las aristas
    visitadas. Devuelve True si se encontró o False si no
    """ 
    return _dfs_hierholzer(grafo, v, aristas_visit, camino, v)

#                   FLEURY                #

def fleury(grafo: Grafo):
    v = vertice_grado_impar(grafo)
    aristas = obtener_aristas(grafo)
    grafo_aux = grafo
    aristas_visit = set()
    camino = []
    camino.append(v)
    dfs_fleury(grafo_aux, v, aristas_visit, camino)
    return camino
    
def dfs_fleury(grafo: Grafo, v, aristas_visit: set, camino: list):
    for w in grafo.adyacentes(v):
        if (v,w) not in aristas_visit:
            grafo.eliminar_arista(v,w)
            if not es_conexo(grafo):
                dfs_fleury(grafo,v,aristas_visit,camino)
            grafo.agregar_arista(v,w)
            camino.append(w)
            aristas_visit.add((w,v))
            aristas_visit.add((v,w))
            dfs_fleury(grafo,w,aristas_visit,camino)


# Auxiliares #

def vertice_grado_impar(grafo: Grafo):
    grados = obtener_grados(grafo)
    for v in grafo.obtener_vertices():
        if not grados[v]%2 == 0:
            return v
    return None
        
    

def obtener_aristas(grafo: Grafo):
    aristas = []
    visitados = set()
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            if w not in visitados:
                aristas.append((v,w))
            visitados.add(v)
    return aristas

