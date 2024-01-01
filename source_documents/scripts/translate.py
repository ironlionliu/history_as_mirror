# from transformers import AutoTokenizer, AutoModel
import os
import json
from utils import get_turbo_Azure



def translate_by_glm():
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).half().cuda()
    model = model.eval()
    directory = '../pure_documents'
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(f'{directory}/{filename}', 'r') as file:
                document = json.load(file)
            document_paragraph = '\n'.join(document)
            print(document_paragraph)
    prompt = f'''
    根据用三个反引号包裹的资治通鉴的原文```{document_paragraph}```\
    翻译成现代白话文，注意翻译后的白话文的回车换行与原文保持一致
    '''
    response, history = model.chat(tokenizer, prompt)

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
            response = get_turbo_Azure(prompt = prompt)
            print(response)
        break


if __name__ == '__main__':
    translate_by_openai()