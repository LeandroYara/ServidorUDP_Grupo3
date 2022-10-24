import datetime
import os
import random
import socket
import select
import time

IPC = "192.168.1.113"
PORTC = random.randint(10000, 60000)
IPS = "192.168.137.208"
PORTS = 5005
ADDRC = (IPC, PORTC)
ADDRS = (IPS, PORTS)
SIZE = 1024
timeout = 1

def main():

    sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockTCP.bind(ADDRC)
    sockTCP.connect(ADDRS)
    print(f"Cliente conectado al servidor {IPS}:{PORTS}")
    numeroCod = sockTCP.recv(1024)
    numeroCliente = int.from_bytes(numeroCod, 'little')
    print("Numero de cliente: " + str(numeroCliente))
    puertoNuevo = PORTC + numeroCliente
    print(f"Puerto actual: {puertoNuevo}")
    sockTCP.send(puertoNuevo.to_bytes(3, 'little'))
    conexCod = sockTCP.recv(1024)
    conexionesSimultaneas = int.from_bytes(conexCod, 'little')
    print(f"Conexiones simultaneas esperadas: {conexionesSimultaneas}")
    
    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockUDP.bind((IPC, puertoNuevo))

    fileCod, addr = sockUDP.recvfrom(SIZE)
    fileName = fileCod.decode()
    sizeCod, addr = sockUDP.recvfrom(SIZE)
    serverSize = int.from_bytes(sizeCod, 'little')

    print("Se establecio la comunicación con el servidor")
    print("IP y puerto del servidor: " + "(" + str(addr[0]) + ", " + str(addr[1]) + ")")
    print("Nombre del archivo por recibir: " + fileName)
    print("Tamano del archivo por recibir: " + str(serverSize))

    file = open(f"ArchivosRecibidos/{numeroCliente}-Prueba-{conexionesSimultaneas}", 'wb')
    
    now = datetime.datetime.now()
    inicio = time.time()

    while True:
        ready = select.select([sockUDP], [], [], timeout)
        if ready[0]:
            data, addr = sockUDP.recvfrom(SIZE)
            file.write(data)
        else:
            print ("%s Terminado!" % fileName)
            file.close()
            break
    
    final = time.time()
    tiempoProceso = final - inicio
    print(f"Tiempo de comunicacion y envio: {tiempoProceso}")
    
    filesize = os.path.getsize(f"ArchivosRecibidos/{numeroCliente}-Prueba-{conexionesSimultaneas}")
    
    year = str(now)[:4]
    month = str(now)[5:7]
    day = str(now)[8:10]
    hour = str(now)[11:13]
    minute = str(now)[14:16]
    second = str(now)[17:19]
    
    save_path = 'Logs/'
    file_name = 'C'+ str(numeroCliente) + '-' + year + '-' + month + '-' + day + '-' + hour + '-' + minute + '-' + second + '-' + fileName + '-' + str(conexionesSimultaneas) + '-' + 'log.txt' 
    completeName = os.path.join(save_path,file_name)
    newFile = open(completeName, 'w')
    if serverSize == filesize:
        newFile.write('El archivo se ha enviado exitosamente'+'\n')
    else:
        newFile.write('El archivo ha tenido un fallo o paquete faltante al enviarse'+'\n')
    newFile.write('El archivo enviado fue: ' + fileName +'\n')
    newFile.write('El archivo tiene un tamano de: ' + str(filesize) + ' bytes\n')
    newFile.write('El cliente al que le fue enviado es: ' + str(numeroCliente) +'\n')
    newFile.write('El puerto del cliente es: ' + str(puertoNuevo))
    newFile.write(f'El tiempo de transferencia para este cliente fue {tiempoProceso} segundos\n')
    
main()