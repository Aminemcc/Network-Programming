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
            with open(f"files\\{filename}", "wb") as f:
                while True:
                    print("Downloading")
                    try:
                        received_data = client_socket.recv(buffer_size)
                        print(received_data)
                        print("\n-\n")
                        if received_data.decode().endswith("!finish"):
                            f.write(received_data[0:-len("!finish")])
                            print("Finished")
                            break
                    except:
                        pass
                    f.write(received_data)
            continue
        else:
            print(f"Received : {received_data}")


except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)