-- MySQL dump 10.13  Distrib 8.1.0, for Win64 (x86_64)
--
-- Host: localhost    Database: uu
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bl_media_data`
--

DROP TABLE IF EXISTS `bl_media_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bl_media_data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL DEFAULT '',
  `desc` text COMMENT 'description...',
  `type` int NOT NULL DEFAULT '0' COMMENT 'media type:article(0) or video(1) or music(2) or pic(3)',
  `url` varchar(255) NOT NULL DEFAULT '' COMMENT 'media url,empty if article',
  `context` mediumtext COMMENT 'article content.',
  `ordering` int NOT NULL DEFAULT '0' COMMENT 'ordering.',
  `createtime` int NOT NULL DEFAULT '0',
  `updatetime` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bl_media_data`
--

LOCK TABLES `bl_media_data` WRITE;
/*!40000 ALTER TABLE `bl_media_data` DISABLE KEYS */;
INSERT INTO `bl_media_data` VALUES (1,'test','test...',0,'','<s><span style=\"color:#E53333;\">hghhh</span></s><span style=\"font-size:16px;\"><strong></strong></span>',0,1728660695,1728675407),(2,'hello','he',0,'','<p>\n	<strong>HTML内容</strong> \n</p>\n<h1 style=\"text-align:center;\">\n	<strong>hello world</strong> \n</h1>\n<h1 style=\"text-align:center;\">\n	<strong><span style=\"color:#9933E5;\">好，世界</span></strong> \n</h1>',0,1728670903,1728672869),(3,'百事7','77',0,'','<h3 style=\"text-align:center;\">\n	<span style=\"background-color:#E56600;\"><b><span style=\"font-family:&quot;color:#E56600;\"><span style=\"color:#60D978;\">6666</span><span style=\"color:#003399;\"></span></span><span style=\"font-family:KaiTi_GB2312;\"></span></b></span>\n</h3>',0,1728671450,1728675098),(31,'333','333',1,'video/20241012\\a5bb839523d9f79325eba0378cbf69d4.mp4',NULL,0,1728732050,1728750478),(32,'3','2',1,'video/20241013\\525ed29363dfe03b837904cf803c2c3f.mp4',NULL,0,1728750362,1728750362),(34,'盗将行','m4a',2,'music/20241013\\d4fd5064099821737655235bf84ad896.m4a',NULL,0,1728754718,1728755579),(36,'匆匆那年','mp3',2,'music/20241013\\86e1901d4b505b156f0a533a0df57b54.mp3',NULL,0,1728755563,1728755563),(38,'pic2','png',3,'pic/20241013\\a24f12658d5e9ff976e59502f59215b7.png',NULL,0,1728756496,1728756496),(39,'1','jpg',3,'pic/20241013\\bc481dceeca0d19638da31f9ac9043d4.jpg',NULL,0,1728756923,1728756923);
/*!40000 ALTER TABLE `bl_media_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-22  4:02:00
