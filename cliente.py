import socket
import select

UDP_IP = "127.0.0.1"
UDP_SR = "127.0.0.1"
IN_PORT = 5005
ADDRC = (UDP_IP, IN_PORT)
ADDRS = (UDP_SR, IN_PORT)
SIZE = 1024
timeout = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto("Nueva solicitud", ADDRS)
data, addr = sock.recvfrom(1024)
fileName = data[0]
numeroCliente = data[1]

print ("Se establecio la comunicación con el servidor")
print("IP y puerto del servidor: " + addr)
print ("Nombre del archivo por recibir: ", fileName)

file = open(fileName, 'wb')

while True:
    ready = select.select([sock], [], [], timeout)
    if ready[0]:
        data, addr = sock.recvfrom(1024)
        file.write(data)
    else:
        print ("%s Terminado!" % fileName)
        file.close()
        break