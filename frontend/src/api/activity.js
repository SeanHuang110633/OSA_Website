// src/api/activity.js
import service from "./request";

/**
 * 取得活動列表 (全量)
 * @returns {Promise}
 */
export function getActivities() {
  return service.get("/activities/");
}
