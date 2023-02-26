import socketserver
import random


class MyTCPHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.BUFFERSIZE = 1024

    def handle(self):
        self.data = self.request.recv(self.BUFFERSIZE).strip()
        self.data_decoded = str(self.data, "utf-8")
        self.datas = self.data_decoded.split(" ")
        if self.datas[0].lower() == "download":
            self.filename = " ".join(self.datas[1:]).strip()
            print(f"Opening {self.filename}")
            try:
                with open(f"files\\{self.filename}", "rb") as f:
                    print(f"Sending {self.filename} to {self.client_address[0]}")
                    self.request.sendall(bytes(f"!download {self.filename}","utf-8"))
                    i = 1
                    while line := f.readline():
                        # print(f"{i}")
                        i += 1
                        size = len(line)
                        for left in range(0, size, self.BUFFERSIZE):
                            right = left + self.BUFFERSIZE
                            if right > size:
                                right = size
                            data_to_send = line[left:right]
                            self.request.sendall(data_to_send)
                self.request.sendall(bytes("!finish", "utf-8"))
                print(f"Done")
            except:
                print("File Does not Exists")
                self.request.sendall(bytes("File Does not Exists", "utf-8"))
        else:
            print("{} wrote:".format(self.client_address[0]))
            self.data = str(self.data, "utf-8")
            self.data_to_send = [i for i in self.data]
            random.shuffle(self.data_to_send)
            self.data = "".join(self.data_to_send)
            self.data = bytes(self.data, "utf-8")
            self.request.sendall(self.data)

if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 5002

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()