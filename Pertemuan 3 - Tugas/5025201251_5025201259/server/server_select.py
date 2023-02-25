import socket
import select
import sys

server_ip = "localhost"
server_port = 6969
buffer_size = 1024


def send_file(filename):

    pass




def main():
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
                        data = sock.recv(buffer_size)
                        data = data.decode()
                        datas = data.split(" ")
                        if datas[0] == "download":
                            send_file(datas[1])
                        print(datas)
                    
                        if data:
                            sock.send(str.encode(datas[0]))
                        else:                    
                            sock.close()
                            input_socket.remove(sock)
                    except:
                        break
    except KeyboardInterrupt:        
        server_socket.close()
        sys.exit(0)


if __name__ == "__main__":
    main()
