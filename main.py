
from selenium.webdriver.chrome.service import Service
from processing import gpt_processing
from selenium import webdriver
from classes import statcan, rbc, pbo, boc, source
from monitoring import statscan_mon, boc_mon
import pandas as pd
from gmail import send_email
import pprint


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    options= webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(options=options, service=service)



    all_files_copy = pd.read_csv("temp_database_copy.csv")
    stay_on = True
    release_dates = []
    titles = []
    urls = []
    dates_retrieved = []
    summaries = []
    gpt_outputs = []
    files = []
    institution = []
    while stay_on:
        manual = input("Do you wish to manually input a release? [yes, no, exit] \n")
        if manual == 'yes':
            release_type = input("Is it a StatsCan, BoC, PBO, RBC or other? [type answer as written in the question] \n")
            if release_type == "StatsCan":
                url = input("What is the url? \n")
                if url not in all_files_copy['url'].values:
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    statcan = statcan.Statcan(url=url, release_date=release_date, driver=driver)
                    type = input('What type of release is this? [The Daily, Articles and reports] \n')
                    if type == 'The Daily':
                        statcan.statcan_daily_scrape()
                        release_dates.append(statcan.output['release_date'])
                        titles.append(statcan.output['title'])
                        urls.append(statcan.output['url'])
                        dates_retrieved.append(statcan.output['date_retrieved'])
                        institution.append('statistics canada') 
                        summaries.append(gpt_processing.summary_processing(statcan.output))
                        files.append(gpt_processing.classify_file(statcan.output['title']))
                    elif type == 'Articles and reports':
                        statcan.statcan_report_scrape()
                        release_dates.append(statcan.output['release_date'])
                        titles.append(statcan.output['title'])
                        urls.append(statcan.output['url'])
                        dates_retrieved.apepnd(statcan.output['date_retrieved'])
                        institution.append('statistics canada') 
                        summaries.append(gpt_processing.summary_processing(statcan.output))
                        files.append(gpt_processing.classify_file(statcan.output['title']))
                else:
                    print('This release already exists in the database.')
            elif release_type == 'PBO':
                url = input("What is the url?")
                if url not in all_files_copy['url'].values:
                    print('THIS SECTION OF COMMANS IS NOT COMPLETE YET')
                else:
                    print('This release already exists in the database.')
            elif release_type == 'RBC':
                url = input("What is the url? \n")
                if url not in all_files_copy['url'].values:
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    email = input('What format is this RBC release? [email, website] \n')
                    rbc = rbc.Rbc(url=url, release_date=release_date, email= email, driver=driver)
                    if email == 'email':
                        rbc.rbc_email_scrape()
                        release_dates.append(rbc.output['release_date'])
                        titles.append(rbc.output['title'])
                        urls.append(rbc.output['url'])
                        dates_retrieved.apepnd(rbc.output['date_retrieved'])
                        institution.append('rbc') 
                        summaries.append(gpt_processing.summary_processing(rbc.output))
                        files.append(gpt_processing.classify_file(rbc.output['title']))
                    elif type == 'website':
                        rbc.rbc_website_scrape()
                        release_dates.append(rbc.output['release_date'])
                        titles.append(rbc.output['title'])
                        urls.append(rbc.output['url'])
                        dates_retrieved.apepnd(rbc.output['date_retrieved'])
                        institution.append('rbc') 
                        summaries.append(gpt_processing.summary_processing(rbc.output))
                        files.append(gpt_processing.classify_file(rbc.output['title']))
                else:
                    print('This release already exists in the database.')
            elif release_type == 'other':
                pass
        elif manual == 'no':
            scrape_type = input('Which source do you want to scrape? \n[StatsCan, BoC] \n')
            if scrape_type == 'StatsCan':
                statscan_mon.statcan_monitor(all_files_copy, driver)
                print('DONE')
            elif scrape_type == "BoC":
                boc_mon.boc_monitor(all_files_copy, driver)
                print('DONE')
        elif manual =='exit':
            print('THANK YOU')
            stay_on = False
    df_extended = pd.DataFrame(zip(release_dates, titles, urls, dates_retrieved, summaries, files, institution), columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files', 'institution'])
    all_files_copy = pd.concat([df_extended, all_files_copy], ignore_index=True)        
    all_files_copy.to_csv('temp_database_copy.csv', encoding='utf-8', index=False)
    driver.quit()
"""
TODO: check over the main function

"""

"""
release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_date).group()
release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
"""
    