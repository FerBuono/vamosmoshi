#!/usr/bin/python3
import sys
from grafo import Grafo
from funciones_grafos import dijkstra_minimos, orden_topologico, bfs, ciclo_euleriano, arbol_tendido_minimo_prim
from funciones_auxiliares import ver_sedes, escribir_kml
from funciones_vamosmoshi import ir, itinerario, viaje, reducir_caminos

def main():
    seguir = True
    archivo_sedes = sys.argv[1]
    sedes, grafo_sedes = ver_sedes(archivo_sedes)
    while seguir:
        entrada = input().split(", ")
        entrada = entrada[0].split() + entrada[1:]

        if entrada[0] == "ir":
            camino, tiempo = ir(entrada, grafo_sedes, sedes)
            if camino == None:
                print("No se encontro recorrido")
                continue
            print(" -> ".join(camino))
            print("Tiempo total:", tiempo)

        elif entrada[0] == "itinerario":
            camino = itinerario(entrada, grafo_sedes)
            if camino == None:
                print("No se encontro recorrido")
                continue
            print(" -> ".join(camino))
            
        elif entrada[0] == "viaje":
            camino, tiempo = viaje(entrada, grafo_sedes, sedes)
            if camino == None:
                print("No se encontro recorrido")
                continue
            print(" -> ".join(camino))
            print("Tiempo total:", tiempo)

        elif entrada[0] == "reducir_caminos":
            peso = reducir_caminos(entrada, grafo_sedes)
            print("Peso total:", peso)

        else:
            print("Entrada incorrecta, pruebe nuevamente")

main()