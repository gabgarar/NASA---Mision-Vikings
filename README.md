
# ANALISIS DE DATOS SISMOGRÁFICOS PROCEDENTES DE LA MISIÓN VIKING


### INTRODUCCIÓN

El propósito clave de nuestro proyecto es un clasificador a tiempo real de datos procedentes de un rover u otra sonda espacial.
Esto se logrará con un cliente TCP(sonda que toma muestras)y un servidor TCP(el que se encargará de recibir los datos y clasificarlos en tiempo real). 

Para todo ello dispondremos el proyectos en diferentes fases. 
	***![Ver gráfico super chulo si hace click](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/easterEGG/lel.jpg)***
* La **fase 1** del proyecto será la **fase analítica de los datos**. Se estudiará:
	- Como se distribuyen los datos en los diferentes archivos.
	- Que tipo de datos disponemos.
	- Qué características tienen esos datos, haciendo uso de estadísticas básicas y distribuciones.
	- Estandarización o normalización de los datos.
	- Estudio de correlaciones lineales e introducción en correlaciones no lineales.
	- Librerías usará cada parte.
* La **fase 2** del proyecto será la **preparación de la entrada** del clasificador y su **entrenamiento**.
	- Subdivisión del dataframe en grupos linealmente independientes.
	- Aplicación de algorítmo PCA.
	- Qué algoritmo de clasificación usar y su por qué.
	- Estudio de los datos de salida del algoritmo de clasificación.
	- Como exportar el modelo para su uso posterior
* La **fase 3** del proyecto será preparar el cliente y el servidor:
	* Cliente:
		- Como establecer la conexión.
		- Como preparar los datos simulados para envíar.
	* Servidor:
		- Como establecer la conexión
		- Como importar el modelo
		- Como tratar la entrada de datos
		- Como categorizar en tiempo de flujo real
	
		

## INDICE

