import request from "./request"; 

export function fetchMembers(params = {}) {
  return request.get("/members", { params });
}