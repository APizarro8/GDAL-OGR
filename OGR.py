# -*- coding: utf-8 -*-
#Ejercicio 1 parte I
#Propósito: Utilizar métodos de GDAL/OGR para consultar información vectorial, modificarla o eliminarla.
#Autor: Alicia Pizarro
#Fecha: 30/12/2017

import ogr
import os

#Establecer el espacio de trabajo
path = 'D:\\Practica4_py\\UNEP-EDE__forest_area__1445948601'
os.chdir(path)

#Obtener el driver para shapefile
driverName = "ESRI Shapefile"
driver = ogr.GetDriverByName(driverName)

if driver is None:
    print 'No se encuentra el driver elegido.'
else:
    print  'El driver {0} es correcto.'.format(driverName)
    
#Abrir el shapefile de origen para lectura: el 0 para lectura, y el 1 para modificar
shapefile = 'UNEP-EDE__forest_area__1445948601.shp'
dataSource = driver.Open(shapefile, 1)

#Obtener el número de layers del shapefile
numeroLayers = dataSource.GetLayerCount() 
print 'El número de layers es de: ', numeroLayers

#Crear un objeto layer
layer = dataSource.GetLayer() #index es 0 y opcional para shapefiles

#Obtener el número de features sobre el layer
numeroFeatures = layer.GetFeatureCount()
print 'El número de features es de: ',numeroFeatures

#Obtener la referencia espacial del layer
spatialRef = layer.GetSpatialRef()
print 'No se ha encontrado sistema de referencia en el shapefile.'

if spatialRef:
    print spatialRef.ExportToProj4() #Exporta el SCR a formato PROJ.4 
else:
    print 'No se ha podido exportar el SCR a formato PROJ.4 debido a su inexistencia.'

#Obtener el número de campos de la tabla de atributos del layer
feature = layer.GetFeature(0) #Registro 0
layerDef = layer.GetLayerDefn() #Crea el objeto 
numeroField = layerDef.GetFieldCount() 
print 'El número de campos de la tabla de atributos de la layer es: ', numeroField

print '\n'

#Obtener nombre y características de los campos
for field in range(numeroField):
    fieldName = layerDef.GetFieldDefn(field).GetName()
    fieldTypeCode = layerDef.GetFieldDefn(field).GetType()
    fieldWidth = layerDef.GetFieldDefn(field).GetWidth()
    fieldType = layerDef.GetFieldDefn(field).GetFieldTypeName(fieldTypeCode)
    precision = layerDef.GetFieldDefn(field).GetPrecision()
    print 'Nombre: {0} \nTipo: {1} \nLongitud: {2} \nPrecisión: {3}'.format(fieldName, \
                                                                            fieldType, \
                                                                            fieldWidth, \
                                                                            fieldTypeCode, \
                                                                            precision)
    print '\n'

#Extraer el nombre de los países que pertenecen a "Eastern Europe"
layer.SetAttributeFilter("SREG_NAME = 'Eastern Europe'")
print 'Los países que pertenecen a la subregion "Eastern Europe" son:'
for feature in layer:
    print feature.GetField("NAME")
print '\n'


#Modificar el valor del campo DEVELOPED de la región con ID = 0 asignándole el valor 1
feature = layer.GetFeature(0) #Posicionarse 
feature.SetField("DEVELOPED", 1) #Establecer nuevo valor
layer.SetFeature(feature) #Reescribir 

#Para los países cuyo código ISO_2_CODE está vacío, asignar campo de valor 'NN'
layer.SetAttributeFilter("ISO_2_CODE IS NULL")
for feature in layer:
    print feature.GetField("NAME") 
    feature.SetField("ISO_2_CODE", "NN") #Establecer el nuevo valor
    layer.SetFeature(feature) #Reescribir 
    
layer.SetAttributeFilter(None) #Limpiar filtro
layer.GetFeature(0) #Reinicializar lectura


feature.Destroy()
dataSource.Destroy()
