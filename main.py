
from selenium.webdriver.chrome.service import Service
from processing import gpt_processing
from selenium import webdriver
from classes import statcan, rbc, pbo, boc, source
from gmail import send_email
import pprint


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("----------------------------")
    #rbc.rbc_email_scrape("http://view.website.rbc.com/?qs=252693f6703bfe6d95f0c536c2c7ee9f7244cf155cbfebb7c0d992e5f5b31a311ad856fb417e3136f18422d16689747e4d3c542f49bed74450aa1d874c8eff0315fcb987ab8a6a8a9984a8deeebde978")
    #rbc.rbc_email_scrape('http://view.website.rbc.com/?qs=a15bb554423f2e6a43da32adab780a64a077f0addb8582d5923332f64ce294472d01b53f8817b134041c7da41846f02f7037165d5c0398488bfec2dcd050deebe4864bb2b2aeb21102d2bb70cacc6ca2')
    #pprint.pp(statcan.statcan_scrape("https://www150.statcan.gc.ca/n1/daily-quotidien/231212/dq231212a-eng.htm"), indent=2)
    #pbo.pbo_scrape(url= 'https://www.pbo-dpb.ca/en/publications/LEG-2324-018-S--amendment-excise-tax-act-exempt-psychotherapy-mental-health-support-services-from-gst--modification-loi-taxe-accise-afin-exonerer-services-psychotherapie-accompagnement-sante-mentale-tps', report=False)
    #rbc.rbc_website(url='https://thoughtleadership.rbc.com/rbc-consumer-spending-tracker/')
    service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
    options= webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options, service=service)

    def print_result(output):
        if not output['p_first']:
            for x in range(len(output['headings'])):
                print('__________________________') 
                print(output['headings'][x])
                print(output['content'][x])
        else:
            for x in range(len(output['content'])):
                print('__________________________')
                if x >= 1:
                    print(output['headings'][x-1])                
                print(output['content'][x])

    stat1 = statcan.Statcan(url="https://www150.statcan.gc.ca/n1/daily-quotidien/240119/dq240119b-eng.htm", release_date='19/01/2024', driver=driver)
    stat1.statcan_scrape()
    print(stat1)
    gpt_output = gpt_processing.statcan_processing(stat1.output)
    print(gpt_output)
    send_email.send_email(gpt_output, stat1.output['title'])



    driver.quit()
"""
TODO: include a parser that seperates the <p> and <ul> with the same format as BoC
TODO: classify the corresponsing release for file
TODO: start monitoring stage

"""

"""
release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_date).group()
release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
"""
    