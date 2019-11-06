from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import DoubleType
import numpy as np
import pandas as pd
import prepro
import string
import sys

if (len(sys.argv) > 1):
	spark = SparkSession.builder.master("local[*]").appName("Clustering").getOrCreate()

	df = spark.read.format("csv").option("header", "false").option("inferSchema", "true").load(sys.argv[1])

	df = df.na.drop()
	df.show()

	def my_mean(*cols):
	    return float(np.mean(list(cols)))
	udf_mean = udf(my_mean, DoubleType())

	def my_median(*cols):
	    return float(np.median(list(cols)))
	udf_median = udf(my_median, DoubleType())

	def my_min(*cols):
	    return float(np.min(list(cols)))
	udf_min = udf(my_min, DoubleType())

	def my_max(*cols):
	    return float(np.max(list(cols)))
	udf_max = udf(my_max, DoubleType())

	def my_rms(*cols): #root mean square
	    return float(np.sqrt(np.mean(np.array(list(cols))**2)))
	udf_rms = udf(my_rms, DoubleType())

	columns = ['_c5', '_c6', '_c7', '_c8', '_c9', '_c10', '_c11', '_c12', '_c13', '_c14', '_c15', '_c16', '_c17', '_c18', '_c19', '_c20', '_c21', '_c22', '_c23', '_c24', '_c25', '_c26', '_c27', '_c28', '_c29', '_c30', '_c31', '_c32', '_c33', '_c34', '_c35', '_c36', '_c37', '_c38', '_c39', '_c40', '_c41', '_c42', '_c43', '_c44', '_c45', '_c46', '_c47', '_c48', '_c49', '_c50', '_c51', '_c52', '_c53', '_c54', '_c55']

	df = df.withColumn("mean", udf_mean(*columns))
	df = df.withColumn("median", udf_median(*columns))
	df = df.withColumn("min", udf_min(*columns))
	df = df.withColumn("max", udf_max(*columns))
	df = df.withColumn("rms", udf_rms(*columns))


	df.show()

	df.write.option("header", "true").csv(sys.argv[1] + ".output")

else:
	print("Missing argument: file path required. Use: spark-submit extractAmpData.py path")