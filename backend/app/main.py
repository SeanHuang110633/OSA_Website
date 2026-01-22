import uvicorn  # ASGI 伺服器，負責執行 FastAPI 應用程式
import os       # 處理系統操作（路徑、環境變數）
from contextlib import asynccontextmanager  # 用於管理 App 的生命週期（啟動與關閉）
from fastapi import FastAPI  # Web 框架核心
from fastapi.middleware.cors import CORSMiddleware  # 處理跨來源資源共用的安全性設定
from fastapi.staticfiles import StaticFiles  # 讓 FastAPI 可以讀取並顯示靜態檔案（如圖片）
from app.core.database import engine # 直接引入 engine，確保資料庫連線在 App 啟動時建立
from app.routers import event_router  # 8. 引入「活動消息模組」的 API Router


# =========================================================
# 生命週期管理 (Lifespan Events)
# =========================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 啟動時執行顯式檢查
    try:
        # 使用 SQLAlchemy 的 connect 進行簡單連線測試 (Ping)
        with engine.connect() as connection:
            print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    yield
    # 關閉時執行 (如果需要釋放資源寫在這裡)
    print("🛑 System shutting down...")

# =========================================================
# 初始化 FastAPI App
# =========================================================
app = FastAPI(
    title="Event Management System API", # Swagger UI 上顯示的名稱
    version="1.0.0",
    description="Backend API for managing events, categories, and translations.",
    lifespan=lifespan  # 將定義好的生命週期管理員掛載上去
)

# =========================================================
# CORS 設定 
# =========================================================
# 從 .env 讀取允許連線的清單，若沒設定則提供預設開發路徑
origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in origins_str.split(",")]

# 從 .env 讀取允許連線的清單，若沒設定則提供預設開發路徑
origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in origins_str.split(",")]

# todo : 部署時記得修改這裡的設定，避免安全性問題，例如不要使用 ["*"],至於要怎麼設定等到要上線時再說
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 只允許名單內的來源存取，比之前的 ["*"] 更安全
    allow_credentials=True,
    allow_methods=["*"],    # 允許所有 HTTP 動詞 (GET, POST, etc.)
    allow_headers=["*"],    # 允許所有標頭資訊
)

# =========================================================
# 掛載靜態檔案目錄
# =========================================================
os.makedirs("uploads", exist_ok=True) # 確保上傳目錄存在，避免報錯
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") # 讓 /uploads/abc.jpg 可以被外部訪問

# =========================================================
# 註冊 Router (路由)
# =========================================================
# 加上 /api 前綴，方便區分靜態檔案與 API 介面
# 這樣網址會變成: http://localhost:8000/api/events/...
app.include_router(event_router.router, prefix="/api")

# =========================================================
# 程式進入點
# =========================================================
if __name__ == "__main__":
    # reload=True 讓你在修改程式碼後，伺服器會自動重啟
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)