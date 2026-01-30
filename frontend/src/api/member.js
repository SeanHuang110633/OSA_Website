import request from "./request"; // 路徑依你們專案調整

export function fetchMembers(params = {}) {
  return request.get("/members", { params });
}