""" Copyright 2024 Emanuel Bierschneider

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. """
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