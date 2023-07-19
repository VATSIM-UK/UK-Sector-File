import math
import datetime
from datetime import date

class Airac:
    '''Class for general functions relating to AIRAC'''

    def __init__(self):
        # First AIRAC date following the last cycle length modification
        startDate = "2019-01-02"
        self.baseDate = date.fromisoformat(str(startDate))
        # Length of one AIRAC cycle
        self.cycleDays = 28

    def initialise(self, dateIn=0):
        # Calculate the number of AIRAC cycles between any given date and the start date
        if dateIn:
            inputDate = date.fromisoformat(str(dateIn))
        else:
            inputDate = date.today()

        # How many AIRAC cycles have occured since the start date
        diffCycles = (inputDate - self.baseDate) / datetime.timedelta(days=1)
        # Round that number down to the nearest whole integer
        numberOfCycles = math.floor(diffCycles / self.cycleDays)

        return numberOfCycles

    def currentCycle(self):
        # Return the date of the current AIRAC cycle
        numberOfCycles = self.initialise()
        numberOfDays = numberOfCycles * self.cycleDays + 1
        currentCycle = self.baseDate + datetime.timedelta(days=numberOfDays)
        print(f"Current AIRAC Cycle is: {currentCycle}")
        return currentCycle

    def nextCycle(self):
        # Return the date of the next AIRAC cycle
        numberOfCycles = self.initialise()
        numberOfDays = (numberOfCycles + 1) * self.cycleDays + 1
        return self.baseDate + datetime.timedelta(days=numberOfDays)

    def url(self, next:bool=True):
        # Return a generated URL based on the AIRAC cycle start date
        baseUrl = "https://www.aurora.nats.co.uk/htmlAIP/Publications/"
        if next:
            baseDate = self.nextCycle() # if the 'next' variable is passed, generate a URL for the next AIRAC cycle
        else:
            baseDate = self.currentCycle()

        basePostString = "-AIRAC/html/eAIP/"

        formattedUrl = baseUrl + str(baseDate) + basePostString
        print(formattedUrl)
        return formattedUrl
