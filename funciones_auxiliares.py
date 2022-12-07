from grafo import Grafo

def ver_sedes(archivo_sedes):
    sedes = {}
    grafo_sedes = Grafo(False, [])
    cant_ciudades = 0
    with open(archivo_sedes, "r") as archivo:
        for cont, linea in enumerate(archivo):
            linea = linea.rstrip("\n").split(",")
            if cont == 0:
                cant_ciudades += int(linea[0])
                continue
            if 0 < cont <= cant_ciudades:
                sedes[linea[0]] = (linea[1], linea[2])
                grafo_sedes.agregar_vertice(linea[0])
            elif cont > cant_ciudades + 1:
                grafo_sedes.agregar_arista(linea[0], linea[1], int(linea[2]))
    return sedes, grafo_sedes


def escribir_kml(grafo, camino, sedes, archivo):
    visitados = {}
    with open(archivo, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://earth.google.com/kml/2.1">\n')
        f.write('\t<Document>\n')
        f.write('\t\t<name>Prueba</name>\n')
        f.write('\n')
        for localidad in camino:
            if localidad not in visitados:
                f.write('\t\t<Placemark>\n')
                f.write(f'\t\t\t<name>{localidad}</name>\n')
                f.write('\t\t\t<Point>\n')
                f.write(f'\t\t\t\t<coordinates>{sedes[localidad][0]}, {sedes[localidad][1]}</coordinates>\n')
                f.write('\t\t\t</Point>\n')
                f.write('\t\t</Placemark>\n')
                f.write('\n')
                visitados[localidad] = True
        for i in range(len(camino)-1):
            f.write('\t\t<Placemark>\n')
            f.write('\t\t\t<LineString>\n')
            f.write(f'\t\t\t\t<coordinates>{sedes[camino[i]][0]}, {sedes[camino[i]][1]} {sedes[camino[i+1]][0]}, {sedes[camino[i+1]][1]}</coordinates>\n')
            f.write('\t\t\t</LineString>\n')
            f.write('\t\t</Placemark>\n')
            f.write('\n')
        f.write('\t</Document>\n')
        f.write('</kml>')

def escribir_pj(arbol, sedes, archivo):
    visitados = {}
    with open(archivo, "w") as f:
        f.write(f'{len(arbol)}\n')
        for v in arbol:
            f.write(f'{v},{sedes[v][0]},{sedes[v][1]}\n')
        f.write(f'{arbol.cantidad_de_aristas()}\n')
        for v in arbol:
            for w in arbol.adyacentes(v):
                f.write(f'{v},{w},{arbol.peso(v,w)}\n')
                arbol.eliminar_arista(v, w)