import socket
import json

# создаём сокет и связываем его с IP-адресом и портом

sock = socket.socket()
ip = "192.168.0.14"
port = 9999
sock.bind((ip, port))


sock.listen(10)

while True:
    # начинаем принимать соединения
    conn, addr = sock.accept()

    ls = [1, 2, 3, 4, 5]
    conn.send(json.dumps(ls).encode('utf-8'))
