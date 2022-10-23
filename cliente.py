import random
import socket
import select
import time

IPC = "127.0.0.1"
PORTC = random.randint(10000, 60000)
IPS = "127.0.0.1"
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
    
    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockUDP.bind((IPC, puertoNuevo))

    inicio = time.time()

    fileCod, addr = sockUDP.recvfrom(1024)
    fileName = fileCod.decode()

    print("Se establecio la comunicación con el servidor")
    print("IP y puerto del servidor: " + "(" + str(addr[0]) + ", " + str(addr[1]) + ")")
    print("Nombre del archivo por recibir: " + fileName)

    file = open("ArchivosRecibidos/"+ str(numeroCliente) + "-" + fileName, 'wb')

    while True:
        ready = select.select([sockUDP], [], [], timeout)
        if ready[0]:
            data, addr = sockUDP.recvfrom(1024)
            file.write(data)
        else:
            print ("%s Terminado!" % fileName)
            file.close()
            break
    
    final = time.time()
    tiempoProceso = final - inicio
    print(f"Tiempo de comunicacion y envio: {tiempoProceso}")
    
main()