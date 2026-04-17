from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx

# ✅ 这一行必须存在，且是顶级定义
app = FastAPI()

# 允许跨域
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

# 首页路由
@app.get("/")
async def root():
    return FileResponse("chat.html")

# 聊天接口
@app.post("/chat")
async def chat(req: ChatRequest):
    msg = req.msg.strip()

    # 固定回复，先测试接口是否通
    if "你好" in msg:
        return {"reply": "你好呀！我是静静和豪哥的专属小助手~"}
    
    # 豆包API调用
    API_KEY = "ark-63e744bb-7c89-4310-ba55-ce73394833c1-5fdc4"
    MODEL = "ep-20260417123409-bfnq9"
    BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "user", "content": msg}]
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
            data = resp.json()
            return {"reply": data["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"reply": f"💔 API调用失败：{str(e)}"}
