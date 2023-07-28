import api

import argparse

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse parts of the UK eAIP, using our AIP API")
    parser.add_argument("page", help="The part of the AIP to parse", choices=["all", "ENR4.1", "ENR4.4"])

    args = vars(parser.parse_args())

    runner = Runner(args)

    runner.run()
