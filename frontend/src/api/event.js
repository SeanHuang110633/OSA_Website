import request from "./request";

// 取得消息列表
export function getEvents(params) {
  // params 包含: page, size, locale
  return request({
    url: "/events/",
    method: "get",
    params: params,
  });
}

// 取得單一消息詳情
export function getEventDetail(id, locale) {
  return request({
    url: `/events/${id}`,
    method: "get",
    params: { locale },
  });
}
