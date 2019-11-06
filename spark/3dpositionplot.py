from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import pandas as pd
import prepro
import string
import sys
import numpy as np

#######################################################################################################
#LEE ESTO PORFA

#Usando la opción -a en este programa, la salida es una animación en vez de una imagen 

#ESto para matplotlib animator apt-get install ffmpeg
#Necesita instalar pandas
#Necesita instalar tkinter #sudo apt-get install python3-tk
#Asegurarse que se utiliza python3.6 porfavor #PON EN CONSOLA export PYSPARK_PYTHON=/usr/bin/python3.6
#Instalar ffmepg para la animacion apt-get install ffmpeg
#######################################################################################################

#Configuramos spark, creamos el sparkContext y la sesion
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

dfGroup = df.groupBy(df.MEAN_X_AXIS_CROSSINGS, df.MEAN_Y_AXIS_CROSSINGS, df.MEAN_Z_AXIS_CROSSINGS).count()

dfGroup = dfGroup.withColumnRenamed("count", "countGroup")
#Coge el valor del maximo numero de elementos en un grupo
countMax = dfGroup.agg({"countGroup": "max"}).head()[0]

#Se normaliza respecto al maximo numero de apariciones del mismo punto
dfFinal = dfGroup.withColumn("countGroup", (dfGroup.countGroup / countMax))

figure = plt.figure()
ax = Axes3D(figure)
pdDF = dfFinal.toPandas()

rgba_color = np.zeros((pdDF.count()[0], 4))
rgba_color[:,0] = 0.921
rgba_color[:,1] = 0.25
rgba_color[:,2] = 0.203 #Color rojo para todos
rgba_color[:,3] = pdDF['countGroup'] 

#ANIMATION
if (len(sys.argv) > 1 and sys.argv[1] == "-a"):
	print("ANIMATING...")
	def init():
	    ax.scatter(pdDF['MEAN_X_AXIS_CROSSINGS'], pdDF['MEAN_Y_AXIS_CROSSINGS'], pdDF['MEAN_Z_AXIS_CROSSINGS'], color=rgba_color)
	    ax.set_xlabel('x mean')
	    ax.set_ylabel('y mean')
	    ax.set_zlabel('z mean')
	    return figure,

	def animate(i): 
	    ax.view_init(elev=10., azim=i)
	    return figure,

	# Animate

	anim = animation.FuncAnimation(figure, animate, init_func=init,frames=360, interval=20, blit=True)
	# Save
	anim.save('seismic_hotspots.mp4', fps=30, extra_args=['-vcodec', 'libx264'],  progress_callback= lambda x, i: print(f'Saving frame {x}/{i}')) #progress_callback requires matplotlib 3.1.1
	print("Saved")
else:
	plot = ax.scatter(pdDF['MEAN_X_AXIS_CROSSINGS'], pdDF['MEAN_Y_AXIS_CROSSINGS'], pdDF['MEAN_Z_AXIS_CROSSINGS'], color=rgba_color)
	ax.set_xlabel('x mean')
	ax.set_ylabel('y mean')
	ax.set_zlabel('z mean')

	fig = plot.get_figure()
	fig.savefig("output.png")

dfFinal.write.csv("output.txt")
