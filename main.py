
from selenium.webdriver.chrome.service import Service
from processing import gpt_processing
from selenium import webdriver
from classes import statcan, rbc, pbo, boc, source
from monitoring import statscan_mon, boc_mon
import pandas as pd
from gmail import send_email
import pprint
import datetime



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    options= webdriver.ChromeOptions()
    #options.add_argument('headless')
    driver = webdriver.Chrome(options=options, service=service)


    #load temporary database
    all_files_copy = pd.read_csv("temp_database.csv")
    stay_on = True
    #TODO: validate standardization of each of the lists
    release_dates = []
    titles = []
    urls = []
    dates_retrieved = []
    summaries = []
    gpt_outputs = []
    files = []
    institution = []
    news = []
    emailable_summaries = []

    def include_to_staging(release_date, title, url, date_retrieved, institution, summary, files, news):
        release_dates.append(release_date)
        titles.append(title)
        urls.append(url)
        dates_retrieved.append(date_retrieved)
        institution.append(institution) 
        summaries.append(summary)
        files.append(files)
        news.append(news)
        print("Release staged")


    """
    How it works:
    - through a series of input functions, the corresponding scrape is done
    - if its not scraped, then it's just manually added with no scraping
    - info is added into corresponding lists that are zipped at the end of commands and added to the temp database
    """
    while stay_on:
        manual = input("Do you wish to manually input a release? [yes, no, exit] \n")
        if manual == 'yes':
            release_type = input("Is it a StatsCan, BoC, PBO, RBC or other? [type answer as written in the question] \n")
            if release_type == "StatsCan":
                url = input("What is the url? \n")
                url = url.replace('/n1', '')
                if url not in all_files_copy['url'].values:
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    statcan_report = statcan.Statcan(url=url, release_date=release_date, driver=driver)
                    type = input('What type of release is this? [The Daily, Articles and reports] \n')
                    if type == 'The Daily':
                        statcan_report.statcan_daily_scrape()
                        include_to_staging(release_date= statcan_report.output['release_date'],
                                           title=statcan_report.output['title'],
                                           url=statcan_report.output['url'],
                                           date_retrieved=statcan_report.output['date_retrieved'],
                                           institution='Statistics Canada',
                                           summary=gpt_processing.summary_processing(statcan_report.output),
                                           files=gpt_processing.classify_file(statcan_report.output['title']),
                                           news=False)
                    elif type == 'Articles and reports':
                        statcan_report.statcan_report_scrape()
                        include_to_staging(release_date= statcan_report.output['release_date'],
                                           title=statcan_report.output['title'],
                                           url=statcan_report.output['url'],
                                           date_retrieved=statcan_report.output['date_retrieved'],
                                           institution='Statistics Canada',
                                           summary=gpt_processing.summary_processing(statcan_report.output),
                                           files=gpt_processing.classify_file(statcan_report.output['title']),
                                           news=False)
                    emailable_summaries.append(statcan_report)
                else:
                    print('This release already exists in the database.')
            #___________PBO___________
            elif release_type == 'PBO':
                report_type = input("Is this a report or a legislative costing note? \n [report, legislative] \n")
                url = input("What is the url?")
                title_report = input('What is the title of the release? \n')
                release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                if url not in all_files_copy['url'].values and report_type == 'report':
                    pbo_report = pbo.Pbo(url, True, release_date, title_report)
                    pbo_report.pbo_scrape()
                    include_to_staging(release_date=release_date,
                                           title=title_report,
                                           url=url,
                                           date_retrieved=pbo_report.output['date_retrieved'],
                                           institution='Parliamentary Budget Office',
                                           summary=pbo_report.output['highlights'],
                                           files=gpt_processing.classify_file(pbo_report.output['title']),
                                           news=False)
                elif url not in all_files_copy['url'].values and report_type == 'legislative':
                    pbo_report = pbo.Pbo(url, False, release_date, title_report)
                    pbo_report.pbo_scrape()
                    include_to_staging(release_date=release_date,
                                           title=title_report,
                                           url=url,
                                           date_retrieved=pbo_report.output['date_retrieved'],
                                           institution='Parliamentary Budget Office',
                                           summary=pbo_report.output['highlights'],
                                           files=gpt_processing.classify_file(pbo_report.output['title']),
                                           news=False)
                elif url in all_files_copy['url'].values:
                    print('This release already exists in the database.')
                else:
                    print('Please try again!')
            #____________RBC____________
            elif release_type == 'RBC':
                url = input("What is the url? \n")
                if url not in all_files_copy['url'].values:
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    email = input('What format is this RBC release? [email, website] \n')
                    rbc_report = rbc.Rbc(url=url, release_date=release_date, email= email, driver=driver)
                    if email == 'email':
                        rbc_report.rbc_email_scrape()
                        include_to_staging(release_date=release_date,
                                            title=rbc.output['title'],
                                            url=url,
                                            date_retrieved=rbc_report.output['date_retrieved'],
                                            institution='RBC',
                                            summary=gpt_processing.summary_processing(rbc_report.output),
                                            files=gpt_processing.classify_file(rbc_report.output['title']),
                                            news=False)
                    elif type == 'website':
                        rbc_report.rbc_website_scrape()
                        include_to_staging(release_date=release_date,
                                            title=rbc.output['title'],
                                            url=url,
                                            date_retrieved=rbc_report.output['date_retrieved'],
                                            institution='RBC',
                                            summary=gpt_processing.summary_processing(rbc_report.output),
                                            files=gpt_processing.classify_file(rbc_report.output['title']),
                                            news=False)
                else:
                    print('This release already exists in the database.')
            #____________BoC____________
            elif release_type == 'BoC':
                report_type = input("What BoC type of release is this? [Summary of deliberations, Quarterly Financial Report, other]")
                url = input("What is the url?")
                release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                if url not in all_files_copy['url'].values and (report_type == 'Summary of deliberations' or report_type == 'Quarterly Financial Report'):
                    boc_report = boc.Boc(url, report_type, release_date, driver)
                    boc_report.boc_scrape()
                    include_to_staging(release_date=release_date,
                                       title=boc_report.output['title'],
                                       url=url,
                                       date_retrieved=boc_report.output['date_retrieved'],
                                       institution='Bank of Canada',
                                       summary=gpt_processing.summary_processing(boc_report.output),
                                       files=gpt_processing.classify_file(boc_report.output['title']),
                                       news=False)
                elif url not in all_files_copy['url'].values and report_type == 'other':
                    response = input("Release doesn't exist in the database, and this type of release is not scrapable. Do you still want to include it? [yes, no]\n")
                    if response == 'yes':
                        title = input('What is the title of this release?')
                        include_to_staging(release_date=release_date,
                                       title=title,
                                       url=url,
                                       date_retrieved=datetime.date.today().strftime("%d/%m/%Y"),
                                       institution='Bank of Canada',
                                       summary='No Summary',
                                       files=gpt_processing.classify_file(title),
                                       news=False)
                    else:
                        print('Please try again.')

            elif release_type == 'other':
                url = input('What is the url of the release? \n')
                news = input("Is this a news article? [yes, no]\n")
                if url not in all_files_copy['url'].values and news == 'yes':
                    title = input('What is the title of the release? \n')
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    institution = input('What is the institution name? \n')

                    include_to_staging(release_date=release_date,
                                       title=title,
                                       url=url,
                                       date_retrieved=datetime.date.today().strftime("%d/%m/%Y"),
                                       institution=institution,
                                       summary='No Summary',
                                       files= gpt_processing.classify_file(title),
                                       news=True)
                elif url not in all_files_copy['url'].values and news == 'no':
                    include_to_staging(release_date=release_date,
                                       title=title,
                                       url=url,
                                       date_retrieved=datetime.date.today().strftime("%d/%m/%Y"),
                                       institution=institution,
                                       summary='No Summary',
                                       files= gpt_processing.classify_file(title),
                                       news=False)
        elif manual == 'no':
            scrape_type = input('Which source do you want to scrape? \n[StatsCan, BoC] \n')
            if scrape_type == 'StatsCan':
                temp_titles, temp_release_dates, temp_urls, temp_dates_retrieved, temp_summary, temp_files, temp_institution, temp_emailable = statscan_mon.statcan_monitor(all_files_copy, driver)
                titles.extend(temp_titles)
                release_dates.extend(temp_release_dates)
                urls.extend(temp_urls)
                dates_retrieved.extend(temp_dates_retrieved)
                summaries.extend(temp_summary)
                files.extend(temp_files)
                institution.extend(temp_institution)
                emailable_summaries.extend(temp_emailable)
                print('DONE')
            elif scrape_type == "BoC":
                boc_mon.boc_monitor(all_files_copy, driver)
                print('DONE')
        elif manual =='exit':
            email = True
            while email:
                email_question = input("Do you wish to send an email summary regarding one of the reports? \n [yes, no]")
                if email_question == 'yes':
                    for x, item in enumerate(emailable_summaries):
                        print(f"[{x}] - {item.output['title']}")
                    number = input('Type the number of the corresponding report to email.')
                    send_email.send_email(gpt_processing.statcan_processing(emailable_summaries[x-1].output), emailable_summaries[x-1].output['title'])
                elif email_question == 'no':
                    print('Thank you. Have a great rest of your day!')
                    email = False
                    stay_on = False
    
    df_extended = pd.DataFrame(zip(release_dates, titles, urls, dates_retrieved, summaries, files, institution), columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files', 'institution'])
    all_files_copy = pd.concat([df_extended, all_files_copy], ignore_index=True)        
    all_files_copy.to_csv('temp_database.csv', encoding='utf-8', index=False)
    driver.quit()
"""
TODO: check over the main function


"""

"""
release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_date).group()
release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
"""
    