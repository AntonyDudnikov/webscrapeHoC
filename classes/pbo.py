from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from classes.source import Source
from selenium import webdriver
from datetime import datetime
import pprint
import random
import time
import re

class Pbo(Source):
    def __init__(self, url: str, report: bool, release_date: str, title: str, driver) -> None:
        super().__init__()
        self.report = report
        self.driver = driver
        self.output['url'] = url
        self.output['type'] = 'Report' if report else 'Legislative Costing Note'
        self.output['release_date'] = release_date
        self.output['institution'] = 'Parliamentary Budget Officer'
        self.output['title'] = title
        self.output['p_first'] = True
        self.output['headings'] = []
        self.output['content'] = []


    def _table_extraction(self, table) -> dict:
        """
        Extracts the table within a pbo legislative costing note from a WebElement object to a dict
        input:
            - WebElement of the <table> element
        output:
            - two dimensional dict where, first dim. is the first column value and the 2nd dim. are the values
        """
        column_names = [i.text for i in (table.find_elements(By.XPATH, './thead/tr/*'))]
        column_names = [i.replace("\xad", "") if ("\xad" in i) else i for i in column_names]
        rows = table.find_elements(By.XPATH, './tbody/*')
        output = {}
        for r in rows:
            elements = [i.text for i in (r.find_elements(By.XPATH, './*'))]
            output[elements[0]] = dict(zip(column_names[1:], elements[1:]))
        return output

    def pbo_scrape(self):
        """
        Scrapes all the content and exports in a dicitonary
        Inputs:
            - url: url of the website to scrape
            - report: the type of release, as the xml formatting is different for both types
        Outputs:
            - dicitonary of title, highlights, summary
        """
        
        self.driver.get(self.output['url'])
        if self.report:
            self.output['headings'].append('Summary')
            aggregate = False
            #----- Summary -------
            summ = self.driver.execute_script("""return document.querySelector('div#pb-art pboml-parser').shadowRoot.querySelector('section[id="markdown-2"]')""")
            summary_items = summ.find_elements(By.XPATH, "./div/*")
            for section in summary_items:
                if section.tag_name == 'ul': #ul
                    if aggregate:
                            for item in section.find_elements(By.XPATH, './li'):
                                self.output['content'][-1] = self.output['content'][-1] + ' ' + f"- {item.text}"
                    else:
                            self.output['content'].append(f"- {section.text}")
                    aggregate = True
                elif section.tag_name == 'p': #<p>
                    if aggregate: #consecutive <p>, so concatenate text to last item in content
                        self.output['content'][-1] = self.output['content'][-1] + ' ' + section.text
                    else:
                        self.output['content'].append(section.text)
                    aggregate = True

                
        else: #legislative costing note 
            #----- Summary -----
            self.output['summary'] = self.driver.find_element(By.XPATH, "//div[@id='pb-abs']").text #sumamry of the costing note
        
            #----- Content -----
            content = self.driver.execute_script("""return document.querySelector('div#pb-art pboml-parser').shadowRoot.querySelector('main[class="flex flex-col gap-8 print:block"]')""")
            sections = content.find_elements(By.XPATH, './*')
            self.output['headings'] = []
            self.output['content'] = []
            self.output['tables'] = {}
            #first section
            self.output['content'].append(sections[0].find_element(By.XPATH, "./div[@class='pboml-prose']").text)
            for item in sections[1:]:
                #print('___________')
                try:
                    heading = item.find_element(By.XPATH, './h2')
                    tables = item.find_elements(By.TAG_NAME, 'table')
                    if heading.text not in ['Data Sources', 'Note', 'Prepared by', ''] and not tables:
                        self.output['headings'].append(heading.text)
                        body = item.find_element(By.XPATH, "./div[@class='pboml-prose']").text
                        self.output['content'].append(body)
                    elif tables:
                        self.output['tables'][item.find_element(By.TAG_NAME, 'h2').text] = self._table_extraction(content.find_element(By.TAG_NAME, 'table'))
                    else:
                        pass
                except: 
                    pass    