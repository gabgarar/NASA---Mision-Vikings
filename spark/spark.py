from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import concat
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import pandas as pd
import prepro
import string

#######################################################################################################
#LEE ESTO PORFA

#ESto para matplotlib animator apt-get install ffmpeg
#Necesita instalar pandas
#Necesita instalar tkinter #sudo apt-get install python3-tk
#Asegurarse que se utiliza python3.6 porfavor #PON EN CONSOLA export PYSPARK_PYTHON=/usr/bin/python3.6
#######################################################################################################

#Configuramos spark, creamos el sparkContext y la sesión
conf = SparkConf().setMaster('local[*]').setAppName('Clustering')
sc = SparkContext(conf = conf)
spark = SparkSession.builder.master("local").appName("Clustering").getOrCreate()

headers = prepro.read_headers("event_wind_summary.lbl")
#Cogemos los datos del archivo
RDDvar = sc.textFile("event_wind_summary.tab")

#Separamos cada numero de la linea
rawData = RDDvar.map(lambda line: line.split())

#Hacemos que cada numero se interprete como un float
rawData = rawData.map(lambda array: [float(x) for x in array])

#Transformamos a datafra,e
df = rawData.toDF(headers)

df = df.withColumn("combined", concat(df.MAXIMUM_X_AXIS, df.WINDSPEED, df.PRESSURE, df.AIR_TEMPERATURE))

dfFeatures = df.select("MAXIMUM_X_AXIS", "WINDSPEED", "PRESSURE", "AIR_TEMPERATURE")

#El algoritmo de ml pide que tengamos una columna llamada features para poder usarse, con las columnas que va a procesar
assembler = VectorAssembler(
	#Todas, no hay miedo
    inputCols=['MAXIMUM_X_AXIS', 'WINDSPEED', 'PRESSURE', 'AIR_TEMPERATURE'], #_18 es el eje Z, no lo pongo para plotearlo
    outputCol='features')

#agregamos la columna
trainingData = assembler.transform(dfFeatures)

trainingData.show()

for i in range(4, 5):
	kmeans = KMeans().setK(i)
	model = kmeans.fit(trainingData)

	#Mostramos la info del resultado, copiado y pegado de la página de documentación
	wssse = model.computeCost(trainingData)
	print("Within Set Sum of Squared Errors = " + str(wssse))

	# Shows the result.
	centers = model.clusterCenters()
	print("Cluster Centers: ")
	for center in centers:
	    print(center)

	transformed = model.transform(trainingData)
	transformed.show()    

	transformed.write.option("header", "true").json("prueba.out")

	figure = plt.figure()
	ax = Axes3D(figure)
	pdDF = transformed.toPandas()

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

	######################################################################################################
	plot = ax.scatter(pdDF['MAXIMUM_X_AXIS'], pdDF['WINDSPEED'], pdDF['PRESSURE'], c=pdDF['prediction'])
	ax.set_xlabel('MAXIMUM_X_AXIS')
	ax.set_ylabel('WINDSPEED')
	ax.set_zlabel('PRESSURE')

	fig = plot.get_figure()
	fig.savefig("output.png")

