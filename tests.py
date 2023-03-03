from psutil import process_iter
proc_name = ['Telegram.exe', "steam.exe", "mspaint.exe"]
while True:
    for proc in process_iter():
        if proc.name() in proc_name:
            print("KILL:", proc.name())
            proc.kill()
