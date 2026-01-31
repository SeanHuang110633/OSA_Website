from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models.member_model import Department


class MemberRepository:
    """
    MemberRepository
    ----------------
    Repository 層負責「資料存取」
    - 不處理商業邏輯
    - 不做過度資料過濾
    - 專心負責把資料「完整、安全」地從 DB 撈出來
    """

    def __init__(self, session: Session):
        """
        初始化 Repository
        session 由 FastAPI dependency injection 傳入
        """
        self.session = session

    def get_all_active_members_by_dept(self):
        """
        取得「所有啟用中的部門」以及其底下的所有成員

        設計重點說明：
        1. 這裡「只」過濾 Department.is_active
           - 停用部門不應出現在前端
        2. 不在 Repository 層過濾 Member.status
           - 避免因為資料狀態不一致導致整個部門消失
           - 若 DB 中成員 status 資料不乾淨，會造成 API 回傳空陣列
        3. 成員的顯示與過濾（例如 status == 1）
           - 應交由 Service 層處理
           - 較安全、也較符合分層設計（Separation of Concerns）

        回傳資料結構：
        [
          Department(
            id=1,
            name={...},
            members=[Member(...), Member(...)]
          ),
          ...
        ]
        """

        # 建立查詢語句
        statement = (
            # 以 Department 為主表查詢
            select(Department)

            # 只撈啟用中的部門
            .where(Department.is_active == True)

            # 依部門排序欄位排序，確保前端顯示順序穩定
            .order_by(Department.sort_order.asc())

            # 使用 selectinload 預先載入 members
            # 避免 N+1 Query 問題
            # 查詢流程：
            # 1. 先查所有 Department
            # 2. 再用 IN (...) 一次查完所有 Member
            .options(selectinload(Department.members))
        )

        # 執行查詢並回傳結果（List[Department]）
        return self.session.exec(statement).all()