from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from processing import gpt_processing
from gmail import send_email
from classes.source import Source
from classes import statcan
from selenium import webdriver
from datetime import datetime
import pandas as pd
import random
import time
import re

#create a csv file to keep track of viewed releases
#load and upload csv file in file directory
statcan_file = pd.DataFrame()

def load_statcan_mon_file():
    statcan_file = pd.read_csv("statscan_mon_file.csv")
    return statcan_file

def _upload_statcan_mon_file(statcan_file):
    #statcan_file = pd.DataFrame({'release_date':[], 'title':[], 'url': [], 'date_retrieved':[]})
    statcan_file.to_csv('statscan_mon_file.csv', encoding='utf-8', index=False)

def statcan_monitor(statcan_file, driver):
    """
    Montiring function for daily releases that would return corresponding URLS of new releases.
    INPUT: statcan_file which is the monitored database
    OUTPUT: list of urls of new releases
    """
    driver.get("https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/rel-com/all_subjects-eng.htm")
    #window_handles = driver.window_handles
    #parent_window = window_handles[0]

    table = driver.find_elements(By.XPATH, "//table[@id='release-list']/tbody/*")

    release_dates = []
    titles = []
    urls = []
    dates_retrieved = []

    for item in table:
        """
        check if item is in existing dataframe
        if not, retreive, process and add. if yes than skip
        if yes, break for loop
        append 
        """
        print('_______________NEW ITEM_________________')
        url = item.find_element(By.XPATH, './td/a').get_attribute('href')

        if url not in statcan_file['url']:
            release_date = item.find_element(By.XPATH, "./td/a/p[@class='text-img-list keynext']").text
            release_date = re.search( r'(\d{4}-\d{2}-\d{2})', release_date).group()
            release_date = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            
            #Extraction
            item.click()
            stat = statcan.Statcan(url=url, release_date=release_date, driver=driver)
            stat.statcan_scrape()
            print(stat)
            release_dates.append(stat.output['release_date'])
            titles.append(stat.output['title'])
            urls.append(stat.output['url'])
            dates_retrieved.append(stat.output['date_retrieved'])
            driver.back()
            driver.back()
           
            #Processing
            #gpt_output = gpt_processing.statcan_processing(stat.output)

            #send email
            #send_email.send_email(gpt_output, stat1.output['title'])
    df_extended = pd.DataFrame(zip(release_dates, titles, urls, dates_retrieved), columns=["release_date", 'title', 'url', 'date_retrieved'])
    statcan_file = pd.concat([statcan_file, df_extended], ignore_index=True)      
    # statcan_file.append({'release_date': stat.output['release_date'],
    #                              'title': stat.output['title'],
    #                              'url': stat.output['url'],
    #                              'date_retrieved': stat.output['date_retrieved']})
            
    _upload_statcan_mon_file(statcan_file)
        
