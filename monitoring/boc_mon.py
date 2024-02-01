from selenium.webdriver.common.by import By
from processing import gpt_processing
from gmail import send_email
from classes import boc
from selenium import webdriver
from datetime import datetime
import pandas as pd
import re

def boc_monitor(all_files, driver)-> tuple:
    """
    Montiring function for bank of canada releases that would return corresponding URLS of new releases.
    INPUT: all_files which is the monitored database, and driver which is a webdriver
    OUTPUT: list of urls of new releases
    """
    driver.get("https://www.bankofcanada.ca/publications/browse/?content_type%5B%5D=19359&content_type%5B%5D=22219")

    table = driver.find_elements(By.XPATH, "//main[@id='main-content']/div/div[2]/div[2]/div/div/div/div[2]/div/div/*")
    table_string = "//main[@id='main-content']/div/div[2]/div[2]/div/div/div/div[2]/div/div"
    release_dates = []
    titles = []
    urls = []
    dates_retrieved = []
    summary = []
    files = []
    institution = []

    for index in range(len(table[:-1])):
        url = driver.find_element(By.XPATH, table_string+f"/div[{index+1}]/article/div/h3/a").get_attribute('href')
        if url not in all_files['url'].values:
            #Extraction
            release_date = driver.find_element(By.XPATH, table_string+f"/div[{index+1}]/article/div/span").text
            release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
            release_dates.append(release_date)

            title = driver.find_element(By.TAG_NAME, table_string+f"/div[{index+1}]/article/div/h3").text
            titles.append(title)

            urls.append(url)
            tag = driver.find_element(By.XPATH, table_string+f"/div[{index+1}]/article/div/h3/a").get_attribute('data-content-type')
            click = driver.find_element(By.XPATH, table_string+f"/div[{index+1}]/article/div/h3")
            click.click()
            boc_class = boc.Boc(url, tag, release_date, driver)
            boc_class.boc_scrape()
            print(boc_class)

            summary.append(gpt_processing.summary_processing(boc_class.output, False))
            files.append(['Finance and Middle Class Prosperity'])
            institution.append('Bank of Canada')
            dates_retrieved.append(boc_class.output['date_retrieved'])
            driver.back()
    return (titles, release_dates, urls, dates_retrieved, summary, files, institution)         

    # if titles:
    #     df_extended = pd.DataFrame(zip(release_dates, titles, urls, dates_retrieved, summary, files, institution), columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files', 'institution'])
    #     all_files = pd.concat([df_extended, all_files], ignore_index=True)        
    #     all_files.to_csv('temp_database_copy.csv', encoding='utf-8', index=False)
                
    #TODO: test this function, fix errors




