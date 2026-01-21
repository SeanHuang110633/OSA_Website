// frontend/mock/download.js
import Mock from "mockjs";

export default [
  {
    url: "/api/downloads/",
    method: "get",
    response: ({ query }) => {
      const locale = query.locale || "zh-TW";
      const { type, category } = query;

      // 1. 準備原始完整資料 (對應你資料庫中的 download_categories 與 downloads)
      const allData = [
        {
          category_name: locale === "zh-TW" ? "獎助學金" : "Scholarships",
          category_slug: "scholarship",
          items: [
            {
              id: 1,
              type: "regulation",
              title:
                locale === "zh-TW"
                  ? "國立中央大學學生獎學金辦法"
                  : "NCU Student Scholarship Regulations",
              department:
                locale === "zh-TW" ? "生活輔導組" : "Student Services Division",
              published_at: "2024-12-01T08:00:00",
              attachments: [
                {
                  type: "file",
                  file_format: "pdf",
                  path: "/uploads/dl/reg_01.pdf",
                  title: "法規全文 (PDF)",
                },
                {
                  type: "file",
                  file_format: "odf",
                  path: "/uploads/dl/reg_01.odt",
                  title: "法規全文 (ODF)",
                },
              ],
            },
            {
              id: 2,
              type: "form",
              title:
                locale === "zh-TW"
                  ? "校內獎學金申請表"
                  : "Internal Scholarship Application Form",
              department:
                locale === "zh-TW" ? "生活輔導組" : "Student Services Division",
              published_at: "2025-01-15T10:00:00",
              attachments: [
                {
                  type: "file",
                  file_format: "doc",
                  path: "/uploads/dl/form_02.doc",
                  title: "申請表 (DOC)",
                },
                {
                  type: "link",
                  file_format: null,
                  path: "https://portal.ncu.edu.tw",
                  title: "線上申請系統",
                },
              ],
            },
          ],
        },
        {
          category_name:
            locale === "zh-TW" ? "宿舍管理" : "Dormitory Management",
          category_slug: "dormitory",
          items: [
            {
              id: 3,
              type: "regulation",
              title:
                locale === "zh-TW"
                  ? "學生宿舍管理辦法"
                  : "Student Dormitory Regulations",
              department:
                locale === "zh-TW" ? "生活輔導組" : "Student Services Division",
              published_at: "2024-08-20T09:00:00",
              attachments: [
                {
                  type: "file",
                  file_format: "pdf",
                  path: "/uploads/dl/dorm_reg.pdf",
                  title: "管理辦法 (PDF)",
                },
              ],
            },
            {
              id: 4,
              type: "form",
              title:
                locale === "zh-TW" ? "退宿申請表" : "Dormitory Withdrawal Form",
              department:
                locale === "zh-TW" ? "生活輔導組" : "Student Services Division",
              published_at: "2025-01-05T16:00:00",
              attachments: [
                {
                  type: "file",
                  file_format: "pdf",
                  path: "/uploads/dl/dorm_out.pdf",
                  title: "申請表下載",
                },
              ],
            },
          ],
        },
        {
          category_name:
            locale === "zh-TW" ? "諮商輔導" : "Counseling Services",
          category_slug: "counseling",
          items: [
            {
              id: 5,
              type: "form",
              title:
                locale === "zh-TW"
                  ? "個別諮商申請表"
                  : "Individual Counseling Application",
              department:
                locale === "zh-TW" ? "諮商輔導組" : "Counseling Division",
              published_at: "2024-09-01T08:30:00",
              attachments: [
                {
                  type: "file",
                  file_format: "pdf",
                  path: "/uploads/dl/counsel_form.pdf",
                  title: "申請表下載",
                },
              ],
            },
          ],
        },
      ];

      // 2. 篩選邏輯
      let filteredData = allData;

      // A. 先篩選「類型」 (Type: regulation/form)
      // 這會過濾每個類別中的 items，如果該類別篩選後沒有 items 則移除該類別
      if (type) {
        filteredData = filteredData
          .map((cat) => ({
            ...cat,
            items: cat.items.filter((item) => item.type === type),
          }))
          .filter((cat) => cat.items.length > 0);
      }

      // B. 再篩選「分類」 (Category Slug: scholarship/dormitory/...)
      if (category) {
        filteredData = filteredData.filter(
          (cat) => cat.category_slug === category,
        );
      }

      return filteredData;
    },
  },
];
