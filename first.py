import os
# os.system('python main.py')


file = open("user.txt", "r")
file.seek(0)
active = file.readlines()[0]
if active == "0":
    os.system('python second.py')
else:
    os.system('python main.py')