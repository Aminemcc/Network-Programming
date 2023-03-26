import socket
import select
import sys
import re
import os
from threading import Thread

def read_config(filename):
    conf_file = open(filename, "r")
    items = re.findall("\s*(\w+)\s+([\w.]+)\s*", conf_file.read())
    config = {}
    for item in items:
        try:
            config[item[0]] = int(item[1])
        except:
            config[item[0]] = item[1]
    return config
config = read_config("httpserver.conf")

def generate_header(protocol="HTTP", version="1.1", status=200, extension="html", charset="UTF-8", content_length=None):
    if status == 200:
        message = "OK"
    elif status == 404:
        message = "Not found"
    else:
        message = "Others"
    if extension != "html":
        extension = "plain"
    header = f"{protocol}/{version} {status} {message}\r\n"
    if status not in [404, "404"]:
        header += f"Content-Type: text/{extension}; charset={charset}\r\nContent-Length:{content_length}\r\n"
    header += "\r\n"
    return header


print(config)
server_address = (config["ip"], config["port"])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(120)

input_socket = [server_socket]

def handle(sock):
    try:
        # receive data from client, break when null received          
        data = sock.recv(4096)
        
        data = data.decode('utf-8')
        request_header = data.split('\r\n')
        try:
            print("Request : ", end = "")
            print(request_header[0].split())
            request_file = request_header[0].split()[1]
        except:
            request_file = "other"
        response_header = b''
        response_data = b''
        
        if request_file == 'index.html' or request_file == '/' or request_file == '/index.html' or request_file == "":
            f = open('index.html', 'r')
            response_data = f.read()
            f.close()
            
            content_length = len(response_data)
            response_header = generate_header(content_length=content_length)
            sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

        else:
            try:
                f = open(request_file[1::], "rb")
                file_exists = True
            except:
                f = open("404.html", "rb")
                file_exists = False
            response_data = f.read()
            f.close()
            content_length = len(response_data)
            _, extension = os.path.splitext(request_file)

            if file_exists:
                response_header = generate_header(extension=extension[1::], content_length=content_length)
            else:
                response_header = generate_header(status="404")
            
            sock.sendall(bytes(response_header, "utf-8") + response_data)
    except:
        return None    
    pass

def main():
    threads = []
    try:
        while True:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            
            for sock in read_ready:
                if sock == server_socket:
                    client_socket, client_address = server_socket.accept()
                    input_socket.append(client_socket)                       
                
                else:
                    new_thread = Thread(target=handle, args=(sock,))
                    threads.append(new_thread)
                    new_thread.start()

    except KeyboardInterrupt:
        for thread in threads:
            thread.kill()        
        server_socket.close()
        sys.exit(0)

if __name__ == '__main__':
    main()