import socket
import time
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
ADDR = (UDP_IP, UDP_PORT)
SIZE = 1024

tipo = input("Ingrese 1 si quiere enviar el archivo de 100MB o ingrese 2 si quiere enviar el archivo de 250MB: ")

if tipo == "1":
    file = open("ArchivosEnvio/100MB.bin", "rb")
elif tipo == "2":
    file = open("ArchivosEnvio/250MB.bin", "rb")

file_name = sys.argv[1]


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(ADDR)

while (True):
    sock.sendto(file_name, ADDR)
    print ("Sending %s ..." % file_name)

    file = open("ArchivosEnvio/" + file_name, "r")
    data = file.read(SIZE)
    while(data):
        if(sock.sendto(data, ADDR)):
            data = file.read(SIZE)
            time.sleep(0.02) # Give receiver a bit time to save