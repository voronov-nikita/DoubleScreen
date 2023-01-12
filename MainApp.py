# <<------------- Этот код пересатл работать ------------->>
# Поэтому я принял решене откатить файлы client.py и server.py до прошлой(работающей) версии
#


import client, server

while True:
    client.StartClientApp().run()
    server.StartServerApp().run()