- [ 1) FASE DE ANÁLISIS](#1-fase-de-análisis).
  - [1.1) PROCEDENCIA DE LOS DATOS](#11-procedencia-de-los-datos).
  - [1.2) ESTRUCTURACIÓN DE LOS DATOS Y ESTADÍSTICAS](#12-estructuración-de-los-datos-y-estadísticas).
    - [1.2.1) ESTRUCTURA DE LOS ARCHIVOS](#121-estructura-de-los-archivos).
    - [1.2.2) ESTRUCTURA DE LOS DATOS](#122-estructura-de-los-datos).
    - [1.2.3) LECTURA DEL DATASET](#123-lectura-del-dataset-e-importación-de-librerías).
    - [1.2.4) ESTADÍSTICAS BÁSICAS DE VARIABLES A ANALIZAR](#124-estadísticas-básicas-de-variables-a-analizar).
  - [1.3) AGRUPACIÓN DE DATOS](#insertar-hn)
    - [1.3.1) NORMALIZACIÓN DEL DATASET](#insertar-hn).
    - [1.3.2) MATRIZ DE CORRELACIÓN](#insertar-hn).
    - [1.3.3) ANÁLISIS DE RELACIONES LINEALES](#insertar-hn).
    - [1.3.4) AGRUPACIÓN DE VARIABLES COMO GRUPOS INDEPENDIENTES](#insertar-hn).
  - [1.4) VARIABLES NO RELACIONADAS LINEALMENTE](#insertar-hn)
  
- [ 2) FASE DE MODELADO DE ALGORITMOS NO SUPERVISADOS](#2-fase-de-modelado-de-algoritmos-no-supervisados).
  - [2.1) REDUCCIÓN DE VARIABLES DEPENDIENTES A INDEPENDIENTES](#21-reducción-de-variables-dependientes-a-independientes).
    - [2.1.1) INTRODUCCIÓN PCA](#211-introducción-pca).
    - [2.1.2) APLICACIÓN PCA SOBRE CADA GRUPO DE VARIABLES DEPENDIENTES](#212-aplicación-pca-sobre-cada-grupo-de-variables-dependientes).
  - [2.2) MODELOS DE CLASIFICACIÓN NO SUPERVISADOS](#22-modelos-de-clasificación-no-supervisados).
    - [2.2.1) INTRODUCCIÓN MODELOS NO SUPERVISADOS](#221-introducción-modelos-no-supervisados).
    - [2.2.2) MODELO K-MEANS](#222-modelo-k-means).
      - [2.2.2.1) INTRODUCCIÓN DEL MODELO K-MEANS](#2221-introducción-del-modelo-k-means).
      - [2.2.2.2) MODELADO](#2222-modelado).
    - [2.2.3) MODELO GMM](#223-modelo-gmm).
      - [2.2.3.1) INTRODUCCIÓN MODELO GMM](#2231-introducción-modelo-gmm).
      - [2.2.3.2) MODELADO](#2232-modelado).
  
  
  ##
  ## 1 FASE DE ANÁLISIS
  ### 1.1) PROCEDENCIA DE LOS DATOS
  
  El programa Viking fue una de las misiones más ambiciosas lograda por EEUU.
  Dicho programa constaba de dos sondas, cada una de ellas formada por un orbitador y un módulo de aterrizaje. Ambas eran exactamente iguales, por ello que se las denominaran sondas gemelas.

  Para tratar sobre ellas, siempre que se muestren datos en parejas, la primera se referirá a Viking 1 y la siguiente a Viking 2.
  Los aterrizadores lograron aterrizar en lugares diferentes, una lo logró en agosto de 1975 y la siguiente en septiembre del año 1975 también.
  Su misión principal era lograr fotografías del terreno, obtener datos básicos que sirvieran para recopilar información y un conjunto de 3 experimentos biológicos.

  Todo estaba planeado para lograr recopilar datos suficientes a lo largo de 90 días tras el aterrizaje. 
  Al final, los orbitadores lograron transmitir datos hacia el planeta Tierra , una hasta el año 1980 y la otra hasta el 1978.
  Referente a los módulos de aterrizaje, la Viking 1 retransmitió datos a la Tierra hasta el año 1980, y la Viking 2 hasta el 1982.
  
  ### 1.2) ESTRUCTURACIÓN DE LOS DATOS Y ESTADÍSTICAS
  
  Todos los datos recopilados del proyecto Viking están en un servidor público perteneciente a la universidad de Washington y dados por  la NASA.
  El enlace que usaremos para descargar los archivos es:
  
  https://pds-geosciences.wustl.edu/missions/vlander/seismic.html.
  
   #### 1.2.1) ESTRUCTURA DE LOS ARCHIVOS
   Los archivos podremos encontrarlos en tres formatos diferentes: csv, lbl o tab.
   Los archivos csv son archivos comúnmente utilizados, separados los datos por columnas y con un separador común. En nuestro caso es la coma.
   Los archivos tab, es el otro tipo contenedor de datos, donde cada dato está separado por un número de bytes establecidos en el archivo lbl y éste cambiará según la columna y su contenido.
   El tercer tipo de archivo lbl, contendrá información sobre el documento al que referencia, que datos tiene de cada columna, en que byte empieza y en cual acaba, y el tipo de datos que contiene.
    
   ```ruby
	PDS_VERSION_ID           = PDS3
 
	RECORD_TYPE              = FIXED_LENGTH
	FILE_RECORDS             = 256087
	RECORD_BYTES             = 152
	^TABLE                   = "EVENT_WIND_SUMMARY.TAB"

	DATA_SET_ID              = "VL2-M-SEIS-5-RDR-V1.0"
	PRODUCT_ID               = "EVENT_WIND_SUMMARY"
	PRODUCT_CREATION_TIME    = 2016-12-12T00:00:00
	SPACECRAFT_NAME          = "VIKING LANDER 2"
	INSTRUMENT_NAME          = "VIKING LANDER 2 SEISMOLOGY EXPERIMENT"
	TARGET_NAME              = "MARS"
	START_TIME               = 1976-09-04T00:53:01
	STOP_TIME                = 1978-03-17T06:52:23
	SPACECRAFT_CLOCK_START_COUNT = "N/A"
	SPACECRAFT_CLOCK_STOP_COUNT  = "N/A"



	OBJECT                   = TABLE
	  INTERCHANGE_FORMAT     = ASCII
	  ROWS                   = 256087
	  ROW_BYTES              = 152
	  COLUMNS                = 24
	  DESCRIPTION            = "This file is a summary of the Viking Seismometer 
	    Data Event mode records, intended as a high-level index to events of 
	    interest, and for large-scale correlation with meteorological data.  
	    In Event mode, raw readings were compressed in the instrument itself 
	    by recording the number of positive-going zero crossings in a 1.01s 
	    interval, and recording an envelope value generated by digital filtering.
	    For details see VPDS_EVENT_WINDS_FORMAT.TXT in the DOCUMENT directory.
	    Time is Local Lander Time."

	  OBJECT                 = COLUMN
	    COLUMN_NUMBER        = 1
	    NAME                 = ARCHIVED_RECORD_NUMBER
	    DATA_TYPE            = ASCII_INTEGER
	    START_BYTE           = 1
	    BYTES                = 6
	    DESCRIPTION          = "An ordinal number indicating the record in 
	      the present file and in the corresponding archive files 
	      (VPDS_EVENT_XAMP.CSV etc.) Note that those files only carry the 
	      records with 51 readings, hence there are fewer records in the 
	      archive file than in the present summary."
	  END_OBJECT             = COLUMN
   
   ```

    

   #### 1.2.2) ESTRUCTURA DE LOS DATOS
     
   Los que nos interesarán en concreto será el high_wind_summary y el event_wind_summary.
   En ellos podremos encontrar las siguientes variables, tal y como describe su archivo lbl correspondiente:
	
   ***Variables temporales***:
   *	**SEISMIC_TIME_SOLS**: es una variable que engloba la escala de tiempo en soles decimales para datos sismográficos.
	Su ecuación es: sol+(hr*3600.0+min*60.0+sec) /88775.0
   *	**METEO_TIME_SOLS**: es una variable que engloba la escala de tiempo en soles decimales para datos meteorológicos.
	Su ecuación es: sol+(hr*3600.0+min*60.0+sec) /88775.0
   *	**DATA_ACQUISITION_SOL**: indica en que día marciano (sol) fueron adquiridos los datos, tomando como el sol 0 el día de aterrizaje.
   *	**DATA_ACQUISITION_HOUR**
   *	**DATA_ACQUISITION_MINUTE**
   *	**DATA_ACQUISITION_SECOND**
   *	**WIND_SEISMIC_INTERVAL**: tiempo en segundos transcurridos entre adquisición de datos de lectura del viento y datos sismográficos. Tomar unicamente cuando este valor sea positivo.


   ***Variables meteorológicas:***
   *	**WINDSPEED**: velocidad del viento en m/s.
   *	**PRESSURE**: presión atmosférica en mbar.
   *	**WIND_DIRECTION**: dirección del viento relativa al viento en grados.
   *	**AIR_TEMPERATURE**: temperatura del aire en kelvin.

   ***Variables sismográficas:***
   *	**FIRST_X_AXIS**: primera lectura tomada del sismografo en el eje X.
   *	**MEDIAN_X_AXIS**: La media de valores tomados en el eje X. Cada valor esta medido en digital unit (DU) y se corresponde a 2 nm tomados a 3Hz.
   *	**MAXIMUM_X_AXIS, MINIMUM_X_AXIS**: valor máximo y mínimo de las lecturas tomadas. Pueden ser tanto valores positivos o negativos, en el eje X.
   *	**RMS_X_AXIS_X100**: valor eficaz o valor cuadrático medio. Nos permite calcular la magnitud de unos valores discretos en valores positivos.
   *	**MEAN_X_AXIS_CROSSINGS**: La media de valores en los que la onda toma el valor 0 en el eje descrito. En este caso será la variable X.

   #### 1.2.3) LECTURA DEL DATASET E IMPORTACIÓN DE LIBRERÍAS
     
   Para empezar a analizar los datos, deberemos de leer dichos datos del dataset seleccionado. Empezaremos haciendo uso del archivo EVENT_WIND_SUMMARY.
   Debido al formato declarado anteriormente de los archivos tab y lbl, en Python no se pueden leer directamente por lo que hemos juntado ambos en un archivo csv.
   Lo primero será importar todas las librerías necesarias para nuestro proyecto en spark.

   Para la parte del entrenamiento del modelo KMeans, PCA 

   ```python
	from pyspark import SparkConf, SparkContext
	from pyspark.sql import SparkSession
	from pyspark.ml.clustering import KMeans
	from pyspark.ml.feature import VectorAssembler, PCA, StandardScaler

	import matplotlib.pyplot as plt
	import seaborn as sns; sns.set()
	import pandas as pd
	import prepro
	import string

	import time
   ```
   Para el servidor, que va a ser el que importe los modelos pre-entrenados:

   ```python
	from pyspark import SparkConf,SparkContext
	from pyspark.streaming import StreamingContext
	from pyspark.sql import SQLContext
	from pyspark.ml.feature import VectorAssembler, PCAModel, StandardScalerModel
	from pyspark.ml.clustering import KMeansModel
	
	import sys
	import requests
	import prepro
   ```

   Para el código del rover o cliente:

   ```python
	import socket
	import sys
	import requests
	import prepro
	import time
	import pandas as pd
	import numpy as np
   ```

   Una vez importadas las librerías en los respectivos archivos, leemos las cabeceras de los archivos .lbl con el código:
   
   
    
     
   #### 1.2.4) ESTADÍSTICAS BÁSICAS DE VARIABLES A ANALIZAR
   
   Sobre cada variable, hablaremos de la media, la desviación estandar, el mínimo, máximo y percentiles.
   
   ***Variables temporales***:
   *	**SEISMIC_TIME_SOLS**: Podemos ver que los valores mínimos están en 101 y los máximos en valores 1381 soles decimales.
	Observando los percentiles podemos decir que los valores están distribuidos por la normal de forma uniforme.
	
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/1.png)
	
   *	**METEO_TIME_SOLS**: es una variable que engloba la escala de tiempo en soles decimales para datos meteorológicos.
	
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/2.png)
   *	**WIND_SEISMIC_INTERVAL**: En la documentación se expone que los valores en las ultimas tomas y en las primeras tomas del dataset, no tenía que tenerse en cuenta debido a que los valores eran excesivos.
	Esto hace que la media y la desviación estándar inicial no pueda usarse.
   	
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/3.png)

   ***Variables meteorológicas:***
   *	**WINDSPEED**:La velocidad del viento varía entre 0 m/s hasta los 531 m/s. Este valor no tiene sentido. Por lo que seguramente nos tocará hacer una limpieza inicial de valores.
        Viendo los percentiles, hasta un 75% de los datos tomados están por debajo de los 5m/s, valores con vientos de valor bajos – medios.
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/4.png)
   *	**PRESSURE**: La presión irá desde los 0 milibares hasta los 10,7.
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/5.png)
   *	**WIND_DIRECTION**: dirección del viento relativa al viento en grados, de 0º a 360º.
   *	**AIR_TEMPERATURE**: temperatura del aire en kelvin, desde los 50k hasta los 337k.
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/6.png)

   ***Variables sismográficas:***
   *	**RMS_X_AXIS_X100**: Debido a que los valores van desde unos -130 hasta +130, usaremos el RMS para sacar una magnitud de dichos valores. 
   	  Sus estadísticas por tanto son:
	  Podemos observar que van desde 0 DU hasta 12700 DU.
