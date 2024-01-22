from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import datetime
import pprint
import json

class Source:
    
    def __init__(self) -> None:
        self.output = {'date_retrieved': datetime.date.today().strftime("%d/%m/%Y")}

    def __str__(self) -> str:
        return pprint.pformat(self.output, indent=2, width=90, compact=True, depth=1)
    
    def setup_driver(self):
        service = Service(executable_path="C:\Program Files (x86)\chromedriver.exe")
        options= webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options, service=service)
        return driver
    
    def convert_to_json(self) -> json:
        return json.dumps(self.output)