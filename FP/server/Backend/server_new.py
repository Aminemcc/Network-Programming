import socket
import select
import sys
import re
import os
import threading


class Server:
    def __init__(self, config_file : str = "httpserver.conf", buffer_size : int = 2048):
        self.frontend_path = os.path.join(os.getcwd(), "../Frontend")
        self.backend_path = os.path.join(os.getcwd(), "./files")
        self.buffer_size = buffer_size
        self.isRunning = False
        self.config = self.read_config(config_file)
        self.address = (self.config["ip"], self.config["port"])
        self.socket = self.init_socket()

        self.timeout = 2
        self.clients = {}
        """
        self.clients :
            id :
                thread, address, socket, status, lock
        """
        self.threads = [] #contain id of the thread, access the thread in clients

        self.active_thread = 0
        self.count_thread = 0 # Will also become ID of thread
        self.count_thread_lock = threading.Lock()
        self.max_active_thread = 100

    def read_config(self, filename):
        conf_file = open(filename, "r")
        items = re.findall("\s*(\w+)\s+([\w.]+)\s*", conf_file.read())
        config = {}
        for item in items:
            try:
                config[item[0]] = int(item[1])
            except:
                config[item[0]] = item[1]
        return config

    def init_socket(self):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.bind(self.address)
        return _socket

    def handle_new_client(self, socket, address):
        # Function to initiate the thread and call self._handler
        if self.active_thread >= self.max_active_thread:
            #Doesn't accept any more client at the moment
            return False
        with self.count_thread_lock:
            self.count_thread += 1
            id = self.count_thread
        thread = threading.Thread(target=self.handler, args=(id, socket,address,))
        self.clients[id] = {}
        self.clients[id]["thread"] = thread
        self.clients[id]["lock"] = threading.Lock()
        if self.isRunning:
            #hanya start jika server running
            thread.start()
        return True
    
    def handler(self, id, socket, address):
        self.active_thread += 1
        self.threads.append(id)
        with self.clients[id]["lock"]:
            self.clients[id]["address"] = address
            self.clients[id]["socket"] = socket
            self.clients[id]["status"] = True
        try:
            while self.clients[id]["status"]:
                read_ready, _, _ = select.select([socket], [], [], self.timeout)
                if socket in read_ready:
                    data = socket.recv(self.buffer_size)
                    if bool(data):
                        request_header = data.decode("utf-8")
                        cmd, filename = self.get_cmd_file(request_header)
                        print(f"cmd : {cmd}, request file : {filename}")
                        if cmd in ["GET", "HEAD"]:
                            content, file_to_send, status = self.getFile(cmd, filename)
                            ext = os.path.splitext(file_to_send)[1][1:]
                            if ext == "html":
                                header = self.generate_header(status=status, content_length=len(content))
                            else:
                                header = self.generate_header(status=status, content_length=len(content), extension=ext)
                            data_to_send = header.encode("utf-8")
                            if cmd == "GET":
                                data_to_send += content
                            socket.sendall(data_to_send)
                            
                        elif cmd == "POST":
                            # Handle POST request
                            post_data = self.get_post_data(str(request_header))
                            
                            if post_data:
                                print(f"Nama file: {post_data}")
                                # ... additional processing ...
                                response = b'HTTP/1.1 200 OK\n\nFile received.'
                                socket.sendall(response)
                            else:
                                response = b'HTTP/1.1 400 Bad Request\n\nInvalid request.'
                                socket.sendall(response)
                        elif cmd == "GET" and filename == "/download":
                            self.handle_file_download(socket)
                        else:
                            print("Command error")
                    else:
                        #Stopping Client
                        self.clients[id]["status"] = False
                elif not self.isRunning:
                    #timeout
                    self.clients[id]["status"] = False
        finally:
            socket.close()
            self.active_thread -= 1

    def get_post_data(self, request_data):
        pattern = r'Content-Disposition: form-data; name="nama_file"\r\n\r\n(.*?)[\r\n]+'
        match = re.search(pattern, request_data, re.DOTALL)
        if match:
            return match.group(1)
        return None

    def get_cmd_file(self, data):
        request_header = data.split('\r\n')
        request_header = request_header[0].split()
        cmd = request_header[0]
        request = request_header[1][1:]
        return (cmd, request)

    def getFile(self, cmd, filename):
        """
        Return : (file_data, status)
        file_data should be sent to the client with corresponding status
        """
        _filename = filename
        status = 200
        if filename in ["/", ""]:
            _filename = "index.html"
        elif os.path.basename(filename)[0] == ".":
            # Forbidden 403
            _filename = "403.html"
            status = 403
        else:
            pass
        _filepath = os.path.join(self.frontend_path, _filename)
        try:
            with open(_filepath, "rb") as f:
                return (f.read(), _filename, status)
        except FileNotFoundError as e:
            with open(os.path.join(self.frontend_path, "404.html"), "rb") as f:
                return (f.read(), "404.html", 404)

    def generate_header(self, protocol="HTTP", version="1.1", status=200, extension="html", charset="utf-8",content_length=0):
        if status == 200:
            message = "OK"
        elif status == 301:
            message = "Moved Permanently"
        elif status == 403:
            message = "Forbidden"
        elif status == 404:
            message = "Not found"
        elif status == 500:
            message = "Internal Server Error"
        else:
            message = "Others"
        if extension != "html":
            extension = extension
        header = f"{protocol}/{version} {status} {message}"
        header += "\r\n"
        if status not in [404]:
            header += f"Content-Type: text/{extension}; charset={charset}\r\nContent-Length:{content_length}"
            header += "\r\n"
        header += "Access-Control-Allow-Origin: *\r\n"
        header += "Access-Control-Allow-Methods: GET, POST\r\n"  # Include allowed methods
        header += "\r\n"
        return header

    def start(self):
        print(f"Access : ")
        self.socket.listen(1)
        self.isRunning = True
        # try:
        while self.isRunning:
            try:
                #read_ready, write_ready, exception
                read_ready, _, _ = select.select([self.socket], [], [], self.timeout)

                #Setiap Client baru
                for client in read_ready:
                    client_socket, client_address = self.socket.accept()
                    self.handle_new_client(client_socket, client_address)
                # print(f"Active user : {self.active_thread}")
            except KeyboardInterrupt:
                self.isRunning = False

        print("STOP")
        for id in self.threads:
            self.clients[id]["status"] = False
            self.clients[id]["thread"].join()

        self.socket.close()
        sys.exit(0)


def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()