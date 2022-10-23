import os
import socket
import threading
import time
import sys
import tqdm

IPS = "127.0.0.1"
PORTS = 5005
ADDRS = (IPS, PORTS)
SIZE = 1024

def main():
    
    cuentaCliente = 1

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
    sockTCP.bind(ADDRS)
    sockTCP.listen()
    print(f"El servidor esta escuchando en ({IPS}, {PORTS})...")
    
    while True:
        conn, addr = sockTCP.accept()
        conn.send(cuentaCliente.to_bytes(2, 'little'))
        puertoCod = conn.recv(1024)
        puertoNuevo = int.from_bytes(puertoCod, 'little')
        thread = threading.Thread(target=handle_client, args=(addr, barrera, fileName, fileSize, cuentaCliente, puertoNuevo, IPS, PORTS))
        cuentaCliente += 1
        thread.start()
        print(f"[CONEXIONES ACTIVAS]: {threading.active_count() - 1}")

def handle_client(addr, barrera, fileName, fileSize, cuentaCliente, puertoNuevo, IPS, PORTS):
    
    barrera.wait()
    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockUDP.bind((IPS, PORTS + cuentaCliente))
    
    inicio = time.time()
    sockUDP.sendto(fileName.encode(), (addr[0], puertoNuevo))
    
    print(f"Enviando {fileName} al cliente {cuentaCliente}...")
    file = open("ArchivosEnvio/" + fileName, "rb")
    data = file.read(SIZE)
    
    progress = tqdm.tqdm(range(fileSize), f"Enviando {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    while(data):
        if(sockUDP.sendto(data, (addr[0], puertoNuevo))):
            data = file.read(SIZE)
            progress.update(len(data))
    file.close()
    print(f"{fileName} enviado al cliente {cuentaCliente}!")
    
    final = time.time()
    tiempoProceso = final - inicio
    print(f"El tiempo de procesamiento y envio para el cliente {cuentaCliente} es: {tiempoProceso}")
    
main()