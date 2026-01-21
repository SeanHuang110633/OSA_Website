// frontend/mock/event.js
// 模擬事件相關的 API 回應
import Mock from "mockjs";

export default [
  // 1. 取得活動列表 (對應 GET /api/events/)
  {
    url: "/api/events/",
    method: "get",
    response: ({ query }) => {
      const locale = query.locale || "zh-TW";

      return [
        {
          id: 1,
          slug: "speech-1",
          title:
            locale === "zh-TW"
              ? "AI 時代的職場競爭力講座"
              : "Career Competitiveness in the AI Era",
          category: {
            slug: "speech",
            name: locale === "zh-TW" ? "專題演講" : "Keynote Speech",
          },
          published_at: "2025-09-10T09:00:00",
          organizer_info: {
            name: "職涯發展中心",
            tel: "03-4227151 #57281",
            email: "career@ncu.edu.tw",
          },
        },
        {
          id: 2,
          slug: "activity-2",
          title:
            locale === "zh-TW"
              ? "聖誕音樂晚會 - 雪夜之歌"
              : "Christmas Concert - Song of Snowy Night",
          category: {
            slug: "activity",
            name: locale === "zh-TW" ? "學生活動" : "Student Activity",
          },
          published_at: "2025-11-01T10:00:00",
          organizer_info: {
            name: "學生會",
            tel: "03-4227151 #58000",
            email: "student_council@ncu.edu.tw",
          },
        },
      ];
    },
  },

  // 2. 取得單一活動詳情 (對應 GET /api/events/{id})
  {
    url: /^\/api\/events\/\d+$/,
    method: "get",
    response: ({ query, url }) => {
      const locale = query.locale || "zh-TW";
      const id = url.split("/").pop();

      // 模擬從後端 Service 拿到的 Fallback 邏輯
      return {
        id: parseInt(id),
        slug: `speech-${id}`,
        title:
          locale === "zh-TW"
            ? "AI 時代的職場競爭力講座"
            : "Career Competitiveness in the AI Era",
        category: {
          slug: "speech",
          name: locale === "zh-TW" ? "專題演講" : "Keynote Speech",
        },
        published_at: "2025-09-10T09:00:00",
        organizer_info: {
          name: "職涯發展中心",
          tel: "03-4227151 #57281",
          email: "career@ncu.edu.tw",
        },
        // 詳情頁專屬多語系欄位
        content:
          locale === "zh-TW"
            ? "<p>本講座邀請 Google 資深工程師分享如何在 AI 浪潮中保持競爭力...</p>"
            : "<p>This seminar invites senior engineers from Google to share insights on maintaining competitiveness in the AI wave...</p>",
        location: locale === "zh-TW" ? "秉文堂" : "Bingwen Hall",
        attachments: [
          {
            type: "file",
            title: "講座講義.pdf",
            path: "/uploads/2025/ai_slides.pdf",
          },
          {
            type: "link",
            title: "線上報名連結",
            path: "https://forms.gle/xyz123",
          },
        ],
      };
    },
  },
];
