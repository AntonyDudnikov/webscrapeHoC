from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from classes.source import Source
from classes.boc import Boc
from selenium import webdriver
from datetime import datetime
import pprint
import re

"""
INTRUCTIONS:
- purpose of rbc_scrape is to retreive the release meta data and corresponding written content for the email version sent before the website release
- exported in a dictionary
- use this url to see an ex: https://www150.statcan.gc.ca/n1/daily-quotidien/231212/dq231212a-eng.htm

Foward guidance: http://view.website.rbc.com/?qs=252693f6703bfe6d95f0c536c2c7ee9f7244cf155cbfebb7c0d992e5f5b31a311ad856fb417e3136f18422d16689747e4d3c542f49bed74450aa1d874c8eff0315fcb987ab8a6a8a9984a8deeebde978
Current Analysis: http://view.website.rbc.com/?qs=7aa1d53a83f9af89a53641b2b2baaa70861124ec3602afd0c164ca82446dce5f7275f5aee14c5fe5c50771b0354a7cf3baf9e33929c59986bf3f834a7e98e2333b54fdd224be418fdcbae49cac3bc617
Daily Economic Update: http://view.website.rbc.com/?qs=a15bb554423f2e6a43da32adab780a64a077f0addb8582d5923332f64ce294472d01b53f8817b134041c7da41846f02f7037165d5c0398488bfec2dcd050deebe4864bb2b2aeb21102d2bb70cacc6ca2
Financial Martkes Monthly: http://view.website.rbc.com/?qs=a8ecc4d5687bb73ec86c05cdcedcfecab1683ea57ba289c9137a48fe7fe75549dc0389a3bfb7dc1e0ea49c4704a647d3512a4b49c71074a2c52ad55428024ae338f099ae058c41494329685a6bc65709
Canadian and provincial outlook: http://view.website.rbc.com/?qs=b17d27d115dc6462d30b3bf759c2b60df4c4e8545f2f973b9660a45f356c1f9d96414077fb709496fd549c18fa1e1a28fbc37f4731b7c2620365be318d77392a9ea922d8fe1768fbb72456617e5e5160
"""

