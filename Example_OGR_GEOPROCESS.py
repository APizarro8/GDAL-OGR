# -*- coding: utf-8 -*-
#Ejercicio 2 parte I
#Propósito: Utilizar los módulos correspondientes para trabajar con shapefiles,
#Crear un rectángulo que delimite cada país del shapefile de origen paracrear un shapefile que contenga estos polígonos.
#Autor: Alicia Pizarro
#Fecha: 29/12/2017

import ogr
import os
import sys
import osr

#Establecer el espacio de trabajo
path = 'D:\\Practica4_py\\UNEP-EDE__forest_area__1445948601'
os.chdir(path)

#Obtener el driver para el shp
driver = ogr.GetDriverByName('ESRI Shapefile')
inshapeEntrada = 'UNEP-EDE__forest_area__1445948601.shp'
indataSource = driver.Open ('UNEP-EDE__forest_area__1445948601.shp' , 0)

if driver is None:
    print 'No se encuentra el driver elegido.'
else:
    print  'El driver es correcto.'

print "\n"
    
#Se obtiene la capa del shapefile:
layer = indataSource.GetLayer(0)

#Se establece el shape de destino, y se crea el driver de salida:
shapeSalida = 'rectangulo.shp'
outDriver = ogr.GetDriverByName("ESRI Shapefile")

#Se comprueba que existe el shapefile de destino, eliminarlo y si no existe que imprima por pantalla que no se puede crear.
if os.path.exists(shapeSalida):
    outDriver.DeleteDataSource(shapeSalida)
    
if shapeSalida is None:
    print 'No se puede crear el fichero ' + 'shapefileSalida.shp'
    sys.exit(1)
    
#Se crea la referencia espacial
spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')
print spatialReference

#Se crea el shape destino con la referencia espacial anteriormente definida, así como la geometría de polígono.
shapeOut= outDriver.CreateDataSource(shapeSalida)
finalLayer = shapeOut.CreateLayer('Layer', spatialReference,geom_type=ogr.wkbPolygon)

# Se crean los campos ID, COUNTRY Y CODE y se añaden al shapefile de salida.
fieldDef = ogr.FieldDefn('ID', ogr.OFTInteger)
fieldDef.SetWidth(3)
finalLayer.CreateField(fieldDef)
idField = 0
fieldDefn = ogr.FieldDefn('COUNTRY', ogr.OFTString)
fieldDefn.SetWidth(50)
finalLayer .CreateField(fieldDefn)
fieldDefn = ogr.FieldDefn('CODE', ogr.OFTString)
fieldDefn.SetWidth(3)
finalLayer .CreateField(fieldDefn)

#Se define una lista con los países y se obtiene el número de features.
paises = []
features = layer.GetFeatureCount()
print 'El número de registros es de:' ,features

print "\n"

#Se itera para adquirir los campos ISO_3_CODE y NAME del shapefile de origen y añadirlos a los campos del shapefile de
#destino con los campos anteriormente creados (COUNTRY y CODE). 
try:
    for h in range (layer.GetFeatureCount()):
        feature = layer.GetFeature(h)
        codigo_del_pais = feature.GetField('ISO_3_CODE')
        nombre_del_pais = feature.GetField ('NAME')
        geometry = feature.GetGeometryRef()
        minLongitude, maxLongitude, minLatitude, maxLatitude = geometry.GetEnvelope()
   
        #Se añade todo lo anterior a una lista.append
        paises.append((nombre_del_pais, codigo_del_pais, minLatitude, maxLatitude, minLongitude, maxLongitude))

        #Se crea un anillo para el posterior polígono.
        linearRing = ogr.Geometry(ogr.wkbLinearRing)

        linearRing.AddPoint(minLongitude, minLatitude)
        linearRing.AddPoint(maxLongitude, minLatitude)
        linearRing.AddPoint(maxLongitude, maxLatitude)
        linearRing.AddPoint(minLongitude, maxLatitude)
        linearRing.AddPoint(minLongitude, minLatitude)

    #Se crea el objeto polígono.
    poligono = ogr.Geometry(ogr.wkbPolygon)
    #Se añade al polígono el anillo creado.
    poligono.AddGeometry(linearRing)
    #Se define el objeto feature de destino 
    featureDefn = finalLayer.GetLayerDefn()
    finalfeature = ogr.Feature(featureDefn)
    #Se añade la geomatría y ls valores de los campos creados anteriormente.
    finalfeature.SetGeometry(poligono)
    idField = idField + 1
    finalfeature.SetField('ID', idField)
    finalfeature.SetField("COUNTRY",nombre_del_pais)
    finalfeature.SetField("CODE",codigo_del_pais)
    finalLayer.CreateFeature(finalfeature)

except (AttributeError):
    print"Hay errores" 

#Se destruye el objeto.    
finalfeature.Destroy()

#Se imprimen la información de los países y se imprime por pantalla.
for nombre_del_pais, codigo_del_pais, minLatitude, maxLatitude, minLongitude, maxLongitude in paises:
        print "{0} ({1} lat=(2:.4f)..{3:.4f}, long={4:.4f}..{5:.4f})".format(nombre_del_pais, 
            codigo_del_pais, minLatitude, maxLatitude, minLongitude, maxLongitude)


#Se destruye el shapefile de salida.
shapeOut.Destroy()
