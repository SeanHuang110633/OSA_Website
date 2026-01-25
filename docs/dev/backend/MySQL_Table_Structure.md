# 資料庫表結構

目前這些是前台會用到的表(table)，還有一個activity表(就是主頁的活動卡片要呈現的東西)尚再處理，後續會新增上來，可以繼續先用假資料開發前端。

```sql
CREATE TABLE `event_categories` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `slug` VARCHAR(50) NOT NULL COMMENT '網址或CSS用的代碼，如 speech, activity',
  `names` JSON NOT NULL COMMENT '多語系名稱，存 {"zh-TW": "演講", "en-US": "Speech"}',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '1:啟用, 0:停用 (分類軟刪除用)',
  `sort_order` INT NOT NULL DEFAULT '0' COMMENT '顯示順序',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- 2. 主表 events (實體表)
-- -----------------------------------------------------
CREATE TABLE `events` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_id` INT UNSIGNED NOT NULL, -- 對應 event_categories.id
  `status` TINYINT NOT NULL DEFAULT '0' COMMENT '0:草稿(Draft), 1:發布(Published), 2:下架/封存(Archived)',

  -- 核心時間與發布控制
  `starts_at` DATETIME DEFAULT NULL COMMENT '活動開始時間',
  `ends_at` DATETIME DEFAULT NULL COMMENT '活動結束時間',
  `published_at` DATETIME DEFAULT NULL COMMENT '文章顯示日期 (排序與預約發布用)',

  -- 共用資訊
  `organizer_info` JSON DEFAULT NULL COMMENT '主辦單位資訊，存 JSON {"name":"課外組", "tel":"分機123"}',
  `is_target` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '特殊標記 (如:是否為目標活動)',
  `is_featured` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否置頂 (取代舊系統 status=3 的功能)',

  -- 系統欄位
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL DEFAULT NULL, -- 邏輯刪除欄位

  PRIMARY KEY (`id`),
  KEY `idx_cat_status` (`category_id`, `status`), -- 列表頁過濾用
  KEY `idx_publish` (`published_at`), -- 列表頁排序用 (最新消息)

  -- 外鍵約束：確保分類存在
  CONSTRAINT `fk_event_category` FOREIGN KEY (`category_id`) REFERENCES `event_categories` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- 3. 翻譯表 event_translations (活動內容多語系)
