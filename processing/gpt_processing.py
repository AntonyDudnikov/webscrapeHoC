import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

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
    Return the format in a HTML format under these rules:
        - headings use <h3>
    """

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
            elif x >= 1:
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

def pbo_processing(output):
    """
    GPT API request for parliamentary budget office reports
    Input: dictionary of release metadata and content
    Output: string content of GPT LLM output
    """
    response = client.chat.completions.create(
        model = 'gpt-4-1106-preview',
        #model="gpt-3.5-turbo-1106",
        temperature=0.0,
        stream=False,
        messages=[
            {"role":"system", 'content': system_prompt},
            {'role': 'user', 'content': print_result(output)}
        ]
    )
    return response.choices[0].message.content

def rbc_processing():
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