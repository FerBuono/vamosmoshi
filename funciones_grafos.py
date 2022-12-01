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
    return padre, dist #tambien se puede poner None , None en el caso de que no se encuentre el destino

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

def grados_grafo_no_dirigido(grafo: Grafo):
    grados = {}
    for v in grafo.obtener_vertices:
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

def _dfs(grafo: Grafo,v,visitados: set,padre,orden):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            padre[w] = v
            orden[w] = orden[v]+1
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
    return len(visitados) == grafo.cant()

def vertices_grado_impar(grafo: Grafo):
    grados = obtener_grados(grafo)
    impares = 0
    for v in grafo.obtener_vertices():
        if not (grados[v] % 2) == 0:
            impares += 1
    return impares