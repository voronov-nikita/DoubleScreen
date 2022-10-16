import socket
import webbrowser
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname_ex(socket.gethostname())[-1][-1], 4321))

print(socket.gethostbyname_ex(socket.gethostname())[-1][-1])

server.listen()

while True:
    user, adres = server.accept()
    while True:
        data = user.recv(1024).decode("utf-8").lower()
        print(data)

        if data == "youtube":
            webbrowser.open("https://www.youtube.com")
        elif data == "мэш":
            webbrowser.open("https://school.mos.ru")
        elif data == "google":
            webbrowser.open("https://www.google.com")
        elif data == "vk":
            webbrowser.open("https://www.vk.com")

        elif data=="steam":
            os.startfile("C:/Program Files (x86)/Steam/steam.exe")
        elif data=="discord":
            os.startfile("C:/Users/MSI/AppData/Local/Discord/app-1.0.9006/Discord.exe")
