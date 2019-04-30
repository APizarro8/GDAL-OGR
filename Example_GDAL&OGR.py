# -*- coding: utf-8 -*- 
#Propósito:Manejar los métodos de GDAL para consultar información sobre el dataset vectorial.
#Mostar valores de los pixeles parar todas las bandas del arcivo .img para los puntos en el .shp
#Utilizar método de imagen completa
#Autor: Alicia Pizarro
#Fecha: 01/12/2017

## Importación de librerías 
import gdal 
import ogr
import os
import sys
from gdal import*

#Establecer el directorio de trabajo
path = 'xxDATAxx'
os.chdir(path)

# Driver para el formato .jpg
driver = gdal.GetDriverByName('HFA')
#Registrar todos los drivers
gdal.AllRegister()

#Abrir la imagen
Raster = ('xxxxx.img')
ds = gdal.Open(Raster, GA_ReadOnly)

if ds is None:
    print "No se puede abrir la imagen"
    sys.exit (1)
else:
    print "La imagen", Raster,"se ha podido abrir correctamente"

# Obtener algunas de las propiedades del raster (numero de filas y columnas) y las muestra en pantalla:
columnas = ds.RasterXSize
filas = ds.RasterYSize

# Obtiene los coeficientes de transformacion de una imagen (lista de informacion para georeferenciar una imagen).
geotransform = ds.GetGeoTransform()
orginX = geotransform[0]
orginY = geotransform[3]
pixelancho = geotransform[1]
pixelalto = geotransform[5]

print "Ancho del pixel: ", pixelancho, " y Alto de pixel: ", \
                                                   pixelalto

#Abrir el shapefile
driver = ogr.GetDriverByName('ESRI Shapefile')
shapefile = 'arctic_bsst200901.shp'
shp = driver.Open(shapefile)

if shapefile is None:
    print 'No se encuentra el shapefile.'
    sys.exit(1)
else:
    print "El archivo ", shapefile, "se ha podido abrir correctamente."
    
dataSource = driver.Open(shapefile, 0)
if dataSource is None:
    print 'No se puede abrir el shapefile ', shapefile
    sys.exit(1)
    
#Crear un objeto layer  y obtener el número de bandas   
layer = dataSource.GetLayer()
numLayers = dataSource.GetLayerCount()
feature = layer.GetNextFeature()
print 'El número de layers es de: ',numLayers

#Obtener el tamaño y bandas de la imagen
filas = ds.RasterYSize
print 'El número de filas del archivo es de: ',filas
columnas = ds.RasterXSize
print 'El número de columnas del archivo es de: ',columnas
bandas = ds.RasterCount
print 'El número de bandas del archivo es de: ',bandas

#Crear una lista para almacenar los datos de entrada de las distintas bandas.
listaBandas = []

#Leer las bandas y almacenar todos los datos en la lista 
for i in range(bandas):
    while feature:
        banda = ds.GetRasterBand(i+1) 
        data = banda.ReadAsArray(0, 0, columnas, filas) 
        listaBandas.append(data)
        print "Los valores de lectura completa por banda son: ","\n", listaBandas
        break

print "\n"

#Se destruyen los objetos creados.  
shapefile.Destroy()
feature.Destroy()

