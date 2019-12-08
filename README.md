
# ANALISIS DE DATOS SISMOGRÁFICOS PROCEDENTES DE LA MISIÓN VIKING


### INTRODUCCIÓN
Lo primero que haremos es realizar un estudio de los datos recopilados por el proyecto Viking durante su vida útil en la superficie de Marte.
Una vez hecho el estudio, se realizará un clasificador capaz de analizar a tiempo real un flujo de datos con tal de valorarlos.
Esto surge debido a que no se tenía en consideración las rachas de viento encontradas en el planeta.
El brazo en el que se encontraba el sismógrafo, estaba unido al caparazón del módulo, por ello que, al vibrar, daba lecturas erróneas al sismógrafo.
Por ello que queramos clasificar qué lecturas son válidas de las que no.

## INDICE

- [ 1 FASE DE ANÁLISIS](#1-fase-de-análisis).
  - [1.1) PROCEDENCIA DE LOS DATOS](#insertar-hn).
  - [1.2) ESTRUCTURACIÓN DE LOS DATOS Y ESTADÍSTICAS](#insertar-hn).
    - [1.2.1) ESTRUCTURA DE LOS ARCHIVOS](#insertar-hn).
    - [1.2.2) ESTRUCTURA DE LOS DATOS](#insertar-hn).
    - [1.2.3) LECTURA DEL DATASET](#insertar-hn).
    - [1.2.4) ESTADÍSTICAS BASÍCAS DE VARIABLES A ANALIZAR](#insertar-hn).
  - [1.3) AGRUPACIÓN DE DATOS](#insertar-hn)
    - [1.3.1) NORMALIZACIÓN DEL DATASET](#insertar-hn).
    - [1.3.2) MATRIZ DE CORRELACIÓN](#insertar-hn).
    - [1.3.3) ANÁLISIS DE RELACIONES LINEALES](#insertar-hn).
    - [1.3.4) AGRUPACIÓN DE VARIABLES COMO GRUPOS INDEPENDIENTES](#insertar-hn).
  - [1.4) VARIABLES NO RELACIONADAS LINEALMENTE](#insertar-hn)
   
- [ 2) FASE DE MODELADO DE ALGORITMOS NO SUPERVISADOS](#insertar-hn).

- [ 3) FASE DE PREDICTOR Y GENERADOR DE DATOS PARA SIMULACIÓN](#insertar-hn).
  - [3.1) INTRODUCCIÓN KERAS](#insertar-hn).
  - [3.2) MONTAJE DE GENERADOR DE DATOS PARA SIMULACIONES EN FLUJO](#insertar-hn).
  - [3.3) CREACIÓN DEL SERVIDOR](#insertar-hn).

- [ 4) CLASIFICACIÓN DE FLUJO](#insertar-hn).
  - [4.1) PUESTA A PUNTO DEL SERVICIO DE CLASIFICACIÓN CLIENTE-SERVIDOR](#insertar-hn).
  - [4.2) FUNCIONAMIENTO GENRAL DEL SISTEMA](#insertar-hn).
  
  
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
  
  Todos los datos recopilados del proyecto Viking están en un servidor público perteneciente a la universidad de Washington y dados por la NASA.
  El enlace que usaremos para descargar los archivos es:
  
  https://pds-geosciences.wustl.edu/missions/vlander/seismic.html.
  
     #### 1.2.1) ESTRUCTURA DE LOS ARCHIVOS
    Los archivos podremos encontrarlos en tres formatos diferentes: csv, lbl o tab.
    Los archivos csv son archivos comúnmente utilizados, separados los datos por columnas y con un separador común. En nuestro caso es la coma.
    Los archivos tab, es el otro tipo contenedor de datos, donde cada dato está separado por un número de bytes establecidos en el archivo lbl y éste cambiará según la columna y su contenido.
    El tercer tipo de archivo lbl, contendrá información sobre el documento al que referencia, que datos tiene de cada columna, en que byte empieza y en cual acaba, y el tipo de datos que contiene.
    
    ```
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


		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 2
		    NAME                 = SEISMIC_TIME_SOLS
		    DATA_TYPE            = ASCII_REAL
		    START_BYTE           = 7
		    BYTES                = 12
		    DESCRIPTION          = "The mission time in decimal Sols (i.e. 
					   sol+(hr*3600.0+min*60.0+sec)/88775.0)."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 3
		    NAME                 = ORIGINAL_FILE_NUMBER
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 19
		    BYTES                = 6
		    DESCRIPTION          = "The file number of the original data  (i.e. 
		      file number 0101 corresponds to VUSA.0101)."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 4
		    NAME                 = ORIGINAL_RECORD_NUMBER
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 25
		    BYTES                = 7
		    DESCRIPTION          = "The line number in the original VUSA file to 
		      which the present record corresponds."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 5
		    NAME                 = DATA_ACQUISITION_SOL
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 32
		    BYTES                = 4
		    DESCRIPTION          = "The sol number on which the data were acquired. 
		      Landing day is sol 0." 
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 6
		    NAME                 = DATA_ACQUISITION_HOUR
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 36
		    BYTES                = 4
		    DESCRIPTION          = "The hour of acquisition end."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 7
		    NAME                 = DATA_ACQUSITION_MINUTE
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 40
		    BYTES                = 4
		    DESCRIPTION          = "The minute of acquisition end."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 8
		    NAME                 = DATA_ACQUISITION_SECOND
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 44
		    BYTES                = 4
		    DESCRIPTION          = "The second of acquisition end.  Note that the 
		      data in the VUSA file are reported at 1Hz, thus the end of acquisition 
		      is typically 51 seconds after this time."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 9
		    NAME                 = MEDIAN_X_AXIS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 48
		    BYTES                = 5
		    DESCRIPTION          = "The median X-axis reading. 1 digital unit (DU)
		      corresponds roughly to 2nm at 3Hz (see seismic_dataset.cat)"
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 10
		    NAME                 = FIRST_X_AXIS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 53
		    BYTES                = 5
		    DESCRIPTION          = "The first X-axis reading in the record."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 11
		    NAME                 = MAXIMUM_X_AXIS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 58
		    BYTES                = 5
		    DESCRIPTION          = "The maximum X-axis reading in the record."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 12
		    NAME                 = MINIMUM_X_AXIS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 63
		    BYTES                = 5
		    DESCRIPTION          = "The minimum X-axis reading in the record."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 13
		    NAME                 = RMS_X_AXIS_X100
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 68
		    BYTES                = 6
		    DESCRIPTION          = "100 times the RMS X-axis reading."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 14
		    NAME                 = RMS_Y_AXIS_X100
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 74
		    BYTES                = 6
		    DESCRIPTION          = "100 times the RMS Y-axis reading."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 15
		    NAME                 = RMS_Z_AXIS_X100
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 80
		    BYTES                = 6
		    DESCRIPTION          = "100 times the RMS Z-axis reading."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 16
		    NAME                 = MEAN_X_AXIS_CROSSINGS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 86
		    BYTES                = 5
		    DESCRIPTION          = "The mean number of X-axis zero-crossings 
					    in the record."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 17
		    NAME                 = MEAN_Y_AXIS_CROSSINGS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 91
		    BYTES                = 5
		    DESCRIPTION          = "The mean number of Y-axis zero-crossings 
					    in the record."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 18
		    NAME                 = MEAN_Z_AXIS_CROSSINGS
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 96
		    BYTES                = 5
		    DESCRIPTION          = "The mean number of Z-axis zero-crossings 
					    in the record."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 19
		    NAME                 = METEO_TIME_SOLS
		    DATA_TYPE            = ASCII_REAL
		    START_BYTE           = 101
		    BYTES                = 11
		    DESCRIPTION          = "The mission time in decimal Sols (i.e. 
					   sol+(hr*3600.0+min*60.0+sec)/88775.24).
					   of the meteorological data"
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 20
		    NAME                 = WINDSPEED
		    DATA_TYPE            = ASCII_REAL
		    START_BYTE           = 112
		    BYTES                = 7
		    UNIT                 = "m/s"
		    DESCRIPTION          = "nearest windspeed (m/s)."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 21
		    NAME                 = PRESSURE 
		    DATA_TYPE            = ASCII_REAL
		    START_BYTE           = 119
		    BYTES                = 7
		    UNIT                 = "mbar"
		    DESCRIPTION          = "pressure (mbar)."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 22
		    NAME                 = WIND_DIRECTION
		    DATA_TYPE            = ASCII_REAL
		    START_BYTE           = 126
		    BYTES                = 8
		    UNIT                 = "deg"
		    DESCRIPTION          = "wind direction (degrees clockwise from 
					    North towards which the wind is blowing)."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 23
		    NAME                 = AIR_TEMPERATURE
		    DATA_TYPE            = ASCII_REAL
		    START_BYTE           = 134
		    BYTES                = 8
		    UNIT                 = "K"
		    DESCRIPTION          = "Measured air temperature (K). Note that 
		      this value has not been screened for possible lander thermal 
		      contamination (see Hess et al. 1977)."
		  END_OBJECT             = COLUMN

		  OBJECT                 = COLUMN
		    COLUMN_NUMBER        = 24
		    NAME                 = WIND_SEISMIC_INTERVAL
		    DATA_TYPE            = ASCII_INTEGER
		    START_BYTE           = 142
		    BYTES                = 9
		    UNIT                 = "second"
		    DESCRIPTION          = "Time in seconds between closest wind 
		      measurement and the end of the seismic record (for the first 
		      and last sol of the file, this value should be ignored). Positive
		      means seismic data obtained after meteorology"
		  END_OBJECT             = COLUMN

	          END_OBJECT               = TABLE
		  END
	```
    

     #### 1.2.2) ESTRUCTURA DE LOS DATOS
     #### 1.2.3) LECTURA DEL DATASET
     #### 1.2.4) ESTADÍSTICAS BASÍCAS DE VARIABLES A ANALIZAR


  

