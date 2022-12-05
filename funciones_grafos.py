from grafo import Grafo
import heapq
from collections import deque

def dijkstra_minimos(grafo, origen, destino):
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
                heapq.heappush(q, (dist[w], w))
    return padre, dist

def arbol_tendido_minimo_prim(grafo):
    origen = grafo.vertice_aleatorio()
    arbol = Grafo(False, grafo.obtener_vertices())
    peso_total = 0
    visitados = set()
    visitados.add(origen)
    q = []
    for w in grafo.adyacentes(origen):
        heapq.heappush(q, (grafo.peso(origen, w), origen, w))
    while len(q) > 0:
        peso, origen, destino = heapq.heappop(q)
        if destino in visitados:
            continue
        visitados.add(destino)
        arbol.agregar_arista(origen, destino, peso)
        peso_total += peso
        for w in grafo.adyacentes(destino):
            if w not in visitados:
                heapq.heappush(q, (grafo.peso(destino, w), destino, w))
    return arbol, peso_total


def orden_topologico(grafo):
    gr_ent = {}
    resultado = []
    q = deque()
    for v in grafo:
        gr_ent[v] = 0
    for v in grafo:
        for w in grafo.adyacentes(v):
            gr_ent[w] += 1
    for v in grafo:
        if gr_ent[v] == 0:
            q.appendleft(v)
    while len(q) > 0:
        v = q.pop()
        resultado.append(v)
        for w in grafo.adyacentes(v):
            gr_ent[w] -= 1
            if gr_ent[w] == 0:
                q.appendleft(w)
    return resultado

def obtener_grados_salida(grafo):
    grados = {}
    for v in grafo.obtener_vertices():
        grados[v] = 0
        for w in grafo.adyacentes(v):
            grados[v] += 1
    return grados

#       Recorridos        #

def bfs(grafo, origen):
    visitados = set()
    padre = {}
    orden = {}
    cola = deque()
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

def _dfs(grafo, v, visitados, padre, orden):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            padre[w] = v
            orden[w] = orden.setdefault(v, 0)+1
            visitados.add(w)
            _dfs(grafo,w,visitados,padre,orden)
    

def dfs(grafo, origen):
    padre = {}
    visitados = set()
    orden = {}
    padre[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    _dfs(grafo,origen,visitados,padre,orden)
    return padre , orden

def dfs_completo(grafo):
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

def es_conexo(grafo):
    visitados = set()
    v = grafo.vertice_aleatorio()
    visitados.add(v)
    _dfs(grafo, v, visitados, {}, {})
    return len(visitados) == grafo.cant

def vertices_grado_impar(grafo):
    grados = obtener_grados_salida(grafo)
    impares = 0
    for v in grafo.obtener_vertices():
        if not (grados[v] % 2) == 0:
            impares += 1
    return impares

#   Ciclo   #

def ciclo_euleriano(grafo, origen):
    ciclo = [] 
    if es_conexo(grafo) and vertices_grado_impar(grafo) == 0:
        ciclo = hierholzer(grafo, origen)
    elif es_conexo and vertices_grado_impar(grafo) == 2:
        return ciclo
    else:
        return
    return ciclo

#            HIERHOLZER            #

def hierholzer(grafo, origen):
    camino = []
    aristas_visit = {}
    camino.append(origen)
    dfs_hierholzer(grafo, origen, aristas_visit, camino)
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
    return camino

def dfs_hierholzer(grafo, v, aristas_visit, camino):
    """
    Encuentra un ciclo que comienza en v y termina en v sin utilizar las aristas
    visitadas. Devuelve True si se encontró o False si no
    """ 
    return _dfs_hierholzer(grafo, v, aristas_visit, camino, v)
    
def _dfs_hierholzer(grafo, v, aristas_visit, camino, origen):
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

#                   FLEURY                #

def fleury(grafo):
    v = vertice_grado_impar(grafo)
    aristas = obtener_aristas(grafo)
    grafo_aux = grafo
    aristas_visit = set()
    camino = []
    camino.append(v)
    dfs_fleury(grafo_aux, v, aristas_visit, camino)
    return camino
    
def dfs_fleury(grafo, v, aristas_visit, camino):
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

def vertice_grado_impar(grafo):
    grados = obtener_grados_salida(grafo)
    for v in grafo.obtener_vertices():
        if not grados[v]%2 == 0:
            return v
    return None
        
    

def obtener_aristas(grafo):
    aristas = []
    visitados = set()
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            if w not in visitados:
                aristas.append((v,w))
            visitados.add(v)
    return aristas

