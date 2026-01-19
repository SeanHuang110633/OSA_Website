import uvicorn
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 1. 引入您的資料庫核心設定
# 確保 app/core/database.py 中有定義 create_db_and_tables
from app.core.database import create_db_and_tables

# 2. 引入 Router
from app.routers import event_router

# =========================================================
# 生命週期管理 (Lifespan Events)
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時執行：自動建立資料庫表格 (對應 SQLModel table=True 的模型)
    print("🚀 System starting up... Creating database tables...")
    # create_db_and_tables()
    yield
    # 關閉時執行 (如果需要釋放資源寫在這裡)
    print("🛑 System shutting down...")

# =========================================================
# 初始化 FastAPI App
# =========================================================
app = FastAPI(
    title="Event Management System API",
    version="1.0.0",
    description="Backend API for managing events, categories, and translations.",
    lifespan=lifespan
)

# =========================================================
# CORS 設定 
# =========================================================
# 從環境變數讀取 ALLOWED_ORIGINS，並轉成 List
# 預設包含 localhost 與 127.0.0.1 確保開發順利
origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ❌ 這裡不再使用 ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# 掛載靜態檔案目錄
# =========================================================
# 確保上傳目錄存在，避免報錯
os.makedirs("uploads", exist_ok=True)

# 讓 /uploads/abc.jpg 可以被外部訪問
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# =========================================================
# 註冊 Router (路由)
# =========================================================
# 建議加上 /api 前綴，方便區分靜態檔案與 API 介面
# 這樣網址會變成: http://localhost:8000/api/events/...
app.include_router(event_router.router, prefix="/api")

# =========================================================
# 程式進入點
# =========================================================
if __name__ == "__main__":
    # reload=True 讓你在修改程式碼後，伺服器會自動重啟
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)