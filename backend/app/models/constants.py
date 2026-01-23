# app/models/constants.py
# 定義常數類別，用於事件狀態碼與附件類型(這個檔案暫時不用了，但先留著以備未來擴充)
class EventStatus:
    DRAFT = 0
    PUBLISHED = 1
    ARCHIVED = 2

class AttachmentType:
    IMAGE = "image"
    FILE = "file"
    LINK = "link"