
from selenium.webdriver.chrome.service import Service
from processing import gpt_processing
from selenium import webdriver
from classes import statcan, rbc, pbo, boc, source
from monitoring import statscan_mon, boc_mon
import pandas as pd
from gmail import send_email
import pprint
import datetime

files = {
    "Digital Government":0,
    "Agriculture, Agri-Food and Food Security":1,
    "Canadian Heritage":2,
    "Crown-indigenous Relations":3,
    "Finance and Middle Class Prosperity":4,
    "Employment, Future Workforce Development and Disability inclusion":5,
    "Environment and Climate Change":6,
    "Families, Children and Social Development":7,
    "Federal Economic Development Agency for Eastern, Central and Southern Ontario":8,
    "Fisheries, Oceans and the Canadian Coast Guard":9,
    "Foreign Affairs":10,
    "Health":11,
    "Housing and Diversity and Inclusion":12,
    "Immigration, Refugees and Citizenship":13,
    "Federal Economic Development Agency for Northern Ontario":14,
    "Innovation, Science and Industry":15,
    "International Development":16,
    "International Trade":17,
    "Supply Chain Issues":18,
    "Small Business Recovery and Growth":19,
    "Red Tape Reduction":20,
    "Justice and Attorney General of Canada":21,
    "Mental Health and Suicide Prevention":22,
    "Addictions":23,
    "Northern Affairs and Artic Sovereignty; Canadian Northern Economic Development Agency":24,
    "Prairie Economic Development (Advisor to the Leader, Economy)":25,
    "Pacific Economic Development":26,
    "Sport; Economic Development Agency of Canada for the Regions of Quebec":27,
    "National Defence":28,
    "National Revenue":29,
    "Natural Resources":30, 
    "Official Languages":31,
    "Atlantic Canada Opportunities Agency":32, 
    "Public Safety":33,
    "Public Services and Procurement":34, 
    "Emergency Preparedness":35, 
    "Rural Economic Development & Connectivity":36,
    "Seniors":37,
    "Tourism":38,
    "Transport":39,
    "Treasury Board":40, 
    "Veterans Affairs":41,
    "Women and Gender Equality and Youth":42, 
    "Ethics and Accountable Government":43,
    "Infrastructure and Communities":44,
    "Labour":45,
    "Indigenous Services":46, 
    "Pan-Canadian Trade and Competition":47,
    "Hunting, Fishing and Conservation":48,
    "Democratic Reform":49
}

file_advisors = {
    "Connor MacDonald":[
        "Agriculture, Agri-Food and Food Security",
        "Crown-indigenous Relations",
        "Environment and Climate Change",
        "Health",
        "Mental Health and Suicide Prevention",
        "Addictions",
        "Natural Resources",
        "Indigenous Services"
    ],
    "Darren Hall":[
        "Digital Government",
        "Federal Economic Development Agency for Eastern, Central and Southern Ontario",
        "Housing and Diversity and Inclusion ",
        "Federal Economic Development Agency for Northern Ontario",
        "International Trade",
        "Red Tape Reduction",
        "Prairie Economic Development (Advisor to the Leader, Economy)",
        "Pacific Economic Development ",
        "Atlantic Canada Opportunities Agency ",
        "Rural Economic Development & Connectivity",
        "Tourism",

    ],
    "David Murray":[
        "Hunting, Fishing and Conservation"
    ],
    "Elan Harper":[
        "Finance and Middle Class Prosperity",
        "Employment, Future Workforce Development and Disability Inclusion",
        "Innovation, Science and Industry",
        "Small Business Recovery and Growth",
        "National Revenue",
        "Treasury Board", 
        "Pan-Canadian Trade and Competition"
    ],
    "Emma Hopper":[
        "Ethics and Accountable Government"
    ],
    "Mark Emes":[
        "Families, Children and Social Development", 
        "Fisheries, Oceans and the Canadian Coast Guard", 
        "Supply Chain Issues",
        "Seniors",
        "Transport",
        "Women and Gender Equality and Youth", 
        "Infrastructure and Communities" 
    ],
    "Sean Phelan": [
        "Foreign Affairs", 
        "International Development",
        "Justice and Attorney General of Canada", 
        "Northern Affairs and Artic Sovereignty; Canadian Northern Economic Development Agency",
        "National Defence", 
        "Public Services and Procurement", 
        "Veterans Affairs",
        "Democratic Reform",
    ],
    "Yuan Yi Zhu":[
        "Canadian Heritage", 
        "Immigration, Refugees and Citizenship", 
        "Sport; Economic Development Agency of Canada for the Regions of Quebec",
        "Official Languages", 
        "Public Safety", 
        "Emergency Preparedness", 
        "Labour"
    ]
}

