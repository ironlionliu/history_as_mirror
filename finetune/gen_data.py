import pandas as pd
from utils.utils import get_root_path
from utils.utils import num_tokens_from_string
import os
import re
import json

root_path = get_root_path()

def get_chapter_map():
    chapter_map = {}
    print(get_root_path())
    files = os.listdir(f'{root_path}/source_documents/documents_ziyexing_translated')
    pattern = r'\d+'
    for file in files:
        if not file.endswith('.json'):
            continue
        index = re.findall(pattern, file)[0]
        chapter_map[str(index)] = json.load(
            open(f'{root_path}/source_documents/documents_ziyexing_translated/'+file, 'r'))
    return chapter_map

def gen_translate():
    chapter_map = get_chapter_map()
    data = []
    analysis = []
    for i in range(0, 293):
        volume = chapter_map.get(str(i))
        for j in range(1, len(volume)):
            if len(volume[j].get('original')) > 2000:
                continue
            data.append({
                'instruction': '将给定的资治通鉴的原文翻译成现代汉语',
                'input': volume[j].get('original'),
                'output': volume[j].get('translation'),
            })
            analysis.append({
                'chapter': i,
                'index': j,
                'original': len(volume[j].get('original')),
                'translation': len(volume[j].get('translation'))
            })
            
    context = '\n\n'.join([f"{item.get('output')}\n{item.get('translation')}" for item in data])
    print(num_tokens_from_string(context))
    pd.DataFrame(analysis).to_csv(f'{root_path}/finetune/zztj_translation_analysis.csv', index=False, encoding='utf-8-sig')
    with open(f'{root_path}/finetune/zztj_translation.json', 'w') as file:
        file.write(json.dumps(data, ensure_ascii=False))

def gen_pretrain():
    chapter_map = get_chapter_map()
    data = []
    analysis = []
    for i in range(0, 293):
        volume = chapter_map.get(str(i))
        for j in range(1, len(volume)):
            if len(volume[j].get('original')) > 2000:
                for k in range(0, len(volume[j].get('original')), 2000):
                    data.append({
                        'text': volume[j].get('original')[k:k+2000],
                    })
                continue
            data.append({
                'text': volume[j].get('translation'),
            })
    with open(f'{root_path}/finetune/zztj_pretrain.json', 'w') as file:
        print(len(data))
        context = ''.join([item.get('text') for item in data])
        print(len(context))
        print(num_tokens_from_string(context))
        data = data[0:96]
        file.write(json.dumps(data, ensure_ascii=False))
            
if __name__ == '__main__':
    # gen_translate()
    gen_pretrain()