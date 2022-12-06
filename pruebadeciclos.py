from grafo import Grafo
import heapq
from collections import deque
from funciones_grafos import hierholzer
from funciones_grafos import fleury
from funciones_grafos import arbol_tendido_minimo_prim


##      PARA HIERHOLZER
def agregar_aristas(grafo: Grafo):
    grafo.agregar_arista("Arg", "Uru")
    grafo.agregar_arista("Arg", "Bra")
    grafo.agregar_arista("Arg", "Par")
    grafo.agregar_arista("Arg", "Chil")
    grafo.agregar_arista("Arg", "Peru")
    grafo.agregar_arista("Arg", "Ecua")
    grafo.agregar_arista("Uru", "Bra")
    grafo.agregar_arista("Uru", "Boliv")
    grafo.agregar_arista("Uru", "Par")
    grafo.agregar_arista("Bra", "Boliv")
    grafo.agregar_arista("Bra", "Chil")
    grafo.agregar_arista("Chil", "Peru")
    grafo.agregar_arista("Chil", "Ecua")
    grafo.agregar_arista("Par", "Peru")
    grafo.agregar_arista("Par", "Ecua")
    grafo.agregar_arista("Ecua", "Peru")

def agregar_vertices(grafo: Grafo):
    grafo.agregar_vertice("Arg")
    grafo.agregar_vertice("Uru")
    grafo.agregar_vertice("Bra")
    grafo.agregar_vertice("Par")
    grafo.agregar_vertice("Chil")
    grafo.agregar_vertice("Peru")
    grafo.agregar_vertice("Ecua")
    grafo.agregar_vertice("Boliv")
##   #   PARA FLEURY
#def agregar_vertices(grafo: Grafo):
#    grafo.agregar_vertice("Arg")
#    grafo.agregar_vertice("Uru")
#    grafo.agregar_vertice("Bra")
#    grafo.agregar_vertice("Par")
#    grafo.agregar_vertice("Chil")
#    grafo.agregar_vertice("Peru")
#    
#    
#def agregar_aristas(grafo: Grafo):
#    grafo.agregar_arista("Arg", "Uru")
#    grafo.agregar_arista("Arg", "Bra")
#    grafo.agregar_arista("Arg", "Par")
#    grafo.agregar_arista("Arg", "Chil")
#    grafo.agregar_arista("Uru", "Bra")
#    grafo.agregar_arista("Uru", "Par")
#    grafo.agregar_arista("Uru", "Peru")
#    grafo.agregar_arista("Bra", "Chil")
#    grafo.agregar_arista("Bra", "Peru")
#    grafo.agregar_arista("Chil", "Par")
#    
def crear_grafo():
    g = Grafo(False, [])
    agregar_vertices(g)
    agregar_aristas(g)
    return g
    
def main():
    g = crear_grafo()
    camino, peso = arbol_tendido_minimo_prim(g)
    #camino, peso = fleury(g)
    print(camino)
    print(peso)
    
main()