Tal y como muestran los percentiles, tomaremos en cuenta hasta unos 350 DU. Los mayores serán valores sin sentido o no concluyentes.

   *	**MEAN_X_AXIS_CROSSINGS**: Se puede ver que irá desde 0 hasta los 31. Cuanto más rápido oscile la onda, mayor será el número de pasos por 0.
	Este tipo de valores puede usarse para el estudio sonoro de fondo para la detección de sonidos, estructuras o efectos en tiempos discretos.
	
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/7.png)
   
### 1.3) AGRUPACIÓN DE DATOS
  
#### 1.3.1) NORMALIZACIÓN DEL DATASET
 
Nuestro dataset tiene variables que describen efectos diferentes. Cada una tomará una distribución diferente de datos. 
Para que todas escalen entre los mismos valores, usaremos la normalización o estandarización.
Para hacerlo en Python:

 ```python
	#df_norm = (fd -fd.min()) / (fd.max() - fd.min() )
	df_norm = StandardScaler().fit_transform(fd.astype(float))
	df_norm = pd.DataFrame(df_norm, columns=fd.columns)
   ```

#### 1.3.2) MATRIZ DE CORRELACIÓN
  
Trataremos de encontrar relaciones lineales entre pares de variables, dejando en dichos pares las demás variables como constantes.
Esto nos permitirá encontrar relaciones y grupos entre variables.

