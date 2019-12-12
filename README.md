
# ANALISIS DE DATOS SISMOGRÁFICOS PROCEDENTES DE LA MISIÓN VIKING
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)
![Spark](https://img.shields.io/badge/spark-v2.4.4+-blue.svg)
![Contributors](https://img.shields.io/badge/contributors-3-orange)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
![Hi](https://img.shields.io/badge/last%20commit-december%202019-yellow)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

### SOBRE NOSOTROS

```
	Trabajo realizado por: 
	*	Gabriel García García        : gabgarar@gmail.com   			github@gabgarar
	*	Miguel Ángel Castillo Moreno : miguelangelcastillomoreno98@gmail.com	github@Miguel-ACM
	*	Jorge García Cerros          : jorgecrrs98@hotmail.com			github@JorgeGCrrs	
```
		
## INDICE
- [INTRODUCCIÓN](#introducción).
- [ 1) FASE DE ANÁLISIS](#1-fase-de-análisis).
  - [1.1) PROCEDENCIA DE LOS DATOS](#11-procedencia-de-los-datos).
  - [1.2) ESTRUCTURACIÓN DE LOS DATOS Y ESTADÍSTICAS](#12-estructuración-de-los-datos-y-estadísticas).
    - [1.2.1) ESTRUCTURA DE LOS ARCHIVOS](#121-estructura-de-los-archivos).
    - [1.2.2) ESTRUCTURA DE LOS DATOS](#122-estructura-de-los-datos).
    - [1.2.3) LECTURA DEL DATASET](#123-lectura-del-dataset-e-importación-de-librerías).
    - [1.2.4) ESTADÍSTICAS BÁSICAS DE VARIABLES A ANALIZAR](#124-estadísticas-básicas-de-variables-a-analizar).
  - [1.3) AGRUPACIÓN DE DATOS](#13-agrupación-de-datos)
    - [1.3.1) NORMALIZACIÓN DEL DATASET](#131-normalización-del-dataset).
    - [1.3.2) MATRIZ DE CORRELACIÓN](#132-matriz-de-correlación).
    - [1.3.3) ANÁLISIS DE CORRELACIONES LINEALES](#133-análisis-de-correlaciones-lineales).
    - [1.3.4) AGRUPACIÓN DE VARIABLES COMO GRUPOS INDEPENDIENTES](#134-agrupación-de-variables-como-grupos-independientes).
  - [1.4) VARIABLES NO CORRELACIONADAS LINEALMENTE](#14-variables-no-correlacionadas-linealmente)
  
- [ 2) FASE DE MODELADO](#2-fase-de-modelado).
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
    - [2.2.4) ANÁLISIS DE RESULTADOS](#224-análisis-de-resultados)
      - [2.2.4.1) ANÁLISIS DEL VIENTO CUANDO ES MENOR A 1 M/S](#2241-análisis-del-viento-cuando-es-menor-a-1-ms).
      - [2.2.4.2) ANÁLISIS DEL VIENTO CUANDO ES MENOR A 50 M/S](#2242-análisis-del-viento-cuando-es-menor-a-50-ms).
      - [2.2.4.3) CONCLUSIONES FINALES Y PARA FUTURO](#2243-conclusiones-finales-y-para-futuro).
- [ 3) FASE DE CLASIFICACIÓN A TIEMPO REAL](#3-fase-de-clasificación-a-tiempo-real).
  - [ 3.1) GENERACIÓN Y ENVÍO DE DATOS](#31-generación-y-envío-de-datos).
  - [ 3.2) RECEPCIÓN Y CLASIFICACIÓN DE DATOS](#32-recepción-y-clasificación-de-datos).
- [ 4) PRUEBAS DE RENDIMIENTO](#4-pruebas-de-rendimiento).
  - [ 4.1) RENDIMIENTO LOCAL](#41-rendimiento-local).
  - [ 4.2) RENDIMIENTO EN AWS](#42-rendimiento-en-aws).
- [ 5) CÓMO EJECUTAR EL CÓDIGO](#5-cómo-ejecutar-el-código).
  - [ 5.1) ENTRENAMIENTO DEL MODELO](#51-entrenamiento-del-modelo).
  - [ 5.2) CLASIFICACIÓN A TIEMPO REAL](#52-clasificación-a-tiempo-real).

## INTRODUCCIÓN


El propósito clave de nuestro proyecto es un clasificador a tiempo real de datos procedentes de un rover u otra sonda espacial.
Esto se logrará con un cliente TCP(sonda que toma muestras)y un servidor TCP(el que se encargará de recibir los datos y clasificarlos en tiempo real). 
	
Para todo ello dispondremos el proyectos en diferentes fases. 
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
* La **fase 3** del proyecto será **preparar el cliente y el servidor**:
	* Cliente:
		- Como establecer la conexión.
		- Como preparar los datos simulados para envíar.
	* Servidor:
		- Como establecer la conexión
		- Como importar el modelo
		- Como tratar la entrada de datos
		- Como categorizar en tiempo de flujo real
  
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
	from pyspark.sql.functions import udf
	from pyspark.sql.types import StringType

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
Este sería un ejemplo de normalización en Python, aunque para spark utilizaremos la estandarización que veremos en el punto [2.2.2.2](#2222-modelado):

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
  
#### 1.3.3) ANÁLISIS DE CORRELACIONES LINEALES


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

## 2) FASE DE MODELADO

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

Para modelar usando GMM debemos incluir la siguiente librería

```python
   from pyspark.ml.clustering import GaussianMixture
```

A continuación vamos a hacer un bulce en el que se creará varios modelos para GMM y los entrenaremos para posteriormente ver los resultados obtenidos de dicho entrenamiento.

```python
   #agregamos la columna
   trainingData = assembler.transform(df)
   
   log = open("log.txt", "a+")
   #Entrenamos el modelo de mezcla gaussiana
   for i in range (3, 8):
   	gmm = GaussianMixture().setk(i)
  	model = gmm.fit(trainingdata)
	
   transformed = model.transform(trainingData)
```
Para mostrar el gráfico generado se hará de la misma manera con la que se genera el grafico en el modelo de K-Means en el apartado [2.2.2.2](#2222-modelado).

  #### 2.2.4) ANÁLISIS DE RESULTADOS:

**Hay que tener especial cuidado en:**
Cada vez que entrenas el modelo de KMeans, los grupos serán los mismos pero la enumeración cambiará.
En este análisis, cuando me refiera por ejemplo al TAG 0, tendremos que fijarnos sobre los siguientes gráficos y tablas dadas durante el punto 2.2.4).

El análisis de resultados lo haremos en función del viento. Lo que queremos encontrar son patrones entre las lecturas del sismógrafo y la velocidad del viento junto a otras variables.

  ##### 2.2.4.1) ANÁLISIS DEL VIENTO CUANDO ES MENOR A 1 M/S
Empecemos analizando los resultados de nuestro algoritmo de clustering cuando la velocidad del viento sea menor que 1m/s. Veamos como se comporta el sismógrafo cuando no existe.

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/graph_less1.PNG)

Podemos comprobar que los TAGs 0,1 y 3 se mantienen constantes, mientras que el 2, en color cyan, son los valores anormales.
Respecto a las estadísticas básicas,en la siguiente tabla tenemos en la parte superior estadísticas, y en la inferior el número de lecturas de cada categoría.

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/ests_less1.PNG)

**Observaciones**
*	TAGS 0,1 y 3, tienen estadísticas similares
*	Velocidad del viento y los cruces ceros se mantienen constantes en todos los grupos
*	Cuanto menor presión atmosférica , mayor temperatura del aire
*	Cuanto menor presión y mayor temperatura del aire, mayor lecturas del sismógrafo. Esto se ve en los TAGs 1 y 2. 
*	En cuanto al número de lecturas, vemos que el algoritmo tiene en cuenta sobre todo, el RMS_X a la hora de clasificar.

  ##### 2.2.4.2) ANÁLISIS DEL VIENTO CUANDO ES MENOR A 50 M/S

En el siguiente gráfico, pueden verse mucho mejor la influencia del viento en los datos del sismógrafo. Tomando forma en mariposa, donde a mayor velocidad del viento, todos los datos se acaban volviendo de color cyan.

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/graph_less2.PNG)

Para analizarlo, como antes usaremos sus estadísticas.
Viendo la siguiente tabla:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/ests_less2.PNG)

**Observaciones**
*	Las estadísticas se mantienen iguales al analisis de velocidad de viento nulo.
*	La velocidad del viento y los cruces ceros siguen manteniéndose constantes.
*	Cuanto menor presión del aire, sigue estando una mayor temperatura
*	En el TAG 2, donde las lecturas del sismógrafo son mayores, la media de la velocidad del viento también aumenta respecto a los 	demás.

  ##### 2.2.4.3) CONCLUSIONES FINALES Y PARA FUTURO

Según los datos anteriores, podemos entonces tomar como datos fiables todos los TAGs 0, 1 y 3 para futuras misiones y como no fiables el TAG 2, ya que necesita un análisis posterior.

Debido a que la cantidad de TAG 2 son alrededor de 20.000 lecturas, en un futuro podríamos estudiarlo con spark.
Para hacer el modelo mas sencillo, y sacar conclusiones sobre estos datos, esta parte lo haremos con python.
El proceso es el mismo que el anterior, unicamente que tomamos como dataset de entrada los valores de TAG 2, y le aplicamos nuevamente un algortimo de clustering de 3 grupos.

El código para lograrlo será:
``` python
pr = fd[fd.TAG_KM == 2]
pr_norm = StandardScaler().fit_transform(pr.astype(float))
pr_norm= pd.DataFrame(pr_norm, columns=pr.columns)

# Indicamos el numero de columnas que tiene que salir 
sklearn_pca = sklearnPCA(n_components=1)

# Aplicamos PCA para los dos conjuntos que hemos hecho a partir de analisis de correlaciones
datos_pca_gp_1_pr = sklearn_pca.fit_transform(pr_norm[gp_1])
datos_pca_gp_2_pr = sklearn_pca.fit_transform(pr_norm[gp_2])

# Unimos para formar el dataset de entrenamiento del algoritmo de clustering

core_pr = pr_norm[gp_3]; 
core_pr['sismo'] = datos_pca_gp_1_pr; 
core_pr['pre_temp'] = datos_pca_gp_2_pr; 
core_pr[core_pr == np.nan].count()

# Entrenamos el modelo
model_kmeans_pr = KMeans(n_clusters=3).fit(core_pr)

# Sacamos los centroides
centroids_pr = model_kmeans_pr.cluster_centers_

# Sacamos los tags del dataset
labels_pr = model_kmeans_pr.predict(core_pr)

pr["TAG_KM"] = labels_pr; 
```

Una vez tenemos el dataset con los labels o TAG, unicamente será mostrar los resultados en forma de gráfica y de estadísticos.

El gráfico general de los 3 TAGs será:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/graph_less3_1.PNG)

