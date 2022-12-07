from grafo import Grafo
from funciones_grafos import dijkstra_minimos, bfs, orden_topologico, ciclo_euleriano, arbol_tendido_minimo_prim
from funciones_auxiliares import escribir_kml, escribir_pj

def ir(entrada, grafo, sedes):
    origen = entrada[1]
    destino = entrada[2]
    if not grafo.pertenece(origen) or not grafo.pertenece(destino):
        return None, None
    archivo_kml = entrada[3].strip()
    dic_padres, dic_distancias = dijkstra_minimos(grafo, origen, destino)
    if dic_distancias[destino] == float("inf"):
        return None, None
    camino = [destino]
    while destino != origen:
        camino.insert(0, dic_padres[destino])
        destino = dic_padres[destino]
    escribir_kml(grafo, camino, sedes, archivo=archivo_kml)
    return camino, dic_distancias[entrada[2].strip()]

def itinerario(entrada, grafo):
    grafo_orden = Grafo(True, [])
    with open(entrada[1], "r") as archivo:
        for linea in archivo:
            linea = linea.rstrip("\n").split(",")
            grafo_orden.agregar_vertice(linea[0])
            _, dic_orden = bfs(grafo, linea[0])
            if linea[1] not in dic_orden:
                return None
            grafo_orden.agregar_vertice(linea[1])
            grafo_orden.agregar_arista(linea[0], linea[1])
    for v in grafo:
        if not grafo_orden.pertenece(v):
            grafo_orden.agregar_vertice(v)
    camino = orden_topologico(grafo_orden)
    return camino

def viaje(entrada, grafo, sedes):
    origen = entrada[1]
    if not grafo.pertenece(origen):
        return None, None
    ciclo, tiempo_total = ciclo_euleriano(grafo, origen)
    if ciclo == None:
        return None, None
    aristas = 0
    for _ in range(len(ciclo) - 1):
        aristas += 1
    if aristas != grafo.cantidad_de_aristas():
        return None, None
    archivo_kml = entrada[2].strip()
    escribir_kml(grafo, ciclo, sedes, archivo=archivo_kml)
    return ciclo, tiempo_total

def reducir_caminos(entrada, grafo, sedes):
    archivo = entrada[1].strip()
    arbol, peso = arbol_tendido_minimo_prim(grafo)
    escribir_pj(arbol, sedes, archivo)
    return peso