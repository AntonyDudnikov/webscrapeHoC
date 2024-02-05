from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from processing import gpt_processing
from gmail import send_email
from classes import statcan
from selenium import webdriver
from datetime import datetime
import pandas as pd
import main
import re

#create a csv file to keep track of viewed releasesdrive

#load and upload csv file in file directory
statcan_file = pd.DataFrame()

def statcan_monitor(statcan_file, driver) -> tuple:
    """
    Montiring function for daily releases that would return corresponding URLS of new releases.
    INPUT: statcan_file which is the monitored database
    OUTPUT: list of urls of new releases
    """
    driver.get("https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/rel-com/all_subjects-eng.htm")

    table = driver.find_elements(By.XPATH, "//table[@id='release-list']/tbody/*")

    release_dates = []
    titles = []
    urls = []
    dates_retrieved = []
    summary = []
    gpt_outputs = []
    files = []
    advisors = [[],[]]
    quotes = []
    institution = []
    emailable = []

    for index in range(len(table)):
        """
        check if item is in existing dataframe
        if not, retreive, process and add. if yes than skip
        if yes, break for loop
        append 
        
        """
        print('_______________NEW ITEM_________________')
        item = driver.find_element(By.XPATH, f"//table[@id='release-list']/tbody/tr[{index+1}]")
        url = item.find_element(By.XPATH, './td/a').get_attribute('href')
        #TODO: mind you the href doesn't include the .../n1/... in the url. Issues in manual inputs if thats the case
        if url not in statcan_file['url'].values:
            release_date = item.find_element(By.XPATH, "./td/a/p[@class='text-img-list keynext']").text
            release_date = re.search( r'(\d{4}-\d{2}-\d{2})', release_date).group()
            release_date = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            
            #Extraction
            item.click()
            stat = statcan.Statcan(url=url, release_date=release_date, driver=driver)
            stat.statcan_daily_scrape()
            print(stat)
            release_dates.append(stat.output['release_date'])
            titles.append(stat.output['title'])
            urls.append(stat.output['url'])
            dates_retrieved.append(stat.output['date_retrieved'])
            institution.append('statistics canada')
            summary.append(gpt_processing.summary_processing(stat.output, manual=False))
            emailable.append(stat)
            files.append(gpt_processing.classify_file(stat.output['title']))
            quotes.append(gpt_processing.quote_identifier(stat.output, manual=False))
            driver.get("https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/rel-com/all_subjects-eng.htm")
        else:
            print('The Database is up to date for Statistics Canada The Daily releases.')
    return (titles, release_dates, urls, dates_retrieved, summary, files, institution, emailable, quotes)

    # if titles:
    #     df_extended = pd.DataFrame(zip(release_dates, titles, urls, dates_retrieved, summary, files), columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files'])
    #     statcan_file = pd.concat([df_extended, statcan_file], ignore_index=True)                  
    #     statcan_file.to_csv('temp_database_copy.csv', encoding='utf-8', index=False)

        