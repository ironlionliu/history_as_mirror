import re
from bs4 import BeautifulSoup
import tiktoken
import os
from langchain_openai import AzureChatOpenAI
from typing import Optional, Union, List
from enum import Enum
from configobj import ConfigObj


os.environ["AZURE_OPENAI_ENDPOINT"] = "https://scc-01-uks-gpt-group01-model01.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "5c052b9003414d3e81a29f799b5e81f4"
token_max_length = 30000


def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-4-32k")
    num_tokens = len(encoding.encode(string))
    return num_tokens


def openai_client():
    AZURE_DEPLOYMENT = 'gpt-4-32k'
    # AZURE_DEPLOYMENT = 'gpt-35-turbo-16k'
    API_VERSION = '2023-07-01-preview'
    return AzureChatOpenAI(
        temperature=0.0, openai_api_version=API_VERSION, azure_deployment=AZURE_DEPLOYMENT)

def gen_class(attr_json_path:str='', class_name:str=''):
    from pydantic import create_model
    from pydantic.fields import FieldInfo
    import json
    fields = {}
    type_map = {
        "float": float,
        "str": str,
    }
    attr_json = open(attr_json_path, 'r').read()
    for key, item in json.loads(attr_json).items():
        fields[key] = (type_map[item['type']], FieldInfo(description=item['description']))
    model = create_model(class_name, **fields)
    return model

def print_class(MyClass):
    for attr_name in MyClass.__dict__:
        if not attr_name.startswith("__"):  # 排除特殊属性
            attr_value = getattr(MyClass, attr_name)
            print(f"{attr_name}: {attr_value}")


def get_root_path():
    this_file_name = 'utils/utils.py'
    return os.path.dirname(os.path.abspath(__file__).replace(this_file_name, ''))


def get_config():
    config_path = os.path.join(get_root_path(), 'application.cfg')
    config = ConfigObj(config_path)
    return config


if __name__ == "__main__":
    # print(handle_pdf('financial_reports/lenovo.pdf'))
    text = handle_html(
        filepath='financial_reports/qualcomm_call.html', element_path='call')
    # print(text)
    print(len(text))
    print(num_tokens_from_string(text))
