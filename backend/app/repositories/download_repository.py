from typing import List, Optional, Tuple
from sqlmodel import Session, select, col, func
from sqlalchemy.orm import selectinload
from sqlalchemy import or_

from app.models.download_model import Download, DownloadCategory, DownloadStatus

class DownloadRepository:
    def __init__(self, session: Session):
        """
        注入資料庫會話 (Dependency Injection)
        """
        self.session = session

    def get_list_with_total(
        self, 
        skip: int = 0, # 分頁用，跳過前 N 筆
        limit: int = 10, # 分頁用，限制每頁回傳筆數
        dl_type: Optional[str] = None, # law, table
        category_id: Optional[int] = None,
        search_query: Optional[str] = None
    ) -> Tuple[List[Download], int]:
        """
        取得下載列表與總筆數 (支援分頁、過濾、模糊搜尋)
        """
        # 1. 建立基礎查詢
        # selectinload: 預先載入關聯，解決 N+1 問題
        statement = (
            select(Download)
            .where(Download.deleted_at == None) # 排除軟刪除項目
            .join(Download.category).where(DownloadCategory.is_active == True) # 只取啟用的分類(如果有分類被停用，則該分類下的下載項目也不顯示)
            .options(
                selectinload(Download.category), # 為了回傳資料時有分類資訊
                selectinload(Download.attachments) # 為了回傳資料時有附件
            )
        )

        # 2. 條件過濾(type, category)，與上面分開寫可以增加可讀性、方便後續擴充，且避免沒有傳入參數時搜尋出錯誤資料
        if dl_type:
            statement = statement.where(Download.type == dl_type)
        
        if category_id:
            statement = statement.where(Download.category_id == category_id)

        # 3. 模糊搜尋 (針對 JSON 欄位中的標題內容)
        if search_query:
            # 使用 MySQL 的 JSON_SEARCH 或簡單將 JSON 轉為字串進行 LIKE 比對
            # 這裡採用轉字串比對，可同時搜尋中英文標題
            statement = statement.where(
                Download.title.cast(func.String).like(f"%{search_query}%")
            )

        # 4. 計算總筆數 (Pagination 需要 total count)
        # 注意：計算總數必須在套用 offset/limit 之前
        count_statement = select(func.count()).select_from(statement.subquery())
        total = self.session.exec(count_statement).one()

        # 5. 排序與分頁
        statement = (
            statement.order_by(col(Download.published_at).desc())
            .offset(skip)
            .limit(limit)
        )

        results = self.session.exec(statement).all()
        
        return results, total

    def get_by_id(self, download_id: int) -> Optional[Download]:
        """
        取得單一下載項目詳情
        """
        statement = (
            select(Download)
            .where(Download.id == download_id)
            .where(Download.deleted_at == None)
            .options(
                selectinload(Download.category),
                selectinload(Download.attachments)
            )
        )
        return self.session.exec(statement).first()