Debido a que en el modelo de clustering todas las variables de entrada tendrán que ser independientes, deberemos de encontrar grupos en primer lugar para quitar la dependencia entre esas variables.
Para todo esto haremos uso de las matrices de correlación.

Cada valor tomará valores decimales entre -1 y 1.
Cuando más se acerque a 0, menos relación lineal habrá entre variables.
Cuando más se acerque a -1, mas relación inversa habrá entre variables (Al aumentar una, disminuye la otra), y cuando más se acerque al 1, el caso contrario.

Podremos realizarlas en Python con:

  ```python
	f, ax = plt.subplots(figsize=(20,20))
	corr=df_norm.corr()
	sns.heatmap(corr, square=True , cmap=sns.diverging_palette(220, 20, as_cmao=True), ax=ax , annot = True
   ```
  
#### 1.3.3) ANÁLISIS DE CORRELACIONES LINEALES ENTRE VARIABLES


El resultado será el siguiente gráfico:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/8.png)


Es una tabla bastante amplia, pero la usaremos únicamente como visión general a la hora de hacer los grupos.
Tomaremos los valores como correlacionados fuertemente como 1.0.5 y -0.5…-1, una correlación débil entre 0.3 … 0.5 y -0.5 … -0.3 y sin correlación hasta el 0.


