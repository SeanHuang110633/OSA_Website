// // frontend/mock/download.js
import Mock from "mockjs";

// --- 模擬資料庫原始資料 (Master Data) ---
const categories = [
  {
    id: 1,
    slug: "scholarship",
    names: { "zh-TW": "獎助學金", "en-US": "Scholarships" },
    is_active: true,
  },
  {
    id: 2,
    slug: "dormitory",
    names: { "zh-TW": "宿舍管理", "en-US": "Dorm Management" },
    is_active: true,
  },
  {
    id: 3,
    slug: "counseling",
    names: { "zh-TW": "諮商輔導", "en-US": "Counseling" },
    is_active: true,
  },
];

const downloads = [
  {
    id: 1,
    category_id: 1,
    type: "regulation",
    title: {
      "zh-TW": "國立中央大學學生獎學金辦法",
      "en-US": "NCU Scholarship Regulations",
    },
    department: { "zh-TW": "生活輔導組", "en-US": "Student Services Division" },
    published_at: "2024-12-01T08:00:00",
    attachments: [
      {
        id: 101,
        type: "file",
        file_format: "pdf",
        path: "/files/reg_01.pdf",
        title: "PDF",
        sort_order: 1,
      },
      {
        id: 102,
        type: "file",
        file_format: "odf",
        path: "/files/reg_01.odt",
        title: "ODF",
        sort_order: 2,
      },
    ],
  },
  {
    id: 2,
    category_id: 1,
    type: "form",
    title: {
      "zh-TW": "校內獎學金申請表",
      "en-US": "Scholarship Application Form",
    },
    department: { "zh-TW": "生活輔導組", "en-US": "Student Services Division" },
    published_at: "2025-01-15T10:00:00",
    attachments: [
      {
        id: 201,
        type: "file",
        file_format: "doc",
        path: "/files/form_02.doc",
        title: "DOC",
        sort_order: 1,
      },
    ],
  },
  // ... 可以自行增加更多資料
];

// --- 輔助工具：多語系轉換 (模擬 Service 層邏輯) ---
const getLang = (obj, locale) => obj[locale] || obj["zh-TW"] || "Unknown";

export default [
  // 1. 取得分類清單 API
  {
    url: "/api/downloads/categories",
    method: "get",
    response: ({ query }) => {
      const locale = query.locale || "zh-TW";
      return categories
        .filter((c) => c.is_active)
        .map((c) => ({
          id: c.id,
          slug: c.slug,
          name: getLang(c.names, locale),
        }));
    },
  },

  // 2. 取得下載分頁列表 API
  {
    url: "/api/downloads/",
    method: "get",
    response: ({ query }) => {
      const {
        locale = "zh-TW",
        page = 1,
        size = 10,
        type,
        category_id,
        query: searchText,
      } = query;

      // A. 模擬 Repository 篩選邏輯
      let result = downloads.filter((d) => {
        let match = true;
        if (type && d.type !== type) match = false;
        if (category_id && d.category_id !== parseInt(category_id))
          match = false;
        if (searchText) {
          const titleStr = JSON.stringify(d.title);
          if (!titleStr.includes(searchText)) match = false;
        }
        return match;
      });

      const total = result.length;

      // B. 模擬分頁 (Pagination)
      const start = (page - 1) * size;
      const end = start + parseInt(size);
      const pagedData = result.slice(start, end);

      // C. 模擬 Service 層：DTO 扁平化與多語系轉換
      const items = pagedData.map((d) => {
        const cat = categories.find((c) => c.id === d.category_id);
        return {
          id: d.id,
          type: d.type,
          category: {
            slug: cat.slug,
            name: getLang(cat.names, locale),
          },
          title: getLang(d.title, locale),
          department: d.department ? getLang(d.department, locale) : null,
          published_at: d.published_at,
          attachments: d.attachments, // 附件直接回傳
        };
      });

      return {
        total,
        page: parseInt(page),
        size: parseInt(size),
        items,
      };
    },
  },
];
