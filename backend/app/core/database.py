# backend/app/core/database.py
import os, ssl
from typing import Generator
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv


# 1. 讀取專案根目錄下的 .env 檔案，並將其中的鍵值對注入到系統的環境變數中
load_dotenv()

# 2. 取得連線字串(從環境變數讀取)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2.1 確保 DATABASE_URL 存在
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file or environment variables")

   
# 3. 建立 Engine
# Engine 是 SQLAlchemy/SQLModel 與資料庫對話的「工廠」，它持有方言（Dialect，這裡是 MySQL）的處理邏輯與連線池管理
# pool_recycle=3600: 每小時自動回收連線，防止 MySQL 閒置過久斷線
# pool_pre_ping=True: 在應用程式每次使用連線前，會先發送一個類似 SELECT 1 的微小指令給資料庫，確認連線是否還活著(我們的環境應該不需要但可以先留著)
# echo=True: 開發時顯示 SQL，上線部署時可改為 False
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    pool_recycle=3600,
    pool_pre_ping=True,
)

# 4. 建立資料庫和表格
def create_db_and_tables():
    # =========================================================
    # [重要] 必須在這裡 import 所有的 Model
    # =========================================================
    from app.models.event_model import Event, EventCategory, EventTranslation, EventAttachment
    
    # 開始建立表格
    SQLModel.metadata.create_all(engine)

# 5. 提供資料庫會話 (Dependency)
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session