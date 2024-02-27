from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from processing import gpt_processing
from monitoring import statscan_mon
from selenium import webdriver
from datetime import datetime
from classes import statcan
import pandas as pd
import main
import re
import time


service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
#options.add_argument('headless')
driver = webdriver.Chrome(options=options, service=service)
driver.get("https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/rel-com/all_subjects-eng.htm")

all_files_copy = pd.read_csv("final.csv")

release_dates = []
titles = []
urls = []
dates_retrieved = []
summaries = []
gpt_outputs = []
release_files = [[], []]
advisors = [[],[]]
institutions = []
news = []
quotes = []
emailable_summaries = []

all_files_copy = pd.read_csv("final.csv")

def file_allocation(list_files:list):
    for x in range(len(list_files)):
        release_files[x].append(list_files[x].lstrip().rstrip())
        for key, value in main.file_advisors.items():
            if list_files[x] in value:
                advisors[x].append(key)

def go_forward(times:int, driver):
    driver.get("https://www150.statcan.gc.ca/n1/dai-quo/ssi/homepage/rel-com/all_subjects-eng.htm")
    for x in range(times):
        button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='release-list_next']")))
        button.click()
        

cut = False

for x in range(2, 6):
    if cut:
        break
    if x == 0:
        temp_titles, temp_release_dates, temp_urls, temp_dates_retrieved, temp_summary, temp_files, temp_institution, temp_emailable, temp_quotes = statscan_mon.statcan_monitor(all_files_copy, driver)
        titles.extend(temp_titles)
        release_dates.extend(temp_release_dates)
        urls.extend(temp_urls)
        dates_retrieved.extend(temp_dates_retrieved)
        quotes.extend(temp_quotes)
        summaries.extend(temp_summary)
        for x in temp_files:
            file_allocation(x)
        institutions.extend(temp_institution)
        emailable_summaries.extend(temp_emailable)
        news.append(False)
        print('DONE')
    elif x != 0:
        table = driver.find_elements(By.XPATH, "//table[@id='release-list']/tbody/*")
        go_forward(x, driver)
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
            release_date = item.find_element(By.XPATH, "./td/a/p[@class='text-img-list keynext']").text
            release_date = re.search( r'(\d{4}-\d{2}-\d{2})', release_date).group()
            release_date = datetime.strptime(release_date, "%Y-%m-%d").strftime("%d/%m/%Y")
            if url not in all_files_copy['url'].values:
                #Extraction
                item.click()
                try:
                    stat = statcan.Statcan(url=url, release_date=release_date, driver=driver)
                    stat.statcan_daily_scrape()
                    release_dates.append(stat.output['release_date'])
                    titles.append(stat.output['title'])
                    urls.append(stat.output['url'])
                    dates_retrieved.append(stat.output['date_retrieved'])
                    news.append(False)
                    institutions.append('statistics canada')
                    summaries.append(gpt_processing.summary_processing(stat.output, manual=False))
                    emailable_summaries.append(stat)
                    file_allocation(gpt_processing.classify_file(stat.output['title']))
                    quotes.append(gpt_processing.quote_identifier(stat.output, manual=False))
                except:
                    cut = True
                    print('FUNDS RAN OUT!')
                    break
                go_forward(x, driver)
            print(f"Total releases captured in this run: {len(titles)}")
    else:
        print('___skip___')

df_extended = pd.DataFrame(
    zip(release_dates, titles, urls, dates_retrieved, summaries, quotes, institutions,
        release_files[0], release_files[1], advisors[0], advisors[1], news),
    columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'quotes', 'institution',
                "file_1", "file_2", "file_advisor_1", "file_advisor_2", "news_bool"]
)

print(len(df_extended))
print(df_extended)
all_files_copy = pd.concat([df_extended, all_files_copy], ignore_index=True)        
all_files_copy.to_csv('final.csv', encoding='utf-8', index=False)
all_files_copy.to_json('final.json', 'records', indent=2)
driver.quit()