publication_type = {
    'Forward Guidance': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/dd272ebb-b9e7-43d2-b907-037b4d3e053d.png",
    'Current Analysis': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/3310053c-b208-4c2d-ae96-99b159409d17.png",
    'Daily Economic Update': 'https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/b2db5087-740f-49af-884a-694d1c612a5a.png',
    'Financial Markets Monthly': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/ee274d98-7713-48d3-937e-121d4a74b6a8.png",
    'Canadian and Provincial Outlook': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/7a36074b-b366-4ac2-aaa0-d3ce8d4797a4.png",
    'Focus on Canadian housing':'https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/3/cbf6ae30-b4e6-4d93-89aa-d4253677183f.png'
}
class Rbc(Source):

    def __init__(self, url: str, email:bool, release_date: str, driver:webdriver) -> None:
        super().__init__()
        self.driver = driver
        self.output['url'] = url
        self.output['format'] = 'email' if email else 'website'
        self.output['release_date'] = release_date
        self.output['institution'] = 'RBC'
        self.publication_type = {
            'Forward Guidance': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/dd272ebb-b9e7-43d2-b907-037b4d3e053d.png",
            'Current Analysis': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/3310053c-b208-4c2d-ae96-99b159409d17.png",
            'Daily Economic Update': 'https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/b2db5087-740f-49af-884a-694d1c612a5a.png',
            'Financial Markets Monthly': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/ee274d98-7713-48d3-937e-121d4a74b6a8.png",
            'Canadian and Provincial Outlook': "https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/2/7a36074b-b366-4ac2-aaa0-d3ce8d4797a4.png",
            'Focus on Canadian housing':'https://image.website.rbc.com/lib/fe8d1574706d057b7d/m/3/cbf6ae30-b4e6-4d93-89aa-d4253677183f.png'
            }           

    def rbc_email_scrape(self):
        self.driver.get(self.output['url'])
        
        sections = self.driver.find_elements(By.XPATH, "//td[@class='responsive-td']") #all <table> blocks of the web
        self.output['p_first'] = True
        self.output['headings'] = []
        """
        section[1]: image of rbc publicaiton type
        section[2]: title block with possible date
        section[3]: body of the publication 
        """
        #------publication type------/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/a/img
        image = sections[1].find_element(By.TAG_NAME, 'img')
        test = [i for i in publication_type if publication_type[i] == image.get_attribute('src')]
        if test:
            self.output['RBC type'] = test[0]
        else:
            print('NEW RBC TYPE')
            self.output['RBC type'] = 'Other'
        #------date------
        try:
            date_text = sections[2].find_element(By.TAG_NAME, 'p')
            if date_text.text != "":
                date = re.search( r'(\b\w+ \d{1,2}\w*, \d{4}\b)', date_text.text).group() #extract date
                date = date.replace('th', '').replace('rd', '').replace('nd', '').replace('st', '') #remove any suffix
                self.output['release_date'] = datetime.strptime(date, "%B %d, %Y").strftime("%d/%m/%Y") #convert to format
                self.output['scrape_date'] = datetime.today().strftime("%d/%m/%Y") #todays date formatted
            else:
                self.output['release_date'] = datetime.today().strftime("%d/%m/%Y")
                self.output['scrape_date'] = datetime.today().strftime("%d/%m/%Y") 
        except:
            self.output['release_date'] = datetime.today().strftime("%d/%m/%Y")
            self.output['scrape_date'] = datetime.today().strftime("%d/%m/%Y")  

        #------title------
        self.output['title'] = sections[2].find_element(By.TAG_NAME, 'h1').text

        #------content------
        #FIX ISSUES
        tables = sections[3].find_elements(By.XPATH, "./*")#list of all word elements
        self.output['content'] = [x.text for x in tables]
        for x in range(len(self.output['content'])):
            self.output['content'][x] = re.sub("\n", ' - ', self.output['content'][x])

        #------graphs------
        images = sections[3].find_elements(By.TAG_NAME, "img")
        self.output["images"] = [s.get_attribute("src") for s in images]


    def rbc_website_scrape(self):
        self.driver.get(self.output['url'])

        #------date------
        date = self.driver.find_element(By.XPATH, "//p[@class='byline text-script']")
        release_date = re.search( r'(\w+ \d{1,2}, \d{4})', date.text).group()
        release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
        self.output['release_date'] = release_date

        #------title------
        category = self.driver.find_element(By.XPATH, "//*[@id='page-title']").text
        title = self.driver.find_element(By.XPATH, "//main/section[@class='banner html-bnr']").find_element(By.TAG_NAME, 'h1').text
        self.output['title'] = title
        self.output['category'] = category
        #------highlights------
        content = self.driver.find_elements(By.XPATH, "//div[@class='article-content']/*")
        self.output['headings'] = []
        self.output['content'] = []
        aggregate = False #indicator to show whether to combine the <p>
        acceptable = ['h1', 'h2', 'h3', 'h4', 'ul', 'p']
        not_acceptable = ["See previous versions:", "Disclaimer", "See our Canadian Inflation Watch here.", "Read the full Housing Trends and Affordability report for extensive market-by-market analysis."]
        #p_first logic
        done = False
        i = 0
        while not done:
            if content[i].tag_name == 'p':
                self.output['p_first'] = True
                done = True
            elif content[i].tag_name in acceptable[:4]:
                self.output['p_first'] = False
                done = True
            i += 1

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


    
        
        
                

"""test
ECONOMICS
https://thoughtleadership.rbc.com/all-quiet-on-most-fronts-in-canadas-housing-markets/
https://thoughtleadership.rbc.com/rbc-inflation-watch/
https://thoughtleadership.rbc.com/rbc-consumer-spending-tracker/

SPECIAL REPORTS
https://thoughtleadership.rbc.com/rbc-consumer-spending-tracker/
https://thoughtleadership.rbc.com/rbc-us-inflation-watch/

HOUSING AFFORDABILITY
https://thoughtleadership.rbc.com/high-rates-and-prices-make-it-less-affordable-to-own-a-home-in-canada/

MONHTLY HOUSING MARKET
https://thoughtleadership.rbc.com/canadas-housing-market-downturn-is-spreading/
"""