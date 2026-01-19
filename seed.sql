-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: osa_newdb_test
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` json NOT NULL COMMENT '部門名稱 {"zh-TW": "生活輔導組", "en-US": "Student Services Division"}',
  `description` json DEFAULT NULL COMMENT '部門簡介 (含HTML) {"zh-TW": "<p>...</p>", "en-US": "<p>...</p>"}',
  `email` varchar(255) DEFAULT NULL COMMENT '部門共用信箱',
  `website_url` json DEFAULT NULL COMMENT '部門網站 {"zh-TW": "https://.../zh", "en-US": "https://.../en"}',
  `image_path` varchar(500) DEFAULT NULL COMMENT '部門代表圖 (原 group_pic)',
  `sort_order` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1:啟用, 0:隱藏',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,'{\"en-US\": \"Student Service Division\", \"zh-TW\": \"生活輔導組\"}','{\"en-US\": \"<p>Responsible for student life counseling...</p>\", \"zh-TW\": \"<p>負責學生生活輔導、獎助學金...</p>\"}','ncu57212@ncu.edu.tw','{\"en-US\": \"https://life.ncu.edu.tw/en\", \"zh-TW\": \"https://life.ncu.edu.tw\"}','dept_life.jpg',1,1,'2026-01-15 14:44:01','2026-01-15 14:44:01'),(2,'{\"en-US\": \"Counseling Center\", \"zh-TW\": \"諮商輔導中心\"}','{\"en-US\": \"<p>Providing counseling services...</p>\", \"zh-TW\": \"<p>提供心理諮商與測驗服務...</p>\"}','ncu57268@ncu.edu.tw','{\"en-US\": \"https://counsel.ncu.edu.tw/en\", \"zh-TW\": \"https://counsel.ncu.edu.tw\"}','dept_counsel.jpg',2,1,'2026-01-15 14:44:01','2026-01-15 14:44:01');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `download_attachments`
--

DROP TABLE IF EXISTS `download_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `download_attachments` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `download_id` bigint unsigned NOT NULL,
  `type` enum('file','link') NOT NULL DEFAULT 'file',
  `file_format` varchar(10) DEFAULT NULL COMMENT 'pdf, doc, odf, xls...',
  `path` varchar(500) NOT NULL COMMENT '檔案相對路徑 或 外部 URL',
  `title` varchar(255) DEFAULT NULL,
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_dl_format` (`download_id`,`file_format`),
  CONSTRAINT `fk_dl_attach` FOREIGN KEY (`download_id`) REFERENCES `downloads` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `download_attachments`
--

LOCK TABLES `download_attachments` WRITE;
/*!40000 ALTER TABLE `download_attachments` DISABLE KEYS */;
INSERT INTO `download_attachments` VALUES (1,1,'file','pdf','/downloads/dorm_rules.pdf','法規全文 (PDF)',1),(2,1,'file','doc','/downloads/dorm_rules.docx','法規全文 (Word)',2),(3,2,'file','odf','/downloads/venue_form.odt','申請表 (ODT)',1),(4,2,'file','pdf','/downloads/venue_form.pdf','申請表 (PDF)',2),(5,3,'link',NULL,'https://scholarship.ncu.edu.tw/rules','線上查看',1);
/*!40000 ALTER TABLE `download_attachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `download_categories`
--

DROP TABLE IF EXISTS `download_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `download_categories` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(50) NOT NULL COMMENT '網址代碼 (如: scholarship)',
  `names` json NOT NULL COMMENT '{"zh-TW": "獎學金", "en-US": "Scholarships"}',
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_dl_slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `download_categories`
--

LOCK TABLES `download_categories` WRITE;
/*!40000 ALTER TABLE `download_categories` DISABLE KEYS */;
INSERT INTO `download_categories` VALUES (1,'scholarships','{\"en-US\": \"Scholarships\", \"zh-TW\": \"獎助學金\"}',1),(2,'regulations','{\"en-US\": \"Regulations\", \"zh-TW\": \"法規辦法\"}',2),(3,'forms','{\"en-US\": \"Forms\", \"zh-TW\": \"表單下載\"}',3);
/*!40000 ALTER TABLE `download_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `downloads`
--