Correlaciones de variables meteorológicas:
		
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/9.png)


Podemos ver que hay una relación inversa entre la temperatura y la presión en un rango de correlación alto.
También hay una relación directa entre la presión y la variable temporal de adquisición de datos meteorológicos. 
Habría que discutir más adelante si introducir las variables temporales en el modelo, ya que las variables al fin y al cabo varían según este, pero no todas de forma lineal como lo hace la presión, por lo que puede sesgar el modelo.
	
De este conjunto agruparemos únicamente la presión y la temperatura, sin tener 
en cuenta la variable temporal.


Correlaciones de variables temporales:

Debido a que son escalas temporales, la de segundos, minutos, horas y soles serán independientes entre ellas pero serán dependientes sobre todo de METEO_TIME_SOLS y de SEISMIC_TIME_SOLS debido a que se crean a partir de las mismas.


Correlaciones de variables sismográficas:
		
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/10.png)

Recordemos que el sismógrafo toma lecturas en tres ejes, eje X, eje Y, eje Z. 
Se ve muy claramente que todas las variables están relacionadas entre ellas fuertemente, y que el valor del viento también les afecta.
Esto quiere decir que los valores del viento afectan de forma lineal a los valores tomados del sismógrafo.
		

#### 1.3.4) AGRUPACIÓN DE VARIABLES COMO GRUPOS INDEPENDIENTES

Una vez hecho el estudio de correlaciones, dividiremos el dataset en pequeños subgrupos.
Todas las variables dentro de cada subgrupo estarán dentro de un grado de correlación, relacionada entre ellas.
Cada uno de los subgrupos serán independientes entre ellos.
Como un modelo solo puede tener de entrada variables independientes, aplicaremos PCA a cada subgrupo de variables dependientes para dejarlo en una sola variable.
En Python referenciaremos a dichas variables con:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/11.png)


### 1.4) VARIABLES NO CORRELACIONADAS LINEALMENTE

