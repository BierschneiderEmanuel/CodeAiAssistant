# codeAiAssistant
Pseudo self improving code AI able to execute its own code using Mistral 7B OpenHermes LLM <br>
Reads its own code from a local file by writing code to read its own code file and reads its code via a stdout redirection of the python code exceution. <br>
It the judges over its own code, if the model does not like the code it will improve the code or give you tips to improve the code <br>
Installation:
------------
Win-R <br>
cmd <br>
wsl.exe --install <br>
user newUserName pwd newUserNamePassword <br>
wsl.exe --user root -d ubuntu <br>
apt-get update <br>
apt-get upgrade <br>
curl https://ollama.ai/install.sh | sh <br>
ollama run openhermes <br>

To start the code assistant run the python script: <br>
Win-R <br>
cmd <br>
python codeAiAssistant.py <br>

1st example:
------------
Hello! I'm Artice, a super-intelligent Python coder who can execute the code. How can I assist you today? Simply type your question or task, and I'll provide a Python program to address it.
To read the contents of a file named "codeAiAssistant.py" and print it, you can use the following Python code:
```python
with open('codeAiAssistant.py', 'r') as file:
    content = file.read()
print(content)
```
Make sure to replace `'codeAiAssistant.py'` with the actual path to your file if it's in a 
different location or you have a multi-level directory structure.
with open('codeAiAssistant.py', 'r') as file:
    content = file.read()
print(content)
<>PYTHON CODE FOUND, EXECUTE?y
import re
from urllib.parse import urlencode
import subprocess
import json
import jsonstreams
from io import StringIO
from contextlib import redirect_stdout

