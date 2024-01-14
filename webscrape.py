from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#import undetected_chromedriver as uc
import random
import time
import re
from datetime import date

results = { 
    'statCan':
        {'urlDaily': 
            {'url': 'https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/rel-com/all_subjects-eng.htm',
            'check': 'statcan',
            'xpath':
                {'title': '//*[@id="wb-cont"]',
                'release_date': '/html/body/main/section/p[1]',
                'body': '/html/body/main/section'
                }        
            },
         },
    'rbcFG':
        {'urlEmail':
            {'url': 'https://www.view.website.rbc.com/',
             'check' : 'website.rbc',
             #xpath for the table row <tr> that holds the release date and heading
             'xpath':
                {'date': "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/p/em",
                 'title': "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/h1",
                }
             
            }, 
         },
    'pbo':
        {'url': 'https://www.pbo-dpb.ca/en/publications/RP-2324-020-S--costing-support-ev-battery-manufacturing--etablissement-couts-soutien-accorde-fabrication-batteries-ve'},
    'fraser':
        {'url': 'https://www.fraserinstitute.org/studies/thinking-about-poverty-part-3-helping-the-poor-a-critical-analysis-of-poverty-policy-in-canada'},
    'bankOfCanada':{}
}


def webscrape(url:str):
    #dictionary to output
    result = {'date':date.today()}
    load_page = random.randint(5,10)
    next_element = random.randint(5,10)
    result['url'] = url
    #options = uc.ChromeOptions() 
    #options.headless = False
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe") #load driver
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    #time.sleep(load_page)
    #time.sleep(5)
    if re.search(r"statcan", url):
        result['title'] = driver.find_element(By.XPATH, results['statCan']['xpath']['title']).text
        result['release_date'] = driver.find_element(By.XPATH, results['statCan']['xpath']['release_date']).text
        result['institution_name'] = 'Statistics Canada'
        section_content = driver.find_element(By.XPATH, '/html/body/main/section')
        elements = section_content.find_elements(By.XPATH, './*')
        headings = []
        content = []
        aggregate = False
        for element in elements:
            if element.tag_name == 'p':
                if aggregate: #consecutive <p>, so concatenate text to last item in content
                    content[-1] = content[-1] + element.text
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
                result['chart'] = True
        result['release_date'] = re.findall(r'\d{4}-\d{2}-\d{2}', content[0])
        del content[0] #delete release date
        result['headings'] = headings
        result['content'] = content
    #elif re.search(r'rbc', url):
        #title xpath: /html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/h1
        #content Xpath: /html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table/tbody/tr/td/table[1]
    return result

    driver.close()