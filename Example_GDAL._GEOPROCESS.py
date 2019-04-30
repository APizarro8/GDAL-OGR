# -*- coding: utf-8 -*-
#Propósito:Con los ráster del Corredor del Henares realizar tareas de geoprocesamiento. 
#Autor: Alicia Pizarro
#Fecha: 02/12/2017

## IMPORTACIÓN DE LIBERÍAS
import gdal
import os
import sys
import osr

#Establecer el espacio de trabajo
path = 'xxDATAxxENTRADAxx'
os.chdir(path)

# Se registran todos los drivers. 
gdal.AllRegister()

# Imágenes consideradas para la realizacion del mosaico. 
MDT_1 = 'MDTxxx.asc'
MDT_2 = 'MDTxxx.asc'

#Creación de listas 
filas = []
columnas = []
maxX= []
minY = []
minXm = []
minYm= []

# Modelo Digital del Terreno primero, el cúal va a ser analizado: 
print "Raster del cuál se obtendrá información: " + MDT_1 + '\n'
ds_1 = gdal.Open(MDT_1)
bandas = ds_1.RasterCount
banda_1 = ds_1.GetRasterBand(1)
filas_1 = ds_1.RasterYSize
columnas_1 = ds_1.RasterXSize
print "Filas: \t", filas_1, "Columnas: \t", columnas_1, "Bandas: \t", banda_1

#Obtener los coeficientes de transformación del dataSet
transform_1 = ds_1.GetGeoTransform()
minX_1 = transform_1[0]
maxY_1= transform_1[3]
anchoPixel_1 = transform_1[1]
altoPixel_1= transform_1[5]
maxX_1 = minX_1 + (columnas_1 * anchoPixel_1)
minY_1 = maxY_1 +(filas_1 * altoPixel_1)
print "Ancho pixel: \t", anchoPixel_1, "Alto pixel: \t", altoPixel_1

print '\n'

# Modelo Digital del Terreno segundo, el cúal va a ser analizado: 
print "Raster del cuál se obtendrá información: " + MDT_2 + '\n'
ds_2 = gdal.Open(MDT_2)
bandas = ds_2.RasterCount
banda_2 = ds_2.GetRasterBand(1)
filas_2 = ds_2.RasterYSize
columnas_2 = ds_2.RasterXSize
print "Filas: \t", filas_2, "Columnas: \t", columnas_2, "Bandas: \t", banda_2

# Con el GeoTrasform ()se obtienen los coeficientes de trasformacion de una imagen.   
transform_2 = ds_2.GetGeoTransform()
minX_2 = transform_1[0]
maxY_2 = transform_1[3]
anchoPixel_2 = transform_1[1]
altoPixel_2= transform_1[5]
maxX_2 = minX_2 + (columnas_2 * anchoPixel_2)
minY_2 = maxY_2 +(filas_2 * altoPixel_2)
print "Ancho pixel: \t", anchoPixel_2, "Alto pixel: \t", altoPixel_2

#Obtener las coordenadas máximas y mínimas del futuro mosaico 
minXm = min(minX_1, minX_2)
maxXm = max(maxX_1, maxX_2)
minYm = min(minY_1, minY_2)
maxYm = max(maxY_1, maxY_2)

#Obtener info del futuro mosaico desde una de las imágenes 
columnasm = int((maxXm - minXm)/anchoPixel_1)
filasm = int((maxYm - minYm)/abs(altoPixel_1))

#Obtener el offset respecto de la imagen de origen
xOffset_1 = []
yOffset_1= []
xOffset_2 = []
yOffset_2 = []

xOffset_1 = int((minX_1 - minXm)/anchoPixel_1)
yOffset_1 = int((maxY_1 - maxYm)/altoPixel_1)
xOffset_2 = int((minX_2 - minXm)/anchoPixel_2)
yOffset_2 = int((maxY_2 - maxYm)/altoPixel_2)

#Crear el mosaico
driver = gdal.GetDriverByName('GTiff')
dsMosaico = driver.Create('Mosaico.tiff', columnasm, filasm, 1, banda_1.DataType)
bandaMosaico = dsMosaico.GetRasterBand(1)

#Leer los dataSet y escribirlos en el Mosaico
data_1 = banda_1.ReadAsArray(0, 0, columnas_1, filas_1)
bandaMosaico.WriteArray(data_1, xOffset_1, yOffset_1)

# Leer la imagen 2º (completa)  y escribirla en la salida (imagen mosaico). 
data_2 = banda_2.ReadAsArray(0, 0, columnas_2, filas_2)
bandaMosaico.WriteArray(data_2, xOffset_2, yOffset_2)

################################################### FINISH #########################################################
####################################################################################################################