Para tratar sobre la atmósfera de Marte y poder analizarla, deberemos de considerar ciertos valores como la temperatura, la presión y la velocidad del viento.

El aire, el cual está formado de materia y gases, que compone la atmósfera ejerce una presión sobre los objetos de la superficie. Cuanto más pese el aire, más presión ejercerá sobre la superficie. A esta presión se la denomina presión atmosférica, y se mide a partir de un barómetro. Sus unidades de medición pueden ser en bares o en pascales entre otras.
Dicha presión atmosférica disminuye al aumento de altitud, la humedad y la temperatura. 
Al variar esta presión atmosférica se produce las corrientes de aire. Esto es debido a que al ejercer el aire más peso en un lugar que en otro, hace que exista un movimiento de materia y gases en la atmósfera, produciendo en tanto una corriente.

En Marte, la presión atmosférica es muy baja. Unas 120 veces más baja que la de la Tierra. Por ello que se necesite una mayor velocidad de viento para poder levantar polvo. Aunque en la Tierra se necesite una velocidad de unos 50/60 km/h, en Marte se necesitará unos 150-200 km/h. Esto también afecta en gran modo a las vibraciones sobre el módulo.
Surge una duda entonces de todo, ¿Cómo puede ser que exista velocidades de viento tan altas con una presión tan baja en Marte?
Esto es debido a esas variaciones tan grandes de temperaturas al día, ya que pueden varias de unos 10ºC a -100ºC al día.
Tras todo esto, aunque aparezcan que el viento sea independiente de la presión y la temperatura en el estudio de correlaciones, están relacionadas de una forma no lineal.
Lo mismo ocurre con las variables temporales.

Estas relaciones no lineales no afectarán en principio al entrenamiento del modelo, aunque estarán metidas de forma indirecta.

## 2 FASE DE MODELADO
  ### 2.1) REDUCCIÓN DE VARIABLES DEPENDIENTES A INDEPENDIENTES
  #### 2.1.1) INTRODUCCIÓN PCA
  La funcionalidad de aplicar PCA o análisis de componentes principales es describir las características de un conjunto de variables y reducirlas a un conjunto de variables no correlacionadas de dimensiones menores.

  Debido a que para entrenar un modelo no supervisado deberán ser todas sus variables de entrenamiento independientes, deberemos de aplicar a cada subgrupo hecho anteriormente PCA.

  #### 2.1.2) APLICACIÓN PCA SOBRE CADA GRUPO DE VARIABLES DEPENDIENTES

Vamos a crear los grupos y a agruparlos en una sola columna.
```python
# Grupo 1 -> Magnitud del sismogrado y la velocidad del viento correlacionadas
sisms = ['RMS_X_AXIS_X100', 'WINDSPEED']

# Grupo 2 -> Presion y temperatura atmosferica correlacionadas
pre_temp = ['PRESSURE', 'AIR_TEMPERATURE']

# Variables independientes entre si 
indep = ['MEAN_X_AXIS_CROSSINGS', 'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

#Agrupamos los datos segun las cabeceras inputCols en una unica columna outpuCol
assembler = VectorAssembler(inputCols=sisms, outputCol='sisms')
df = assembler.transform(df)

assembler = VectorAssembler(inputCols=pre_temp, outputCol='pre_temp')
df = assembler.transform(df)

assembler = VectorAssembler(inputCols=indep, outputCol='indep')
df = assembler.transform(df)
```

Una vez tenemos cada grupo de variables en una sola columna, podemos proceder a estandarizar los datos de cada uno de los grupos.
El modelo de escalado lo guardamos, ya que lo tendremos que utilizar en un futuro para predecir nuevos datos.
```python
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
```
Finalmente procedemos a aplicar PCA a los dos primeros grupos, para dejarlos como una única variable.
En el dataframe final tendremos todos los datos originales, junto con las variables con PCA y la estandarizacion ya aplicadas.

### 2.2) MODELOS DE CLASIFICACIÓN NO SUPERVISADOS
  #### 2.2.1) INTRODUCCIÓN MODELOS NO SUPERVISADOS