Donde puede apreciarse muy bien que tanto los colores verdes y rojos son predominantes.
PAra visualizar el cyan de mejor forma:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/graph_less3_2.PNG)

Y los estadísticos:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/describes/ests_less3.PNG)

Por tanto, el TAG 0 y 1, serán datos no fiables finales.
El TAG 2, dada las estadísticas, tiene una velocidad del viento bastante pequeña, un RMS alto y una media de X Crossing bajo también.
Esto puede ser un posible evento.


  ## 3) FASE DE CLASIFICACIÓN A TIEMPO REAL
  ### 3.1) GENERACIÓN Y ENVÍO DE DATOS
Debido a que el número de datos que tenemos recopilados son limitados, deberemos de crear mediante distribuciones un dataset cuyo uso será simular un flujo de datos dinámico entre el cliente y el servidor para su posterior tratamiento.
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
Crearemos una función, la cual será usada por el cliente o rover para generar numValues datos.
Haremos uso de la unidad tipificada para generar datos a través de la desviación típica y la media.

Por ello,en el siguiente código generamos numValues datos entre 0 y 1. Una vez tenemos esto, sabemos que la desviación típica por definición nos indica en que magnitud suelen variar los datos de una variable. Multiplicando los datos z(0,1) * std tendremos las desviaciones.
Como los datos ahora están centrados en el valor 0, solo queda sumarle la media mean .
Así ya tenemos numValues datos situados en una media con una desviación std.

