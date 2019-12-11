from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler, PCAModel, StandardScalerModel
from pyspark.ml.clustering import KMeansModel
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

import sys
import requests
import prepro

def tagToTxt(tag):
    if tag == 3:
        return "Posible sismo";
    else:
        return "Datos normales";

# Establecemos la configuracion de SPARK 
conf = SparkConf()
conf.setAppName("SismographStream")

# Establece las variables de contexto de funcionamiento de spark 
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")

# Recibira datos cada 10 seg
ssc = StreamingContext(sc, 10)

# Guarda la sesion en caso de fallo
ssc.checkpoint("checkpoint_SismographStream")

# Leemos los datos del puerto 9012 por direccion localhost
dataStream = ssc.socketTextStream("localhost",9012)

# Cogemos todos los datos relevantes para iniciar nuestro modelo y que posteriormente dividiremos
    # segun las correlaciones lineales entre variables
headers = ['RMS_X_AXIS_X100', 'WINDSPEED', 'PRESSURE','AIR_TEMPERATURE', 'MEAN_X_AXIS_CROSSINGS', 
            'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

# Grupo 1 -> Magnitud del sismogrado y la velocidad del viento correlacionadas
sisms = ['RMS_X_AXIS_X100', 'WINDSPEED']

# Grupo 2 -> Presion y temperatura atmosferica correlacionadas
pre_temp = ['PRESSURE','AIR_TEMPERATURE']

# Variables independientes entre si 
indep = ['MEAN_X_AXIS_CROSSINGS', 'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

# Funciones a usar
def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

# Lo que haremos con cada rdd
def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        if rdd.isEmpty():
            return

        sql_context = get_sql_context_instance(rdd.context)
        
        rdd = rdd.map(lambda line: line.split())

        #Hacemos que cada numero se interprete como un float
        rdd = rdd.map(lambda array: [float(x) for x in array])

        #Transformamos a dataframe de SPARK, y le metemos como cabecera todas las variables que usamos para entrenas
            # el modelo
        df = rdd.toDF(headers)

        #Agrupamos los datos segun las cabeceras inputCols en una unica columna outpuCol
        assembler = VectorAssembler(inputCols=sisms, outputCol='sisms')
        df = assembler.transform(df)

        assembler = VectorAssembler(inputCols=pre_temp, outputCol='pre_temp')
        df = assembler.transform(df)

        assembler = VectorAssembler(inputCols=indep, outputCol='indep')
        df = assembler.transform(df)


        #Cargamos el modelo de estandarización entrenado anteriormente para cada grupo
        scaler = StandardScalerModel.load('model/KMScalerSisms.scaler')
        df = scaler.transform(df)

        scaler = StandardScalerModel.load('model/KMScalerPreTemp.scaler')
        df = scaler.transform(df)

        scaler = StandardScalerModel.load('model/KMScalerIndep.scaler')
        df = scaler.transform(df)

        #Cargamos el modelo entrenado de PCA con los datos reales de la mision para aplicar PCA sobre simulados
             # Aplicamos pca sobre los datos de RMS y WINDSPEED
        pca = PCAModel.load('model/KMPCAsisms.PCA')
        df = pca.transform(df)
            # Aplicamos pca sobre los datos de PRESSURE y AIR_TEMPERATURE
        pca = PCAModel.load('model/KMPCApreTemp.PCA')
        df = pca.transform(df)

        #Como las columnas en las que hemos aplicado PCA y las de variables independientes estan en el dataFrame df
            # deberemos de seleccionar cuales usaremos para clasificar dicho grupo ( se almacenara en df['features'])
        assembler = VectorAssembler(
            inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
            outputCol='features')

        #Agregamos la columna features al dataFrame -> Esta variable es la única que toma el modelo de K-Means para entrenar
        df = assembler.transform(df)
        
        # Ahora mismo, df tiene:
            # Datos en crudo
            # Datos estandarizados
            # Datos con PCA
            # Datos preparados features para clasificar segun el modelo de KMeans(a continuacion)

        # Cargamos el modelo de KMeans entrenado con los datos reales de la mision
        kmeans = KMeansModel.load('model/KM4.model')

        # Categorizamos los datos df['features']
        dfTransformed = kmeans.transform(df)

        func_udf = udf(tagToTxt, StringType())

        # Sacamos la categorizacion de dicho vector o TAG en la variable prediction
            # Seleccionamos unicamente la magnitud del sismografo, con la presion por ejemplo para visualizarlo
            #** pueden usarse cualquier otra
        dfTransformed = dfTransformed.select("RMS_X_AXIS_X100", "WINDSPEED", "PRESSURE", "MEAN_X_AXIS_CROSSINGS", "prediction")

        dfTransformed = dfTransformed.withColumn('meaning', func_udf(dfTransformed['prediction']))

        #Mostramos
        dfTransformed.show()
    except:
        e = sys.exc_info()
        print("Error: %s" % str(e))


dataStream.foreachRDD(process_rdd)

ssc.start()

ssc.awaitTermination()
