
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from classes import rbc
from classes import statcan
from classes import pbo
from classes import boc
from classes import source
import pprint
"""
ADD CMHC MEDIA RELEASES
"""


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
                

    #______statcan______
    # stat1 = statcan.Statcan(url="https://www150.statcan.gc.ca/n1/daily-quotidien/240111/dq240111a-eng.htm", 
    #            release_date='11/01/2024', driver=driver)
    # stat1.statcan_scrape()
    # print(stat1)
    # print_result(stat1.output)

    #_______BoC 1_______
    # boc1 = boc.Boc(url='https://www.bankofcanada.ca/2023/11/quarterly-financial-report-third-quarter-2023/',
    #                 type='Quarterly Financial Report',
    #                 release_date='30/09/2023',
    #                 driver=driver)
    # boc1.boc_scrape()
    # print(boc1)
    # print_result(boc1.output)
    # print(boc1.output['headings'])

    #_______BoC 2_______
    # boc2 = boc.Boc(url='https://www.bankofcanada.ca/2023/03/summary-governing-council-deliberations-fixed-announcement-date-march-8-2023/', 
    #                type= 'Summary of Deliberations',
    #                release_date='22/03/2023',
    #                driver=driver)
    # boc2.boc_scrape()
    # print(boc2)
    # print_result(boc2.output)
    # print(boc2.output['headings'])

    # #_______RBC 1_______
    # rbc1 = rbc.Rbc(url='https://thoughtleadership.rbc.com/all-quiet-on-most-fronts-in-canadas-housing-markets/',
    #                email=False,
    #                release_date='7/12/2023',
    #                driver=driver)
    # rbc1.rbc_website()
    # print(rbc1)
    # print_result(rbc1.output)

    # #_______RBC 2_______
    # rbc2 = rbc.Rbc(url='http://view.website.rbc.com/?qs=b17d27d115dc6462d30b3bf759c2b60df4c4e8545f2f973b9660a45f356c1f9d96414077fb709496fd549c18fa1e1a28fbc37f4731b7c2620365be318d77392a9ea922d8fe1768fbb72456617e5e5160',
    #                email=True,
    #                release_date='11/12/2023',
    #                driver=driver)
    # rbc2.rbc_email_scrape()
    # print(rbc2)
    # print(rbc2.output['content'])

    # #_______pbo 1_______
    pbo1 = pbo.Pbo(url='https://www.pbo-dpb.ca/en/publications/LEG-2324-017-M--revenue-corporate-tax-rate-increase-based-ceo-median-worker-pay-ratio--recettes-tirees-augmentation-taux-imposition-societes-fondee-ratio-entre-salaire-pdg-comparativement',
                   report=False,
                   release_date='6/12/2023',
                   title='Revenue of a Corporate Tax Rate Increase Based on CEO-to-Median Worker Pay Ratio',
                   driver=driver)
    pbo1.pbo_scrape()
    print(pbo1)

    # #_______pbo 2_______
    # pbo2 = pbo.Pbo(url='https://www.pbo-dpb.ca/en/publications/RP-2324-020-S--costing-support-ev-battery-manufacturing--etablissement-couts-soutien-accorde-fabrication-batteries-ve',
    #                report=True,
    #                release_date='17/11/2023',
    #                title='Costing Support for EV Battery Manufacturing',
    #                driver=driver)
    # pbo2.pbo_scrape()
    # print(pbo2)
    # print(pbo2.output)



    driver.quit()
"""
TODO: include a parser that seperates the <p> and <ul> with the same format as BoC
TODO: standardize the scraping output for all scrapers
TODO: learn and create tests
"""

"""
release_date = re.search( r'(\w+ \d{1,2}, \d{4})', release_date).group()
release_date = datetime.strptime(release_date, "%B %d, %Y").strftime("%d/%m/%Y")
"""
    