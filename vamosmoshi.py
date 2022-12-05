import sys
from grafo import Grafo
from funciones_grafos import dijkstra_minimos, orden_topologico, bfs, ciclo_euleriano, arbol_tendido_minimo_prim

CANT_SEDES = 10

def ver_sedes(archivo_sedes):
    sedes = {}
    grafo_sedes = Grafo(False, [])
    cant_ciudades = 0
    with open(archivo_sedes, "r") as archivo:
        for cont, linea in enumerate(archivo):
            linea = linea.rstrip("\n").split(",")
            if cont == 0:
                if cant_ciudades == 0:
                    cant_ciudades += int(linea[0])
                continue
            if 0 < cont <= cant_ciudades:
                sedes[linea[0]] = (linea[1], linea[2])
            elif cont > CANT_SEDES + 1:
                grafo_sedes.agregar_vertice(linea[0])
                grafo_sedes.agregar_vertice(linea[1])
                grafo_sedes.agregar_arista(linea[0], linea[1], int(linea[2]))
    return sedes, grafo_sedes

def escribir_kml(camino, archivo, origen, destino):
    with open(archivo, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
        f.write('\t<Document>\n')
        if destino:
            f.write(f'\t\t<name>Ruta desde {origen} a {destino}</name>\n')
        else:
            f.write(f'\t\t<name>Ruta desde {origen}</name>\n')
        for localidad in camino:
            f.write('\t\t<Placemark>\n')
            f.write(f'\t\t\t<name>{localidad[0]}</name>\n')
            f.write('\t\t\t<Point>\n')
            f.write(f'\t\t\t\t<coordinates>{localidad[1][0]}, {localidad[1][1]}</coordinates>\n')
            f.write('\t\t\t</Point>\n')
            f.write('\t\t</Placemark>\n')
            f.write('\n')
        for i in range(len(camino)-1):
            f.write('\t\t<Placemark>\n')
            f.write('\t\t\t<LineString>\n')
            f.write(f'\t\t\t\t<coordinates>{camino[i][1][0]}, {camino[i][1][1]} {camino[i+1][1][0]}, {camino[i+1][1][1]}</coordinates>\n')
            f.write('\t\t\t</LineString>\n')
            f.write('\t\t</Placemark>\n')
            f.write('\n')
        f.write('\t</Document>\n')
        f.write('</kml>')

def main():
    seguir = True
    archivo_sedes = sys.argv[1]
    sedes, grafo_sedes = ver_sedes(archivo_sedes)
    while seguir:
        entrada = input().split(", ")
        entrada = entrada[0].split() + entrada[1:]
        if entrada[0] == "ir":
            origen = entrada[1]
            destino = entrada[2]
            archivo_kml = entrada[3]
            dic_padres, dic_distancias = dijkstra_minimos(grafo_sedes, origen, destino)
            if dic_distancias[destino] == float("inf"):
                print("No se encontro recorrido")
                continue
            camino = [destino]
            while destino != origen:
                camino.insert(0, dic_padres[destino])
                destino = dic_padres[destino]
            print(" -> ".join(camino))
            print("Tiempo total:", dic_distancias[entrada[2]])
            camino_completo = []
            for localidad in camino:
                camino_completo.append([localidad, sedes[localidad]])
            escribir_kml(camino_completo, archivo_kml, origen, destino)
            
        elif entrada[0] == "itinerario":
            grafo_orden = Grafo(True, [])
            error = False
            with open(entrada[1]) as archivo:
                for linea in archivo:
                    linea = linea.rstrip("\n").split(",")
                    grafo_orden.agregar_vertice(linea[0])
                    dic_padres, dic_orden = bfs(grafo_sedes, linea[0])
                    if linea[1] not in dic_orden:
                        print("No se encontro recorrido")
                        error = True
                        break
                    grafo_orden.agregar_vertice(linea[1])
                    grafo_orden.agregar_arista(linea[0], linea[1])
            if error:
                continue
            for v in grafo_sedes:
                if not grafo_orden.pertenece(v):
                    grafo_orden.agregar_vertice(v)
            orden = orden_topologico(grafo_orden)
            print(" -> ".join(orden))
            
        elif entrada[0] == "viaje":
            origen = entrada[1]
            archivo_kml = entrada[2]
            ciclo = ciclo_euleriano(grafo_sedes, origen)
            if ciclo == None:
                print("No se encontro recorrido")
                continue   
            print(" -> ".join(ciclo))
            camino_completo = []
            for localidad in ciclo:
                camino_completo.append([localidad, sedes[localidad]])
            escribir_kml(camino_completo, archivo_kml, origen, None)

        elif entrada[0] == "reducir_caminos":
            archivo = entrada[1]
            arbol, peso = arbol_tendido_minimo_prim(grafo_sedes)
            print("Peso total:", peso)
            visitados = {}
            with open(archivo, "w") as f:
                for v in arbol:
                    for w in arbol.adyacentes(v):
                        if w not in visitados:
                            f.write(f'{v},{w},{arbol.peso(v,w)}\n')


main()