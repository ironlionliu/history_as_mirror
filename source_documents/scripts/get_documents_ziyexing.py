from bs4 import BeautifulSoup
import requests
import time
import os
import json
import re


def get_urls_from_menu(menu_path='../documents_ziyexing/资治通鉴-目录.html'):
    htmlHandler = open('{}'.format(menu_path), 'r', encoding='gbk')
    bs = BeautifulSoup(htmlHandler, 'html.parser')
    url_list = bs.find('table', {'id': 'table6'}).find_all('td')
    url_map = {}
    for item in url_list:
        try:
            title = item.find('a').text.strip().replace(
                ' ', '').replace('\n', '').replace('\t', '')
            if '卷' in title:
                url_map[title] = item.find('a').get('href')
        except Exception as e:
            pass
    # 补充缺失的译文
    # url_map = {
    #     '资治通鉴》卷三十一译文 [后半部]': 'http://www.ziyexing.com/files-4/yywj-161.htm'
    # }
    # 补卷28译文
    url_map = {
        '资治通鉴卷二十八译文': 'http://www.ziyexing.com/files-4/yywj-157.htm'
    }
    return url_map


def get_documents_by_url_list():
    url_map = get_urls_from_menu()
    order = 0
    for name, url in url_map.items():
        response = requests.get(url)
        response.encoding = 'gbk'
        doc = response.text
        print(name)
        try:
            with open(f'../documents_ziyexing/({order}){name}.html', 'w') as file:
                file.write(doc)
        except Exception as e:
            print(doc)
        order += 1
        time.sleep(2)


def parse_document(directory='', filename=''):
    htmlHandler = open(os.path.join(directory, filename), 'r')
    bs = BeautifulSoup(htmlHandler, 'html.parser')
    paragraphs = bs.find_all('p', {'align': 'left'})[-1].text
    split_documents = split_document(paragraphs, filename)
    with open(os.path.join(directory + '_translated', filename.replace('.html', '.json')), 'w') as file:
        file.write(json.dumps(split_documents, ensure_ascii=False))


def split_document(content='', filename=''):
    paragraphs = re.split(r'【原文】|【译文】|《译文》', content)
    title = paragraphs[0]
    result = []
    result.append({
        'title': title
    })
    try:
        for i in range(1, len(paragraphs)):
            if i % 2 == 1:
                result.append({
                    'original': paragraphs[i],
                    'translation': paragraphs[i+1]
                })
    except Exception as e:
        print(filename)
        print(e)
    return result
    


def visit_documents(directory='../documents_ziyexing'):
    for filename in os.listdir(directory):
        if filename.startswith('('):
            document = parse_document(directory=directory, filename=filename)


if __name__ == '__main__':
    # get_urls_from_menu()
    # get_documents_by_url_list()
    visit_documents()
    # parse_document(directory = '../documents_ziyexing', filename = '(203)卷二〇四唐纪二十.html')
