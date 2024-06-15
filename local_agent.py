import json
from openai import OpenAI
BASE_URL = 'https://127.0.0.1:8000/v1'


def local_client():
    messages = [
        {
            'role': 'user',
            'content': '你是谁？',
        }
    ]
    base_url = BASE_URL
    client = OpenAI(
        api_key="0",
        base_url=LOCAL_BASE_URL,
    )
    response = client.chat.completions.create(
        model='test',
        # temperature=1.0,
        messages=messages
    )
    print(response)
    return response
