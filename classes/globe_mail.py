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

        if self.first:
            self.driver.get("https://sec.theglobeandmail.com/user/login?intcmp=site-header")
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='inputEmail']"))
            )
            self.driver.find_element(By.XPATH, "//input[@id='inputEmail']").send_keys(os.getenv('GLOBE_EMAIL'))
            self.driver.find_element(By.XPATH, "//input[@id='inputPassword']").send_keys(os.getenv("GLOBE_PASSWORD"))
            self.driver.find_element(By.XPATH, "//*[@id='app']/div/div/div/span/form/button").click()
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.XPATH, "//*[@id='skip-link-target']/h1"))
            # )
            time.sleep(5)
            self._grab_content()
        else:
            self._grab_content()

        print(f"CONTENT - {self.output['content']}")
        print(f"DONE - {self.output['title']}")
    
if __name__ == "__main__":
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    options= webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)
    globe = GlobeMail("https://www.theglobeandmail.com/world/article-former-tennis-pro-roger-federer-tells-students-that-effortless-is-a/", "12/06/2024", driver, True) 
    globe.globe_scrape()
    print(globe.output['content'])
        
#//*[@id="site-header"]/header/div[1]/div/div[3]/div/a Log in button
#/html/body/div[1]/div[1]/div[1]/header/div[1]/div/div[3]/div/a