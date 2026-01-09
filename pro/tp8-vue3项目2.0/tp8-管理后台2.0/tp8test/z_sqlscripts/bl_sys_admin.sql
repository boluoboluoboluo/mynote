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
-- Table structure for table `bl_sys_admin`
--

DROP TABLE IF EXISTS `bl_sys_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bl_sys_admin` (
  `id` int NOT NULL AUTO_INCREMENT,
  `admin_name` varchar(50) NOT NULL DEFAULT '' COMMENT '用户名',
  `password` varchar(500) NOT NULL DEFAULT '' COMMENT '密码',
  `nick_name` varchar(100) NOT NULL DEFAULT '' COMMENT '昵称',
  `role_id` int NOT NULL DEFAULT '0' COMMENT '角色id',
  `email` varchar(100) NOT NULL DEFAULT '' COMMENT '邮箱',
  `createtime` int NOT NULL DEFAULT '0' COMMENT '创建时间戳',
  `updatetime` int NOT NULL DEFAULT '0' COMMENT '更新时间戳',
  `is_del` int NOT NULL DEFAULT '0' COMMENT '是否逻辑删除状态，0启用1停用',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bl_sys_admin`
--

LOCK TABLES `bl_sys_admin` WRITE;
/*!40000 ALTER TABLE `bl_sys_admin` DISABLE KEYS */;
INSERT INTO `bl_sys_admin` VALUES (1,'admin','$2y$10$lhg7DATJFn0putQDxs1YOulGyryIhpAoRbuH9zvxG8gdCXjFuL6uW','管理员',1,'',1695138978,1696378645,0),(2,'test','$2y$10$x13IFIY0NIY8Jsw8KljP/Onh0ZH7D3SZfeE.U16ZetHLEjJbFpDC6','手动复位法',2,'1@q.com',1696288731,1696470450,0),(5,'uu','$2y$10$YRc5e4Ikr.PEBfRsAIdBkewKPyP8R1bQxwr10dY6sk8R/nAxsNHIC','秃头披风侠',1,'',1696378622,1696378622,0),(6,'a','$2y$10$ebG52iiAvzKzgIQxx8Gguu.zJCfLNEVy28dVi7wVfdzEYF5BNXlHy','a',3,'',1696470488,1696470488,0);
/*!40000 ALTER TABLE `bl_sys_admin` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-22  3:59:56
