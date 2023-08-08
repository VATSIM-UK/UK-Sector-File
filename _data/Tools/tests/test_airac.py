import unittest
from datetime import date
from src.util import airac

class TestAirac(unittest.TestCase):
    def setUp(self):
        self.airac = airac.Airac()

    def test_initialise(self):
        self.assertEqual(self.airac.initialise("2020-01-02"), 0)  # 0 date
        self.assertEqual(self.airac.initialise("2023-07-12"), 45) # random date
        self.assertEqual(self.airac.initialise("2023-07-19"), 46) # random date
        self.assertEqual(self.airac.initialise("2023-08-09"), 46) # edge case
        self.assertEqual(self.airac.initialise("2023-08-10"), 47) # edge case
        self.assertEqual(self.airac.initialise("2028-12-20"), 116) # far edge case
        self.assertEqual(self.airac.initialise("2028-12-21"), 117) # far edge case

    def test_cycle(self):
        # next_cycle = False
        self.airac.initialise("2020-01-02")
        self.assertEqual(self.airac.cycle(), date(2020, 1, 2)) # 0 date
        self.airac.initialise("2021-05-16")
        self.assertEqual(self.airac.cycle(), date(2021, 4, 22)) # random date
        self.airac.initialise("2023-12-27")
        self.assertEqual(self.airac.cycle(), date(2023, 11, 30)) # edge case
        self.airac.initialise("2023-12-28")
        self.assertEqual(self.airac.cycle(), date(2023, 12, 28)) # edge case

        # next_cycle = True
        self.airac.initialise("2020-01-02")
        self.assertEqual(self.airac.cycle(next_cycle=True), date(2020, 1, 30)) # 0 date
        self.airac.initialise("2021-05-16")
        self.assertEqual(self.airac.cycle(next_cycle=True), date(2021, 5, 20)) # random date
        self.airac.initialise("2023-12-27")
        self.assertEqual(self.airac.cycle(next_cycle=True), date(2023, 12, 28)) # edge case
        self.airac.initialise("2023-12-28")
        self.assertEqual(self.airac.cycle(next_cycle=True), date(2024, 1, 25)) # edge case

    def test_url(self):
        # next_cycle = False
        self.airac.initialise("2020-01-02")
        self.assertEqual(self.airac.url(next_cycle=False), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2020-01-02-AIRAC/html/eAIP/") # 0 date
        self.airac.initialise("2021-05-16")
        self.assertEqual(self.airac.url(next_cycle=False), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2021-04-22-AIRAC/html/eAIP/") # random date
        self.airac.initialise("2023-12-27")
        self.assertEqual(self.airac.url(next_cycle=False), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2023-11-30-AIRAC/html/eAIP/") # edge case
        self.airac.initialise("2023-12-28")
        self.assertEqual(self.airac.url(next_cycle=False), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2023-12-28-AIRAC/html/eAIP/") # edge case

        # next_cycle = True
        self.airac.initialise("2020-01-02")
        self.assertEqual(self.airac.url(next_cycle=True), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2020-01-30-AIRAC/html/eAIP/") # 0 date
        self.airac.initialise("2021-05-16")
        self.assertEqual(self.airac.url(next_cycle=True), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2021-05-20-AIRAC/html/eAIP/") # random date
        self.airac.initialise("2023-12-27")
        self.assertEqual(self.airac.url(next_cycle=True), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2023-12-28-AIRAC/html/eAIP/") # edge case
        self.airac.initialise("2023-12-28")
        self.assertEqual(self.airac.url(next_cycle=True), "https://www.aurora.nats.co.uk/htmlAIP/Publications/2024-01-25-AIRAC/html/eAIP/") # edge case


if __name__ == '__main__':
    unittest.main()
