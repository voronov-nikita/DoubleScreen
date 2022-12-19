import socket
import json

sock = socket.socket()
ip = "192.168.0.14"
port = 9999
sock.connect((ip, port))

while True:
    data2 = sock.recv(16384)
    key = json.loads(data2, encoding="utf-8")
    print(key)
