# <<------------- Этот код снова работает ------------->>
# Этот код требуется для того, чтобы не запускать одновременно код client.py или server.py
# В будущем, скорее всего, из этого кода сделется единый интерфейс приложения.
# На данный момент это единственный способ опробовать приложение


def client_app():
    import client
    app = client.QApplication(client.sys.argv)
    ex = client.DekstopApp()
    ex.show()  # показываем (транслируем) на экран
    client.sys.exit(app.exec())


def server_app():
    import server
    grid = server.QGridLayout()
    while True:
        server.sock.listen()  # слушвем сервер
        conn, addr = server.sock.accept()
        app = server.QApplication(server.sys.argv)
        ex = server.Dekstop(addr, conn, grid)
        ex.show()  # показываем (транслируем) на экран
        server.sys.exit(app.exec())


while True:
    n = input("Что открыть ?\n>>>")
    if n == "client":
        client_app()
        break
    elif n == "server":
        server_app()
        break
    print("Такой команды нет!")
print("Stop")
