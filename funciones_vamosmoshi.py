from grafo import Grafo
from funciones_grafos import dijkstra_minimos, bfs, orden_topologico, ciclo_euleriano, arbol_tendido_minimo_prim
from funciones_auxiliares import escribir_kml

def ir(entrada, grafo, sedes):
    origen = entrada[1]
    destino = entrada[2]
    archivo_kml = entrada[3]
    dic_padres, dic_distancias = dijkstra_minimos(grafo, origen, destino)
    if dic_distancias[destino] == float("inf"):
        return None, None
    camino = [destino]
    while destino != origen:
        camino.insert(0, dic_padres[destino])
        destino = dic_padres[destino]
    escribir_kml(camino, sedes, archivo_kml, origen, destino)
    return camino, dic_distancias[entrada[2]]

def itinerario(entrada, grafo):
    grafo_orden = Grafo(True, [])
    with open(entrada[1]) as archivo:
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
    archivo_kml = entrada[2]
    ciclo, tiempo_total = ciclo_euleriano(grafo, origen)
    if ciclo == None:
        return None, None
    escribir_kml(ciclo, sedes, archivo_kml, origen, None)
    return ciclo, tiempo_total

def reducir_caminos(entrada, grafo):
    archivo = entrada[1]
    arbol, peso = arbol_tendido_minimo_prim(grafo)
    visitados = {}
    with open(archivo, "w") as f:
        for v in arbol:
            for w in arbol.adyacentes(v):
                if w not in visitados:
                    f.write(f'{v},{w},{arbol.peso(v,w)}\n')
    return peso