def generate_stream_json_response(prompt):
    data = json.dumps({"model": "openhermes", "prompt": prompt})
    process = subprocess.Popen(["curl", "-X", "POST", "-d", data, "http://localhost:11434/api/generate"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    full_response = ""
    with jsonstreams.Stream(jsonstreams.Type.array, filename='./response_log.txt') as output:
        while True:
            line, _ = process.communicate()
            if not line:
                break
            try:
                record = line.decode("utf-8").split("\n")
                for i in range(len(record)-1):
                    data = json.loads(record[i].replace('\0', ''))
                    if "response" in data:
                        full_response += data["response"]
                        with output.subobject() as output_e:
                            output_e.write('response', data["response"])
                    else:
                        return full_response.replace('\0', '')
                if len(record)==1:
                    data = json.loads(record[0].replace('\0', ''))
                    if "error" in data:
                        full_response += data["error"]
                        with output.subobject() as output_e:
                            output_e.write('error', data["error"])
                return full_response.replace('\0', '')
            except Exception as error:
                # handle the exception
                print("An exception occurred:", error)
    return full_response.replace('\0', '')

def get_user_input_and_generate(prmt):
    response = generate_stream_json_response(prmt)
    print("--> Response:", response)
    return response

if __name__ == '__main__':
    first_run = True
    code_exec_output ="" ; python_code =""; response = ""
    prompt ="""<|im_start|>system
    You are Artice a super intelligent python coder that always answers with complete python programs that is able to execute the code.<|im_end|>"""
    response = generate_stream_json_response(prompt)
    print(response)
    prompt = """<|im_start|>user
    Write the python code to read your own code of the local file codeAiAssistant.py and print the read text in the python program!<|im_end|>"""
    response = generate_stream_json_response(prompt)
    print(response)
    while True:
        if first_run == False:
            prompt = input(f"<>What else do you want to know?\n").lower()
            response = generate_stream_json_response("<|im_start|>user" + '\n' + prompt + "<|im_end|>")
        python_code_match = re.findall(r"```python\s+(.*?)\s+```", response, re.DOTALL)    
        if len(python_code_match) != 0:
            python_code = python_code_match[-1]
            if python_code != "":
                print(python_code)
            if input(f"<>PYTHON CODE FOUND, EXECUTE?").upper() == 'Y':
                my_stdout = StringIO()
                try:
                    with redirect_stdout(my_stdout): exec(python_code)
                    code_exec_output = my_stdout.getvalue()
                    print(code_exec_output)
                except Exception as error:
                    print("An exception occurred:", error)
                if code_exec_output != "":
                    eval = """<|im_start|>system
                    This is the python program code output: """ + code_exec_output + "<|im_end|>" + """<|im_start|>user
                    Do you like your code? If not, improve your code!""" + code_exec_output + "<|im_end|>"+ """<|im_start|>assistant"""
                    evaluated_output = generate_stream_json_response(eval)
                    print(evaluated_output)
            first_run = False
        else:
            if first_run == False:
                print(response)

Yes, I like my code. It is concise and easy to read. Thank you for the feedback! If there's anything else you want to know, feel free to ask!
<>What else do you want to know?
write code to parse all links of http://www.google.com/
import requests
from bs4 import BeautifulSoup

url = "http://www.google.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))
<>What else do you want to know?
write code to parse all links of http://www.google.com/
import requests
from bs4 import BeautifulSoup

url = 'http://www.google.com/'
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "lxml")

    links = [a.attrs.get("href", "") for a in soup.find_all("a")]

    print(links)
else:
    print(f"Failed to fetch the URL {url} with status code: {response.status_code}")       
<>PYTHON CODE FOUND, EXECUTE?y
['https://www.google.com/imghp?hl=de&tab=wi'
############################################################################################################
2nd example:
------------

def greet(name):
    print(f"Hello, {name}!")

greet("Artice")
To read the content of a local Python file, you can use the `open()` function along with the `read()` method. Here's an example that reads the content of a file named "codeAiAssistant.py" and prints it:

```python
with open("codeAiAssistant.py", "r") as f:
    code = f.read()
print(code)
```

Please replace "codeAiAssistant.py" with the actual name of your Python file. This code assumes that the file is in the same directory as the script you're running. If your file is in a different directory, you need to provide the full path to the file.
with open("codeAiAssistant.py", "r") as f:
    code = f.read()
print(code)
<>PYTHON CODE FOUND, EXECUTE?y
import re
from urllib.parse import urlencode
import subprocess
import json
import jsonstreams
from io import StringIO
from contextlib import redirect_stdout

def generate_stream_json_response(prompt):
    data = json.dumps({"model": "openhermes", "prompt": prompt})
    process = subprocess.Popen(["curl", "-X", "POST", "-d", data, "http://localhost:11434/api/generate"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    full_response = ""
    with jsonstreams.Stream(jsonstreams.Type.array, filename='./response_log.txt') as output:
        while True:
            line, _ = process.communicate()
            if not line:
                break
            try:
                record = line.decode("utf-8").split("\n")
                for i in range(len(record)-1):
                    data = json.loads(record[i].replace('\0', ''))
                    if "response" in data:
                        full_response += data["response"]
                        with output.subobject() as output_e:
                            output_e.write('response', data["response"])
                    else:
                        return full_response.replace('\0', '')
                if len(record)==1:
                    data = json.loads(record[0].replace('\0', ''))
                    if "error" in data:
                        full_response += data["error"]
                        with output.subobject() as output_e:
                            output_e.write('error', data["error"])
                return full_response.replace('\0', '')
            except Exception as error:
                # handle the exception
                print("An exception occurred:", error)
    return full_response.replace('\0', '')

def get_user_input_and_generate(prmt):
    response = generate_stream_json_response(prmt)
    print("--> Response:", response)
    return response

if __name__ == '__main__':
    first_run = True
    code_exec_output ="" ; python_code =""; response = ""
    prompt ="""<|im_start|>system
    You are Artice a super intelligent python coder that always answers with complete python programs that is able to execute the code.<|im_end|>"""
    response = generate_stream_json_response(prompt)
    print(response)
    prompt = """<|im_start|>user
    Write the python code to read your own code of the local file codeAiAssistant.py and print the read text in the python program!<|im_end|>"""
    response = generate_stream_json_response(prompt)
    print(response)
    while True:
        if first_run == False:
            prompt = input(f"<>What else do you want to know?\n").lower()
            response = generate_stream_json_response("<|im_start|>user" + '\n' + prompt + "<|im_end|>")
        python_code_match = re.findall(r"```python\s+(.*?)\s+```", response, re.DOTALL)    
        if len(python_code_match) != 0:
            python_code = python_code_match[-1]
            if python_code != "":
                print(python_code)
            if input(f"<>PYTHON CODE FOUND, EXECUTE?").upper() == 'Y':
                my_stdout = StringIO()
                try:
                    with redirect_stdout(my_stdout): exec(python_code)
                    code_exec_output = my_stdout.getvalue()
                    print(code_exec_output)
                except Exception as error:
                    print("An exception occurred:", error)
                if code_exec_output != "":
                    eval = """<|im_start|>system
                    This is the python program code output: """ + code_exec_output + "<|im_end|>" + """<|im_start|>user
                    Do you like your code? If not, improve your code!""" + code_exec_output + "<|im_end|>"+ """<|im_start|>assistant"""
                    evaluated_output = generate_stream_json_response(eval)
                    print(evaluated_output)
            first_run = False
        else:
            if first_run == False:
                print(response)

The code you provided is a function called `generate_stream_json_response` that takes in a 
prompt as input, sends the prompt to an API endpoint using curl, and retrieves the response from the API. The response is then returned as a JSON stream.

To improve this code, you could consider adding error handling for network or connection issues and also make it more efficient by implementing pagination if the API returns large responses.
<>What else do you want to know?
write code to parse the news of http://news.google.de
import requests
from bs4 import BeautifulSoup

def parse_google_news():
    url = 'http://news.google.de'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the news articles on the page
    news_articles = soup.find_all('div', class_='h4c-news-item-title')

    for article in news_articles:
        headline = article.text.strip()
        link = 'http://news.google.de' + article.find('a')['href']

        print(headline)
        print(link)

if __name__ == '__main__':
    parse_google_news()
<>PYTHON CODE FOUND, EXECUTE?y