DROP TABLE IF EXISTS `downloads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `downloads` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `category_id` int unsigned NOT NULL,
  `type` enum('regulation','form','other') NOT NULL DEFAULT 'other' COMMENT 'regulation:法規, form:表格',
  `title` json NOT NULL COMMENT '{"zh-TW": "學生宿舍管理辦法", "en-US": "Dormitory Rules"}',
  `department` json DEFAULT NULL COMMENT '發布單位名稱，如 {"zh-TW": "生活輔導組"}',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '0:Draft, 1:Published, 2:Archived',
  `published_at` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_dl_cat_type` (`category_id`,`type`),
  CONSTRAINT `fk_dl_category` FOREIGN KEY (`category_id`) REFERENCES `download_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `downloads`
--

LOCK TABLES `downloads` WRITE;
/*!40000 ALTER TABLE `downloads` DISABLE KEYS */;
INSERT INTO `downloads` VALUES (1,2,'regulation','{\"en-US\": \"NCU Student Dormitory Management Guidelines\", \"zh-TW\": \"國立中央大學學生宿舍管理辦法\"}','{\"en-US\": \"Student Housing Service Division\", \"zh-TW\": \"住宿服務組\"}',1,'2024-08-01 00:00:00','2026-01-15 14:44:01','2026-01-15 14:44:01',NULL),(2,3,'form','{\"en-US\": \"Student Activity Venue Application Form\", \"zh-TW\": \"學生活動場地借用申請表\"}','{\"en-US\": \"Extracurricular Activities Division\", \"zh-TW\": \"課外活動組\"}',1,'2024-09-01 00:00:00','2026-01-15 14:44:01','2026-01-15 14:44:01',NULL),(3,1,'other','{\"en-US\": \"President Scholarship Guidelines\", \"zh-TW\": \"校長獎學金申請辦法\"}','{\"en-US\": \"Student Service Division\", \"zh-TW\": \"生活輔導組\"}',1,'2024-09-15 00:00:00','2026-01-15 14:44:01','2026-01-15 14:44:01',NULL);
/*!40000 ALTER TABLE `downloads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_attachments`
--

DROP TABLE IF EXISTS `event_attachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_attachments` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `event_id` bigint unsigned NOT NULL,
  `type` enum('image','file','link') NOT NULL,
  `path` varchar(500) NOT NULL COMMENT '檔案路徑 或 URL',
  `title` varchar(255) DEFAULT '' COMMENT '顯示名稱',
  `sort_order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_event_attach` (`event_id`),
  CONSTRAINT `fk_event_attach` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_attachments`
--