Los modelos no supervisados permiten buscar patrones entre los datos que tenemos, sin la necesidad de que estos estén etiquetados. Como solo tenemos los datos de entrada y no datos de salida utilizar este tipo de modelo tiene como finalidad describir la estructura de los datos para encontrar algún tipo de organización que simplifique el análisis.

Estos algoritmos también suelen tomar el nombre de algoritmos de clustering, ya que intentan formar grupos (clusters) a partir de los datos con características similares.
  #### 2.2.2) MODELO K-MEANS
  ##### 2.2.2.1) INTRODUCCIÓN DEL MODELO K-MEANS
K-Means es uno de los algoritmos de clustering más populares. Intenta dividir unos datos en k grupos, siendo k un número seleccionado por el usuario, en el cual cada observación pertenece al grupo con la media más cercana.

El algoritmo funciona de la siguiente manera: 
- Se inicializan los centros de los clusters, por ejemplo, de manera aleatoria.
- Se hacen varias iteraciones de lo siguiente: Se asigna a cada punto los centroides, cada dato al que tenga más cercano. Una vez hecho esto, se actualizan los centroides calculando la posición promedia de todos los elementos en ese grupo. 
- Se repite este último paso haya que los centroides apenas se muevan, es decir, se haya alcanzado el resultado óptimo.

Es un algoritmo muy costoso computacionalmente, con una complejidad de O(n^2). Además, por la forma en la que se implementa, requiere comunicación constante entre nodos, lo cual lo hace difícil de paralelizar. Sin embargo, no es imposible, y Spark implementa en su librería una versión paralelizable de este algoritmo.

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/12.png)

Este gráfico muestra una la mejora experimentada gracias a utilizar una versión paralelizable, en el que se observa que la mejora no es especialmente grande por el problema discutido anteriormente, pero sí bastante significante.

  ##### 2.2.2.2) MODELADO
Para poder modelar con K-means utilizando las librerias de machine learning que nos proporciona Spark, primero tenemos que agrupar todos los datos de entrenamiento en una columna features.

```python
assembler = VectorAssembler(
    inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
    outputCol='features')

trainingData = assembler.transform(df)
```

A continuación vamos a hacer un bucle que cree el modelo con distintos números de grupos para observar cuál produce un resultado más correcto sin sobreajustarse a los datos.
Como no tenemos la posibilidad de validar los datos, utilizamos todos los que tenemos para entrenar.
```python
#Bucle para probar con distinto numero de grupos
for i in range(3, 8):
	#Entrenamos el modelo de Kmeans con un numero de grupos igual a i
	kmeans = KMeans().setK(i)
	model = kmeans.fit(trainingData)

	#Computamos el coste del modelo
	wssse = model.computeCost(trainingData)

	#Guardado del modelo
	model.write().overwrite().save('model/KM' + str(i) + '.model')

	#Añadimos el coste a los arrays
	computingCostIndex.append(i)
	computingCost.append(wssse)
```
Como se puede observar en el código, otra de las cosas que hemos hecho es guardar este modelo para futuras predicciones, y añadirlo a unos arrays que utilizaremos para generar gráficas sobre el error según el número de grupos. A continuación clasificamos sobre el mismo dataset con el que hemos entrenado, y guardamos las estadísticas de cada grupo en un documento, para poder analizarlo luego.
```
	transformed = model.transform(trainingData)

	describe = transformed
	for j in range (i):
		describeGrouped = describe.filter(describe.prediction == j)
		describeGrouped = describeGrouped.describe()
		describeGrouped.write.option("header", "true").csv("describe/describe_kmeans_" + str(i) + "/precition_" + str(j) + ".txt", mode="overwrite")

```
Por último, vamos a generar gráficos que nos permitan visualizar cómo se han dividido los grupos. Esta operación es costosa ya que no está paralelizada.
```python
    #Transformamos el dataframe de spark a un dataframe de pandas para poder representarlo
	pdDF = transformed.toPandas()

	#Creamos varios graficos que ilustren los grupos formados y los guardamos
	plt.figure()
	sns_fig = sns.scatterplot(x=pdDF['RMS_X_AXIS_X100'], y=pdDF['SEISMIC_TIME_SOLS'], hue=pdDF['prediction'], linewidth=0, alpha = 0.7, palette=color_dict, legend=False)
	plt.savefig("images/KM" + str(i) + "_rms_sols.png")
```

