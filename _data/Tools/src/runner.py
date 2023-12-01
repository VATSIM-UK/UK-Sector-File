import os
import argparse

import api

class Runner:
    def __init__(self, args):
        self.args = args
        self.aipApi = api.AipAPI()

    def readCurrentData(self, page):
        with open(f"./../../{page}", "r") as f:
            return f.read().split("\n")
        
    def writeLines(self, page, data):
        with open(f"./../../{page}", "w") as f:
            f.write("\n".join(data))

    def run(self):
        if self.args["page"] == "ENR4.1" or self.args["page"] == "all":  # ENR4.1
            # get current data
            currentData = self.readCurrentData("Navaids/VOR_UK.txt")

            # get new data
            newData = self.aipApi.parseENR4_1()

            # compare
            for i, line in enumerate(currentData):  
                vorID = line.split(" ")[0]
                if vorID in newData.keys():  # only rewrite if the VOR/DME is in both the old data and the new data, otherwise existing data is kept
                    # if the VOR/DME is in both the old data and the new data, write the new data onto the old data (if the data is the same we still write, just no change will be visible because the written data is the same as the stored data)
                    dataAboutVORDME = newData[vorID]
                    currentData[i] = f"{vorID} {dataAboutVORDME['frequency']} {' '.join(dataAboutVORDME['coordinates'])} ; {dataAboutVORDME['name']}"

            self.writeLines("Navaids/VOR_UK.txt", currentData)
        
        elif self.args["page"] == "ENR4.4" or self.args["page"] == "all":
            currentData = self.readCurrentData("Navaids/FIXES_UK.txt")

            newData = self.aipApi.parseENR4_4()

            for i, line in enumerate(currentData):
                fixID = line.split(" ")[0]
                if fixID in newData.keys():
                    dataAboutFix = newData[fixID]
                    currentData[i] = f"{fixID} {' '.join(dataAboutFix['coordinates'])}"

            self.writeLines("Navaids/FIXES_UK.txt", currentData)
        
        elif self.args["page"] == "ENR3.2" or self.args["page"] == "all":
            newData = self.aipApi.parseENR3_2()

            lowerAirways = os.listdir("../../Airways/RNAV/Lower")
            upperAirways = os.listdir("../../Airways/RNAV/Upper")

            for airway in newData.keys():
                prevLowerIndex = None
                prevUpperIndex = None
                firstLower = True
                firstUpper = True
                lowerLines = []
                upperLines = []
                for i, waypoint in enumerate(newData[airway]["waypoints"]):
                    try:
                        lowerLimit = waypoint["lowerlimit"]
                    except KeyError:
                        lowerLimit = 0

                    try:
                        upperLimit = waypoint["upperlimit"]
                    except KeyError:
                        upperLimit = 0

                    lb = False

                    if i == 0: # special logic for first wpt: only include in lower if next wpt is also in lower
                        if newData[airway]["waypoints"][1]["lowerlimit"] < 245:
                            lowerLines.append(waypoint["name"])
                            lb = True
                    
                    if i == 0:
                        if newData[airway]["waypoints"][1]["upperlimit"] > 245:
                            upperLines.append(waypoint["name"])
                            continue

                    if lb: 
                        continue

                    # two VERY annoying exceptions
                    if airway == "M40" and waypoint["name"] == "IDESI":
                        lowerLines.append("XXXXX")
                        lowerLines.append(waypoint["name"])
                        prevLowerIndex = i
                    elif airway == "L620" and waypoint["name"] == "CLN":
                        lowerLines.append("XXXXX")
                        lowerLines.append(waypoint["name"])
                        prevLowerIndex = i
                    
                    elif lowerLimit < 245:
                        if firstLower:
                            lowerLines.append(waypoint["name"])
                            prevLowerIndex = i
                            firstLower = False
                        elif prevLowerIndex == i - 1:
                            lowerLines.append(waypoint["name"])
                            prevLowerIndex = i
                        else:  # add in spacing line with a filler wpt of `XXXXX`
                            lowerLines.append("XXXXX")
                            lowerLines.append(waypoint["name"])
                            prevLowerIndex = i
                    if upperLimit > 245:  # same logic as above
                        if firstUpper:
                            upperLines.append(waypoint["name"])
                            prevUpperIndex = i
                            firstUpper = False
                        elif prevUpperIndex == i - 1:
                            upperLines.append(waypoint["name"])
                            prevUpperIndex = i
                        else:
                            upperLines.append("XXXXX")
                            upperLines.append(waypoint["name"])
                            prevUpperIndex = i

                # put into file format
                lowerOutput = []
                for i in range(len(lowerLines) - 1):
                    if lowerLines[i] == "XXXXX":
                        lowerOutput.append(";Non-contiguous")
                    elif lowerLines[i + 1] == "XXXXX":
                        pass
                    else:
                        lowerOutput.append(lowerLines[i].ljust(5, " ") + " " + lowerLines[i + 1].ljust(5, " "))
                
                upperOutput = []
                for i in range(len(upperLines) - 1):
                    if upperLines[i] == "XXXXX":
                        upperOutput.append(";Non-contiguous")
                    elif upperLines[i + 1] == "XXXXX":
                        pass
                    else:
                        upperOutput.append(upperLines[i].ljust(5, " ") + " " + upperLines[i + 1].ljust(5, " "))

                print(airway, lowerOutput, upperOutput)
                        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse parts of the UK eAIP, using our AIP API")
    parser.add_argument("page", help="The part of the AIP to parse", choices=["all", "ENR3.2", "ENR4.1", "ENR4.4"])

    args = vars(parser.parse_args())

    runner = Runner(args)

    runner.run()
