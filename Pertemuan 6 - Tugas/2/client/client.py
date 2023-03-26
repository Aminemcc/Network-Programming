import socket
import re

BUFFERSIZE = 1<<24

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
config = read_config("../server/httpserver.conf")
HOST = config["ip"]
PORT = config["port"] 

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))


#GET [filename] [no protocol needed for client.py]
data_to_send = input(">> ")
filename = re.findall("(\w+) ([\w ]+)$")[1]
print(filename)
sock.sendall(bytes(data_to_send , "utf-8"))

received = str(sock.recv(BUFFERSIZE), "utf-8")

with open

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