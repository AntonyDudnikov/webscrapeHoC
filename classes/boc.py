from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from classes.source import Source
import pprint
import json
import re

class Boc(Source):
    """
    Class
    """
    def __init__(self, url: str, type: str, release_date: str, driver:webdriver) -> None:
        super().__init__()
        self.driver = driver
        self.output['url'] = url
        self.output['type'] = type
        self.output['release_date'] = release_date
        self.output['institution'] = 'Bank of Canada'

    def _unwrap_content(self, content) -> list:
        """
        To unwrap the list of web elements to obtain the higher dimension 
        WebElements in each of the list items. Each input item has a further
        <div> before the <h>/<p>/<ul>
        INPUT:
        content: list of WebElements that represent the blocks of <h> and <p>

        OUTPUT:
        content_webelements: list of children WebElements of each input's elements
        """
        content_webelements = []
        for x in content:
            foo = x.find_elements(By.XPATH, './div/*')
            for lower in foo:
                content_webelements.append(lower)
        return content_webelements

    def _content_scrape(self, content) -> tuple:
        """
        Helper function to minimize clutter in boc_scrape. Mean to extract
        the information from a list of the webelement blocks that encompass
          the body.

        INPUT:
        content: list of <div> webelements that act as blocks of information
        that seperate the headings
        type: indicator variable to identify the type of BoC publication

        OUTPUT:
        p_first: bool indicator to specify order of headings and content
        headings: list of string headings
        body: list of string body of paragraphs

        Logic:
            - to increase dimensionality of webelement that houses the body
              of the report up to the webelement that has the direct info
            - identify it, see if it's a heading, a <p>/<ul> that would eiher
              need to be aggregated and added to output or just added
        """
        headings = []
        body = []
        content = self._unwrap_content(content) #extract the higher dimension web elements (the elemnts inside the div)
        aggregate = False
        acceptable = ['h2', 'h3', 'h4', 'ul', 'p']
        p_first = content[0] in acceptable[3:]
        for child in content:
            if child.tag_name in ['h2', 'h3', 'h4']:
                headings.append(child.text)
                aggregate = False
            elif child.tag_name == 'ul':
                if aggregate:
                    for item in child.find_elements(By.XPATH, './li'):
                        body[-1] = body[-1] + ' ' + f"- {item.text}"
                else:
                    body.append(f"- {child.text}")
                aggregate = True
            elif child.tag_name in 'p':
                if aggregate: #consecutive <p>, so concatenate text to last item in content
                    body[-1] = body[-1] + ' ' + child.text
                else:
                    body.append(child.text)
                aggregate = True
            else:
                #indicator of whether there where tables/graphs not recorded
                self.output['charts'] = True
        return (p_first, headings, body)

    def boc_scrape(self):

        self.driver.get(self.output['url']) #load in the page
        if self.output['type'] == 'research': #if this page is research
            pass
        elif self.output['type'] == 'Quarterly Financial Report': # if its a Quarterly Financial Report 
            """
            seperate the qquaterly and summary of deliberations
            - release date grabbing is differenet
            - the XML path to content is different 
            use the helper function to extract the content
            """
            content = self.driver.find_element(By.XPATH, "//main[@id='main-content']").find_elements(By.CLASS_NAME, 'row')

            #_______title_______
            title = content[0].find_element(By.XPATH, "//h1[@class='post-heading']").text
            self.output['title'] = title

            #_______body_______
            body = content[1].find_elements(By.XPATH, './div/*')
            self.output['p_first'], self.output['headings'], self.output['content'] = self._content_scrape(body[1:-2])
            self.output['charts'] = False
            
        elif self.output['type'] == 'Summary of deliberations': # if its a Summary of Deliberations
            content = self.driver.find_elements(By.XPATH, "//main[@id='main-content']/div/div/div/*")

            #_______title & date_______
            self.output['title'] = content[0].find_element(By.TAG_NAME, 'h1')
            release_date = content[0].find_element(By.CLASS_NAME, 'post-date').text
            release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_date).group()
            self.output['release_date'] = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")

            #_______body_______

            self.output['p_first'], self.output['headings'], self.output['content'] = self._content_scrape(content[2:-1])
        else:
            pass


