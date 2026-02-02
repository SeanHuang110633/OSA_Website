import request from './request'

// 取得資源列表
// params 可能包含: locale, page, size, type, category_id, query
export function getResources(params) {
  return request({
    url: '/resources/',
    method: 'get',
    params,
  })
}

// 取得單一資源詳情
export function getResourceDetail(id, locale = 'zh-TW') {
  return request({
    url: `/resources/${id}`,
    method: 'get',
    params: { locale },
  })
}

// 若未來需要取得分類，可在此加入對應方法
export default {
  getResources,
  getResourceDetail,
}
