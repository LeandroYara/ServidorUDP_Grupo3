import os
import socket
import threading
import time
import sys
import tqdm

IP = "127.0.0.1"
PORT = 5005
ADDR = (IP, PORT)
SIZE = 1024

def main():
    
    cuentaCliente = 1
    basePuerto = PORT + 1

    tipo = input("Ingrese 1 si quiere enviar el archivo de 10MB o ingrese 2 si quiere enviar el archivo de 5MB: ")
    clientesSimultaneos = int(input("Ingrese el numero de usuarios concurrentes que quiere aceptar: "))
    
    barrera = threading.Barrier(clientesSimultaneos)

    if tipo == "1":
        filePath = "ArchivosEnvio/10MB.bin"
    elif tipo == "2":
        filePath = "ArchivosEnvio/5MB.bin"
    
    fileName = os.path.basename(filePath)
    fileSize = os.path.getsize("ArchivosEnvio/" + fileName)

    sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockTCP.bind(ADDR)
    sockTCP.listen()
    print(f"El servidor esta escuchando en ({IP}, {PORT})...")
    
    while True:
        conn, addr = sockTCP.accept()
        sockTCP.send(str(cuentaCliente).encode())
        thread = threading.Thread(target=handle_client, args=(addr, barrera, fileName, fileSize, cuentaCliente, IP, basePuerto))
        cuentaCliente += 1
        thread.start()
        print(f"[CONEXIONES ACTIVAS]: {threading.active_count() - 1}")

def handle_client(addr, barrera, fileName, fileSize, cuentaCliente, IP, basePuerto):
    
    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockUDP.bind((IP, basePuerto + cuentaCliente))
    barrera.wait()
    
    inicio = time.time()
    mensaje, addr = sockUDP.recvfrom(SIZE)
    print("(" + str(addr[0]) + ", " + str(addr[1]) + ")" + ": " + mensaje.decode())
    sockUDP.sendto(fileName.encode(), addr)
    sockUDP.sendto(cuentaCliente.to_bytes(2, 'little'), addr)
    
    print(f"Enviando {fileName} al cliente {cuentaCliente}...")
    file = open("ArchivosEnvio/" + fileName, "rb")
    data = file.read(SIZE)
    
    progress = tqdm.tqdm(range(fileSize), f"Enviando {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    while(data):
        if(sockUDP.sendto(data, addr)):
            data = file.read(SIZE)
            progress.update(len(data))
    file.close()
    print(fileName + " enviado al cliente " + cuentaCliente + "!")
    
    final = time.time()
    tiempoProceso = final - inicio
    print(f"El tiempo de procesamiento y envio para el cliente {cuentaCliente} es: {tiempoProceso}")
    
main()