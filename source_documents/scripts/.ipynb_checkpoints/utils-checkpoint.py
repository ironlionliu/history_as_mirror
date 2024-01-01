import requests
from openai import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
# from langchain.chains import create_extraction_chain
from kor import create_extraction_chain, Object, Text, Number
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import openai
import datetime
import os

MAX_RETRIES = 5

#gpt3.5
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://scc-01-eeatus-gpt-group01-model01.openai.azure.com/"
os.environ["AZURE_OPENAI_API_KEY"] = "a5552ab2d19f422fa2035b0823a6e3c4"
#gpt4
# os.environ["AZURE_OPENAI_ENDPOINT"] = "https://scc-01-uks-gpt-group02-model02.openai.azure.com/"
# os.environ["AZURE_OPENAI_API_KEY"] = "0e465d3d46f2496e932a02d4f1c3428a"
# AZURE_DEPLOYMENT = 'gpt-35-turbo'
AZURE_DEPLOYMENT = 'gpt-35-turbo-16k'


def struct_data(schema={}, result=''):
    llm = AzureChatOpenAI(
        temperature=0, openai_api_version="2023-05-15", azure_deployment=AZURE_DEPLOYMENT)
    chain = create_extraction_chain(llm, schema)
    result = chain.run(result)
    return result['data']


def get_turbo_Azure(prompt='', openai_system_prompt=None):
    chat = AzureChatOpenAI(
        temperature=0, openai_api_version="2023-05-15", azure_deployment=AZURE_DEPLOYMENT)
    messages = [
        SystemMessage(
            content="You are a helpful assistant."),
        HumanMessage(content=prompt)
    ]
    res = chat(messages)
    return res.content


def multi_rounds_conversation(prompts=[]):
    template = """You are a chatbot helping human deal with tasks.
    {chat_history}
    Human: {human_input}
    Chatbot:"""
    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"],
        template=template
    )
    memory = ConversationBufferMemory(memory_key="chat_history")
    llm_chain = LLMChain(
        llm=AzureChatOpenAI(temperature=0, openai_api_version="2023-05-15", azure_deployment=AZURE_DEPLOYMENT),
        # llm=AzureChatOpenAI(temperature=0, openai_api_version="2023-05-15", azure_deployment="gpt-4"),
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    for prompt in prompts:
        res = llm_chain.predict(human_input=prompt)
        # print(res)
    memory.clear()
    return res

if __name__ == '__main__':
    res = get_turbo_Azure(prompt="你好，我是小明")
    # res = struct_data(result='明天天气如何')
    print(res)
