from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import DoubleType
from pyspark.sql.functions import udf
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
from pyspark.ml.feature import VectorAssembler, PCA, MinMaxScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pyspark.ml.clustering import GaussianMixture
from pyspark.ml.feature import Normalizer, StandardScaler #Quedarnos con el que nos mole
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

#Transformamos a dataframe de SPARK
df = rawData.toDF(headers)

#Cogemos las columnas que queremos usar
sisms = ['MEDIAN_X_AXIS', 'FIRST_X_AXIS',
'MAXIMUM_X_AXIS','RMS_X_AXIS_X100',
'RMS_Y_AXIS_X100', 'RMS_Z_AXIS_X100','WINDSPEED']

pre_temp = ['PRESSURE','AIR_TEMPERATURE']

indep = ['MINIMUM_X_AXIS','MEAN_X_AXIS_CROSSINGS',
'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

assembler = VectorAssembler(
inputCols=sisms,
outputCol='sisms')

#agregamos la columna
df = assembler.transform(df)

assembler = VectorAssembler(
inputCols=pre_temp,
outputCol='pre_temp')

#agregamos la columna
df = assembler.transform(df)

assembler = VectorAssembler(
inputCols=indep,
outputCol='indep')

#agregamos la columna
df = assembler.transform(df)

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

#GMM



#--------

dataPCA = PCA(k=1, inputCol='pre_tempNorm', outputCol="pre_tempNormPCA")
fitPCA = dataPCA.fit(df)
df = fitPCA.transform(df)

df.show()

assembler = VectorAssembler(
inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
outputCol='features')

#agregamos la columna
trainingData = assembler.transform(df)


log = open("log.txt", "a+")
for i in range(4, 5):
#start_time = time.time()
	gmm = GaussianMixture().setK(i) #PROBANDO CON GMM 
model = gmm.fit(trainingData)

#mostramos resultado
#transformed.show()

#Mostramos la info del resultado, copiado y pegado de la pagina de documentacion
#wssse = model.computeCost(trainingData)

#print("Within Set Sum of Squared Errors = " + str(wssse))

#guardado del modelo
#model.save('modelo_kmeans_' + str(i) + '.model')

#computingCostIndex.append(i)
#computingCost.append(wssse)

# Shows the result.
#centers = model.clusterCenters()
#print("Cluster Centers: ")
#for center in centers:
#	print(center)

transformed = model.transform(trainingData)

#countTable = transformed.groupBy("prediction").agg({"prediction":"count"})

#transformed = transformed.groupBy('prediction').avg(*features)

#transformed.write.option("header", "true").json("prueba.out")
#print("--- %i: %s seconds ---\n" % (i, (time.time() - start_time)))
#log.write("--- %i: %s seconds ---\n" % (i, (time.time() - start_time)))

#figure = plt.figure()
#ax = Axes3D(figure)
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
anim.save('clustering.mp4', fps=30, extra_args=['-vcodec', 'libx264'], progress_callback= lambda x, i: print(f'Saving frame {x}/{i}')) #progress_callback requires matplotlib 3.1.1
print("Saved")
'''
######################################################################################################

plt.scatter(pdDF['RMS_X_AXIS_X100'], pdDF['SEISMIC_TIME_SOLS'], c = pdDF['prediction'], s = 10)
plt.xlabel("RMS_X_AXIS_X100")
plt.ylabel("SEISMIC_TIME_SOLS")

'''plot = ax.scatter(pdDF['WINDSPEED'].str[0], pdDF['AIR'].str[1], pdDF['features'].str[2], c = pdDF['prediction'])
ax.set_xlabel('windspeed')
ax.set_ylabel('air_temp')
ax.set_zlabel('RMS_X_AXIS_X100')'''

#fig = plt.get_figure()
plt.savefig("output_spark" + str(i) + ".png")


