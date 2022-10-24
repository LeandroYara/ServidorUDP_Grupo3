import datetime
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
        filePath = "ArchivosEnvio/100MB.bin"
    elif tipo == "2":
        filePath = "ArchivosEnvio/250MB.bin"
    
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
        conn.send(clientesSimultaneos.to_bytes(2, 'little'))
        thread = threading.Thread(target=handle_client, args=(addr, barrera, fileName, fileSize, cuentaCliente, puertoNuevo, clientesSimultaneos, IPS, PORTS))
        cuentaCliente += 1
        thread.start()
        print(f"[CONEXIONES ACTIVAS]: {threading.active_count() - 1}")

def handle_client(addr, barrera, fileName, fileSize, cuentaCliente, puertoNuevo, clientesSimultaneos, IPS, PORTS):
    
    barrera.wait()
    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockUDP.bind((IPS, PORTS + cuentaCliente))
    
    sockUDP.sendto(fileName.encode(), (addr[0], puertoNuevo))
    sockUDP.sendto(fileSize.to_bytes(3, 'little'), (addr[0], puertoNuevo))
    
    print(f"Enviando {fileName} al cliente {cuentaCliente}...")
    file = open("ArchivosEnvio/" + fileName, "rb")
    data = file.read(SIZE)
    
    progress = tqdm.tqdm(range(fileSize), f"Enviando {fileName}", unit="B", unit_scale=True, unit_divisor=1024)
    now = datetime.datetime.now()
    
    inicio = time.time()
    while(data):
        if(sockUDP.sendto(data, (addr[0], puertoNuevo))):
            data = file.read(SIZE)
            progress.update(len(data))
    file.close()
    print(f"{fileName} enviado al cliente {cuentaCliente}!")
    
    final = time.time()
    tiempoProceso = final - inicio
    print(f"El tiempo de procesamiento y envio para el cliente {cuentaCliente} es: {tiempoProceso}")
    
    year = str(now)[:4]
    month = str(now)[5:7]
    day = str(now)[8:10]
    hour = str(now)[11:13]
    minute = str(now)[14:16]
    second = str(now)[17:19]
    
    save_path = 'Logs/'
    file_name = 'S'+ str(cuentaCliente) + '-' + year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second + '-' + fileName + '-' + str(clientesSimultaneos) + '-' + 'log.txt' 
    completeName = os.path.join(save_path,file_name)
    newFile = open(completeName, 'w')
    newFile.write('El archivo enviado fue: ' + fileName +'\n')
    newFile.write('El archivo tiene un tamano de: ' + str(fileSize) + ' bytes\n')
    newFile.write('El cliente al que le fue enviado es: ' + str(cuentaCliente) +'\n')
    newFile.write(f'El tiempo de transferencia para este cliente fue: {tiempoProceso} segundos\n')
    
main()