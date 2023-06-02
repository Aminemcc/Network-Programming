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
match = re.search("(\w+)\s.*/([\w.\s\-\_]+)", data_to_send)
if not bool(match):
    match = re.search("(\w+)\s+([\w.\s\-\_]+)", data_to_send)
filename = match.group(2)
print(filename)
sock.sendall(bytes(data_to_send , "utf-8"))
response = sock.recv(BUFFERSIZE)
sock.close()

try:
    response_header = str(response[0:25], "utf-8")
    # print(response)
    header = re.search(r"(\w+)/([\w.]+)\s+(\b\d{3}\b)\s+([\w ]+)", response_header)
    print(f"Protocol     : {header.group(1)}")
    print(f"Version      : {header.group(2)}")
    print(f"Status       : {header.group(3)}")
    print(f"Message      : {header.group(4)}")
except:
    pass
try:
    status = header.group(3)
    message = header.group(4)
except:
    status = "200"
    message = ""

if status == "200" and data_to_send.startswith("DOWNLOAD"):
    with open(filename, "wb") as f:
        f.write(response)
elif status == "200" and data_to_send.startswith("GET"):
    print("<--Start FILE-->\n")
    try:
        response = str(response, "utf-8")
        for line in response.splitlines():
            print(line)
    except:
        print(response)
        pass
    print("\n<--ENDOF FILE-->\n")
else:
    print(f"ERROR : {status} {message}")

