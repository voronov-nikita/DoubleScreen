import socket


def start_client(ip_input):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((str(ip_input), 1234))

    while True:
        client.send(input().encode("utf-8"))


ip_input = input()
if ip_input:
    print('Готово!')
    start_client(ip_input())
