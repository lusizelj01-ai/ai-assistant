from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import httpx
import re

app = FastAPI()

# 🔥 关键：Vercel 必须用这个方式定义根路由，确保返回 chat.html
@app.get("/")
async def read_root():
    return FileResponse("chat.html")

# 挂载静态文件，确保前端能加载
app.mount("/", StaticFiles(directory="."), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    msg: str
    history: list = []

# ====================== 你的 API 信息 ======================
API_KEY = "ark-63e744bb-7c89-4310-ba55-ce73394833c1-5fdc4"
MODEL = "ep-20260417123409-bfnq9"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
# ===========================================================

# 数学计算
def calculate(expr):
    try:
        expr = re.sub(r'[^0-9+\-*/().]', '', expr)
        return f"🧮 结果：{expr} = {eval(expr)}"
    except:
        return "❌ 算不出来哦"

# 模拟天气
def weather(text):
    return "🌤️ 今天天气晴朗，适合出门～"

# 调用豆包 API
async def chat_with_doubao(msg, history):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "你是一个温柔、可爱、简洁的AI小助手，会记住对话内容。"}
    ]

    for h in history[-6:]:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["ai"]})

    messages.append({"role": "user", "content": msg})

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 500
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"💔 API调用失败：{str(e)}"

@app.post("/chat")
async def chat(req: ChatRequest):
    msg = req.msg.strip()
    history = req.history

    if any(k in msg for k in "+-*/") or "计算" in msg:
        return {"reply": calculate(msg)}
    elif "天气" in msg:
        return {"reply": weather(msg)}
    else:
        reply = await chat_with_doubao(msg, history)
        return {"reply": reply}

# 🔥 部署专用：Vercel 不需要本地 uvicorn 启动命令，这里可以直接注释掉
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
