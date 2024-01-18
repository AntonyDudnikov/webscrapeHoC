from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from classes import statcan
import unittest




"""
things to check:
    - release date, retrieval
    - release date right format
    - the p_first logic, equal number of list items or +1 items
    - test first & last paragraph content
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


class TestStatcan(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        runs before any test occurs
        """
        service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
        options= webdriver.ChromeOptions()
        options.add_argument('headless')
        cls.driver = webdriver.Chrome(options=options, service=service)
        
    @classmethod
    def tearDownClass(cls):
        """
        runs after all the tests
        """
        cls.driver.quit()

    # @classmethod
    # def setUp(self):
    #     """
    #     runs before each etst
    #     - set up driver here
    #     """
    #     pass

    # @classmethod
    # def tearDown(self):
    #     """
    #     runs after each test
    #     """
    #     pass

    def test_scrape(self):
        stat1 = statcan.Statcan(url="https://www150.statcan.gc.ca/n1/daily-quotidien/240111/dq240111a-eng.htm", release_date='11/01/2024', driver=self.driver)
        stat1.statcan_scrape()
        self.assertEqual(len(stat1.output['content']), len(stat1.output['headings']))

if __name__ == "__main__":
    unittest.main()