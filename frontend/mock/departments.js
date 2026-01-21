import Mock from "mockjs";

export default [
  // 取得特定部門的成員名單 (對應 GET /api/departments/{id})
  {
    url: /^\/api\/departments\/\d+$/,
    method: "get",
    response: ({ query, url }) => {
      const locale = query.locale || "zh-TW";
      const deptId = url.split("/").pop();

      // 模擬「生活輔導組」資料
      return {
        id: parseInt(deptId),
        name: locale === "zh-TW" ? "生活輔導組" : "Student Services Division",
        description:
          locale === "zh-TW"
            ? "<p>負責學生生活相關事務...</p>"
            : "<p>In charge of student affairs...</p>",
        email: "living@ncu.edu.tw",
        website_url:
          locale === "zh-TW"
            ? "https://osa.ncu.edu.tw/living/zh"
            : "https://osa.ncu.edu.tw/living/en",
        image_path: "/images/depts/living.jpg",
        members: [
          {
            id: 101,
            name: locale === "zh-TW" ? "王小明" : "Wang, Xiao-Ming",
            job_title: locale === "zh-TW" ? "組長" : "Chief",
            email: "ming@ncu.edu.tw",
            tel: "03-4227151 #57201",
            photo_path: "/images/members/101.jpg",
            job_description:
              locale === "zh-TW"
                ? "1. 綜理生輔組業務<br>2. 學生獎懲審核"
                : "1. Oversee division affairs<br>2. Student discipline review",
          },
          {
            id: 102,
            name: locale === "zh-TW" ? "李華" : "Li, Hua",
            job_title: locale === "zh-TW" ? "行政專員" : "Specialist",
            email: "hua@ncu.edu.tw",
            tel: "03-4227151 #57205",
            photo_path: "/images/members/102.jpg",
            job_description:
              locale === "zh-TW"
                ? "1. 獎助學金業務<br>2. 學生宿舍管理"
                : "1. Scholarship processing<br>2. Dormitory management",
          },
        ],
      };
    },
  },
];
