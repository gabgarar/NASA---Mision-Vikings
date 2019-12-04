import socket
import sys
import requests
#import requests_oauthlib
import prepro
import json
import time
import pandas as pd
from copulae import NormalCopula 
import numpy as np

#sudo apt-get install -y python3-oauth python3-oauth2client python3-oauthlib python3-requests-oauthlib

def send_tweets_to_spark(data, tcp_connection):

    for line in data.splitlines(): #.iter_lines()
        try:
            print("Text: " + line)
            print ("------------------------------------------")
            tcp_connection.send(str(line + '\n').encode())
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)

#Devuelve un array con la media y otro con la desviacion tipica de cada columna
def getNormalDist(df):
    mean = df.mean()
    avg = df.std()
    return mean, avg


def generaDatosSimulados(df, mean, std, numValues, copulaSisms, copulaPreTemp):  
    df_simulado = pd.DataFrame(); 
    headers = df.columns; 

    #Genera los datos correlacionados de RMS_X_AXIS_X100 y WINDSPEED
    sismsRand = copulaSisms.random(numValues)
    df_simulado[headers[0]] = sismsRand[:,0] * std[0] + mean[0]
    df_simulado[headers[1]] = sismsRand[:,1] * std[1] + mean[1]

    #Genera los datos correlacionados de PRESSURE y AIR_TEMPERATURE
    preTempRand = copulaPreTemp.random(numValues)
    df_simulado[headers[2]] = preTempRand[:,0] * std[2] + mean[2]
    df_simulado[headers[3]] = preTempRand[:,1] * std[3] + mean[3]

    for i in range(4, 8): #Para el resto que se generan aleatoriamente
        data = np.random.randn(numValues); 
        df_simulado[headers[i]] = data * std[i] + mean[i] ; 

    return df_simulado

#Leemos el archivo con los datos
df = pd.read_csv("../nasa/event/event_wind_summary/event_wind_summary.tab",
    sep='\s+',header=None)

#Ponemos el nombre a cada columna
df.columns = prepro.read_headers("../nasa/event/event_wind_summary/event_wind_summary.lbl.txt")

#Cogemos solo las variables con las que se ha entrenado
trainVar = ['RMS_X_AXIS_X100', 'WINDSPEED', 'PRESSURE','AIR_TEMPERATURE', 'MEAN_X_AXIS_CROSSINGS', 
            'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

copulaSisms = NormalCopula(2)
#GRUPO 1 -> SISMOGRAFO Y VIENTO
groupSisms = ['RMS_X_AXIS_X100', 'PRESSURE']
copulaSisms.fit(df[groupSisms])

copulaPreTemp = NormalCopula(2)
#GRUPO 2 -> TEMPERATURA Y PRESION
groupPreTemp = ['PRESSURE','AIR_TEMPERATURE']
copulaPreTemp.fit(df[groupPreTemp])

df = df[trainVar]

mean, std = getNormalDist(df)

df_simulado = generaDatosSimulados(df, mean, std, 10000, copulaSisms, copulaPreTemp)
print(df_simulado.describe())
print(df_simulado)

TCP_IP = "localhost"
TCP_PORT = 9012
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting sending data.")

while 1:
    resp = "1 2 5 3 2"
    send_tweets_to_spark(resp,conn)
    time.sleep(3)

