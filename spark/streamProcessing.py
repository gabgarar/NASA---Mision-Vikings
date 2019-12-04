from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler, PCAModel, StandardScalerModel
from pyspark.ml.clustering import KMeansModel
import sys
import requests
import prepro

# create spark configuration
conf = SparkConf()
conf.setAppName("SismographStream")

# create spark instance with the above configuration
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
# create the Streaming Context from the above spark context with window size 2 seconds
ssc = StreamingContext(sc, 2)
# setting a checkpoint to allow RDD recovery
ssc.checkpoint("checkpoint_SismographStream")
# read data from port 9009
dataStream = ssc.socketTextStream("localhost",9012)

headers = ['RMS_X_AXIS_X100', 'WINDSPEED', 'PRESSURE','AIR_TEMPERATURE', 'MEAN_X_AXIS_CROSSINGS', 
            'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

#Columnas en las que se agrupan los datos
sisms = ['RMS_X_AXIS_X100', 'WINDSPEED']

pre_temp = ['PRESSURE','AIR_TEMPERATURE']

indep = ['MEAN_X_AXIS_CROSSINGS', 'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']





def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        if rdd.isEmpty():
            return
        # Get spark sql singleton context from the current context
	
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
	        
        #Separamos cada numero de la linea
        rdd = rdd.map(lambda line: line.split())

        #Hacemos que cada numero se interprete como un float
        rdd = rdd.map(lambda array: [float(x) for x in array])

        #Transformamos a dataframe de SPARK
        df = rdd.toDF(headers)

        #--------------------------------------------------------------Creamos nuevas columnas con los grupos
        assembler = VectorAssembler(inputCols=sisms, outputCol='sisms')
        df = assembler.transform(df)

        assembler = VectorAssembler(inputCols=pre_temp, outputCol='pre_temp')
        df = assembler.transform(df)

        assembler = VectorAssembler(inputCols=indep, outputCol='indep')
        df = assembler.transform(df)

        #Vamos a crear nuevas columnas con los datps estrandarizados con 
        scaler = StandardScalerModel.load('model/KMScalerSisms.scaler')
        df = scaler.transform(df)

        scaler = StandardScalerModel.load('model/KMScalerPreTemp.scaler')
        df = scaler.transform(df)

        scaler = StandardScalerModel.load('model/KMScalerIndep.scaler')
        df = scaler.transform(df)

        pca = PCAModel.load('model/KMPCAsisms.PCA')
        df = pca.transform(df)

        pca = PCAModel.load('model/KMPCApreTemp.PCA')
        df = pca.transform(df)

        assembler = VectorAssembler(
            inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
            outputCol='features')

        #agregamos la columna
        df = assembler.transform(df)
        
        kmeans = KMeansModel.load('model/KM4.model')
        dfTransformed = kmeans.transform(df)



        '''scaler = StandardScaler(inputCol="pre_temp", outputCol="pre_tempNorm")
        scalerModel = scaler.fit(df)
        scalerModel.save('model/KMScalerPreTemp.scaler')
        df = scalerModel.transform(df)

        scaler = StandardScalerModel(inputCol="indep", outputCol="indepNorm")
        scalerModel = scaler.fit(df)
        scalerModel.save('model/KMScalerIndep.scaler')
        df = scalerModel.transform(df)'''

        # get the top 10 hashtags from the table using SQL and print them
        #hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 10")
        dfTransformed.show()
    except:
        e = sys.exc_info()
        #e2 = sys.exc_info()[1] 
        print("Error: %s" % str(e))

# split each tweet into words
#words = dataStream.map(lambda line: line.split(" "))
# print in the period

# acculmulate the state
#words = words.updateStateByKey(words)
# do processing for each RDD generated in each interval
#words.foreachRDD(process_rdd)
dataStream.foreachRDD(process_rdd)

# start the streaming computation
ssc.start()

# wait for the streaming to finish
ssc.awaitTermination()

