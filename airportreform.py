import os

for filename in os.listdir("Airports/Other"):    
    file = open(os.path.dirname(os.path.realpath(__file__)) + "/Airports/Other/" + filename, "r")
    lines = file.readlines()
    file.close()


    foldername = os.path.splitext(filename)[0]
    if os.path.exists(os.path.dirname(os.path.realpath(__file__)) + "/Airports/" + foldername):
        continue

    os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "/Airports/" + foldername)
    newFile = open(os.path.dirname(os.path.realpath(__file__)) + "/Airports/" + foldername + "/Basic.txt", "w")
    for line in lines:
        newFile.write(line.strip() + "\n")
    newFile.close()

    os.remove(os.path.dirname(os.path.realpath(__file__)) + "/Airports/Other/" + filename)
