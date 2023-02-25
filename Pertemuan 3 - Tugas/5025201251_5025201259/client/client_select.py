import socket
import sys

server_ip = "localhost"
server_port = 6969

server_address = (server_ip, server_port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        message = sys.stdin.readline()
        client_socket.send(bytes(message, 'utf-8'))
        received_data = client_socket.recv(1024).decode('utf-8')
        sys.stdout.write(received_data)
        sys.stdout.write('>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)