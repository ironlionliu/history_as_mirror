

def handle_baiyang():
    with open('../baiyang_edition/baiyang_origin.txt', 'r', encoding='utf-8') as file:
        for line in file:
            # 对每一行进行处理
            print(line.strip().replace(''))  # 例如，这里使用strip()函数去除行尾的换行符

if __name__ == '__main__':
    handle_baiyang()