-- -----------------------------------------------------
CREATE TABLE `event_translations` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `event_id` BIGINT UNSIGNED NOT NULL,
  `locale` VARCHAR(10) NOT NULL DEFAULT 'zh-TW', -- 存放 zh-TW, en-US

  -- 內容欄位
  `title` VARCHAR(255) NOT NULL,
  `content` MEDIUMTEXT,
  `location` VARCHAR(255) DEFAULT '',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_event_locale` (`event_id`, `locale`), -- 防止同一個活動有重複的語言版本
  CONSTRAINT `fk_event_trans` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- 4. 事件附件表
-- -----------------------------------------------------
CREATE TABLE `event_attachments` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `event_id` BIGINT UNSIGNED NOT NULL,
  `type` ENUM('image', 'file', 'link') NOT NULL,
  `path` VARCHAR(500) NOT NULL COMMENT '檔案路徑 或 URL',
  `title` VARCHAR(255) DEFAULT '' COMMENT '顯示名稱',
  `sort_order` INT NOT NULL DEFAULT '0',

  PRIMARY KEY (`id`),
  CONSTRAINT `fk_event_attach` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# download
-- -----------------------------------------------------
-- 1. 下載分類表 (download_categories)
-- 內容範例：諮商輔導 (counseling), 獎學金 (scholarship)
-- -----------------------------------------------------
CREATE TABLE `download_categories` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `slug` VARCHAR(50) NOT NULL COMMENT '網址代碼 (如: scholarship)',
  `names` JSON NOT NULL COMMENT '{"zh-TW": "獎學金", "en-US": "Scholarships"}',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '1:啟用, 0:停用',
  `sort_order` INT NOT NULL DEFAULT '0',

  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_dl_slug` (`slug`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- 2. 下載主表 (downloads)
-- -----------------------------------------------------
CREATE TABLE `downloads` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_id` INT UNSIGNED NOT NULL,

  -- 下載的類型 (法規 vs 表格)
  -- 建議維持英文 Key，前端再對應中文，避免編碼問題
  `type` ENUM('regulation', 'form', 'other') NOT NULL DEFAULT 'other' COMMENT 'law:法規, table:表格',

  -- 標題 (JSON 多語系)
  `title` JSON NOT NULL COMMENT '{"zh-TW": "學生宿舍管理辦法", "en-US": "Dormitory Rules"}',

  -- 負責單位 (原 publisher_name)
  `department` JSON DEFAULT NULL COMMENT '發布單位名稱，如 {"zh-TW": "生活輔導組"}',

  -- 狀態與時間
  `status` TINYINT NOT NULL DEFAULT '1' COMMENT '0:Draft, 1:Published, 2:Archived',
  `published_at` DATETIME DEFAULT NULL,

  -- 系統欄位
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL DEFAULT NULL, -- 邏輯刪除

  PRIMARY KEY (`id`),
  KEY `idx_dl_cat_type` (`category_id`, `type`),
  CONSTRAINT `fk_dl_category` FOREIGN KEY (`category_id`) REFERENCES `download_categories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- 3. 下載附件表 (download_attachments)
-- 統一管理 PDF, Word, ODF 以及外部連結
-- -----------------------------------------------------
CREATE TABLE `download_attachments` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `download_id` BIGINT UNSIGNED NOT NULL,

  -- 區分是「上傳的檔案」還是「外部網址」
  -- 因為舊資料有同時包含 "PDF檔" 與 "外部連結" 的情況，建議保留此區分
  `type` ENUM('file', 'link') NOT NULL DEFAULT 'file',

  -- 檔案格式 (重要：解決沒有副檔名的 URL 無法判斷格式的問題，並方便統計 ODF)
  `file_format` VARCHAR(10) DEFAULT NULL COMMENT 'pdf, doc, odf, xls...',

  -- 路徑或網址
  `path` VARCHAR(500) NOT NULL COMMENT '檔案相對路徑 或 外部 URL',

  -- 用來顯示 "法規全文(PDF)" 而不是醜醜的檔名 "20250902.pdf"
  `title` VARCHAR(255) DEFAULT NULL,

  `sort_order` INT NOT NULL DEFAULT '0',

  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '邏輯刪除'

  PRIMARY KEY (`id`),
  KEY `idx_dl_format` (`download_id`, `file_format`),
  CONSTRAINT `fk_dl_attach` FOREIGN KEY (`download_id`) REFERENCES `downloads` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

# departments
-- -----------------------------------------------------
-- 1. 部門/單位表 (departments)
-- 原本的 osa2014_group
-- -----------------------------------------------------
CREATE TABLE `departments` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,

  -- 1. 名稱與描述 (JSON 多語系)
  `name` JSON NOT NULL COMMENT '部門名稱 {"zh-TW": "生活輔導組", "en-US": "Student Services Division"}',
  `description` JSON DEFAULT NULL COMMENT '部門簡介 (含HTML) {"zh-TW": "<p>...</p>", "en-US": "<p>...</p>"}',

  -- 2. 聯絡資訊
  `email` VARCHAR(255) DEFAULT NULL COMMENT '部門共用信箱',

  -- [修改] 網站連結改為 JSON，支援中英文不同網址
  `website_url` JSON DEFAULT NULL COMMENT '部門網站 {"zh-TW": "https://.../zh", "en-US": "https://.../en"}',

  `image_path` VARCHAR(500) DEFAULT NULL COMMENT '部門代表圖 (原 group_pic)',

  -- 3. 排序與狀態
  `sort_order` INT NOT NULL DEFAULT '0',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '1:啟用, 0:隱藏',

  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '邏輯刪除'

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- -----------------------------------------------------
-- 2. 成員表 (department_members)
-- 原本的 osa2014_group_member
-- -----------------------------------------------------
CREATE TABLE `department_members` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `department_id` INT UNSIGNED NOT NULL COMMENT '所屬部門 ID',

  -- 1. 基本資料
  `name` JSON NOT NULL COMMENT '姓名 {"zh-TW": "王小明", "en-US": "Wang, Xiao-Ming"}',
  `email` VARCHAR(255) DEFAULT NULL,
  `tel` VARCHAR(50) DEFAULT NULL COMMENT '分機或電話',
  `photo_path` VARCHAR(500) DEFAULT NULL COMMENT '大頭照路徑',

  -- 2. 職務資訊 (核心多語系區塊)
  `job_title` JSON DEFAULT NULL COMMENT '職稱 {"zh-TW": "行政專員", "en-US": "Specialist"}',
  `job_description` JSON DEFAULT NULL COMMENT '負責業務內容 (HTML) {"zh-TW": "1. 獎學金...", "en-US": "1. Scholarship..."}',

  -- 3. 狀態控制
  -- 根據您的需求：1在職, 2暫時離職, 3離職
  `status` TINYINT NOT NULL DEFAULT '1' COMMENT '1:Active(在職), 2:On Leave(留停/暫離), 3:Resigned(離職)',
  `sort_order` INT NOT NULL DEFAULT '0' COMMENT '顯示排序',

  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL DEFAULT NULL COMMENT '邏輯刪除'

  PRIMARY KEY (`id`),
  KEY `idx_dept_status` (`department_id`, `status`), -- 加速查詢某部門的在職名單

  -- 外鍵關聯：連結到 departments 表
  CONSTRAINT `fk_member_dept` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Resource
-- -----------------------------------------------------
-- 1. 資源分類表 (resource_categories)
-- -----------------------------------------------------
CREATE TABLE `resource_categories` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `slug` VARCHAR(50) NOT NULL COMMENT '分類代號 (如: student-service)',
  `names` JSON NOT NULL COMMENT '分類名稱 {"zh-TW": "生活輔導", "en-US": "Student Service"}',
  `description` JSON DEFAULT NULL COMMENT '分類描述，有助於 RAG 語意檢索',
  `sort_order` INT NOT NULL DEFAULT '0',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1',
  `parent_id` INT UNSIGNED DEFAULT NULL, -- 應對未來可能擴展的需求(目前這個欄位沒功能)

  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL DEFAULT NULL, -- 軟刪除(邏輯刪除)

  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_res_slug` (`slug`),
  CONSTRAINT `fk_category_parent` FOREIGN KEY (`parent_id`) REFERENCES `resource_categories` (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4;


-- -----------------------------------------------------
-- 2. 資源連結/內容表 (resources)
-- -----------------------------------------------------
CREATE TABLE `resources` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `category_id` INT UNSIGNED NOT NULL,

  -- 類型區分：link (外部連結), article (內部文章)
  `type` varchar(20) NOT NULL DEFAULT 'link' COMMENT '資源類型',

  -- 1. 標題與描述
  `title` JSON NOT NULL COMMENT '名稱 {"zh-TW": "...", "en-US": "..."}',
  `description` JSON DEFAULT NULL COMMENT '簡短說明',

  -- 2. 內容核心
  -- 將 url 改為 DEFAULT NULL
  `url` JSON DEFAULT NULL COMMENT '目標網址 {"zh-TW": "...", "en-US": "..."}',
  -- 新增詳細內容欄位
  `content` JSON DEFAULT NULL COMMENT '詳細內文 (供 Article 類型顯示及 RAG 使用)',

  -- 3. 排序與狀態
  `sort_order` INT NOT NULL DEFAULT '0',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1',

  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` TIMESTAMP NULL DEFAULT NULL, -- 軟刪除(邏輯刪除)

  PRIMARY KEY (`id`),
  KEY `idx_res_cat` (`category_id`, `sort_order`),
  CONSTRAINT `fk_res_category` FOREIGN KEY (`category_id`) REFERENCES `resource_categories` (`id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8mb4;
```
