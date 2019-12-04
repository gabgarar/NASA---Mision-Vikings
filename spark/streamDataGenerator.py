import socket
import sys
import requests
import requests_oauthlib
import json
import time

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

