import socket, ssl
import re
from bs4 import BeautifulSoup
import sys


host = sys.argv[1]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, 80)
client_socket.connect(server_address)
# context = ssl.create_default_context()
# client_socket = context.wrap_socket(client_socket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
request_header = f'GET / HTTP/1.1\r\nHost: {host}\r\n\r\n'
request_header = bytes(request_header, "utf-8")
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(2048)
    if not received:
        break
    response += received.decode('utf-8')
# re.DOTALL = True
header = re.search(r"(\w*)/([\w.]*)\s*(\b\d{3}\b)\s*([\w ]*)",response)
print(f"Protocol : {header.group(1)}")
print(f"Version  : {header.group(2)}")
print(f"Status   : {header.group(3)}")
print(f"Message  : {header.group(4)}")

print(response)

soup = BeautifulSoup(response, features="html.parser")

# for item in soup.find_all("a"):
#     for span in soup.find_all("span"):
#         print(span)
client_socket.close()