#!/bin/bash
cd "$(dirname "$0")"

echo "🚀 正在启动静静和豪哥的AI助手..."
echo "后端地址：http://127.0.0.1:8000"
echo "请保持此窗口打开，关闭将停止服务"

# 用 pip3 和 python3 安装依赖并启动
pip3 install -r requirements.txt
python3 app.py