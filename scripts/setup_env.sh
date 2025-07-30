#!/bin/bash

echo "Setting up Pet Booking Platform environment..."

# 建立虛擬環境
python -m venv .venv

# 啟動虛擬環境 (windows)
venv\Scripts\activate

# 安裝 Python 套件
pip install -r requirements.txt

# 複製環境變數檔案
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# 進入前端目錄並安裝套件
cd frontend
npm install
cd ..

echo "Environment setup completed!"
echo "Please configure your .env file before running the application"
