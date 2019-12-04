from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext
import sys
import requests

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

def aggregate_tags_count(new_values, total_sum):
    return

def get_sql_context_instance(spark_context):
    if ('sqlContextSingletonInstance' not in globals()):
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']

def process_rdd(time, rdd):
    print("----------- %s -----------" % str(time))
    try:
        # Get spark sql singleton context from the current context
	
        sql_context = get_sql_context_instance(rdd.context)
        # convert the RDD to Row RDD
	
        row_rdd = rdd.map(lambda w: Row(prueba1=w))
        # create a DF from the Row RDD

        df = sql_context.createDataFrame(row_rdd)
        # Register the dataframe as table
        print("a")
        df.registerTempTable("testData")
        # get the top 10 hashtags from the table using SQL and print them
        #hashtag_counts_df = sql_context.sql("select hashtag, hashtag_count from hashtags order by hashtag_count desc limit 10")
        df.show()
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
dataStream.pprint()

# start the streaming computation
ssc.start()

# wait for the streaming to finish
ssc.awaitTermination()

