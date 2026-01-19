# 使用官方輕量級 Python 鏡像
FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴，確保能編譯部分 Python 套件
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴清單並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 開發環境下，我們不 COPY 代碼，而是透過 docker-compose 的 volumes 掛載
# 啟動 FastAPI 並開啟熱重載 (--reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]