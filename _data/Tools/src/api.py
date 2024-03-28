from util import airac, util

import requests
from bs4 import BeautifulSoup
from loguru import logger
import re

class AipAPI:
    def __init__(self):
        self.airac = airac.Airac()
        self.cycle = self.airac.cycle()
        self.rootUrl = self.airac.url()

    def parseENR3_2(self) -> dict[str,dict]:
        """Parse the AIP ENR3.2 page

        Returns:
            dict[str,dict]: A dictionary containing the airway identifier and some information about it (see example below)
            {
                "L6": {"waypoints": [{"name": "DVR", "lowerlimit": 85, "upperlimit": 460}, {"name": "DET"}]},
                ...
            }
        """
        url = self.rootUrl + "EG-ENR-3.2-en-GB.html"
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")

        enr32 = soup.find("div", attrs={"id": "ENR-3.2"})
        airways = list(enr32.children)[1:]

        outputs = {}

        for airway in airways:
            if "AmdtInsertedAIRAC" in str(airway):  # skip amendments
                continue
            tbody = list(airway.children)[2]
            wpts = list(tbody.children)
            routeTitleHTML = wpts[0]
            airwayName = list(list(list(routeTitleHTML.children)[0].children)[0].children)[1].string

            if airwayName == "N84":  # badly formatted airway
                continue

            outputs[airwayName] = {"waypoints": []}

            wpts.pop(0)  # remove name

            # deal with first wpt
            wptName = list(list(wpts[0].children)[1].children)
            if len(wptName) > 4:  # VOR/DME
                wptName = wptName[5].string
            else: # FIX
                wptName = wptName[1].string

            wpts.pop(0)

            outputs[airwayName]["waypoints"].append({"name": wptName})

            # deal with rest of wpts

            for i in range(0, len(wpts), 2):  # pair waypoint names with their data
                wptHTML = wpts[i + 1]
                wptName = list(list(wptHTML.children)[1].children)
                if len(wptName) > 4:  # VOR/DME
                    wptName = wptName[5].string
                else: # FIX
                    wptName = wptName[1].string
                # print(wptName)

                try:
                    wptDataHTML = wpts[i]

                    upperLowerBox = list(list(wptDataHTML.children)[3].children)[0]

                    if airwayName == "N22" and wptName == "BHD":  # for some reason only this waypoint is in a different format :facepalm:
                        upperLimit = 245
                        lowerLimit = 85
                    else:
                        upperLimit = list(list(list(list(list(list(upperLowerBox.children)[0].children)[0].children)[0].children)[0].children)[0].children)[4].string
                        lowerLimit = list(list(list(list(list(list(upperLowerBox.children)[0].children)[0].children)[1].children)[0].children)[0].children)
                        if "FT" in lowerLimit[4].string:
                            lowerLimit = lowerLimit[1].string[:2]
                        else:
                            lowerLimit = lowerLimit[4].string
                    
                    outputs[airwayName]["waypoints"].append({"name": wptName, "lowerlimit": int(lowerLimit), "upperlimit": int(upperLimit)})
                except IndexError:
                    outputs[airwayName]["waypoints"].append({"name": wptName})
                except AttributeError:
                    print(airwayName, wptName)
                    raise ValueError  # NATS broke something if this gets run :(

                # wptLowerLimit = list(list(wpt.children)[1].children)[0].string
                # wptUpperLimit = list(list(wpt.children)[1].children)[2].string
                # print(f"{wptName} {wptLowerLimit} {wptUpperLimit}")
        
        return outputs


    def parseENR4_1(self) -> dict[str,dict]:
        """Parse the AIP ENR4.1 page

        Returns:
            dict[str,dict]: A dictionary containing the VOR identifier and some information about it (see example below)
            {
                "ADN": {"name": "Aberdeen", "frequency": "114.300", "coordinates": ("N057.18.37.620", "W002.16.01.950")},  # name, frequency, coordinates
                ...
            }
        """

        url = self.rootUrl + "EG-ENR-4.1-en-GB.html"
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")

        # get table rows from heading

        ad22 = soup.find("div", attrs={"id": "ENR-4.1"})
        rows = list(list(ad22.children)[1].children)[1].children

        outputs = {}

        for row in rows:
            name = list(list(list(row.children)[0].children)[1].children)[1].string
            name = util.capitalise(name)

            vorDmeNdb = str(list(list(row.children)[0].children)[3])
            if re.search(r"NDB", vorDmeNdb):
                continue # skip NDBs
            elif re.search(r"DME", vorDmeNdb) and not re.search(r"VOR", vorDmeNdb):
                name += " (DME)"  # add DME to the name if it's only a DME

            identifier = list(list(row.children)[1].children)[1].string

            freq = list(list(list(row.children)[2].children)[1].children)[1].string
            try:
                float(freq)
            except ValueError:
                if identifier == "LON":  # LON's frequency isn't on the AIP
                    freq = "113.600"
                else:
                    freq = list(list(list(row.children)[2].children)[3].children)[1].string

            coordA = list(list(list(row.children)[4].children)[0].children)[1].string
            coordB = list(list(list(row.children)[4].children)[1].children)[1].string
            coords = util.ukCoordsToSectorFile(coordA, coordB)

            # logger.debug(f"{identifier} {freq} {' '.join(coords)} ; {name}")

            outputs[identifier] = {"name": name, "frequency": freq, "coordinates": coords}
        
        return outputs
    
    def parseENR4_4(self) -> dict[str,dict]:
        """Parse the AIP ENR4.4 page

        Returns:
            dict[str,dict]: A dictionary containing the FIX identifier and some information about it (see example below)
            {
                "ABBEW": {"coordinates": ("N050.30.11.880", "W003.28.33.640")},  # coordinates
                ...
            }
        """
        url = self.rootUrl + "EG-ENR-4.4-en-GB.html"
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")

        # get table rows from heading

        table = soup.find("table", attrs={"class": "ENR-table"})
        rows = list(list(table.children)[1].children)

        outputs = {}

        for row in rows:
            fixName = list(list(row.children)[0].children)[1].string
            coordA = list(list(list(row.children)[1].children)[0].children)[1].string
            coordB = list(list(list(row.children)[1].children)[1].children)[1].string
            coords = util.ukCoordsToSectorFile(coordA, coordB)

            outputs[fixName] = {"coordinates": coords}

        return outputs
