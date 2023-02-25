import socket
import select
import sys

server_ip = "localhost"
server_port = 6969

server_address = (server_ip, server_port)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:            	
                try:
                    data = sock.recv(1024)
                    print(sock.getpeername(), data.decode())
                
                    if data:
                        sock.send(data)
                    else:                    
                        sock.close()
                        input_socket.remove(sock)
                except:
                    continue
except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)