values = z(0,1) * std + mean 
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
Aquí surgen dos problemas:

*	¿Se mantienen las correlaciones entre variables?
* 	¿Pueden haber valores negativos?

Como se generan datos de cada variable de forma independiente, sin tener en cuenta las demás, las correlaciones que teníamos anteriormente las perdemos.
Esto es un problema, ya que esas relaciones que antes buscábamos entre variables ya no están. Esto nos afectaría si quisieramos aplicar este dataset como dataset de entrenamiento, pero no es el caso.

Referente al segundo punto, como todos los datos deben ser positivos, los datos que haya generado negativos los pasa a valor absoluto. 

En nuestro modelo, todo el flujo de datos será en formato TCP.
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

La recepción será por parte del servidor, que capturará las tramas y las irá clasificando con el modelo ya entrenado, como se ha visto anteriormente.
Una vez configurada las variables de contexto, el código de recepción de datos será:
```python
# Recibira datos cada 10 seg
ssc = StreamingContext(sc, 10)

# Guarda la sesion en caso de fallo
ssc.checkpoint("checkpoint_SismographStream")

# Leemos los datos del puerto 9012 por direccion localhost
dataStream = ssc.socketTextStream("localhost",9012)

#Indicamos lo que hacemos sobre cada rdd de datos
dataStream.foreachRDD(process_rdd)

ssc.start()

ssc.awaitTermination()
```

