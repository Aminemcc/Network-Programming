import socket

HOST = "127.0.0.1"
PORT = 5002
BUFFERSIZE = 1024

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def download_file(sock, filename):
    filename = filename.strip()
    print(f"Starting Download {filename}")
    with open(filename, "wb") as f:
        while True:
            data = sock.recv(BUFFERSIZE)
            # print(data)
            if data == b"!finish":
                # print(data)
                break
            f.write(data)   
    print(f"Downloaded {filename}")

data_to_send = input(">> ")
sock.sendall(bytes(data_to_send , "utf-8"))

received = str(sock.recv(BUFFERSIZE), "utf-8")
datas = received.split(",\n")
if datas[0] == "!download":
    filesize = datas[2].split(" ")[1]
    filename = " ".join(datas[1].split(" ")[1:])
    filename = filename.strip()
    print(f"{datas[1]}\n{datas[2]}")
    print(f"name : {filename}\nsize : {filesize}")
    download_file(sock, filename)
else :
    print("Sent:     {}".format(data_to_send))
    print("Received: {}".format(received))