#### 2.2.3) MODELO GMM

##### 2.2.3.1) INTRODUCCIÓN MODELO GMM

El modelo GMM o modelo de mezcla Gaussiana es un modelo probabilístico en el que todos los puntos de datos se generan a partir de un número finito de distribuciones gaussianas. La finalidad de usar este tipo de modelos es aproximar o estimar a partir de sus componentes encontrando una similitud respecto a los datos que contiene las componentes.

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/13.png)
			Ejemplo de uso de GMM a partir de dos componentes.

##### 2.2.3.2) MODELADO

```python
   #agregamos la columna
   trainingData = assembler.transform(df)
   
   log = open("log.txt", "a+")
   #Entrenamos el modelo de mezcla gaussiana
   for i in range (3, 8):
   	gmm = GaussianMixture().setk(i)
   model = gmm.fit(trainingdata)
```

### 3.1) GENERACIÓN Y ENVÍO DE DATOS
La generación de datos la haremos basadas en las distribuciones normales de cada columna en el dataset original. Para ello, primero vamos a coger las columnas que nos interesan del dataset de la misión Viking y a calcular la media y la desviación típica de estas columnas. 
```python
#Devuelve un array con la media y otro con la desviacion tipica de cada columna
def getNormalDist(df):
    mean = df.mean() #Media
    std = df.std() #Desviacion tipica
    return mean, std

#Cogemos solo las variables con las que se ha entrenado el modelo
trainVar = ['RMS_X_AXIS_X100', 'WINDSPEED', 'PRESSURE','AIR_TEMPERATURE', 'MEAN_X_AXIS_CROSSINGS', 
            'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

df = df[trainVar]

#Cogemos las carasteristicas
mean, std = getNormalDist(df)
```
Ahora tenemos que generar los datos. Esto lo haremos con números aleatorios independientes, los cuales generaremos en una distribución normal para cada variable. En codigo lo haremos con la siguiente función:
```python
def generaDatosSimulados(df, mean, std, numValues):  
    df_simulado = pd.DataFrame()
    headers = df.columns; 

    for i in range(8):
        data = np.random.randn(numValues)
        values = data * std[i] + mean[i]
        values = np.where(values < 0, 0, values)

        df_simulado[headers[i]] = values

    return df_simulado
```
Como todos los datos deben ser positivos, los datos que haya generado negativos los pasa a valor absoluto. Además, esta forma de generar los datos no tiene en cuenta las correlaciones complejas entre ellos, como la que habría entre RMS_X_AXIS_X100 y WINDSPEED. Estas dos cosas se podrían mejorar para crear un simulador más fiel a los datos reales. Sin embargo, no creemos necesario realizarlo inmediatamente ya que sólo van a ser datos de simulación que sirvan para comprobar que el procesamiento a tiempo real funciona.

Vamos ahora a establecer una conexión por TCP en el puerto 9012. Una vez esté establecidad, comenzará a enviar datos indefinidamente en intervalos regulares.
```python
#Abrimos una conexion TCP por el puerto 9012 
TCP_IP = "localhost"
TCP_PORT = 9012
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting sending data.")

# Una vez establecida la conexion, empezamos a generar datos y a enviarselos al servidor
while 1:
    # Generamos datos de 10 en 10 
    df_simulado = generaDatosSimulados(df, mean, std, 10)
    data = df_simulado.to_string(index=False, header=False)
    # Enviamos los datos al servidor
    send_data_to_spark(data,conn)
    # Esperamos un tiempo hasta la proxima generacion 
    time.sleep(10)
```
### 3.2) RECEPCIÓN Y CLASIFICACIÓN DE DATOS
El servidor que se encarga de capturar los datos de una conexión TCP y de clasificarlos va a utilizar Spark. Esto le permitiría trabajar de forma distribuida y con cargas de trabajo muy superiores a la que le someteremos en la simulación.




