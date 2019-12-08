
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


  

