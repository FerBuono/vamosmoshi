import sys
from grafo import Grafo

CANT_SEDES = 10

def ver_sedes(archivo_sedes):
    sedes = {}
    grafo_sedes = Grafo(False, [])
    with open(archivo_sedes, "r") as archivo:
        for cont, linea in enumerate(archivo):
            linea = linea.rstrip("\n")
            linea = linea.split(",")
            if cont == 0 or cont == CANT_SEDES + 1:
                continue
            elif cont <= CANT_SEDES:
                sedes[linea[0]] = (linea[1], linea[2])
            else:
                grafo_sedes.agregar_vertice(linea[0])
                grafo_sedes.agregar_vertice(linea[1])
                grafo_sedes.agregar_arista(linea[0], linea[1], linea[2])
    return sedes, grafo_sedes

def main():
    seguir = True
    archivo_sedes = sys.argv[1]
    sedes, grafo_sedes = ver_sedes(archivo_sedes)
    print(sedes)
    while seguir:
        entrada = input()
        print(entrada)

main()