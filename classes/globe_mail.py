from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from classes.source import Source
from selenium import webdriver
from datetime import datetime
from dotenv import load_dotenv
import random
import time
import re
import os

class GlobeMail(Source):

    def __init__(self, url: str, release_date: str, driver: webdriver) -> None:
        super().__init__()
        self.driver = driver
        self.output['url'] = url
        self.output['institution'] = 'Statistics Canada'
        self.output['release_date'] = release_date
    
    def globe_scrape(self):
        self.driver.get(self.output['url'])
        #main = self.driver.find_elements(By.XPATH, "//*[@id='main-content']/*")
        log_in = self.driver.find_element(By.XPATH, "//*[@id='flashsale-paywall']/div/p[3]/a")
        #//*[@id="app"]/div[2]/div/div/span/form/div[2]/div/div
        log_in.click()
        time.sleep(1)
        # element = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "myDynamicElement"))
        # )
        load_dotenv()
        self.driver.find_element(By.XPATH, "//*[@id='inputEmail']").send_keys(os.getenv('GLOBE_EMAIL'))
        self.driver.find_element(By.XPATH, "//*[@id='inputPassword']").send_keys(os.getenv("GLOBE_PASSWORD"))
        self.driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/span/form/button").click()
        time.sleep(5)
        """
        title: //*[@id="skip-link-target"]/h1
        content: //*[@id="content-gate"]/*
        """
        self.output['title'] = self.driver.find_element(By.XPATH, "//*[@id='skip-link-target']/h1").text
        content = self.driver.find_elements(By.XPATH, "//*[@id='content-gate']/*")
        aggregate = False
        acceptable = ['h1', 'h2', 'h3', 'h4', 'ul', 'p']
        for section in content:
            if section.tag_name == acceptable[4]: #ul
                if aggregate:
                        for item in section.find_elements(By.XPATH, './li'):
                            self.output['content'][-1] = self.output['content'][-1] + ' ' + f"- {item.text}"
                else:
                        self.output['content'].append(f"- {section.text}")
                aggregate = True

            elif section.tag_name in acceptable[:4]: #<h>
                aggregate = False
                self.output['headings'].append(section.text)

            elif section.tag_name == acceptable[-1] and section.text not in not_acceptable: #<p>
                if aggregate: #consecutive <p>, so concatenate text to last item in content
                    self.output['content'][-1] = self.output['content'][-1] + ' ' + section.text
                else:
                    self.output['content'].append(section.text)
                aggregate = True
        print("DONE")
