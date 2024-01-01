from transformers import AutoTokenizer, AutoModel



tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True).half().cuda()
model = model.eval()

document_paragraph = '''
孝殇皇帝
延平元年春正月辛卯，以太尉张禹为太傅，司徒徐防为太尉，参录尚书事。太后以帝在襁褓，欲令重臣居禁内。乃诏禹舍宫中，五日一归府；每朝见，特赞，与三公绝席。
封皇兄胜为平原王。
'''
prompt = f'''
根据用三个反引号包裹的资治通鉴的原文```{document_paragraph}```\
翻译成现代白话文，注意翻译后的白话文的回车换行与原文保持一致
'''
response, history = model.chat(tokenizer, prompt)

print(response)