Ahora deberemos de indicar, que haremos por cada rdd, para ello:

El proceso es muy similar a la parte de entrenamiento del modelo, unicamente que ahora hay que importarlo y usarlo

Lo primero como siempre es arreglar el formato entre linea y linea de datos, por ello:

```python
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
```
Ahora cargamos los modelos tres modelos que entrenamos antes, uno para las variables de rms y viento, otra para presión y temperatura y la última para aquellas independientes, y los aplicamos a los datos.
Para ello:
```python
 #Cargamos el modelo de estandarización entrenado anteriormente para cada grupo
scaler = StandardScalerModel.load('model/KMScalerSisms.scaler')
df = scaler.transform(df)

scaler = StandardScalerModel.load('model/KMScalerPreTemp.scaler')
df = scaler.transform(df)

scaler = StandardScalerModel.load('model/KMScalerIndep.scaler')
df = scaler.transform(df)
```
Ahora ya tenemos los datos de entrada estandarizados, deberemos aplicarles PCA, para reducir variables en este caso de entrenamiento ( Aunque las entradas ya sean linealmente independientes entre si, el modelo fue entrenado con menos variables que las entradas).
Por ello, importaremos el modelo entrenado de PCA y lo aplicamos:
```python
#Cargamos el modelo entrenado de PCA con los datos reales de la mision para aplicar PCA sobre simulados

# Aplicamos pca sobre los datos de RMS y WINDSPEED
pca = PCAModel.load('model/KMPCAsisms.PCA')
df = pca.transform(df)

# Aplicamos pca sobre los datos de PRESSURE y AIR_TEMPERATURE
pca = PCAModel.load('model/KMPCApreTemp.PCA')
df = pca.transform(df)
```
Una vez tenemos los datos, seleccionamos que variables servirán como entrada del modelo y la variable salida del modelo de kmeans( en este caso será features).
Para ello:
```python
assembler = VectorAssembler(
	inputCols=['sismsNormPCA', 'pre_tempNormPCA', 'indepNorm'],
	outputCol='features')

#Agregamos la columna features al dataFrame -> Esta variable es la única que toma el modelo de K-Means para entrenar
df = assembler.transform(df)
```
Hasta este momento, todo se ha volcado sobre df.
Cargamos el modelo de KMeans y lo aplicamos a los datos que ya tenemos
```python
# Cargamos el modelo de KMeans entrenado con los datos reales de la mision
kmeans = KMeansModel.load('model/KM4.model')

# Categorizamos los datos df['features']
dfTransformed = kmeans.transform(df)
```
Y listo.

  ## 4) PRUEBAS DE RENDIMIENTO
