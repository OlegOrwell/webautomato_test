import openai
import pandas as pd
from utils import addresses
from data_preprocessor import batcher
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import os


class TableConverter:
    def __init__(self):
        openai.api_key = "sk-"
        #  openai.api_key = os.environ['OPENAI_API_KEY']

        self.to_transform = pd.read_csv(addresses["source"])
        self.template = pd.read_csv(addresses["template"])

    def completion(self, prompt):
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            temperature=0,
            max_tokens=590,
        )
        print(response)
        return response

    def create_prompt(self, line):
        # PROMPT = f"""You are smart accountant professional with data sheets. You should extract data from this file ```{line.to_json()}``` about person's full name, the date, the plan type, the policy number and the premium amount. Transform extracted data using column names and data formatting (especially look at how data looks at columns Date, Plan and PolicyNumber) as in few-shot example ```{self.template.head(2).to_json()}```. Put transformed data in json."""  # ++++
        PROMPT = f"""You are smart accountant professional with data sheets. You should extract data from this file ```{line.to_json()}```make sure column names and data formatting are as in few-shot example ```{self.template.head(2).to_json()}```. Put transformed data in json."""
        return PROMPT

    def convert(self):
        batches = batcher(self.to_transform)
        prompts = [self.create_prompt(line) for line in batches]
        results = [self.completion(prompt) for prompt in prompts]

        """Somewhere around here data should be validated. Checking data types, structure etc. 
        A lot of validation.
        Also to detect hallucinations - we should check if facts extracted by model exist in original table.
        And if not raise error or somehow handle it."""

        if len(results) > 1:
            multiple_frames = [pd.read_json(result[0].choices[0].text, keep_default_dates=False) for result in results]
            df = pd.concat(multiple_frames, axis=0).reset_index()
        else:
            df = pd.read_json(results[0].choices[0].text, keep_default_dates=False)

        # Simple data validation
        if is_numeric_dtype(df.Premium) is not True:
            print('!!! Possible error Premium data type ')
        if is_string_dtype(df.EmployeeName) is not True:
            print('!!! Possible error in EmployeeName data type ')

        # Check that EmployeeName name consists of 2 words.
        def names_check(line):
            if len(line.split()) != 2:
                print('!!! Possible error in EmployeeName ')
        df.EmployeeName.apply(lambda x: names_check(x))

        # Simple validation of PolicyNumber
        def policy_check(line):
            if len(line) != 7:
                print('!!! Possible error in PolicyNumber ')
            left = line[:2]
            right = line[2:]
            if type(str(left)) is not str:
                print('!!! Possible error in PolicyNumber ')
            if type(int(right)) is not int:
                print('!!! Possible error in PolicyNumber ')
        df.PolicyNumber.apply(lambda x: policy_check(x))

        df.to_csv(addresses["result"], index=False)
        print(pd.read_csv(addresses["result"]))
        print("File created at this address  ", addresses["result"])
