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

def send_data_to_spark(data, tcp_connection):
    first = True
    for line in data.splitlines():
        try:
            if first:
                first = False
                continue
            print("Data: " + line)
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


def generaDatosSimulados(df, mean, std, numValues):  
    df_simulado = pd.DataFrame(); 
    headers = df.columns; 

    for i in range(8):
        data = np.random.randn(numValues); 
        values = data * std[i] + mean[i]
        values = np.where(values < 0, 0, values) #Los valores por debajo de 0 no tienen sentido

        df_simulado[headers[i]] = values ; 

    return df_simulado

print("Creating the data generator...")
#Leemos el archivo con los datos
df = pd.read_csv("../nasa/event/event_wind_summary/event_wind_summary.tab",
    sep='\s+',header=None)

#Ponemos el nombre a cada columna
df.columns = prepro.read_headers("../nasa/event/event_wind_summary/event_wind_summary.lbl.txt")

#Cogemos solo las variables con las que se ha entrenado
trainVar = ['RMS_X_AXIS_X100', 'WINDSPEED', 'PRESSURE','AIR_TEMPERATURE', 'MEAN_X_AXIS_CROSSINGS', 
            'MEAN_Y_AXIS_CROSSINGS', 'MEAN_Z_AXIS_CROSSINGS','WIND_DIRECTION']

df = df[trainVar]

mean, std = getNormalDist(df)


TCP_IP = "localhost"
TCP_PORT = 9012
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)


df_simulado = generaDatosSimulados(df, mean, std, 10)


print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting sending data.")

while 1:
    df_simulado = generaDatosSimulados(df, mean, std, 10)
    data = df_simulado.to_string(index=False, header=False)
    send_data_to_spark(data,conn)
    time.sleep(10)

