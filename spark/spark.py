from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, PCA, MinMaxScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import pandas as pd
import prepro
import string

import time

#######################################################################################################
#LEE ESTO PORFA

#ESto para matplotlib animator apt-get install ffmpeg
#Necesita instalar pandas
#Necesita instalar tkinter #sudo apt-get install python3-tk
#Asegurarse que se utiliza python3.6 porfavor #PON EN CONSOLA export PYSPARK_PYTHON=/usr/bin/python3.6
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

#Transformamos a dataframe de SPARK //
df = rawData.toDF(headers)

#Cogemos las columnas que queremos usar
#features = ['WINDSPEED', 'PRESSURE', 'AIR_TEMPERATURE', 'RMS_X_AXIS_X100', 'RMS_Y_AXIS_X100', 'RMS_Z_AXIS_X100']
features = ['WINDSPEED', 'AIR_TEMPERATURE', 'RMS_X_AXIS_X100']

dfFeatures = df.select(*features)

featuresScaled = []

firstelement=udf(lambda v:float(v[0]),DoubleType())

#NORMALIZATION
for i in features:
    print(i)
    # Convierte la columna a vector con VectorAssembler
    assembler = VectorAssembler(inputCols=[i],outputCol=i+'_V')

    # normalizacion con MinMaxScaler
    scaler = MinMaxScaler(inputCol=i+"_V", outputCol=i+'_S')

    # Crea la pipeline con el assembler y el scaler
    pipeline = Pipeline(stages=[assembler, scaler])

    # Realiza la pipeline
    dfFeatures = pipeline.fit(dfFeatures).transform(dfFeatures)

    #Transforma la columna de arrays con un solo elemento a double
    dfFeatures = dfFeatures.withColumn(i+"_S", firstelement(dfFeatures[i+"_S"])).drop(i+"_V")
	
	#Aniadimos al array que contiene el nombre de las columnas normalizadas
    featuresScaled.append(i+'_S')

dfFeatures.show()

#El algoritmo de ml pide que tengamos una columna llamada features para poder usarse, con las columnas que va a procesar
assembler = VectorAssembler(
    inputCols=featuresScaled,
    outputCol='features')

#agregamos la columna
trainingData = assembler.transform(dfFeatures)


#PCA
dataPCA = PCA(k=3, inputCol='features', outputCol="pcafeatures")
fitPCA = dataPCA.fit(trainingData)
trainingData = fitPCA.transform(trainingData).select("features", "pcafeatures")


log = open("log.txt", "a+")
for i in range(4, 5):
	start_time = time.time()
	kmeans = KMeans().setK(i)
	model = kmeans.fit(trainingData)

	#Mostramos la info del resultado, copiado y pegado de la pagina de documentacion
	wssse = model.computeCost(trainingData)
	print("Within Set Sum of Squared Errors = " + str(wssse))

	# Shows the result.
	centers = model.clusterCenters()
	print("Cluster Centers: ")
	for center in centers:
	    print(center)

	transformed = model.transform(trainingData)

	countTable = transformed.groupBy("prediction").agg({"prediction":"count"})

	transformed2 = transformed.groupBy("prediction").avg(*features)
	#transformed = transformed.groupBy('prediction').avg(*features)

	#transformed.write.option("header", "true").json("prueba.out")
	print("--- %i: %s seconds ---\n" % (i, (time.time() - start_time)))
	log.write("--- %i: %s seconds ---\n" % (i, (time.time() - start_time)))

	figure = plt.figure()
	ax = Axes3D(figure)
	pdDF = transformed.toPandas()

	######################################################################################################
	'''
	print("ANIMATING...")
	def init():
		ax.scatter(pdDF['MAXIMUM_X_AXIS'], pdDF['WINDSPEED'], pdDF['PRESSURE'], c=pdDF['prediction'])
		ax.set_xlabel('MAXIMUM_X_AXIS')
		ax.set_ylabel('WINDSPEED')
		ax.set_zlabel('PRESSURE')
		return figure,

	def animate(i): 
		ax.view_init(elev=10., azim=i)
		return figure,

	# Animate

	anim = animation.FuncAnimation(figure, animate, init_func=init,frames=360, interval=20, blit=True)
	# Save
	anim.save('clustering.mp4', fps=30, extra_args=['-vcodec', 'libx264'],  progress_callback= lambda x, i: print(f'Saving frame {x}/{i}')) #progress_callback requires matplotlib 3.1.1
	print("Saved")
	'''
	######################################################################################################

	plot = ax.scatter(pdDF['features'].str[0], pdDF['features'].str[1], pdDF['features'].str[2], c = pdDF['prediction'])
	ax.set_xlabel('windspeed')
	ax.set_ylabel('air_temp')
	ax.set_zlabel('RMS_X_AXIS_X100')


	fig = plot.get_figure()
	fig.savefig("output_yes_2.png")

