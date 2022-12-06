from grafo import Grafo
from xml.etree.ElementTree import Element, SubElement, tostring
import simplekml

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


def escribir_kml(camino, sedes, archivo):
    kml = Element('kml', xmlns='http://www.opengis.net/kml/2.2')
    document = SubElement(kml, 'Document')
    for localidad in camino:
        placemark = SubElement(document, 'Placemark')
        name = SubElement(placemark, 'name')
        name.text = localidad
        point = SubElement(placemark, 'Point')
        coordinates = SubElement(point, 'coordinates')
        coordinates.text = f'{sedes[localidad][1]}, {sedes[localidad][0]}'
    for i in range(len(camino)-1):
        placemark = SubElement(document, 'Placemark')
        line = SubElement(placemark, 'LineString')
        coordinates = SubElement(line, 'coordinates')
        coordinates.text = f'{sedes[camino[i]][1]}, {sedes[camino[i]][0]} {sedes[camino[i+1]][1]}, {sedes[camino[i+1]][0]}'
    kml = tostring(kml, encoding='unicode')
    with open(archivo, "w") as f:
        f.write(kml)
    #kml = simplekml.Kml()
    #for localidad in camino:
    #    placemark = kml.newpoint(name=localidad, coords=[(sedes[localidad][1], sedes[localidad][0])])
    #for i in range(len(camino)-1):
    #    lin = kml.newlinestring(coords=[(sedes[camino[i]][1], sedes[camino[i]][0]), (sedes[camino[i+1]][1], sedes[camino[i+1]][0])])
    #kml.save(archivo)


def escribir_pj(arbol, sedes, archivo):
    visitados = {}
    with open(archivo, "w") as f:
        f.write(f'{len(arbol)}\n')
        for v in arbol:
            f.write(f'{v},{sedes[v][0]},{sedes[v][1]}\n')
        f.write(f'{arbol.cantidad_de_aristas()}\n')
        for v in arbol:
            for w in arbol.adyacentes(v):
                if w not in visitados:
                    f.write(f'{v},{w},{arbol.peso(v,w)}\n')