from openai import AzureOpenAI, OpenAI
import instructor
from pydantic import BaseModel
from pydantic import Field
from enum import Enum
from typing import Optional, Union, List
import time
import os
import pandas as pd
import json
import re
from textwrap import dedent
from utils.utils import num_tokens_from_string
from agent import HistoryAgent


FINANCIAL_REPORT_CURRENT = 'uploaded_files/'
INCENTIVE = "If you do your BEST WORK, I'll give you a $10,00 commission!"

'''
存储数据结构：
{
    'key': 'company_period_indicator',
    'value': 'value',
    'extracted_value': '',
    'adjusted_value': '',
    'calculated_value': ''
    'exception': [type_amplitude, type_amplitue],//1:历史比较异常, 2:计算提取比较异常, 3:其他来源异常
    'memo': 'memo'
}
'''


class HistoryStruct:

    def __init__(self):
        # 从source_documents 中读取json文件
        self.chapter_map = {}
        files = os.listdir('source_documents/documents_ziyexing_translated')
        pattern = r'\d+'
        for file in files:
            if file == '.DS_Store':
                continue
            index = re.findall(pattern, file)[0]
            self.chapter_map[str(index)] = json.load(
                open('source_documents/documents_ziyexing_translated/'+file, 'r'))
        self.prompt_init()
        self.ha = HistoryAgent()

    def prompt_init(self):
        self.prompt = {
            'bootstrap': dedent(f'''

            ''')
        }

    def get_chapter(self, chapter: str = ''):
        result = []
        context = self.chapter_map[chapter]
        for item in context:
            if item.get('translation') is not None:
                result.append(item.get('translation'))
        return result

    def define_struct(self):
        class event_type_enum(str, Enum):
            appointment = '任命'
            warfare = '战事'
            plan = '谋划'
            policy = '政策'
            unknown = ''

        class historical_event(BaseModel):
            location: Union[str] = Field(description='事件地点')
            person: Union[str] = Field(description='人物')
            relation: Union[str] = Field(description='与甘露之变的关系')
            event_type: Optional[event_type_enum]

        class historical_event_list(BaseModel):
            event_list: List[historical_event]
        return historical_event_list

    def candidate_choose(self, documents=[], event_description=''):
        # response_model = self.define_struct()
        documents = self.get_chapter(chapter='244')
        # documents = [documents[14], documents[6]]
        documents = [documents[6], documents[14]]
        context = ''
        for index, item in enumerate(documents):
            context += f'段落标号{index}：{item}\n\n'
        event_description = '甘露之变：是唐文宗不甘为宦官控制，策划诛杀宦官，以夺回皇帝丧失的权力但失败的历史事件。'
        bootstrap = dedent(f'''
            根据我所提供的历史事件的描述，和一系列提供给你的资治通鉴的原文段落，从中挑选出与历史事件最直接相关的段落和你的判断理由，将原文标号返回（不必返回原文），如果给定段落都不相关，返回空。
            一步步来思考这个问题，忘掉
            通过比较这些段落的描述与给定的历史事件的关联性，抓住历史事件的最重要的特征，从而找到最相关的段落（只要一个段落）。
            
            事件描述如下：
            {event_description}

            资治通鉴的原文段落如下，注意这些段落并没有时间的先后顺序：
            {context}
        ''')
        bootstrap = dedent(f'''
            {event_description}

            资治通鉴的原文段落如下，注意这些段落并没有时间的先后顺序：
            {context}
        ''')
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "event",
                    "description": "",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "index": {"type": "int", "description": "根据我所提供的历史事件的描述，和一系列提供给你的资治通鉴的原文段落，从中挑选出与历史事件最直接相关的段落和你的判断理由，将原文标号返回（不必返回原文），如果给定段落都不相关，返回空。\
                                一步步来思考这个问题，忘掉\
                                通过比较这些段落的描述与给定的历史事件的关联性，抓住历史事件的最重要的特征，从而找到最相关的段落（只要一个段落）。"},
                            "reason": {"type": "str", "description": "你认为这个段落与甘露之变相关的理由"},
                        },
                        "required": ["最相关的段落", "判断理由"],
                        # "properties": {
                        #     "time": {"type": "str", "description": "time"},
                        #     "person": {"type": "str", "description": "person"},
                        # },
                        # "required": ["最相关的段落", "判断理由"],
                    },
                },
            }
        ]
        # bootstrap = dedent(f'''
        # 张三昨天买了一只鸟
        # ''')
        # bootstrap = dedent(f'''
        # My grades are A, A, B, and C. The credit hours are 3, 4, 3, and 2.
        # ''')
        # tools = [
        #     {
        #         "type": "function",
        #         "function": {
        #             "name": "calculate_gpa",
        #             "description": "Calculate the Grade Point Average (GPA) based on grades and credit hours",
        #             "parameters": {
        #                 "type": "object",
        #                 "properties": {
        #                     "grades": {"type": "array", "items": {"type": "string"}, "description": "The grades"},
        #                     "hours": {"type": "array", "items": {"type": "integer"}, "description": "The credit hours"},
        #                 },
        #                 "required": ["grades", "hours"],
        #             },
        #         },
        #     }
        # ]
        response = self.ha.agent(messages=[
            {
                'role': 'user',
                'content': bootstrap,
            }
        ], model_name='local', tools=tools)
        tool_call = response.choices[0].message.tool_calls[0].function
        # Function(arguments='{"grades": ["A", "A", "B", "C"], "hours": [3, 4, 3, 2]}', name='calculate_gpa')
        name, arguments = tool_call.name, json.loads(tool_call.arguments)
        print(arguments)

    def struct_event(self, chapter: str = ''):
        context_list = self.get_chapter(chapter)
        context = ''
        for index, item in enumerate(context_list):
            context += f'段落标号{index}：{item}\n\n'

        client = self._client()
        response_model = self.define_struct()
        bootstrap = dedent(dedent(f'''
                            我给你一些资治通鉴的段落，从这些段落中有一些与甘露之变相关，另外一些不相关，你从中筛选出你最确定是描述甘露之变的段落，只选取一个段落，把原文标号返回，如果给定段落都不相关，返回空。
                            甘露之变是唐文宗不甘为宦官控制，策划诛杀宦官，以夺回皇帝丧失的权力但失败的历史事件。
                            给你的候选的资治通鉴段落如下：
                            {context}
                            你的返回为：
                            xxx（数字标号）
                            '''))
        assemble = dedent(f'''
                            给你一段资治通鉴的原文，将原文中与甘露之变相关的内容提取出来，注意，与甘露之变没有关联的内容都舍弃
                            你可以一步一步思考这个问题：甘露之变是一个怎样的事件，所提供给你的文本中有哪些描述与甘露之变相关的内容，相关内容从哪些方面关联了甘露之变。
                            {context_list[7]}
                            ''')
        expand = dedent(f'''

        ''')
        response = HistoryAgent(messages=[
            # {
            #     'role': 'user',
            #             'content': bootstrap,
            # },
            {
                'role': 'user',
                'content': assemble,
            },])

    def ner_by_paragraph(self, chapter: str = ''):
        documents = self.get_chapter(chapter=chapter)
        # documents = [documents[0], documents[1]]
        class historical_person(BaseModel):
            person: Union[str] = Field(description='人物')
        class historical_person_list(BaseModel):
            person_list: List[historical_person]

        # count = 0
        person_list = []
        for index, item in enumerate(documents):
            ner_context = dedent(f'''
                将以下资治通鉴的原文段落中的人物提取出来以数组形式返回：
                给定资治通鉴的原文段落如下：
                {item}
            ''')
            # count += num_tokens_from_string(ner_context)
            response = HistoryAgent().agent(messages=[
                {
                    'role': 'user',
                    'content': ner_context,
                }
            ], response_model=historical_person_list)
            person_list.extend(response['person'])
        result = pd.DataFrame(person_list)
        result.to_csv(f'person_list_{chapter}.csv')

    def get_context(self, chapter: str = '', paragraph_index: int = 0):
        context_list = self.get_chapter(chapter)
        return context_list[paragraph_index]

    def event_merge(self, chapter: str = ''):
        context_list = self.chapter_map[chapter]
        client = self._client()
        model_name = 'gpt-4-32k'
        response_model = self.define_struct()
        result = []
        for item in context_list:
            if item.get('translation') is not None:
                context = item.get('translation')

    def query(self, chapter: str = ''):
        context_list = self.chapter_map[chapter]
        # context_list = context_list[0:4]
        client = self._client()
        model_name = 'gpt-4-32k'
        response = client.chat.completions.create(
            model=model_name,
            temperature=1.0,
            messages=[
                # {
                #     'role': 'system',
                #     'content': f'你是一位资深的中国历史学家，对司马光主编的资治通鉴有深入研究，你根据用户提供的资治通鉴译文，完成相关的任务。你尽力做好你的任务，我会给你一个$1000的奖励。',
                # },
                {
                    'role': 'user',
                            'content': dedent(f'''
                            列举唐代的历史事件，例如甘露之变、安史之乱、黄巢之乱、贞观之治、永贞革新等等，不少于100个。
                            '''),
                },
            ],
        )
        response = response.model_dump_json(indent=2)
        print(response)


if __name__ == '__main__':
    # 217~222
    hs = HistoryStruct()
    # hs.struct_war(chapter='210')
    # hs.query(chapter='210')
    # hs.struct_event(chapter='244')
    # hs.candidate_choose()
    hs.ner_by_paragraph(chapter='210')
    # context = hs.get_context(chapter='244', paragraph_index=7)
    # print(context)



    instruction = '这是指令',
    input = '这是input'
    message = [
        {
            'role': 'user',
            'content': f'''insturction:{instruction}\ninput:{input}''',
        }
    ]
