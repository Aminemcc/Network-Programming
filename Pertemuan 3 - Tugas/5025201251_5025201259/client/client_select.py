import socket
import sys

server_ip = "localhost"
server_port = 6969
buffer_size = 1024

server_address = (server_ip, server_port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

try:
    while True:
        message = input(">> ")
        client_socket.send(bytes(message, 'utf-8'))
        received_data = client_socket.recv(buffer_size).decode('utf-8')
        if received_data.startswith("!download"):
            datas = received_data.split(" ")
            filename = datas[1]
            with open(filename, "wb") as f:
                while True:
                    received_data = client_socket.recv(buffer_size)
                    if received_data.decode() == "!finish":
                        break
                    f.write(received_data)
        else:
            print(f"Received : {received_data}")


except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)