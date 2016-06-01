import os

for root, dirs, files in os.walk("C:\\"):
    for file in files:
        if file == "WWW.YIFY-TORRENTS.COM.jpg":
            print os.path.join(root, file)
