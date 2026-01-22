// frontend/mock/resource.js
import Mock from "mockjs";

export default [
  // 取得資源連結列表 (可支援按分類 slug 篩選)
  {
    url: "/api/resources/",
    method: "get",
    response: ({ query }) => {
      const locale = query.locale || "zh-TW";
      const { category: categorySlug } = query;

      const allResources = [
        {
          id: 1,
          slug: "student-service",
          category_name: locale === "zh-TW" ? "生活輔導" : "Student Service",
          resources: [
            {
              id: 101,
              title: locale === "zh-TW" ? "學雜費減免" : "Tuition Exemption",
              description:
                locale === "zh-TW"
                  ? "包含低收入戶與各類弱勢減免說明"
                  : "Info for tuition reduction",
              url:
                locale === "zh-TW"
                  ? "https://osa.ncu.edu.tw/living/exemption_zh"
                  : "https://osa.ncu.edu.tw/living/exemption_en",
            },
            {
              id: 102,
              title: locale === "zh-TW" ? "就學貸款" : "Student Loans",
              description:
                locale === "zh-TW"
                  ? "本學期就學貸款辦理時程與須知"
                  : "Semester loan schedule and info",
              url:
                locale === "zh-TW"
                  ? "https://portal.ncu.edu.tw/loan_zh"
                  : "https://portal.ncu.edu.tw/loan_en",
            },
          ],
        },
        {
          id: 2,
          slug: "campus-safety",
          category_name: locale === "zh-TW" ? "校園安全" : "Campus Safety",
          resources: [
            {
              id: 201,
              title: locale === "zh-TW" ? "緊急聯絡電話" : "Emergency Contact",
              description:
                locale === "zh-TW"
                  ? "校安中心 24 小時專線"
                  : "24H Security Hotline",
              url:
                locale === "zh-TW"
                  ? "https://osa.ncu.edu.tw/security/emergency_zh"
                  : "https://osa.ncu.edu.tw/security/emergency_en",
            },
          ],
        },
      ];
    },
  },
];
