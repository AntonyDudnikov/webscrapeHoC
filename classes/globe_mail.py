from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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

    def __init__(self, url: str, release_date: str, driver: webdriver, first:bool) -> None:
        super().__init__()
        self.first = first
        self.driver = driver
        self.output['url'] = url
        self.output['institution'] = 'Statistics Canada'
        self.output['release_date'] = release_date
        self.output['content'] = ''
    
    def _grab_content(self):
        self.output['title'] = self.driver.find_element(By.XPATH, "//*[@id='skip-link-target']/h1").text
        # content = WebDriverWait(self.driver, 5).until(
        #         EC.presence_of_element_located((By.XPATH, "//*[@id='content-gate']/*"))
        #     )
        #//*[@id="skip-link-target"]/h1
            #//*[@id='main-content']/div[1]/header/div/h1
            #//*[@id='skip-link-target']/h1
        content = self.driver.find_element(By.XPATH, "//*[@id='content-gate']")
        print(F"this is the content list: {content}")
        acceptable = ['h1', 'h2', 'h3', 'h4', 'ul', 'p']
        content = content.find_elements(By.XPATH, "./*")
        for section in content:
            if section.tag_name == acceptable[4]: #ul
                self.output['content']+=f"{section.text}:"
                for item in section.find_elements(By.XPATH, './li'):
                    self.output['content']+=f"- {item.text}"
                self.output['content']+="\n"
            elif section.tag_name in acceptable[:4]: #<h>
                self.output['content']+= "\n"+f"heading: {section.text}"+"\n"

            elif section.tag_name == acceptable[-1]: #<p>
                self.output['content']+= section.text
    
    
    def globe_scrape(self):
        self.driver.get(self.output['url'])

        # if self.first:
        #     login = WebDriverWait(self.driver, 30).until(
        #         EC.presence_of_element_located((By.XPATH, "//div[@id='flashsale-paywall']/div/p[3]/a"))
        #     )
        #     login = self.driver.find_element(By.XPATH, "//div[@id='flashsale-paywall']/div/p[3]/a")
        #     login.click()
        #     load_dotenv()
        #     email = WebDriverWait(self.driver, 5).until(
        #         EC.presence_of_element_located((By.XPATH, "//input[@id='inputEmail']"))
        #     )
        #     email = self.driver.find_element(By.XPATH, "//input[@id='inputEmail']")
        #     email.send_keys(os.getenv('GLOBE_EMAIL'))
        #     #self.driver.find_element(By.XPATH, "//input[@id='inputEmail']").send_keys(os.getenv('GLOBE_EMAIL'))
        #     self.driver.find_element(By.XPATH, "//input[@id='inputPassword']").send_keys(os.getenv("GLOBE_PASSWORD"))
        #     self.driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/span/form/button").click()

        """
        //*[@id="main-content"]/div[1]/div
        //*[@id='skip-link-target']/h1

        use a try-except function to get access to the content, if it except, then login and continue
        """
        time.sleep(2)
        try:
            self._grab_content()
        except NoSuchElementException:
            try:
                login = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='primary-paywall']/div[3]/p[3]/a"))
                )
                login = self.driver.find_element(By.XPATH, "//*[@id='primary-paywall']/div[3]/p[3]/a")
                login.click()
                load_dotenv()
                email = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@id='inputEmail']"))
                )
                email = self.driver.find_element(By.XPATH, "//input[@id='inputEmail']")
                email.send_keys(os.getenv('GLOBE_EMAIL'))
                #self.driver.find_element(By.XPATH, "//input[@id='inputEmail']").send_keys(os.getenv('GLOBE_EMAIL'))
                self.driver.find_element(By.XPATH, "//input[@id='inputPassword']").send_keys(os.getenv("GLOBE_PASSWORD"))
                self.driver.find_element(By.XPATH, "//*[@id='app']/div[2]/div/div/span/form/button").click()
                time.sleep(40)
                self._grab_content()
            except TimeoutException or NoSuchElementException:
                time.sleep(30)
                login_button = self.driver.find_element(By.XPATH, "//*[@id='app']/div/div/div[2]/section/div/div[2]/p/a").click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, "//*[@id='inputEmail']").send_keys(os.getenv('GLOBE_EMAIL'))
                self.driver.find_element(By.XPATH, "//*[@id='inputPassword']").send_keys(os.getenv("GLOBE_PASSWORD"))
                self.driver.find_element(By.XPATH, "//*[@id='app']/div/div/div/span/form/button").click()
                self._grab_content()
            """
            //*[@id="app"]/div/div/div[2]/section/div/div[2]/p/a
                //*[@id="inputEmail"]
                //*[@id="inputPassword"]
                //*[@id="app"]/div/div/div/span/form/button
            """


            
        """
        title: //*[@id="skip-link-target"]/h1
        content: //*[@id="content-gate"]/*
        """
        """
        self.output['title'] = self.driver.find_element(By.XPATH, "//div[@class='l-article-title']/header/div/h1").text
        content = self.driver.find_elements(By.XPATH, "//*[@id='content-gate']/*")
        acceptable = ['h1', 'h2', 'h3', 'h4', 'ul', 'p']
        for section in content:
            if section.tag_name == acceptable[4]: #ul
                self.output['content']+=f"{section.text}:"
                for item in section.find_elements(By.XPATH, './li'):
                    self.output['content']+=f"- {item.text}"
                self.output['content']+="\n"
            elif section.tag_name in acceptable[:4]: #<h>
                self.output['content']+= "\n"+f"heading: {section.text}"+"\n"

            elif section.tag_name == acceptable[-1]: #<p>
                self.output['content']+= section.text
        """
        print(f"CONTENT - {self.output['content']}")
        print(f"DONE - {self.output['title']}")
        
