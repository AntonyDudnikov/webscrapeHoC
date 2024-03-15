
from selenium.webdriver.chrome.service import Service
from processing import gpt_processing
from selenium import webdriver
from classes import statcan, rbc, pbo, boc, source
from monitoring import statscan_mon, boc_mon
import pandas as pd
from gmail import send_email
import tabula
import pprint
import datetime
from storage import load_storage

#TODO: check if this block is really necessary
"""
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
"""

file_advisors = {
    "C. MacDonald":[
        "Agriculture, Agri-Food and Food Security",
        "Crown-indigenous Relations",
        "Environment and Climate Change",
        "Health",
        "Mental Health and Suicide Prevention",
        "Addictions",
        "Natural Resources",
        "Indigenous Services"
    ],
    "D. Hall":[
        "Digital Government",
        "Federal Economic Development Agency for Eastern, Central and Southern Ontario",
        "Housing and Diversity and Inclusion",
        "Federal Economic Development Agency for Northern Ontario",
        "International Trade",
        "Red Tape Reduction",
        "Prairie Economic Development (Advisor to the Leader, Economy)",
        "Pacific Economic Development",
        "Atlantic Canada Opportunities Agency",
        "Rural Economic Development & Connectivity",
        "Tourism",

    ],
    "D. Murray":[
        "Hunting, Fishing and Conservation"
    ],
    "E. Harper":[
        "Finance and Middle Class Prosperity",
        "Employment, Future Workforce Development and Disability Inclusion",
        "Innovation, Science and Industry",
        "Small Business Recovery and Growth",
        "National Revenue",
        "Treasury Board", 
        "Pan-Canadian Trade and Competition"
    ],
    "E. Hopper":[
        "Ethics and Accountable Government"
    ],
    "M. Emes":[
        "Families, Children and Social Development", 
        "Fisheries, Oceans and the Canadian Coast Guard", 
        "Supply Chain Issues",
        "Seniors",
        "Transport",
        "Women and Gender Equality and Youth", 
        "Infrastructure and Communities" 
    ],
    "S. Phelan": [
        "Foreign Affairs", 
        "International Development",
        "Justice and Attorney General of Canada", 
        "Northern Affairs and Artic Sovereignty; Canadian Northern Economic Development Agency",
        "National Defence", 
        "Public Services and Procurement", 
        "Veterans Affairs",
        "Democratic Reform",
    ],
    "Y. Zhu":[
        "Canadian Heritage", 
        "Immigration, Refugees and Citizenship", 
        "Sport, Economic Development Agency of Canada for the Regions of Quebec",
        "Official Languages", 
        "Public Safety", 
        "Emergency Preparedness", 
        "Labour"
    ]
}

def file_allocation(list_files:list):
    for x in range(len(list_files)):
        release_files[x].append(list_files[x].lstrip().rstrip())
        inclusion = False
        for key, value in file_advisors.items():
            if list_files[x].lstrip().rstrip() in value:
                advisors[x].append(key)
                inclusion = True
        if not inclusion:
            aq = input(f"This is the heading, who is the corresponding advisor for this heading: {list_files[x]}?\n[C. MacDonald, D. Hall, D. Murray, E. Harper, E. Hopper, M. Emes, S. Phelan, Y. Zhu] \n")
            advisors[x].append(aq)
        