def file_allocation(list_files:list):
    
    for x in range(len(list_files)):
        release_files[x].append(list_files[x].lstrip().rstrip())
        # [advisors[x].append(item) if item else pass for key,value in file_advisors]

    # for file in list_files:
    #     counts.append(files.get(file.lstrip()))
    # for x in range(len(release_files)):release_files[x].append(1 if x in counts else 0)
        
def advisor_classifier(list_files:list):
    count = 0
    for item in list_files:

        count+=1

def print_lists():
    # print(f"Titles: {len(titles)}")
    # print(f"Url: {len(urls)}")
    # print(f"date recieved: {len(dates_retrieved)}")
    # print(f"institutions: {len(institutions)}")
    # print(f"news: {len(news)}")
    # print(f"summaries: {len(summaries)}")
    # print(f"Files: {len(release_files[0])}  {len(release_files[1])}")
    print(f"Titles: {titles}")
    print(f"Url: {urls}")
    print(f"date recieved: {dates_retrieved}")
    print(f"institutions: {institutions}")
    print(f"news: {news}")
    print(f"summaries: {summaries}")
    print(f"Files: {release_files}") 


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    options= webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options, service=service)

    #load temporary database
    all_files_copy = pd.read_csv("temp_database.csv")
    stay_on = True

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
    emailable_summaries = []

    #test = statcan.Statcan(url="https://www150.statcan.gc.ca/n1/daily-quotidien/240202/dq240202a-eng.htm", release_date="02/02/2024", driver=driver)
    
    """
    How it works:
    - through a series of input functions, the corresponding scrape is done
    - if its not scraped, then it's just manually added with no scraping
    - info is added into corresponding lists that are zipped at the end of commands and added to the temp database
    """
    print(files)
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
                        release_dates.append(statcan_report.output['release_date'])
                        titles.append(statcan_report.output['title'])
                        urls.append(statcan_report.output['url'])
                        dates_retrieved.append(statcan_report.output['date_retrieved'])
                        institutions.append('Statistics Canada')
                        summaries.append(gpt_processing.summary_processing(statcan_report.output, False))
                        file_allocation(gpt_processing.classify_file(statcan_report.output['title']))
                        news.append(False)
                        emailable_summaries.append(statcan_report)
                        print_lists()
                    elif type == 'Articles and reports':
                        statcan_report.statcan_report_scrape()
                        release_dates.append(statcan_report.output['release_date'])
                        titles.append(statcan_report.output['title'])
                        urls.append(statcan_report.output['url'])
                        dates_retrieved.append(statcan_report.output['date_retrieved'])
                        institutions.append('Statistics Canada')
                        summaries.append(gpt_processing.summary_processing(statcan_report.output, False))
                        file_allocation(gpt_processing.classify_file(statcan_report.output['title']))
                        news.append(False)
                        emailable_summaries.append(statcan_report)
                        print_lists()
                else:
                    print('This release already exists in the database.')
            #___________PBO___________
            elif release_type == 'PBO':
                report_type = input("Is this a report or a legislative costing note? \n [report, legislative] \n")
                url = input("What is the url?")
                title_report = input('What is the title of the release? \n')
                release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                if url not in all_files_copy['url'].values and (report_type == 'report' or report_type == 'legislative'):
                    pbo_report = pbo.Pbo(url, report_type == "report", release_date, title_report, driver)
                    pbo_report.pbo_scrape()
                    release_dates.append(release_date)
                    titles.append(title_report)
                    urls.append(url)
                    dates_retrieved.append(pbo_report.output['date_retrieved'])
                    institutions.append('Parliamentary Budget Office')
                    summaries.append(pbo_report.output['highlights'])
                    file_allocation(gpt_processing.classify_file(pbo_report.output['title']))
                    news.append(False)
                    print_lists()
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
                    rbc_report = rbc.Rbc(url=url, email= email, release_date=release_date, driver=driver)
                    if email == 'email':
                        rbc_report.rbc_email_scrape()
                        release_dates.append(release_date)
                        titles.append(rbc_report.output['title'])
                        urls.append(url)
                        dates_retrieved.append(rbc_report.output['date_retrieved'])
                        institutions.append('RBC')
                        summaries.append(gpt_processing.summary_processing(rbc_report.output, False))
                        file_allocation(gpt_processing.classify_file(rbc_report.output['title']))
                        news.append(False)
                        print_lists()
                    elif email == 'website':
                        rbc_report.rbc_website_scrape()
                        release_dates.append(release_date)
                        titles.append(rbc_report.output['title'])
                        urls.append(url)
                        dates_retrieved.append(rbc_report.output['date_retrieved'])
                        institutions.append('RBC')
                        summaries.append(gpt_processing.summary_processing(rbc_report.output, False))
                        file_allocation(gpt_processing.classify_file(rbc_report.output['title']))
                        news.append(False)
                        print_lists()
                else:
                    print('This release already exists in the database.\n')
            #____________BoC____________
            elif release_type == 'BoC':
                report_type = input("What BoC type of release is this? [Summary of deliberations, Quarterly Financial Report, other]")
                url = input("What is the url?")
                release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                if url not in all_files_copy['url'].values and (report_type == 'Summary of deliberations' or report_type == 'Quarterly Financial Report'):
                    boc_report = boc.Boc(url, report_type, release_date, driver)
                    boc_report.boc_scrape()
                    release_dates.append(release_date)
                    titles.append(boc_report.output['title'])
                    urls.append(url)
                    dates_retrieved.append(boc_report.output['date_retrieved'])
                    institutions.append('Bank of Canada')
                    summaries.append(gpt_processing.summary_processing(boc_report.output, False))
                    file_allocation(gpt_processing.classify_file(boc_report.output['title']))
                    news.append(False)
                    print_lists()
                elif url not in all_files_copy['url'].values and report_type == 'other':
                    response = input("Release doesn't exist in the database, and this type of release is not scrapable. Do you still want to include it? [yes, no]\n")
                    if response == 'yes':
                        title = input('What is the title of this release?')
                        content = input("What is the content of this release? (For summary inclusion reasons) \n")
                        release_dates.append(release_date)
                        titles.append(title)
                        urls.append(url)
                        dates_retrieved.append(datetime.date.today().strftime("%d/%m/%Y"))
                        institutions.append('Bank of Canada')
                        summaries.appned(gpt_processing.summary_processing(content, True))
                        file_allocation(gpt_processing.classify_file(title))
                        news.append(False)
                        print_lists()
                    else:
                        print('This release already exists in the database.\n')

            elif release_type == 'other':
                url = input('What is the url of the release? \n')
                news_q = input("Is this a news article? [yes, no]\n")
                if url not in all_files_copy['url'].values and (news_q == 'yes' or news_q == 'no'):
                    title = input('What is the title of the release? \n')
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    institution = input('What is the institution name? \n')
                    content_bool = input("Do you wish to include a summary of the release? [yes, no] \n")
                    if content_bool == "yes":
                        content = ""
                        content_grab = True
                        while content_grab:
                            content = content + ' ' + input("Please insert the content below. \n")
                            discontinue = input('Is this all? [yes, no]\n')
                            if discontinue == "yes" or discontinue == 'no':
                                content_grab = discontinue == 'no'
                            else:
                                print('Please try again.')
                                content_grab = True
                        release_dates.append(release_date)
                        titles.append(title)
                        urls.append(url)
                        dates_retrieved.append(datetime.date.today().strftime("%d/%m/%Y"))
                        institutions.append(institution)
                        summaries.append(gpt_processing.summary_processing(content, True))
                        file_allocation(gpt_processing.classify_file(title))
                        news.append(news_q == "yes")
                        print_lists()
                    elif content_bool == 'no':
                        release_dates.append(release_date)
                        titles.append(title)
                        urls.append(url)
                        dates_retrieved.append(datetime.date.today().strftime("%d/%m/%Y"))
                        institutions.append(institution)
                        summaries.append('NO SUMMARY')
                        file_allocation(gpt_processing.classify_file(title))
                        news.append(news == "yes")
                        print_lists()
                else:
                    print('This release already exists in the database.\n')
        elif manual == 'no':
            scrape_type = input('Which source do you want to scrape? \n[StatsCan, BoC] \n')
            if scrape_type == 'StatsCan':
                temp_titles, temp_release_dates, temp_urls, temp_dates_retrieved, temp_summary, temp_files, temp_institution, temp_emailable = statscan_mon.statcan_monitor(all_files_copy, driver)
                titles.extend(temp_titles)
                release_dates.extend(temp_release_dates)
                urls.extend(temp_urls)
                dates_retrieved.extend(temp_dates_retrieved)
                summaries.extend(temp_summary)
                for x in temp_files:
                    file_allocation(x)
                institution.extend(temp_institution)
                emailable_summaries.extend(temp_emailable)
                print('DONE')
                print_lists()
            elif scrape_type == "BoC":
                temp_titles, temp_release_dates, temp_urls, temp_dates_retrieved, temp_summary, temp_files, temp_institution = boc_mon.boc_monitor(all_files_copy, driver)
                titles.extend(temp_titles)
                release_dates.extend(temp_release_dates)
                urls.extend(temp_urls)
                dates_retrieved.extend(temp_dates_retrieved)
                summaries.extend(temp_summary)
                for x in temp_files:
                    file_allocation(x)
                institution.extend(temp_institution)
                print('DONE')
                print_lists()
        elif manual =='exit':
            email = True
            while email:
                email_question = input("Do you wish to send an email summary regarding one of the reports? [yes, no] \n")
                if email_question == 'yes':
                    if emailable_summaries:
                        for x, item in enumerate(emailable_summaries):
                            print(f"[{x}] - {item.output['title']} \n")
                        number = input('Type the number of the corresponding report to email.\n')
                        send_email.send_email(gpt_processing.statcan_processing(emailable_summaries[int(number)].output), emailable_summaries[int(number)].output['title'])
                        print("Email sent. \n")
                    if summaries:
                        for x in range(len(summaries)):
                            print(f"[{x}] - {titles[x]} \n")
                        number = input('Type the number of the corresponding report to email.\n')
                        send_email.send_email(summaries[int(number)], titles[int(number)])
                        print("Email sent.\n")
                elif email_question == 'no':
                    print('Thank you. Have a great rest of your day!')
                    email = False
                    stay_on = False
    #TODO create indicator columns
    #TODO: add corresponding policy advisors
    df_extended = pd.DataFrame(
        zip(release_dates, titles, urls, dates_retrieved, summaries, release_files, institutions,
            release_files[0], release_files[1]),
        columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files', 'institution',
                 "file_1", "file_2"]
    )
    # df_extended = pd.DataFrame(
    #     zip(release_dates, titles, urls, dates_retrieved, summaries, release_files, institutions,
    #         files[0], files[1], files[2], files[3], files[4], files[5], files[6], files[7],
    #         files[8], files[9], files[10], files[11], files[12], files[13], files[14],
    #         files[15], files[16], files[17], files[18]),
    #     columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'files', 'institution',
    #              "dig_gov","agri", 'cad_heritage', 'crown-indig', 'finance', 'employ', 'env', "fam",
    #              "fed_econ_sont", 'fish', "f_affair", 'health', 'housing', 'immigration', 'fed_econ_nont',
    #              'innov_sci', 'inter_dev', 'inter_trade', 'sup_chain'])
    all_files_copy = pd.concat([df_extended, all_files_copy], ignore_index=True)        
    all_files_copy.to_csv('temp_database_copy.csv', encoding='utf-8', index=False)
    driver.quit()

"""
release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_date).group()
release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
"""
    