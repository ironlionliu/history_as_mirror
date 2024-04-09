import os
import json
from utils import get_turbo_Azure
import requests
from datetime import datetime


def slice_paragraph(document=[]):
    slice_num = 5
    paragraph_list = []
    ave_len = len('\n'.join(document))/slice_num
    current_len = 0
    paragraph = []
    for item in document:
        if current_len >= ave_len:
            paragraph_list.append('\n'.join(paragraph))
            current_len = 0
            paragraph = []
        else:
            paragraph.append(item)
            current_len += len(item)
    paragraph_list.append('\n'.join(paragraph))
    return paragraph_list


def translate_by_glm():
    url = 'http://127.0.0.1:8000/chat'
    directory = '../pure_documents'
    translate_directory = '../translate_documents'
    for filename in os.listdir(directory):
        result_list = []
        if filename.endswith('.json'):
            translate_file_path = f'{translate_directory}/{filename}'
            origin_file_path = f'{directory}/{filename}'

            file_exists = os.path.isfile(translate_file_path)
            if file_exists:
                continue
            else:
                with open(origin_file_path, 'r') as file:
                    document = json.load(file)
                paragraph_list = slice_paragraph(document=document)
                history = [
                    {'role': 'system', 'content': '你是一位历史学家，精通文言文翻译，现在负责资治通鉴的翻译工作，将宋代成书的文言文版资治通鉴翻译成白话的现代汉语'}]
                translated_list = []
                count_paragraph = 0
                for paragraph in paragraph_list:
                    print(
                        f'{filename} begin {count_paragraph} {datetime.now().strftime("%H:%M:%S")}')
                    if len(history) >= 3:
                        history = [history[0], history[-2], history[-1]]
                    else:
                        history = [history[0]]
                    prompt = f'''
                    资治通鉴原文：```{paragraph}```


                    把上面资治通鉴原文翻译成通俗易懂的白话文，翻译时不要遗漏任何一句话，人名保持全称，不要省略姓氏，不要有任何其他的多余内容
                    注意翻译后文本的换行情况与原文保持一致，即原文有段落换行的翻译后也保持换行
                    特别注意，不要在回复中出现资治通鉴原文，直接给出翻译结果
                    '''
                    data = {
                        'prompt': prompt,
                        'history': history
                    }
                    # result = requests.post(url, json=data).json()
                    result = {
                        'response': '',
                        'history': history
                    }
                    response = result['response']
                    history = result['history']
                    translated_list.append(response)
                    print(
                        f'{filename} 完成段落：{count_paragraph} {datetime.now().strftime("%H:%M:%S")}')
                    count_paragraph += 1
                    result_list.append(
                        {
                            'instruction': f'''把给定的资治通鉴原文翻译成通俗易懂的白话文，翻译时不要遗漏任何一句话，人名保持全称，不要省略姓氏，不要有任何其他的多余内容
                    注意翻译后文本的换行情况与原文保持一致，即原文有段落换行的翻译后也保持换行
                    特别注意，不要在回复中出现资治通鉴原文，直接给出翻译结果''',
                            'input': paragraph,
                            'output': [
                                "翻译内容"
                            ]
                        },
                    )

                # with open(f'{translate_directory}/{filename}.txt', 'w', encoding='utf-8') as file:
                #     translated_str = '\n'.join(translated_list)
                #     file.write(translated_str)

                with open(f'{translate_directory}/{filename}.json', 'w', encoding='utf-8') as file:
                    json.dump(result_list, file, ensure_ascii=False)
                    

                print(f'{filename} done \n\n {datetime.now().strftime("%H:%M:%S")}')


def translate_by_openai():
    directory = '../pure_documents'
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(f'{directory}/{filename}', 'r') as file:
                document = json.load(file)
            document_paragraph = '\n'.join(document)
            document_paragraph = '''
            孝殇皇帝
            延平元年春正月辛卯，以太尉张禹为太傅，司徒徐防为太尉，参录尚书事。太后以帝在襁褓，欲令重臣居禁内。乃诏禹舍宫中，五日一归府；每朝见，特赞，与三公绝席。
            封皇兄胜为平原王。'''
            prompt = f'''
            根据用三个反引号包裹的资治通鉴的原文```{document_paragraph}```\
            翻译成现代白话文，注意翻译后的白话文的回车换行与原文保持一致
            '''
            response = get_turbo_Azure(prompt=prompt)
            print(response)
        break


if __name__ == '__main__':
    # translate_by_openai()
    translate_by_glm()