def print_lists():
    print(f"Titles: {len(titles)}")
    print(f"Url: {len(urls)}")
    print(f"date recieved: {len(dates_retrieved)}")
    print(f"institutions: {len(institutions)}")
    print(f"news: {len(news)}")
    print(f"summaries: {len(summaries)}")
    print(f"Files: {len(release_files[0])}  {len(release_files[1])}")
    print(f"release_date: {len(release_dates)}")
    print(f"quotes: {len(quotes)}")
    print(f"advisors1: {len(advisors[0])}, advisors2: {len(advisors[1])}")
    # print(f"Titles: {titles}")
    # print(f"Url: {urls}")
    # print(f"date recieved: {dates_retrieved}")
    # print(f"institutions: {institutions}")
    # print(f"news: {news}")
    # print(f"summaries: {summaries}")
    # print(f"Files: {release_files}") 
    # print(f"file advisor: {advisors}")
    # print(f"Quotes: {quotes}")




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #service = Service(executable_path="C:\Program Files (x86)\chrome")
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    options= webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(service=service, options=options)

    #load temporary database
    load_storage.load_storage()
    all_files_copy = pd.read_csv("storage/final_loaded.csv")
    #bool to turn on/off the console control
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
    quotes = []

    """
    How it works:
    - through a series of input functions, the corresponding scrape is done
    - if its not scraped, then it's just manually added with no scraping
    - info is added into corresponding lists that are zipped at the end of commands and added to the temp database
    """
    while stay_on:
        manual = input("What do you wish to do? [manual, automatic, email, exit] \n")
        if manual == 'manual':
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
                        quotes.append(gpt_processing.quote_identifier(statcan_report.output, False))
                        print_lists()
                    elif type == 'Articles and reports':
                        statcan_report.statcan_report_scrape()
                        release_dates.append(statcan_report.output['release_date'])
                        titles.append(statcan_report.output['title'])
                        urls.append(statcan_report.output['url'])
                        dates_retrieved.append(statcan_report.output['date_retrieved'])
                        institutions.append('Statistics Canada')
                        summary_q = input("Do you want an automatic summary? [yes, no] \n")
                        if (summary_q == 'yes' or summary_q == 'no') and summary_q == 'yes':
                            summaries.append(gpt_processing.summary_processing(statcan_report.output, False))
                            pass
                        elif (summary_q == 'yes' or summary_q == 'no') and summary_q == 'no':
                            test = input('Do you want a section specific summary? [yes, no] \n')
                            if (test == 'yes' or test == 'no') and test == 'yes':
                                input = input("Please insert the section of text that you want summarised. \n")
                                summaries.append(gpt_processing.summary_processing(input, manual=True))
                            elif (test == 'yes' or test == 'no') and test == 'no':
                                summaries.append("NO SUMMARY")
                                pass
                        file_allocation(gpt_processing.classify_file(statcan_report.output['title']))
                        news.append(False)
                        quotes.append(gpt_processing.quote_identifier(statcan_report.output, False))
                        print_lists()
                else:
                    print('This release already exists in the database.')
            #___________PBO___________
            elif release_type == 'PBO':
                report_type = input("Is this a report or a legislative costing note? \n [report, legislative] \n")
                url = input("What is the url? \n")
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
                    summaries.append(pbo_report.output['highlights'] if report_type == 'report' else gpt_processing.summary_processing(pbo_report.output, manual=False))
                    file_allocation(gpt_processing.classify_file(pbo_report.output['title']))
                    news.append(False)
                    quotes.append('No Quotes')
                    print(pbo_report)
                    print_lists()
                elif url in all_files_copy['url'].values:
                    print('This release already exists in the database.')
                else:
                    print('Please try again!')
            #____________RBC____________
            elif release_type == 'RBC':
                url = input("What is the url? \n")
                title_q = input("What is the title? \n")
                if url not in all_files_copy['url'].values and title_q not in all_files_copy['title'].values:
                    release_date = input("What is the release date? Write in this format, dd/mm/YYYY \n")
                    email = input('What format is this RBC release? [email, website] \n')
                    rbc_report = rbc.Rbc(url=url, email= email, release_date=release_date, driver=driver)
                    if email == 'email':
                        rbc_report.rbc_email_scrape()
                        release_dates.append(release_date)
                        titles.append(title_q)
                        urls.append(url)
                        dates_retrieved.append(rbc_report.output['date_retrieved'])
                        institutions.append('RBC')
                        summaries.append(gpt_processing.summary_processing(rbc_report.output, False))
                        quotes.append(gpt_processing.quote_identifier(rbc_report.output, False))
                        file_allocation(gpt_processing.classify_file(rbc_report.output['title']))
                        news.append(False)
                    elif email == 'website':
                        rbc_report.rbc_website_scrape()
                        release_dates.append(release_date)
                        titles.append(title_q)
                        urls.append(url)
                        dates_retrieved.append(rbc_report.output['date_retrieved'])
                        institutions.append('RBC')
                        summaries.append(gpt_processing.summary_processing(rbc_report.output, False))
                        quotes.append(gpt_processing.quote_identifier(rbc_report.output, False))
                        file_allocation(gpt_processing.classify_file(rbc_report.output['title']))
                        news.append(False)
                else:
                    print('This release already exists in the database.\n')
            #____________BoC____________
            elif release_type == 'BoC':
                report_type = input("What BoC type of release is this? [Summary of deliberations, Quarterly Financial Report, other] \n")
                url = input("What is the url? \n")
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
                    quotes.append(gpt_processing.quote_identifier(boc_report.output, False))
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
                        summaries.append(gpt_processing.summary_processing(content, True))
                        quotes.append(input("Are there any 'headline' quotes in this release? \n *place each quote in quotations and seperated by a dash, or just say 'No quotes'*"))
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
                        quotes.append(input("Are there any 'headline' quotes in this release? \n *place each quote in quotations and seperated by a dash, or just say 'No quotes'*"))
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
                        quotes.append(input("Are there any 'headline' quotes in this release? \n *place each quote in quotations and seperated by a dash, or just say 'No quotes'* \n"))
                        file_allocation(gpt_processing.classify_file(title))
                        news.append(news == "yes")
                        print_lists()
                else:
                    print('This release already exists in the database.\n')
        elif manual == 'automatic':
            scrape_type = input('Which source do you want to scrape? \n[StatsCan, BoC] \n')
            if scrape_type == 'StatsCan':
                temp_titles, temp_release_dates, temp_urls, temp_dates_retrieved, temp_summary, temp_files, temp_institution, temp_quotes = statscan_mon.statcan_monitor(all_files_copy, driver)
                titles.extend(temp_titles)
                release_dates.extend(temp_release_dates)
                urls.extend(temp_urls)
                dates_retrieved.extend(temp_dates_retrieved)
                quotes.extend(temp_quotes)
                for x in range(len(temp_urls)):
                    news.append(False)
                summaries.extend(temp_summary)
                for x in temp_files:
                    file_allocation(x)
                institutions.extend(temp_institution)
            elif scrape_type == "BoC":
                #(titles, release_dates, urls, dates_retrieved, summary, files, institution, quotes)
                temp_titles, temp_release_dates, temp_urls, temp_dates_retrieved, temp_summary, temp_files, temp_institution = boc_mon.boc_monitor(all_files_copy, driver)
                titles.extend(temp_titles)
                release_dates.extend(temp_release_dates)
                urls.extend(temp_urls)
                dates_retrieved.extend(temp_dates_retrieved)
                summaries.extend(temp_summary)
                for x in temp_files:
                    file_allocation(x)
                institutions.extend(temp_institution)
        elif manual =='email':
            s_a_email = input("Do you wish to send an email only to you or to all advisor? [you, all]\n")
            if s_a_email == 'you':
                email = True
                if summaries:
                    while email:
                        email_question = input("Do you wish to send an email summary regarding one of the reports? [yes, no] \n")
                        if email_question == 'yes':
                            for x in range(len(summaries)):
                                print(f"[{x}] - {titles[x]} \n")
                            number = input('Type the number of the corresponding report to email.\n')
                            send_email.send_email(summaries[int(number)], titles[int(number)], institutions[int(number)], quotes[int(number)])
                            print("Email sent.\n")
                        elif email_question == 'no':
                            print('Thank you. Have a great rest of your day!')
                            email = False
            elif s_a_email == 'all':
                send_email.advisor_send(all_files_copy)
        elif manual == 'exit':
            stay_on = False
    
    print_lists()
    #TODO: issue is in the zip
    df_extended = pd.DataFrame(
        zip(release_dates, titles, urls, dates_retrieved, summaries, quotes, institutions,
            release_files[0], release_files[1], advisors[0], advisors[1], news),
        columns=["release_date", 'title', 'url', 'date_retrieved', 'summary', 'quotes', 'institution',
                 "file_1", "file_2", "file_advisor_1", "file_advisor_2", "news_bool"]
    )

    #TODO: revert all changes (remove gpt_processing comments)
    
    print(f"loaded dataframe: {df_extended.shape}")
    print(f"data lake pre entry: {all_files_copy.shape}")
    all_files_copy = pd.concat([df_extended, all_files_copy], ignore_index=True)   
    print(f"concatenated: {all_files_copy.shape}")     
    all_files_copy.to_csv('storage/final_loaded.csv', encoding='utf-8', index=False)
    all_files_copy.to_json('storage/final_loaded.json', 'records', indent=2)
    load_storage.upload_storage()
    driver.quit()

"""
release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_yesdate).group()
release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
"""
    