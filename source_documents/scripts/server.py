import os
from fastapi import FastAPI, Form
from transformers import AutoTokenizer, AutoModel
import uvicorn
app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm3-6b-32k", trust_remote_code=True).half().cuda()
model = model.eval()


@app.post("/chat/")
async def chat(prompt: str = Form(...), history: list = Form(...)):
    print(response, history)
    response, history = model.chat(tokenizer, prompt, history=history)
    return {
        'response': response,
        'history': history
    }


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
