import unittest
from classes import boc

"""
things to check:
    - 
    - 
    - 
    - 

framework:
    - setup:
        - instatiate the driver
    - run code
    - teardown:
        - close the driver
    - last call is to quit() the driver
"""


class TestBoc(unittest. TestCase):
    def test_scrape(self):
        boc1 = boc.Boc(url='https://www.bankofcanada.ca/2023/11/quarterly-financial-report-third-quarter-2023/',
                type='Quarterly Financial Report',
                release_date='30/09/2023')
        boc1.boc_scrape()   



if __name__ is "__main__":
    unittest.main()