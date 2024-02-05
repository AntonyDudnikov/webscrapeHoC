import os
import re
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

quote_prompt = """You are a news article writer and you need to identify from the content
    supplied with a tripple quotation delimiter any headline worthy quotes. Seperate 
    each quote with a "-"
"""

system_prompt = """You are a policy analyst tasked with summarising Statistics Canada reports
    supplied with the triple quotation delimiter. Follow these instructions:
    1. For each heading, output the heading surrounded with '**' and
        list each variable mentioned in the section. Each variable is surrounded with '*'
    2. Under each variable mentioned, further indent, and list the changes and values of 
        the variable without extra words. Place the percentage first and the amount changed in parenthesis afterwards. 
    3. At the end of report, include a 100 word max summary headed by 'Summary'

    Lastly, be concise in displaying the facts.
    """

system_prompt2 = """You are a policy analyst tasked with summarising Statistics Canada reports
    supplied with the triple quotation delimiter. Follow these instructions:
    1. For each heading, output the heading and
        list each variable mentioned in the section.
    2. Under each variable mentioned, further indent, and list the changes and values of 
        the variable without extra words. Place the percentage first and the amount changed in parenthesis afterwards. 
    3. At the end of report, include a 100 word max summary headed by 'Summary'

    Lastly, be concise in displaying the facts.
    Format the structure with the Summary at the top and the statistics below it.
    Return the format in a HTML format under these rules:
        - headings use <h3>
    """

summary_prompt = """You are a policy analyst tasked with summarising reports
    supplied with the triple quotation delimiter. Please provide a 100 words max summary.
"""

classifying_prompt = """You are given a title of a report and you must classify them into 2 of the most corresponding policy files.
    Return just the file names, with no dashes, seperated by ";".
    Here are the possible files:
    - Digital Government
    - Agriculture, Agri-Food and Food Security
    - Canadian Heritage
    - Crown-indigenous Relations
    - Finance and Middle Class Prosperity
    - Employment, Future Workforce Development and Disability Inclusion
    - Environment and Climate Change
    - Families, Children and Social Development
    - Federal Economic Development Agency for Eastern, Central and Southern Ontario
    - Fisheries, Oceans and the Canadian Coast Guard
    - Foreign Affairs
    - Health
    - Housing and Diversity and Inclusion
    - Immigration, Refugees and Citizenship
    - Federal Economic Development Agency for Northern Ontario
    - Innovation, Science and Industry 
    - International Development 
    - International Trade
    - Supply Chain Issues
    - Small Business Recovery and Growth 
    - Red Tape Reduction
    - Justice and Attorney General of Canada 
    - Mental Health and Suicide Prevention 
    - Addictions
    - Northern Affairs and Artic Sovereignty; Canadian Northern Economic Development Agency
    - Prairie Economic Development (Advisor to the Leader, Economy)
    - Pacific Economic Development 
    - Sport, Economic Development Agency of Canada for the Regions of Quebec
    - National Defence 
    - National Revenue 
    - Natural Resources 
    - Official Languages 
    - Atlantic Canada Opportunities Agency 
    - Public Safety 
    - Public Services and Procurement 
    - Emergency Preparedness 
    - Rural Economic Development & Connectivity
    - Seniors
    - Tourism
    - Transport
    - Treasury Board 
    - Veterans Affairs
    - Women and Gender Equality and Youth 
    - Ethics and Accountable Government
    - Infrastructure and Communities 
    - Labour
    - Indigenous Services 
    - Pan-Canadian Trade and Competition
    - Hunting, Fishing and Conservation
    - Democratic Reform
    """

def summary_gpt_extraction(gpt_output) -> str:
    try:
        matches = re.findall(re.compile(r'<p>(.*?)</p>', re.DOTALL), gpt_output)
        return matches[0]
    except:
        print("NOT AVAILABLE")

def quote_identifier(output, manual:bool) -> str:
    response = client.chat.completions.create(
        model = 'gpt-4-1106-preview',
        #model="gpt-3.5-turbo-1106",
        temperature=0.5,
        stream=False,
        messages=[
            {"role":"system", 'content': quote_prompt},
            {'role': 'user', 'content': output if manual else print_result(output)}
        ]
    )
    reply = response.choices[0].message.content
    reply = re.sub('-\n', '', reply)
    return reply

def print_result(output) -> str:
    #TODO create  before gpt processing
    """
    convert webscrape output into human dialogue for LLM to process
    Input: dictionary of release meta date and content
    Output: single string 
    """
    result = """"""
    if not output['p_first']:
        for x in range(len(output['headings'])):
            result +='\n'
            result += f"heading: {output['headings'][x]}\n"
            result += output['content'][x] + '\n'
    else:
        for x in range(len(output['content'])):
            result +='\n'
            if x == 0:
                result += 'Introduction:\n'
            elif x >= 1 and len(output['headings']) > 0:
                result += f"heading: {output['headings'][x-1]}\n"                
            result += output['content'][x] + '\n'
    return result

def statcan_processing(output) -> str:
    """
    GPT API request for Statistics Canada reports
    Input: dictionary of release metadata and content
    Output: string content of GPT LLM output
    """
    response = client.chat.completions.create(
        model = 'gpt-4-1106-preview',
        #model="gpt-3.5-turbo-1106",
        temperature=0.0,
        stream=False,
        messages=[
            {"role":"system", 'content': system_prompt2},
            {'role': 'user', 'content': print_result(output)}
        ]
    )
    return response.choices[0].message.content

def classify_file(title) -> str:
    """
    GPT API request to classify a release title by a corresponding file.
    INPUT: title name of release
    OUTPUT: max of 2 corresponding files
    """
    response = client.chat.completions.create(
        model = 'gpt-4-1106-preview',
        #model="gpt-3.5-turbo-1106",
        temperature=0.0,
        stream=False,
        messages=[
            {"role":"system", 'content': classifying_prompt},
            {'role': 'user', 'content': title}
        ]
    )
    reply = response.choices[0].message.content
    reply = re.sub('\n', '', reply)
    reply = reply.split(';')
    return reply

def summary_processing(output, manual):
    """
    GPT API request for parliamentary budget office reports
    Input: dictionary of release metadata and content
    Output: string content of GPT LLM output
    """
    response = client.chat.completions.create(
        model = 'gpt-4-1106-preview',
        #model="gpt-3.5-turbo-1106",
        temperature=0.3,
        stream=False,
        messages=[
            {"role":"system", 'content': summary_prompt},
            {'role': 'user', 'content': output if manual else print_result(output)}
        ]
    )
    return response.choices[0].message.content

def rbc_processing():
    pass

def manual_input(text):
    pass


#API key

"""
PROMPT ENGINEERING:

- be explicit and detailed in what you want
- povide exmaples of what u are looking for : 
        system(instructions) ->user(ex input)-> assistant(required output) -> user (Q)
- breakdown the task in steps (GPT 4 might be better suited to incorporate more aspects of complex instructions,
        GPT3.5 might just do 1 of the tasks rather than all)
- user of delimiters to sepcify where to perform action
        ex: triple quotations, XML tags, or just specify



ex: 
You will be provided with meeting notes, and your task is to summarize the meeting as follows:
    
    -Overall summary of discussion
    -Action items (what needs to be done and who is doing it)
    -If applicable, a list of topics that need to be discussed more fully in the next meeting.

"""