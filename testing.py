import os
dir=''
for x in range(ord('A'), ord('Z')+1):
    try:
        dir = f"{chr(x)}:/"
        if dir:
            for i in os.listdir(dir):
                try:
                    for a in os.listdir(dir+str(i)):
                        if a=="Steam":
                            print('Yeees')
                            print(f"{chr(x)}:/{i}/{a}")
                        elif a=="Discord":
                            print('Yeees')
                            print(f"{chr(x)}:/{i}/{a}")
                        elif a=="GitHub Desktop":
                            print("Yees")
                            print(f"{chr(x)}:/{i}/{a}")
                except:
                    pass
    except:
        pass


