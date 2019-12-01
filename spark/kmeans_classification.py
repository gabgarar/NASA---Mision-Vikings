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
#Necesita instalar tkinter #sudo apt-get install python3-tk
#Asegurate de utilizar python3.6 #PON EN CONSOLA export PYSPARK_PYTHON=/usr/bin/python3.6
#######################################################################################################

#Configuramos spark, creamos el sparkContext y la sesion
conf = SparkConf().setMaster('local[*]').setAppName('Clustering')
sc = SparkContext(conf = conf)
spark = SparkSession.builder.master("local").appName("Clustering").getOrCreate()

headers = prepro.read_headers("../nasa/event/event_wind_summary/event_wind_summary.lbl.txt")

#Cogemos los datos del archivo
RDDvar = sc.textFile("../nasa/event/event_wind_summary/event_wind_summary.tab")

#Separamos cada numero de la linea
rawData = RDDvar.map(lambda line: line.split())

#Hacemos que cada numero se interprete como un float
rawData = rawData.map(lambda array: [float(x) for x in array])

#Transformamos a dataframe de SPARK
df = rawData.toDF(headers)

#Cogemos las columnas que queremos usar
sisms = ['MEDIAN_X_AXIS', 'FIRST_X_AXIS',
       'MAXIMUM_X_AXIS','RMS_X_AXIS_X100',
       'RMS_Y_AXIS_X100', 'RMS_Z_AXIS_X100','WINDSPEED']

pre_temp = ['PRESSURE','AIR_TEMPERATURE']

indep = ['MINIMUM_X_AXIS','MEAN_X_AXIS_CROSSINGS',
       'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

#Creamos nuevas columnas con los grupos
assembler = VectorAssembler(inputCols=sisms, outputCol='sisms')
df = assembler.transform(df)

assembler = VectorAssembler(inputCols=pre_temp, outputCol='pre_temp')
df = assembler.transform(df)

assembler = VectorAssembler(inputCols=indep, outputCol='indep')
df = assembler.transform(df)

#Vamos a crear nuevas columnas con los datps estrandarizados con 
scaler = StandardScaler(inputCol="sisms", outputCol="sismsNorm")
scalerModel = scaler.fit(df)
df = scalerModel.transform(df)

scaler = StandardScaler(inputCol="pre_temp", outputCol="pre_tempNorm")
scalerModel = scaler.fit(df)
df = scalerModel.transform(df)

scaler = StandardScaler(inputCol="indep", outputCol="indepNorm")
scalerModel = scaler.fit(df)
df = scalerModel.transform(df)

df = df.drop('sisms', 'pre_temp', 'indep')

#PCA
dataPCA = PCA(k=1, inputCol='sismsNorm', outputCol="sismsNormPCA")
fitPCA = dataPCA.fit(df)
df = fitPCA.transform(df)

dataPCA = PCA(k=1, inputCol='pre_tempNorm', outputCol="pre_tempNormPCA")
fitPCA = dataPCA.fit(df)
df = fitPCA.transform(df)

df.show()

assembler = VectorAssembler(
    inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
    outputCol='features')

#agregamos la columna
trainingData = assembler.transform(df)

#Creamos un par de arrays que guarden el coste de cada modelo para poder
#represemtarñp gráficamente luego
computingCostIndex = []
computingCost = []

#Creo un diccionario con colores para representar graficamente luego los resultados
color_dict = dict({0:'tomato',
                  1:'limegreen',
                  2: 'orange',
                  3: 'saddlebrown',
                  4: 'dodgerblue',
                  5: 'paleturquoise',
                  6: 'orchid',
                  7: 'grey',
                  8: 'lightpink'})

log = open("log.txt", "a+")
#Bucle para probar con distinto número de grupos
for i in range(3, 9):
	#start_time = time.time()
	#Entrenamos el modelo de Kmeans con un numero de grupos igual a i
	kmeans = KMeans().setK(i)
	model = kmeans.fit(trainingData)

	#Computamos el cosete del modelo
	wssse = model.computeCost(trainingData)

	#guardado del modelo
	model.save('model/KM' + str(i) + '.model')

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

	#Creamos varios graficos que ilustren los grupos formados
	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['SEISMIC_TIME_SOLS'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_sols.png")

	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['PRESSURE'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_pres.png")

	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['WIND_DIRECTION'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_winddir.png")	

#Mostramos el gráfico con el coste
plt.figure()
plt.plot(computingCostIndex, computingCost, '-')
plt.ylabel('Within set sum of squared errors')
plt.xlabel('Number of clusters')
plt.savefig("codo2.png")

