from openai import AzureOpenAI, OpenAI
import instructor
from textwrap import dedent
from utils.utils import num_tokens_from_string
import json
import os


class HistoryAgent:

    def __init__(self, model_name='gpt4-0125-Preview'):
        AZURE_OPENAI_API_KEY = 'a5552ab2d19f422fa2035b0823a6e3c4'
        AZURE_OPENAI_ENDPOINT = 'https://scc-01-eeatus-gpt-group01-model01.openai.azure.com/'
        API_VERSION = '2024-02-15-preview'
        AZURE_DEPLOYMENT = model_name
        self.system_prompt = {
            'role': 'system',
            'content': dedent(f'你是一位资深的中国历史学家，有着卓越的历史研究能力，擅长史料的分析思辨，对司马光主编的资治通鉴有深入研究，你根据用户提供的资治通鉴译文，完成相关的任务。你尽力做好你的任务，我会给你一个$1000的奖励。')
        }

    def agent(self, model_name='gpt4-0125-Preview', messages=[], response_model=None):
        if 'gpt' in model_name:
            client = instructor.patch(AzureOpenAI(
                api_key=AZURE_OPENAI_API_KEY, api_version=API_VERSION, azure_deployment=AZURE_DEPLOYMENT, azure_endpoint=AZURE_OPENAI_ENDPOINT))
            messages.insert(0, self.system_prompt)
            print(messages)
            response = client.chat.completions.create(
                model=model_name,
                response_model=response_model,
                temperature=0.0,
                messages=messages
            )
            response = response.model_dump_json(indent=2)
            response = json.loads(response)['choices'][0]['message']['content']
            return response
        elif 'local' in model_name:
            client = OpenAI(
                api_key="0",
                base_url="http://localhost:{}/v1".format(
                    os.environ.get("API_PORT", 8000)),
            )
            response = client.chat.completions.create(
                model=model_name,
                response_model=response_model,
                temperature=0.0,
                messages=messages
            )
            response = response.model_dump_json(indent=2)
            response = json.loads(response)['choices'][0]['message']['content']
            return response


if __name__ == '__main__':
    ha = HistoryAgent()
    response = ha.agent(messages=[
        {
            'role': 'user',
            'content': '讲一下汉代的温室之树',
        }
    ], model_name='local')
    print(response)