Vamos a hacer algunas pruebas de rendimiento sobre la genración del modelo de k-means, y todo el preprocesado que se debe hacer antes, viendo cómo de grande es la mejora por la paralelización.

El ordenador que se utiliza para las pruebas locales tiene las siguientes especificaciones:
 - Una máquina virtual de Ubuntu 18.04
 - Procesador Intel i5-6500K, 4 cores, 3.2 GHz.
 - Memoria de 8Gb, DDR4, 2033MHz

Lo que vamos a comprobar con estas pruebas, de forma precisa, es:
 
 - El tiempo que tarda en el preprocesado (Estandarización, combinación de columnas y PCA)
 - El tiempo que tarda en realizar k-means con 3, 4 y 5 grupos.

  ### 4.1) RENDIMIENTO LOCAL
La comparativa que vamos hacer en local es sencilla: Ver si utilizar más núcleos del procesador ofrece un resultado notable en el código. En el archivo spark/kmeans_classification.py utilizamos esta linea para utilizar todos los núcleos posibles (en este caso 4):
```python
	conf = SparkConf().setMaster('local[*]').setAppName('Clustering')
```
Mientras que utilizamos esta para que solo utilice un core:
```python
	conf = SparkConf().setMaster('local[1]').setAppName('Clustering')
```

Algunos gráficos para los resultados obtenidos son los siguientes:

Tiempo de preprocesado:

![Preprocessing.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/charts/graph2.PNG)

Tiempo de entrenamiento para un k-means con 4 grupos:

![Training.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/charts/graph3.PNG)
 
Como se puede comprobar, el tiempo que se tarda en hacer ambos procesos se reduce aproximadamente un 33%. Algo que se podría esperar si la paralelización fuese perfecta es que fuera una reducción del 75%, ya que hay 4 veces más hilos. Sin embargo, hay partes que no se pueden paralelizar y esto limita la mejora. Además, como se ha comentado anteriormente, el k-means es un algoritmo dificilmente paralelizable y en el que los hilos se tienen que comunicar constantemente entre sí, por lo que la paralelización siempre va a estar algo limitada.


  ### 4.2) RENDIMIENTO EN AWS

Ahora vamos a probar a ejecutar el modelo de entrenamiento de k-means en un cluster de Amazon Web Services. Para ello, vamos a utilizar 3 máquinas (1 master y 2 slaves) m4xlarge. Las especificaciones de estas máquinas son las siguientes:
 - Procesadores Intel Xeon® E5-2686 v4 (Broadwell) de 2,3 GHz o Intel Xeon® E5-2676 v3 (Haswell) de 2,4 GHz
 - 4 CPUs virtuales.
 - 16 GiB de memoria
 - Almacenamiento por EBS
 - 750 Mbps de ancho de banda de EBS dedicado
 - REndimiento de red "alto"

Creamos un cluster de ElasticMapReduce con las 3 máquinas descritas y la siguiente configuración de software:

![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/utils/AWSsoftwareConfig.png)

Respecto a los cambios en el código, estos son mínimos para poder utilizarlo en el cluster. Subiríamos la carpeta nasa junto a la carpeta spark al servidor master, y en el archivo kmeans_classification.py cambiariamos la siguiente linea:
```python
#Cogemos los datos del archivo
RDDvar = sc.textFile("../nasa/event/event_wind_summary/event_wind_summary.tab")
```
Por esta:
```python
#Cogemos los datos del archivo
RDDvar = sc.textFile("event_wind_summary.tab")
```
Esto se hace porque spark va a cargar el fichero que contiene los datos del sistema de ficheros de hadoop. Es por ello por lo que tenemos que ejecutar la siguiente sentencia (desde la carpeta nasa/event/event_wind_summary) para subir el archivo y que pueda encontrarlo:
```bash
hadoop fs -put event_wind_summary.tab event_wind_summary.tab
```
Otras cosas que hay que hacer antes de ejecutar son:
- Instalar seaborn en el master. No hace falta instalarlo en los slaves ya que la generación de los gráficos no está paralelizada. Podemos hacerlo con:
```bash
sudo pip --python-version 3.6 install seaborn
```
- Asegurarnos de que Spark va a utilizar la versión 3.6 de python. Podemos hacerlo con:
```bash
export PYSPARK_PYTHON=/usr/bin/python3.6 
```
Con esto hecho, ya podemos ejecutar el código, que generará en master las imágenes en la carpeta spark/images, y los modelos y describes en el sistema de ficheros de hadoop. La ejecución se realiza con:
```bash
spark-submit --num-executors 2 --executor-cores 4 kmeans_classification_cluster.py 
```
 
