import os
from fastapi import FastAPI, Form
from transformers import AutoTokenizer, AutoModel
import uvicorn
from pydantic import BaseModel

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
print('done')
model = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True).half().cuda()
print('done2')
model = model.eval()

prompt = 'hello'
model.chat(tokenizer, prompt)

# class ChatRequest(BaseModel):
#     prompt: str
#     history: list


# @app.post("/chat/")
# async def chat(request: ChatRequest):
#     # print(request.prompt)
#     # print(request.history)
#     response, history = model.chat(tokenizer, prompt, history=history)
#     return {
#         'response': response,
#         'history': history
#     }


# if __name__ == '__main__':
#     # uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
#     uvicorn.run("server:app", host="127.0.0.1", port=8000)
