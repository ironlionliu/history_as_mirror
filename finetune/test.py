import re



# 测试字符串
test_string = '这是一个测试〔〖胡三省注〗这是被包裹的段落〕这是另一个测试〔〖胡三省注〗〔hard〕这是另一个被包裹的段落〕'

# 调用函数去除嵌套的段落并存储被抠掉的部分
result, removed_parts = remove_and_store_nested_paragraphs_with_prefix(test_string)

# 输出结果
print("去除嵌套的段落后的文本:", result)
print("被抠掉的部分:", removed_parts)