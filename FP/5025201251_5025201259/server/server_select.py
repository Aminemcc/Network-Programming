import socket
import select
import sys
import os

server_address = ('127.0.0.1', 5002)
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
                cmd = sock.recv(1024).decode('utf-8').split()
                
                if(len(cmd) == 2):
                    if(cmd[0]=='download'):
                        download_file = download_file = os.getcwd() +'/5025201251_5025201259/server/files/'+cmd[1]
                        
                        if(os.path.exists(download_file) == False):
                            sock.send('Requested File Not Found'.encode('utf-8'))
                            sock.close()

                        try:
                            f = open(download_file, 'rb')
                            req_data = f.read(1024) 
                            
                            if(req_data):
                                print('file-name:\t' + cmd[1] + '\nfile-size: \t' + str(os.path.getsize(download_file)) + ' bytes' +'\nSending...')
                                sock.send(req_data)
                            
                            f.close()  
                            print('Success')

                        except:
                            print('Error occured'.encode('utf-8'))
                    else: 
                        print('Command Invalid')
                else: 
                    print('Too much argument')
                             
                sock.close()
                input_socket.remove(sock)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)
