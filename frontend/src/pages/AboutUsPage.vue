<template>
  <main class="container page">
    <div class="layout">
      <aside class="side">
        <div class="sideCard">
          <div class="sideTitle">
            <span class="bar" aria-hidden="true"></span>
            <span>各單位連結</span>
          </div>

          <nav class="sideNav">
            <button
              v-for="u in units"
              :key="u.key"
              class="sideBtn"
              :class="{ on: u.key === activeUnitKey }"
              type="button"
              @click="activeUnitKey = u.key"
            >
              <span class="txt">{{ u.name }}</span>
            </button>
          </nav>
        </div>
      </aside>

      <section class="content">
        <div class="crumb">
          <RouterLink class="crumbLink" to="/">首頁</RouterLink>
          <span class="sep">/</span>
          <span class="now">關於我們</span>
        </div>

        <h1 class="h1">
          <span class="barSm" aria-hidden="true"></span>
          關於學務處
        </h1>

        <p class="desc">（待補）請放學務處簡介文字。</p>

        <h2 class="h2">
          <span class="barSm" aria-hidden="true"></span>
          {{ activeUnit.name }}
          <span class="h2Count">（{{ activeUnit.count }} 人）</span>
        </h2>

        <div class="staffList">
          <div v-if="loading" class="state">載入中…</div>
          <div v-else-if="activeUnit.staff.length === 0" class="state">目前沒有資料。</div>
          
          <div v-for="member in activeUnit.staff" :key="member.id" class="staffCard">
            <div class="avatarWrap">
              <img 
                :src="member.img || '/assets/images/default-avatar.png'" 
                :alt="member.nameLine" 
                class="avatar" 
              />
            </div>
            <div class="info">
              <div class="nameLine">{{ member.nameLine }}</div>
              <div class="kv">
                <div class="row">
                  <div class="label">職稱</div>
                  <div class="val">{{ member.title || '無' }}</div>
                </div>
                <div class="row">
                  <div class="label">職掌</div>
                  <div class="val">
                    <div v-for="(line, index) in member.desc" :key="index">
                      {{ line }}
                    </div>
                  </div>
                </div>
                <div v-if="member.email" class="row">
                  <div class="label">信箱</div>
                  <a :href="`mailto:${member.email}`" class="val link">{{ member.email }}</a>
                </div>
                <div v-if="member.tel" class="row">
                  <div class="label">電話</div>
                  <div class="val">{{ member.tel }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script>
export default {
  data() {
    return {
      units: [],
      activeUnitKey: null,
      loading: true,
    };
  },
  computed: {
    activeUnit() {
      const u = this.units.find((u) => u.key === this.activeUnitKey);
      return u || { name: "", count: 0, staff: [] };
    },
  },
  async created() {
    await this.fetchMembers();
  },
  methods: {
    async fetchMembers() {
      this.loading = true;
      try {
        // 1. 確保連向後端 API，加上 /api 前綴
        const response = await fetch('http://localhost:8000/api/members/?locale=zh-TW');
        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();

        // 2. 資料映射：將後端 JSON 欄位轉為前端 Template 使用的變數名
        this.units = data.map(dept => {
          // 只篩選在職成員 (status 1 或 3)
          const activeMembers = dept.members.filter(m => m.status === 1 || m.status === 3);
          
          return {
            key: dept.id.toString(),
            name: dept.name,
            count: activeMembers.length,
            staff: activeMembers.map(m => ({
              id: m.id,
              nameLine: m.name,       // 對應 template 裡的 member.nameLine
              title: m.job_title,    // 對應 template 裡的 member.title
              desc: m.job_description, // 陣列格式
              email: m.email,
              tel: m.tel,
              // 補上後端圖片路徑
              img: m.photo_path ? `http://localhost:8000/uploads/${m.photo_path}` : null
            }))
          };
        });

        // 預設展開第一個部門
        if (this.units.length > 0) {
          this.activeUnitKey = this.units[0].key;
        }
      } catch (err) {
        console.error("無法取得成員資料:", err);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped>
.page {
  padding: 1.7rem 0 3.6rem;
}

.layout {
  display: grid;
  grid-template-columns: 22.5rem 1fr; 
  gap: 1.6rem;
  align-items: start;
}

.sideCard {
  background: #fff;
  border-radius: 1.35rem;
  box-shadow: 0 0.7rem 1.6rem rgba(16, 24, 40, 0.1);
  border: 1px solid rgba(16, 24, 40, 0.1);
  padding: 1.25rem 1.1rem 1.1rem;
}

.sideTitle {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  /* 修正：側欄標題統一為 20px */
  font-size: var(--text-xl); 
  font-weight: 700;
  color: #111827;
  margin-bottom: 1rem;
}

.bar {
  width: 0.5rem;
  height: 1.4rem;
  background: #f2cf57;
  border-radius: 0.2rem;
}

.sideNav {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.sideBtn {
  display: flex;
  align-items: center;
  width: 100%;
  border: 0;
  background: transparent;
  padding: 0.7rem 1rem;
  border-radius: 999px;
  cursor: pointer;
  /* 修正：側欄選單標準化 16px */
  font-size: var(--text-base); 
  font-weight: 400;
  color: #111827;
  text-align: left;
}

.sideBtn:hover {
  background: rgba(15, 23, 42, 0.04);
}

.sideBtn.on {
  background: #fff6dc;
  box-shadow: inset 0 0 0 1px rgba(242, 207, 87, 0.55);
}

.sideBtn .txt {
  letter-spacing: 0.02em;
  line-height: var(--leading-tight);
}

.content {
  background: #fff;
  border-radius: 1.35rem;
  box-shadow: 0 0.7rem 1.6rem rgba(16, 24, 40, 0.1);
  border: 1px solid rgba(16, 24, 40, 0.1);
  padding: 1.35rem 1.5rem 1.6rem;
}

.crumb {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  /* 修正：Meta 資訊標準 14px */
  font-size: var(--text-sm); 
  color: #6b7280;
  margin-bottom: 0.6rem;
}
.crumbLink {
  color: inherit;
  text-decoration: none;
}
.crumbLink:hover {
  text-decoration: underline;
}
.sep {
  opacity: 0.8;
}
.now {
  color: #6b7280;
}

.h1 {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  /* 修正：H1 頁面標題 30px */
  font-size: var(--text-3xl); 
  font-weight: 700;
  color: #111827;
  margin: 0.75rem 0 0.75rem;
  line-height: var(--leading-tight);
}

.h2 {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  /* 修正：H2 區塊標題 24px */
  font-size: var(--text-2xl); 
  font-weight: 700;
  color: #111827;
  margin: 1.3rem 0 0.9rem;
  line-height: var(--leading-tight);
}

.h2Count {
  /* 修正：輔助資訊標準 14px */
  font-size: var(--text-sm);
  color: #64748b;
  font-weight: 400;
}

.barSm {
  width: 0.6rem;
  height: 1.35rem;
  background: #f2cf57;
  border-radius: 0.2rem;
}

.desc {
  /* 修正：內文標準 16px 與行高 1.6 */
  font-size: var(--text-base); 
  line-height: var(--leading-normal);
  color: #334155;
}

.staffList {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.staffCard {
  display: grid;
  grid-template-columns: 16.25rem 1fr; 
  gap: 1.35rem;
  background: #f4f6ff;
  border: 1px solid rgba(16, 24, 40, 0.1);
  border-radius: 1.1rem;
  padding: 1.1rem;
}

.avatarWrap {
  background: #eef2ff;
  border-radius: 1rem;
  border: 1px solid rgba(16, 24, 40, 0.1);
  display: grid;
  place-items: center;
  padding: 0.75rem;
}

.avatar {
  width: 12.5rem;  
  height: 12.5rem;
  object-fit: cover;
  border-radius: 1rem;
  background: #fff;
}

.info {
  padding-top: 0.35rem;
}

.nameLine {
  /* 修正：卡片標題使用 20px */
  font-size: var(--text-xl); 
  font-weight: 700;
  color: #111827;
  margin-bottom: 0.75rem;
  line-height: var(--leading-tight);
}

.kv {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  margin-bottom: 0.9rem;
}

.row {
  display: grid;
  grid-template-columns: 6.2rem 1fr;
  gap: 0.65rem;
  align-items: start;
}

.label {
  /* 修正：欄位標籤 16px */
  font-size: var(--text-base);
  color: #0f172a;
}

.val {
  /* 修正：欄位內容 16px 與行高 1.6 */
  font-size: var(--text-base);
  color: #111827;
  line-height: var(--leading-normal);
}

.val.link {
  color: #1d4ed8;
}

.duty {
  /* 修正：內文標準化 16px */
  font-size: var(--text-base); 
  color: #111827;
  margin-top: 0.65rem;
  line-height: var(--leading-normal);
}

.extra {
  /* 修正：內文標準化 16px */
  font-size: var(--text-base); 
  margin-top: 0.5rem;
  color: #334155;
  line-height: var(--leading-normal);
}

/* RWD */
@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 700px) {
  .staffCard {
    grid-template-columns: 1fr;
  }
  .avatar {
    width: 10rem;
    height: 10rem;
  }
  .h1 { font-size: var(--text-2xl); } /* 手機版降級為 24px */
}

.state {
  padding: 16px;
  border-radius: 12px;
  background: rgba(0,0,0,.04);
  /* 修正：狀態提示 16px */
  font-size: var(--text-base);
  color: #334155;
}
.state--error {
  background: rgba(255,0,0,.06);
  color: #991b1b;
}
</style>