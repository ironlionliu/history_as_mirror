import pandas as pd
from utils.utils import get_root_path
from utils.utils import num_tokens_from_string
import os
import re
import json


def gen_translate():
    chapter_map = {}
    root_path = get_root_path()
    print(get_root_path())
    files = os.listdir(f'{root_path}/source_documents/documents_ziyexing_translated')
    pattern = r'\d+'
    for file in files:
        index = re.findall(pattern, file)[0]
        chapter_map[str(index)] = json.load(
            open(f'{root_path}/source_documents/documents_ziyexing_translated/'+file, 'r'))
    data = []
    count = 0
    for i in range(0, 293):
        volume = chapter_map.get(str(i))
        # print(i)
        # print(len(volume))
        for j in range(1, len(volume)):
            data.append({
                'instruction': '将给定的资治通鉴的原文翻译成现代汉语',
                'input': volume[j].get('original'),
                'output': volume[j].get('translation'),
            })
            count += len(volume[j].get('translation'))
    context = '\n\n'.join([f"{item.get('output')}\n{item.get('translation')}" for item in data])
    print(num_tokens_from_string(context))
    with open(f'{root_path}/LLaMA-Factory/data/zztj_translation.json', 'w') as file:
        file.write(json.dumps(data, ensure_ascii=False))
            
if __name__ == '__main__':
    gen_translate()