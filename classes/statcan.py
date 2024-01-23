from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from classes.source import Source
from selenium import webdriver
from datetime import datetime
import random
import time
import re

"""
INTRUCTIONS:
- purpose of statcan_scrape is to retreive the release meta data and corresponding written content and data tables
- exported in a dictionary
- use this url to see an ex: https://www150.statcan.gc.ca/n1/daily-quotidien/231212/dq231212a-eng.htm
"""
class Statcan(Source):

    def __init__(self, url: str, release_date: str, driver: webdriver) -> None:
        super().__init__()
        self.driver = driver
        self.output['url'] = url
        self.output['institution'] = 'Statistics Canada'
        self.output['release_date'] = release_date

    def statcan_scrape(self):
        self.driver.get(self.output['url'])

        #----- Meta Data -----
        self.output['title'] = self.driver.find_element(By.XPATH, '//*[@id="wb-cont"]').text #title
        # release_date = self.driver.find_element(By.XPATH, "//p[@class='sd-release-date']").text #get release date
        # release_date = re.search(r'\d{4}-\d{2}-\d{2}', release_date).group() #extract it
        # self.output['release_date'] = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d/%m/%Y") #convert it
        #section_content = driver.find_element(By.XPATH, '/html/body/main/section') #overall html section path
        
        elements = self.driver.find_elements(By.XPATH, '/html/body/main/section/*') #all the children
        headings = []
        content = []
        aggregate = False
        #----- p_first -----
        done = False
        i = 2
        while not done:
            if elements[i].tag_name == 'p':
                print()
                self.output['p_first'] = True
                done = True
            elif elements[i].tag_name == 'h2':
                self.output['p_first'] = False
                done = True
            i += 1
        #----- Content -----
        for element in elements[2::]: #iterate all values past the release date on webpage
            if element.tag_name == 'p':
                if aggregate: #consecutive <p>, so concatenate text to last item in content
                    content[-1] = content[-1] + ' ' + element.text
                else:
                    content.append(element.text)
                aggregate = True
            elif element.tag_name == 'h2':
                aggregate = False
                stopwords = ['Contact information', 'Products', 'Looking for more insight?']
                if element.text not in stopwords:
                    headings.append(element.text)
                else:
                    break
            else:
                pass
                #print(f"something else came up: {element.tag_name}")
        self.output['headings'] = headings
        self.output['content'] = content
        
        #----- Data Tables -----
        try:
            buttons =self.driver.find_element(By.CLASS_NAME, 'release_nav').find_elements(By.XPATH, './*')
            tables = buttons[1].click()
            time.sleep(random.randint(2,5))
            release_list = self.driver.find_elements(By.XPATH, '//*[@id="release-list"]/tbody/*')
            self.output['data_tables'] = {}
            for table in release_list:
                raw_title = table.find_element(By.TAG_NAME, 'h3').text
                title = re.sub(re.compile(r'\([^)]*\)'), '', raw_title)
                unit = re.findall(r'\([^)]*\)', raw_title)[0].replace(")", '').replace("(", '')
                self.output['data_tables'][title] = {
                    'unit': unit, #quaterly/annual
                    'url': table.find_element(By.TAG_NAME, 'a').get_attribute('href') #reference url
                }
        except NoSuchElementException:
            print("No tables.")





    
