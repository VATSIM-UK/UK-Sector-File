from PyPDF2 import PdfReader
import re
import requests
from bs4 import BeautifulSoup
import os

def convertCoords(inA, inB):
    # convert from XXXXXX.XXN to NXXX.XX.XX.XXX etc
    outA = inA[-1] + "0" + inA[:2] + "." + inA[2:4] + "." + inA[4:6] + "." + inA[7:9].ljust(3, '0')
    outB = inB[-1] + inB[:3] + "." + inB[3:5] + "." + inB[5:7] + "." + inB[8:10].ljust(3, '0')
    return [outA, outB]  # should be a tuple but meh

ukFixes = []
with open("../../Navaids/FIXES_UK.txt") as f:
    fixes = f.read().split("\n")
    for fix in fixes:
        fix = fix.split(" ")
        ukFixes.append(fix[0])

for airport in os.listdir("../../Airports"):
    airport = "EGVA"
    print(airport)
    text = requests.get(f"https://www.aurora.nats.co.uk/htmlAIP/Publications/2023-08-10-AIRAC/html/eAIP/EG-AD-2.{airport}-en-GB.html").text

    soup = BeautifulSoup(text, "html.parser")

    ps = soup.find_all("p")
    rnps = []
    for p in ps:
        if p.find(string=re.compile("INSTRUMENT APPROACH CHART RNP")):
            rnps.append(p)

    for p in ps:
        if p.find(string=re.compile(r"RNAV1 \(DME/DME or GNSS\) STANDARD DEPARTURE CHART")):
            rnps.append(p)
    
    if len(rnps) == 0:
        continue


    div = soup.find("div", attrs={"id": f"{airport}-AD-2.24"})
    rows = list(list(list(div.children)[1].children)[0].children)

    outData = set()

    for rnp in rnps:
        tr = rnp.parent.parent
        rnpIndex = rows.index(tr) + 1

        rnpLink = list(list(rows[rnpIndex].children)[0].children)[1]["href"]
        rnpLink = rnpLink[15:]

        fullRnpLink = f"https://www.aurora.nats.co.uk/htmlAIP/Publications/2023-08-10-AIRAC/graphics/{rnpLink}"

        with open("tmp.pdf", "wb") as f:
            f.write(requests.get(fullRnpLink).content)

        reader = PdfReader('tmp.pdf')
        page = reader.pages[0]
        text = page.extract_text()

        matches = re.findall(r"([A-Z][A-Z0-9]+)  : ([0-9]{6}\.[0-9]{2}[NS]) ([0-9]{7}\.[0-9]{2}[EW])", text)

        for match in matches:
            coords = convertCoords(match[1], match[2])
            outData.add((match[0], (coords[0], coords[1])))

    outData = list(outData)

    finalOutData = []

    for fixData in outData:
        if fixData[0].startswith("RW"):
            continue
        if fixData[0] not in ukFixes:
            finalOutData.append(fixData)

    finalOutData.sort(key=lambda x: x[0])
    try:
        with open(f"../../Airports/{airport}/Fixes.txt", "r") as f:
            currentFixes = f.read().split("\n")
    except FileNotFoundError:
        continue

    for i, fixData in enumerate(currentFixes):
        fix = fixData.split(" ")[0]
        if fix in [x[0] for x in finalOutData]:
            currentFixes[i] = f"{fix} {' '.join([str(x) for x in finalOutData[[x[0] for x in finalOutData].index(fix)][1]])}"
        #print("\n".join([f"{fix[0]} {' '.join(fix[1])}" for fix in finalOutData]))


    with open(f"C:/Users/olive/OneDrive/Documents/GitHub/UK-Sector-File/Airports/{airport}/Fixes.txt", "w") as f:
        f.write("\n".join(currentFixes))
