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
          關於{{ activeUnit.name || "學務處" }}
        </h1>

        <div
          class="desc"
          v-html="activeUnit.description || '尚無簡介內容。'"
        ></div>

        <h2 class="h2">
          <span class="barSm" aria-hidden="true"></span>
          {{ activeUnit.name }}成員
          <span class="h2Count">（{{ activeUnit.count }} 人）</span>
        </h2>

        <div class="staffList">
          <div v-if="loading" class="state">載入中…</div>
          <div v-else-if="activeUnit.staff.length === 0" class="state">
            目前沒有資料。
          </div>

          <div
            v-for="member in activeUnit.staff"
            :key="member.id"
            class="staffCard"
          >
            <div class="avatarWrap">
              <img :src="placeholder" :alt="member.nameLine" class="avatar" />
            </div>
            <div class="info">
              <div class="nameLine">{{ member.nameLine }}</div>
              <div class="kv">
                <div class="row">
                  <div class="label">職稱</div>
                  <div class="val">{{ member.title || "無" }}</div>
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
                  <a :href="`mailto:${member.email}`" class="val link">{{
                    member.email
                  }}</a>
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
import placeholder from "../assets/avatar_placeholder.png";
export default {
  data() {
    return {
      units: [],
      activeUnitKey: null,
      loading: true,
      placeholder,
    };
  },
  computed: {
    // 取得當前選中的部門資料
    activeUnit() {
      const u = this.units.find((u) => u.key === this.activeUnitKey);
      // [修改] 補上 description 的預設值，避免初始化時報錯
      return u || { name: "", description: "", count: 0, staff: [] };
    },
  },
  async created() {
    await this.fetchMembers();
  },
  methods: {
    async fetchMembers() {
      this.loading = true;
      try {
        // 呼叫後端 API
        const response = await fetch(
          "http://localhost:8000/api/members/?locale=zh-TW",
        );
        if (!response.ok) throw new Error("Network response was not ok");

        const data = await response.json();

        // 資料映射：將後端 JSON 轉為前端格式
        this.units = data.map((dept) => {
          // 篩選在職成員
          const activeMembers = dept.members.filter(
            (m) => m.status === 1 || m.status === 3,
          );

          return {
            key: dept.id.toString(),
            name: dept.name,
            // [新增] 接收後端回傳的部門 HTML 簡介
            description: dept.description,
            count: activeMembers.length,
            staff: activeMembers.map((m) => ({
              id: m.id,
              nameLine: m.name,
              title: m.job_title,
              desc: m.job_description, // 這是陣列
              email: m.email,
              tel: m.tel,
              // [備註] 若後端有圖片，組裝完整 URL，否則為 null (Template 層會處理預設圖)
              img: m.photo_path
                ? `http://localhost:8000/uploads/${m.photo_path}`
                : null,
            })),
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
  font-size: var(--text-2xl);
  font-weight: 700;
  color: #111827;
  margin: 1.3rem 0 0.9rem;
  line-height: var(--leading-tight);
}

.h2Count {
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
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: #334155;
  /* 確保 HTML 內容樣式正常 */
  white-space: pre-wrap;
}

/* 讓 v-html 內部的 p 標籤保持間距 */
.desc :deep(p) {
  margin-bottom: 0.8rem;
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
  font-size: var(--text-base);
  color: #0f172a;
}

.val {
  font-size: var(--text-base);
  color: #111827;
  line-height: var(--leading-normal);
}

.val.link {
  color: #1d4ed8;
}

.duty {
  font-size: var(--text-base);
  color: #111827;
  margin-top: 0.65rem;
  line-height: var(--leading-normal);
}

.extra {
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
  .h1 {
    font-size: var(--text-2xl);
  }
}

.state {
  padding: 16px;
  border-radius: 12px;
  background: rgba(0, 0, 0, 0.04);
  font-size: var(--text-base);
  color: #334155;
}
.state--error {
  background: rgba(255, 0, 0, 0.06);
  color: #991b1b;
}
</style>
