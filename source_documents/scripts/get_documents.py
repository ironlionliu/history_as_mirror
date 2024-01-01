from bs4 import BeautifulSoup
import requests
import time
import os
import json
import re

def get_urls_from_menu(menu_path = '../documents/资治通鉴-目录.html'):
    htmlHandler = open('{}'.format(menu_path), 'r', encoding='utf-8')
    bs = BeautifulSoup(htmlHandler, 'html.parser')
    url_list = bs.find('div', {'class': 'ctext'}).find_all('a')
    url_map = {}
    for item in url_list:
        url_map[item.text] = item.get('href')
    
    return url_map

def get_documents_by_url_list():
    url_map = get_urls_from_menu()
    order = 0
    for name, url in url_map.items():
        print(url)
        doc = requests.get(url).text
        print(doc)
        with open(f'../documents/{name}({order}).html', 'w', encoding='utf-8') as file:
            file.write(doc)
        order += 1
        time.sleep(2)

def parse_document(directory='', filename=''):
    htmlHandler = open(os.path.join(directory, filename), 'r', encoding='utf-8')
    bs = BeautifulSoup(htmlHandler, 'html.parser')
    paragraphs = bs.find('table', {'style': 'width: 100%;'}).find_all('tr', {'class': 'result'})
    
    comments = bs.find_all('span', {'class': 'inlinecomment'})
    for comment in comments:
        comment.decompose()
    number_markers = bs.find_all('td', {'class': 'ctext', 'style': 'width: 60px;'})
    for number_marker in number_markers:
        number_marker.decompose()

    paragraph_list = []
    for paragraph in paragraphs:
        if len(paragraph.text) > 0:
            paragraph_list.append(paragraph.text)
    # 将数组写入JSON文件
    match = re.match(r'(.+)\((\d+)\)\.html', filename)
    arabic_number = int(match.group(2)) + 1
    prefix = match.group(1)
    filename = f'{arabic_number}-{prefix}'
    # new_filename = f"卷{arabic_number}-{chinese_number}.html"
    with open(f'../pure_documents/{filename}.json', 'w', encoding='utf-8') as file:
        json.dump(paragraph_list, file, ensure_ascii=False)
    return paragraph_list


def visit_documents(directory = '../documents'):
    for filename in os.listdir(directory):
        if filename.startswith('卷'):
            document = parse_document(directory=directory, filename=filename)



if __name__ == '__main__':
    # get_documents_by_url_list()
    visit_documents()
    # parse_document(directory = '../documents', filename = '卷一·周纪一(0).html')