Los siguientes gráficos muestran los resultados obtenidos:
 
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/charts/cluster.png)
![Describe.](https://github.com/gabgarar/NASA---Mision-Vikings/blob/master/images/charts/local.png)

Como se puede observar, los resultados de cluster son *peores* que los obtenidos en local. Todos los procesos tardan aproximadamente 5 segundos más. Esto se debe probablemente al tamaño pequeño del dataset, de tan solo 40Mb. Al ser tan pequeño, el sobrecoste de las comunicaciones entre las máquinas es mayor que la acelaración que se produce al tener mayor número de procesadores. Esto es especialmente cierto para el proceso de kmeans, ya que la comunicación entre las máquinas es constante, y sin un dataset grande no se obtienen mejoras de rendimiento notables.

  ## 5) CÓMO EJECUTAR EL CÓDIGO
A continuación proponemos la manera de ejecutar el código obtenido tras el análisis para obtener los gráficos y los datos que hemos obtenido, junto a la simulación a tiempo real.

  ### 5.1) ENTRENAMIENTO DEL MODELO
Para poder ejecutar el código, tenemos que instalar algunas dependencias, si no existen ya en el sistema (ademas de haber instalado Spark). Cabe destacar que hemos utilizado Ubuntu 18, por lo que este tutorial se hará para este SO. También utilizamos python 3.6 para ejecutar el código, por lo que si no se encuentrá en tu sistema primero deberías que instalarlo. A continuación, mostramos como instalar algunas de las dependencias para python utilizadas, instalandolas con pip3:
 - Numpy
```bash
sudo pip3 install numpy
```

 - Matplotlib
```bash
sudo pip3 install matplotlib
```

 - Pandas
```bash
sudo pip3 install pandas
```

 - Seaborn
 ```bash
sudo pip3 install seaborn
```

Por último, debemos asegurarnos de estar utilizando python 3.6 con spark. Una de las maneras de hacerlo sería, suponiendo que tu instalació de python3.6 esté en /usr/bin/python3.6:
```bash
export PYSPARK_PYTHON=/usr/bin/python3.6
```

Ya deberíamos estar listos para ejecutar el código. Se ejecuta desde la carpeta spark:
```bash
spark-submit kmeans_classification
```

Este código genera varios datos. Incluye los gráficos generados en spark/images, las descripciones estadísticas de cada grupo en spark/describes, y los modelos generados en spark/models. Si se ejecuta varias veces el código, las salidas se sobreescriben.
Además, se crea un archivo log.txt en el que se van añadiendo los tiempos que ha tardado cada proceso, el cual se utiliza para generar las gráficas de comparación de tiempos.

  ### 5.2) CLASIFICACIÓN A TIEMPO REAL
La mayor parte de prerrequisitos son iguales que en el apartado anterior, por lo que debería seguirse antes de hacer este. Se debe haber ejecutado además de la sección anterior para que este funcione, ya que requiere los modelos generados.
Primero ejecutamos el generado de datos dentro de la carpeta spark:
```bash
sudo python3 streamDataGenerator.py
```
Este archivo abre una conexión TCP en el puerto 9012, por lo que fracasará si este está siendo utilizado ya. A continuación se ejecuta el procesador, en la misma carpeta, con:
```bash
spark-submit streamProcessing.py
```
Una vez cargue, empezará a procesar los datos que streamDataGenerator empiece a enviar, y a mostrarlos por pantalla.