LOCK TABLES `event_attachments` WRITE;
/*!40000 ALTER TABLE `event_attachments` DISABLE KEYS */;
INSERT INTO `event_attachments` VALUES (1,1,'file','/uploads/2025/loan_guidelines.pdf','申請辦法全文.pdf',1),(2,2,'image','/uploads/2025/xmas_poster.jpg','活動海報',1),(3,3,'link','https://forms.gle/xyz123','報名連結',1),(4,3,'file','/uploads/2025/ai_slides.pdf','講座講義.pdf',2);
/*!40000 ALTER TABLE `event_attachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_categories`
--

DROP TABLE IF EXISTS `event_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_categories` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(50) NOT NULL COMMENT '網址或CSS用的代碼，如 speech, activity',
  `names` json NOT NULL COMMENT '多語系名稱，存 {"zh-TW": "演講", "en-US": "Speech"}',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1:啟用, 0:停用 (分類軟刪除用)',
  `sort_order` int NOT NULL DEFAULT '0' COMMENT '顯示順序',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_categories`
--

LOCK TABLES `event_categories` WRITE;
/*!40000 ALTER TABLE `event_categories` DISABLE KEYS */;
INSERT INTO `event_categories` VALUES (1,'speech','{\"en-US\": \"Keynote Speech\", \"zh-TW\": \"專題演講\"}',1,1),(2,'activity','{\"en-US\": \"Student Activity\", \"zh-TW\": \"學生活動\"}',1,2),(3,'official','{\"en-US\": \"Official Announcement\", \"zh-TW\": \"行政公告\"}',1,3);
/*!40000 ALTER TABLE `event_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_translations`
--

DROP TABLE IF EXISTS `event_translations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event_translations` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `event_id` bigint unsigned NOT NULL,
  `locale` varchar(10) NOT NULL DEFAULT 'zh-TW',
  `title` varchar(255) NOT NULL,
  `content` mediumtext,
  `location` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_event_locale` (`event_id`,`locale`),
  CONSTRAINT `fk_event_trans` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_translations`
--

LOCK TABLES `event_translations` WRITE;
/*!40000 ALTER TABLE `event_translations` DISABLE KEYS */;
INSERT INTO `event_translations` VALUES (1,1,'zh-TW','【公告】114學年度第1學期就學貸款申請須知','<p>請同學注意申請期限...</p>','線上申請'),(2,1,'en-US','[Notice] Student Loan Application for Fall 2025','<p>Please note the deadline...</p>','Online Application'),(3,2,'zh-TW','聖誕音樂晚會 - 雪夜之歌','<p>年度最盛大的音樂饗宴...</p>','依仁堂籃球館'),(4,2,'en-US','Christmas Concert - Song of Snowy Night','<p>The biggest music event of the year...</p>','Yi-Ren Hall'),(5,3,'zh-TW','AI 時代的職場競爭力講座','<p>邀請 Google 資深工程師分享...</p>','秉文堂'),(6,3,'en-US','Career Competitiveness in the AI Era','<p>Guest speaker from Google...</p>','Bing-Wen Hall');
/*!40000 ALTER TABLE `event_translations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `category_id` int unsigned NOT NULL,
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '0:草稿(Draft), 1:發布(Published), 2:下架/封存(Archived)',
  `starts_at` datetime DEFAULT NULL COMMENT '活動開始時間',
  `ends_at` datetime DEFAULT NULL COMMENT '活動結束時間',
  `published_at` datetime DEFAULT NULL COMMENT '文章顯示日期 (排序與預約發布用)',
  `organizer_info` json DEFAULT NULL COMMENT '主辦單位資訊，存 JSON {"name":"課外組", "tel":"分機123"}',
  `is_target` tinyint(1) NOT NULL DEFAULT '0' COMMENT '特殊標記 (如:是否為目標活動)',
  `is_featured` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否置頂 (取代舊系統 status=3 的功能)',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_cat_status` (`category_id`,`status`),
  KEY `idx_publish` (`published_at`),
  CONSTRAINT `fk_event_category` FOREIGN KEY (`category_id`) REFERENCES `event_categories` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,3,1,'2025-09-01 08:00:00','2025-09-30 17:00:00','2025-08-20 09:00:00','{\"tel\": \"03-4227151 #57212\", \"name\": \"生活輔導組\", \"email\": \"ncu57212@ncu.edu.tw\"}',0,1,'2026-01-15 14:44:53','2026-01-15 14:44:53',NULL),(2,2,1,'2025-12-24 18:00:00','2025-12-24 21:00:00','2025-11-01 10:00:00','{\"tel\": \"03-4227151 #57268\", \"name\": \"學生會\", \"email\": \"sa@ncu.edu.tw\"}',0,0,'2026-01-15 14:44:53','2026-01-15 14:44:53',NULL),(3,1,1,'2025-10-15 14:00:00','2025-10-15 16:00:00','2025-09-10 09:00:00','{\"tel\": \"03-4227151 #57281\", \"name\": \"職涯發展中心\", \"email\": \"career@ncu.edu.tw\"}',1,0,'2026-01-15 14:44:53','2026-01-15 14:44:53',NULL);
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_members`
--

DROP TABLE IF EXISTS `group_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `group_members` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `department_id` int unsigned NOT NULL COMMENT '所屬部門 ID',
  `name` json NOT NULL COMMENT '姓名 {"zh-TW": "王小明", "en-US": "Wang, Xiao-Ming"}',
  `email` varchar(255) DEFAULT NULL,
  `tel` varchar(50) DEFAULT NULL COMMENT '分機或電話',
  `photo_path` varchar(500) DEFAULT NULL COMMENT '大頭照路徑',
  `job_title` json DEFAULT NULL COMMENT '職稱 {"zh-TW": "行政專員", "en-US": "Specialist"}',
  `job_description` json DEFAULT NULL COMMENT '負責業務內容 (HTML) {"zh-TW": "1. 獎學金...", "en-US": "1. Scholarship..."}',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '1:Active(在職), 2:On Leave(留停/暫離), 3:Resigned(離職)',
  `sort_order` int NOT NULL DEFAULT '0' COMMENT '顯示排序',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_dept_status` (`department_id`,`status`),
  CONSTRAINT `fk_member_dept` FOREIGN KEY (`department_id`) REFERENCES `departments` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_members`
--

LOCK TABLES `group_members` WRITE;
/*!40000 ALTER TABLE `group_members` DISABLE KEYS */;
INSERT INTO `group_members` VALUES (1,1,'{\"en-US\": \"Da-Ming Wang\", \"zh-TW\": \"王大明\"}','dmwang@ncu.edu.tw','57200','wang.jpg','{\"en-US\": \"Division Chief\", \"zh-TW\": \"組長\"}','{\"en-US\": \"1. Oversee division affairs<br>2. Budget control\", \"zh-TW\": \"1. 綜理全組業務<br>2. 預算控管\"}',1,0,'2026-01-15 14:44:01','2026-01-15 14:44:01'),(2,1,'{\"en-US\": \"Xiao-Mei Li\", \"zh-TW\": \"李小美\"}','xmli@ncu.edu.tw','57201','li.jpg','{\"en-US\": \"Specialist\", \"zh-TW\": \"行政專員\"}','{\"en-US\": \"1. Student Loans<br>2. Financial Aid\", \"zh-TW\": \"1. 就學貸款<br>2. 弱勢助學\"}',1,0,'2026-01-15 14:44:01','2026-01-15 14:44:01'),(3,2,'{\"en-US\": \"Pro Chen\", \"zh-TW\": \"陳專頁\"}','pchen@ncu.edu.tw','57266','chen.jpg','{\"en-US\": \"Counselor\", \"zh-TW\": \"心理師\"}','{\"en-US\": \"1. Individual Counseling<br>2. Group Workshops\", \"zh-TW\": \"1. 個別諮商<br>2. 團體工作坊\"}',1,0,'2026-01-15 14:44:01','2026-01-15 14:44:01');
/*!40000 ALTER TABLE `group_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource_categories`
--

DROP TABLE IF EXISTS `resource_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resource_categories` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `slug` varchar(50) NOT NULL COMMENT '分類代號 (如: student-service)',
  `names` json NOT NULL COMMENT '分類名稱 {"zh-TW": "生活輔導", "en-US": "Student Service"}',
  `sort_order` int NOT NULL DEFAULT '0',
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_res_slug` (`slug`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource_categories`
--

LOCK TABLES `resource_categories` WRITE;
/*!40000 ALTER TABLE `resource_categories` DISABLE KEYS */;
INSERT INTO `resource_categories` VALUES (1,'campus','{\"en-US\": \"Campus Services\", \"zh-TW\": \"校園服務\"}',1,1),(2,'government','{\"en-US\": \"Government Agencies\", \"zh-TW\": \"政府相關\"}',2,1);
/*!40000 ALTER TABLE `resource_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources`
--

DROP TABLE IF EXISTS `resources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `category_id` int unsigned NOT NULL,
  `title` json NOT NULL COMMENT '連結名稱 {"zh-TW": "學雜費減免", "en-US": "Tuition Exemption"}',
  `description` json DEFAULT NULL COMMENT '簡短說明',
  `url` json NOT NULL COMMENT '目標網址 {"zh-TW": "https://...", "en-US": "https://..."}',
  `sort_order` int NOT NULL DEFAULT '0' COMMENT '顯示順序',
  `is_active` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1:啟用, 0:隱藏',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_res_cat` (`category_id`,`sort_order`),
  CONSTRAINT `fk_res_category` FOREIGN KEY (`category_id`) REFERENCES `resource_categories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources`
--

LOCK TABLES `resources` WRITE;
/*!40000 ALTER TABLE `resources` DISABLE KEYS */;
INSERT INTO `resources` VALUES (1,1,'{\"en-US\": \"NCU Portal\", \"zh-TW\": \"Portal 入口\"}','{\"en-US\": \"Single Sign-On System\", \"zh-TW\": \"校務系統單一入口\"}','{\"en-US\": \"https://portal.ncu.edu.tw\", \"zh-TW\": \"https://portal.ncu.edu.tw\"}',1,1,'2026-01-15 14:44:01','2026-01-15 14:44:01'),(2,2,'{\"en-US\": \"Ministry of Education\", \"zh-TW\": \"教育部\"}',NULL,'{\"en-US\": \"https://english.moe.gov.tw\", \"zh-TW\": \"https://www.edu.tw\"}',1,1,'2026-01-15 14:44:01','2026-01-15 14:44:01'),(3,1,'{\"en-US\": \"Dormitory System\", \"zh-TW\": \"宿舍管理系統\"}',NULL,'{\"en-US\": \"https://dorm.ncu.edu.tw/en\", \"zh-TW\": \"https://dorm.ncu.edu.tw\"}',2,1,'2026-01-15 14:44:01','2026-01-15 14:44:01');
/*!40000 ALTER TABLE `resources` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-17 22:23:19
