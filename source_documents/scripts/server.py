import os
from fastapi import FastAPI, Form
from transformers import AutoTokenizer, AutoModel
import uvicorn
from pydantic import BaseModel
from kor import create_extraction_chain, Object, Text, Number

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True).half().cuda()
model = model.eval()


class ChatRequest(BaseModel):
    prompt: str
    history: list


@app.post("/chat/")
async def chat(request: ChatRequest):
    # print(request.prompt)
    # print(request.history)
    prompt = request.prompt
    history = request.history
    response, history = model.chat(tokenizer, prompt, history=history)
    return {
        'response': response,
        'history': history
    }


if __name__ == '__main__':
    # uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
    uvicorn.run(app, host="127.0.0.1", port=8000)
