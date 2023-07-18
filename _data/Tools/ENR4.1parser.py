import requests
from bs4 import BeautifulSoup
from Airac import Airac

def capitalConvert(inp):
    out = []
    for word in inp.split(" "):
        out.append(word[0].upper() + word[1:].lower())
    
    return " ".join(out)

def convertCoords(inA, inB):
    # convert from XXXXXX.XXN to NXXX.XX.XX.XXX etc
    outA = inA[-1] + "0" + inA[:2] + "." + inA[2:4] + "." + inA[4:6] + "." + inA[7:9].ljust(3, '0')
    outB = inB[-1] + inB[:3] + "." + inB[3:5] + "." + inB[5:7] + "." + inB[8:10].ljust(3, '0')
    return [outA, outB]  # probably should be a tuple

cycle = Airac()

url = cycle.url() + "EG-ENR-4.1-en-GB.html"

text = requests.get(url).text

soup = BeautifulSoup(text, "html.parser")

ad22 = soup.find("div", attrs={"id": "ENR-4.1"})
rows = list(list(ad22.children)[1].children)[1].children

with open("output.txt", "w") as f:
    f.write("")

    for row in rows:
        name = list(list(list(row.children)[0].children)[1].children)[1].string
        name = capitalConvert(name)
        print(name)

        identifier = list(list(row.children)[1].children)[1].string
        print(identifier)

        freq = list(list(list(row.children)[2].children)[1].children)[1].string
        try:
            float(freq)
        except ValueError:
            if identifier == "LON":  # LON is weird
                freq = "113.600"
            else:
                freq = list(list(list(row.children)[2].children)[3].children)[1].string
        print(freq)

        coordA = list(list(list(row.children)[4].children)[0].children)[1].string
        coordB = list(list(list(row.children)[4].children)[1].children)[1].string
        coords = convertCoords(coordA, coordB)
        print(coords)
        
        f.write(f"{identifier} {freq} {' '.join(coords)} ; {name}\n")
