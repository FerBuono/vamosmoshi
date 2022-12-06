#!/usr/bin/python3
import sys
from funciones_auxiliares import ver_sedes
from funciones_vamosmoshi import ir, itinerario, viaje, reducir_caminos

def main():

    archivo_sedes = sys.argv[1]
    sedes, grafo_sedes = ver_sedes(archivo_sedes)

    for entrada in sys.stdin:
        entrada = entrada.split(", ")
        entrada = [entrada[0].split()[0]] + [' '.join(entrada[0].split()[1:])] + entrada[1:]
        if entrada[0] == "ir":
            camino, tiempo = ir(entrada, grafo_sedes, sedes)
            if camino == None:
                print("No se encontro recorrido", file=sys.stdout)
                continue
            print(" -> ".join(camino), file=sys.stdout)
            print("Tiempo total:", tiempo, file=sys.stdout)

        elif entrada[0] == "itinerario":
            camino = itinerario(entrada, grafo_sedes)
            if camino == None:
                print("No se encontro recorrido", file=sys.stdout)
                continue
            print(" -> ".join(camino), file=sys.stdout)
            
        elif entrada[0] == "viaje":
            camino, tiempo = viaje(entrada, grafo_sedes, sedes)
            if camino == None:
                print("No se encontro recorrido", file=sys.stdout)
                continue
            print(" -> ".join(camino), file=sys.stdout)
            print("Tiempo total:", tiempo, file=sys.stdout)

        elif entrada[0] == "reducir_caminos":
            peso = reducir_caminos(entrada, grafo_sedes, sedes)
            print("Peso total:", peso, file=sys.stdout)

        elif entrada[0] == "salir":
            break

        else:
            print("Entrada erronea", file=sys.stdout)


main()