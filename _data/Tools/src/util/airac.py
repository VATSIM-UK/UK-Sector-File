"""
eAIP Parser
Chris Parkinson (@chssn)
"""

# Standard Libraries
import math
from datetime import date, timedelta

# Third Party Libraries
from loguru import logger

# Local Libraries

class Airac:
    """Class for general functions relating to AIRAC"""

    def __init__(self):
        # First AIRAC date following the last cycle length modification
        start_date = "2020-01-02"  # 2001
        self.base_date = date.fromisoformat(str(start_date))
        # Length of one AIRAC cycle
        self.cycle_days = 28

        self.cycles = -1

    def initialise(self, date_in=0) -> int:
        """Calculate the number of AIRAC cycles between any given date and the start date"""

        if date_in:
            input_date = date.fromisoformat(str(date_in))
        else:
            input_date = date.today()

        # How many AIRAC cycles have occured since the start date
        diff_cycles = (input_date - self.base_date) / timedelta(days=1)
        # Round that number down to the nearest whole integer
        self.cycles = math.floor(diff_cycles / self.cycle_days)

        return self.cycles

    def cycle(self, next_cycle:bool=False) -> str:
        """Return the date of the current AIRAC cycle"""

        if self.cycles == -1:  # only initialise if not already done
            self.cycles = self.initialise()

        if next_cycle:
            number_of_days = (self.cycles + 1) * self.cycle_days
        else:
            number_of_days = self.cycles * self.cycle_days
        current_cycle = self.base_date + timedelta(days=number_of_days)
        logger.debug("Current AIRAC Cycle is: {}", current_cycle)

        return current_cycle

    def url(self, next_cycle:bool=False) -> str:
        """Return a generated URL based on the AIRAC cycle start date"""

        base_url = "https://www.aurora.nats.co.uk/htmlAIP/Publications/"
        if next_cycle:
            # if the 'next_cycle' variable is passed, generate a URL for the next AIRAC cycle
            base_date = self.cycle(next_cycle=True)
        else:
            base_date = self.cycle()

        base_post_string = "-AIRAC/html/eAIP/"

        formatted_url = base_url + str(base_date) + base_post_string
        logger.debug(formatted_url)

        return formatted_url
