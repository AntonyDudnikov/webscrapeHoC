from selenium.webdriver.common.by import By
from processing import gpt_processing
from gmail import send_email
from classes.source import Source
from classes import boc
from datetime import datetime
import pandas as pd
import re

def boc_monitor(all_files, driver):
    """
    Montiring function for bank of canada releases that would return corresponding URLS of new releases.
    INPUT: all_files which is the monitored database, and driver which is a webdriver
    OUTPUT: list of urls of new releases
    """
    driver.get("https://www.bankofcanada.ca/publications/browse/?content_type%5B%5D=19359&content_type%5B%5D=22219")

    table = driver.find_elements(By.XPATH, "//div[@class='results']/div/div")

    release_dates = []
    titles = []
    urls = []
    dates_retrieved = []
    summary = []
    files = []
    institution = []

    for item in table:
        url = item.find_element(By.TAG_NAME, 'h3').get_attribute('href')
        if url not in all_files['urls'].values:
            #Extraction
            release_date = item.find_element(By.XPATH, "./article/div/span").text
            release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
            release_dates.append(release_date)

            title = item.find_element(By.TAG_NAME, 'h3').text
            titles.append(title)

            urls.append(url)

            click = driver.find_element(By.TAG_NAME, 'h3')
            click.click()
            boc_class = boc.Boc(url, item.find_elements(By.XPATH, './div[@class=media_tags]/span/*')[2].text, release_date, driver)
            boc_class.boc_scrape()
            print(boc_class)
            summary.append(gpt_processing.summary_processing(boc_class.output))
            files.append(['Finance and Middle Class Prosperity'])
            institution.append('Bank of Canada')
            dates_retrieved.append(boc_class.output['date_retrieved'])
            driver.back()
            driver.back()
            driver.back()

    if titles:
        df_extended = pd.DataFrame(zip(release_dates, titles, urls, dates_retrieved, summary, files), columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files'])
        all_files = pd.concat([df_extended, all_files], ignore_index=True)        
        all_files.to_csv('temp_database_copy.csv', encoding='utf-8', index=False)
                
    #TODO: test this function




