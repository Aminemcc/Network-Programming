import socket
import sys
import os

server_address = ('1', 5002)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

sys.stdout.write('>> ')

try:
    while True:
        message = sys.stdin.readline()
        filename = message.split()[1]
        client_socket.send(bytes(message, 'utf-8'))
        
        received_data = client_socket.recv(1024)
        server_msg = received_data.decode('utf-8')
        
        if(server_msg == '' or server_msg == 'Requested File Not Found'):
            print('Error requested')
        else:
            f_destination = open(filename,'wb')
            print('Receiving...')
            f_destination.write(received_data) 
            print('Received')
            f_destination.close()
        
        sys.stdout.write('\nProgram Finished\n')
        sys.stdout.write('>> ')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)
