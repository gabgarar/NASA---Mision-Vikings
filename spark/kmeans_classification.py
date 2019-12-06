from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, PCA, Normalizer, StandardScaler

import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
import prepro
import string

import time

#######################################################################################################
#sudo pip3 install seaborn
#sudo pip3 install pandas
#Puede que necesites instalar tkinter #sudo apt-get install python3-tk
#Asegurate de utilizar python3.6 #PON EN CONSOLA export PYSPARK_PYTHON=/usr/bin/python3.6
#######################################################################################################

#Configuramos spark, creamos el sparkContext y la sesion
conf = SparkConf().setMaster('local[*]').setAppName('Clustering')
sc = SparkContext(conf = conf)
spark = SparkSession.builder.master("local").appName("Clustering").getOrCreate()

#Leemos las cabeceras de cada columna
headers = prepro.read_headers("../nasa/event/event_wind_summary/event_wind_summary.lbl.txt")

#Cogemos los datos del archivo
RDDvar = sc.textFile("../nasa/event/event_wind_summary/event_wind_summary.tab")

#Separamos cada numero de la linea
rawData = RDDvar.map(lambda line: line.split())

#Hacemos que cada numero se interprete como un float
rawData = rawData.map(lambda array: [float(x) for x in array])

#Transformamos a dataframe de SPARK
df = rawData.toDF(headers)


#Vamos a coger los grupos de variables que queremos utilizar para el entrenamiento
	#y a dividirlas segun las correlaciones entre cada grupo
# Grupo 1 -> Magnitud del sismogrado y la velocidad del viento correlacionadas
sisms = ['RMS_X_AXIS_X100', 'WINDSPEED']

# Grupo 2 -> Presion y temperatura atmosferica correlacionadas
pre_temp = ['PRESSURE','AIR_TEMPERATURE']

# Variables independientes entre si 
indep = ['MEAN_X_AXIS_CROSSINGS', 'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

#Cogemos las columnas que queremos usar

#Agrupamos los datos segun las cabeceras inputCols en una unica columna outpuCol
assembler = VectorAssembler(inputCols=sisms, outputCol='sisms')
df = assembler.transform(df)

assembler = VectorAssembler(inputCols=pre_temp, outputCol='pre_temp')
df = assembler.transform(df)

assembler = VectorAssembler(inputCols=indep, outputCol='indep')
df = assembler.transform(df)


#Vamos a estandarizar cada grupo de datos y a guardar el modelo que utilizamos
	# para estandarizar. 
scaler = StandardScaler(inputCol="sisms", outputCol="sismsNorm")
scalerModel = scaler.fit(df)
scalerModel.write().overwrite().save('model/KMScalerSisms.scaler')
df = scalerModel.transform(df)

scaler = StandardScaler(inputCol="pre_temp", outputCol="pre_tempNorm")
scalerModel = scaler.fit(df)
scalerModel.write().overwrite().save('model/KMScalerPreTemp.scaler')
df = scalerModel.transform(df)

scaler = StandardScaler(inputCol="indep", outputCol="indepNorm")
scalerModel = scaler.fit(df)
scalerModel.write().overwrite().save('model/KMScalerIndep.scaler')
df = scalerModel.transform(df)

#Borramos estas columnas a las que ya no les daremos uso
df = df.drop('sisms', 'pre_temp', 'indep')

#Aplicamos PCA a los grupos de variables correlacionadas para agruparlos en una unica
	#variable, ya que kmeans asume que ninguna variable esta correlacionada cuando entrena
dataPCA = PCA(k=1, inputCol='sismsNorm', outputCol="sismsNormPCA")
fitPCA = dataPCA.fit(df)
fitPCA.write().overwrite().save('model/KMPCAsisms.PCA')
df = fitPCA.transform(df)

dataPCA = PCA(k=1, inputCol='pre_tempNorm', outputCol="pre_tempNormPCA")
fitPCA = dataPCA.fit(df)
fitPCA.write().overwrite().save('model/KMPCApreTemp.PCA')
df = fitPCA.transform(df)

#Agrupamos las columnas con las que vamos a entrenar en una columna feautures
assembler = VectorAssembler(
    inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
    outputCol='features')

trainingData = assembler.transform(df)

#Creamos un par de arrays que guarden el coste de cada modelo para poder
#represemtar graficamente luego
computingCostIndex = []
computingCost = []

#Creamos un diccionario con colores para representar graficamente luego los resultados
color_dict = dict({0:'tomato',
                  1:'limegreen',
                  2: 'orange',
                  3: 'saddlebrown',
                  4: 'dodgerblue',
                  5: 'paleturquoise',
                  6: 'orchid',
                  7: 'grey',
                  8: 'lightpink'})

#Bucle para probar con distinto numero de grupos
for i in range(4, 5):
	#Entrenamos el modelo de Kmeans con un numero de grupos igual a i
	kmeans = KMeans().setK(i)
	model = kmeans.fit(trainingData)

	#Computamos el coste del modelo
	wssse = model.computeCost(trainingData)

	#Guardado del modelo
	model.write().overwrite().save('model/KM' + str(i) + '.model')

	#Aniadimos el coste a los arrays
	computingCostIndex.append(i)
	computingCost.append(wssse)

	#Aniadimos la prediccion con el modelo entrenado
	#anteriormente a nuestros datos
	transformed = model.transform(trainingData)

	#Creamos archivos con los datos estadisticos de cada grupo 
	#para su posterior analisis
	describe = transformed
	for j in range (i):
		describeGrouped = describe.filter(describe.prediction == j)
		describeGrouped = describeGrouped.describe()
		describeGrouped.write.option("header", "true").csv("describe/describe_kmeans_" + str(i) + "/precition_" + str(j) + ".txt", mode="overwrite")

	#Transformamos el dataframe de spark a un dataframe de pandas para poder representarlo
	pdDF = transformed.toPandas()
	#Creamos varios graficos que ilustren los grupos formados y los guardamos
	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['SEISMIC_TIME_SOLS'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_sols.png")

	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['PRESSURE'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_pres.png")

	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['WIND_DIRECTION'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_winddir.png")	

#Guardamos el grafico con el coste de cada grupo
plt.figure()
plt.plot(computingCostIndex, computingCost, '-')
plt.ylabel('Within set sum of squared errors')
plt.xlabel('Number of clusters')
plt.savefig("images/codo.png")

