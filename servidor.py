import os
import socket
import time
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
ADDR = (UDP_IP, UDP_PORT)
SIZE = 1024
NCL = 1

tipo = input("Ingrese 1 si quiere enviar el archivo de 100MB o ingrese 2 si quiere enviar el archivo de 250MB: ")

if tipo == "1":
    filePath = "ArchivosEnvio/100MB.bin"
elif tipo == "2":
    filePath = "ArchivosEnvio/250MB.bin"
    
fileName = os.path.basename(filePath)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR)

while (True):
    
    mensaje, addrc = sock.recvfrom(SIZE)
    data = [fileName, NCL]
    NCL += 1
    print(addrc + ": " + mensaje)
    
    sock.sendto(data, addrc)
    
    print ("Enviando %s ..." % fileName)
    file = open("ArchivosEnvio/" + fileName, "r")
    data = file.read(SIZE)
    while(data):
        if(sock.sendto(data, addrc)):
            data = file.read(SIZE)
            time.sleep(0.02) # Give receiver a bit time to save
    file.close()