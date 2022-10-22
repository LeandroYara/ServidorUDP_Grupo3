import socket
import select
import time

IP = "127.0.0.1"
PORT = 5006
ADDR = (IP, PORT)
SIZE = 1024
timeout = 1

def main():

    sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockTCP.bind(ADDR)
    
    sockTCP.connect(ADDR)
    print(f"Cliente conectado al servidor {IP}:{PORT}")
    sockTCP.recv(1024)

    inicio = time.time()

    mensajeCodificado = "Nueva solicitud".encode()
    sockUDP.sendto(mensajeCodificado, ADDR)

    fileCod, addr = sockUDP.recvfrom(1024)
    fileName = fileCod.decode()
    ncb, addr = sockUDP.recvfrom(1024)
    numeroCliente = int.from_bytes(ncb, "little")

    print("Se establecio la comunicación con el servidor")
    print("IP y puerto del servidor: " + "(" + str(addr[0]) + ", " + str(addr[1]) + ")")
    print("Numero de cliente: " + str(numeroCliente))
    print("Nombre del archivo por recibir: " + fileName)

    file = open("ArchivosRecibidos/"+ str(numeroCliente) + fileName, 'wb')

    while True:
        ready = select.select([sockUDP], [], [], timeout)
        if ready[0]:
            data = sockUDP.recvfrom(1024)
            file.write(data)
        else:
            print ("%s Terminado!" % fileName)
            file.close()
            break
    
    final = time.time()
    tiempoProceso = final - inicio
    print(f"Tiempo de comunicacion y envio: {tiempoProceso}")
    
main()