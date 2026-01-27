import request from "./request"; // 使用目前的全局攔截器設定(request.js)

export function getDownloads(params) {
  return request({
    url: "/downloads/",
    method: "get",
    params, // 包含 locale, page, size, type, category_id, query
  });
}

export function getCategories(locale = "zh-TW") {
  return request({
    url: "/downloads/categories",
    method: "get",
    params: { locale },
  });
}
