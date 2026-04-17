from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import traceback

app = FastAPI()

# 允许所有跨域请求
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
API_KEY = "ark-63e744bb-7c89-4310-ba55-ce73
