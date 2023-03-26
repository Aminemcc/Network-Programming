import socket, ssl
import re
from bs4 import BeautifulSoup
import sys

host = sys.argv[1]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, 443)
client_socket.connect(server_address)

client_socket = ssl.wrap_socket(client_socket, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
request_header = f'GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n'
request_header = bytes(request_header, "utf-8")
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(2048)
    if not received:
        break
    response += received.decode('utf-8')

header = re.search(r"(\w*)/([\w.]*)\s*(\b\d{3}\b)\s*([\w ]*)",response)
print(header)
soup = BeautifulSoup(response, features="html.parser")

try:
    charset = soup.find_all("meta")[0]["content"].split()[1].split("=")[1]
except:
    charset = "-"

menus =[]
for menu in soup.find_all("a", {"class": "dropdown-item"}):
    menus.append(menu["title"])
    
print(f"Protocol     : {header.group(1)}")
print(f"Version      : {header.group(2)}")
print(f"Status       : {header.group(3)}")
print(f"Message      : {header.group(4)}")
print(f"Menu         : {menus}")
print(f"Charset      : {charset}")
print(f"Content-Encoding     : {soup.original_encoding}")

client_socket.close()