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
-- Table structure for table `bl_sys_tab`
--

DROP TABLE IF EXISTS `bl_sys_tab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bl_sys_tab` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tab_name` varchar(50) NOT NULL DEFAULT '' COMMENT '菜单(或权限节点)名称',
  `tab_level` int NOT NULL DEFAULT '0' COMMENT '菜单级别，0一级菜单，1二级菜单，2三级节点',
  `parent_id` int NOT NULL DEFAULT '0' COMMENT '所指向的父id',
  `icon` varchar(50) NOT NULL DEFAULT '' COMMENT '图标代码，一级菜单有显示图标',
  `mode_code` varchar(50) NOT NULL DEFAULT '' COMMENT '权限标识，唯一，在具体的后台请求方法配置该项，实现绑定',
  `jmp_url` varchar(50) NOT NULL DEFAULT '' COMMENT '跳转路径，点击二级菜单实现跳转',
  `ordering` int NOT NULL DEFAULT '0' COMMENT '菜单排序',
  `createtime` int NOT NULL DEFAULT '0' COMMENT '创建时间戳',
  `updatetime` int NOT NULL DEFAULT '0' COMMENT '更新时间戳',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb3 ROW_FORMAT=DYNAMIC;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bl_sys_tab`
--

LOCK TABLES `bl_sys_tab` WRITE;
/*!40000 ALTER TABLE `bl_sys_tab` DISABLE KEYS */;
INSERT INTO `bl_sys_tab` VALUES (14,'系统管理',0,0,'&#xe61d','sys-manager','',1,1696376336,1696379029),(15,'菜单管理',1,14,'','/admin/sys/tab_list','/admin/sys/tab_list',0,1696376395,1696376395),(16,'角色管理',1,14,'','/admin/sys/role_list','/admin/sys/role_list',0,1696376437,1696376437),(17,'管理员列表',1,14,'','/admin/sys/admin_list','/admin/sys/admin_list',0,1696376461,1696376461),(18,'测试菜单',0,0,'&#xe625','test-menu','',2,1696378772,1696378941),(19,'test1',1,18,'','ddd','ddd',0,1696378820,1696378820),(20,'test2',1,18,'','eee','eee',0,1696378828,1696378828),(21,'添加vs编辑',2,17,'','/admin/sys/admin_addupdate','',0,1696468848,1696469847),(22,'删除',2,17,'','/admin/sys/admin_del','',0,1696468872,1696468872),(23,'启用',2,17,'','/admin/sys/admin_start','',0,1696469875,1696469875),(24,'停用',2,17,'','/admin/sys/admin_stop','',0,1696469889,1696469889),(25,'添加vs编辑',2,15,'','/admin/sys/tab_addupdate','',0,1696469994,1696469994),(26,'删除',2,15,'','/admin/sys/tab_del','',0,1696470030,1696470030),(27,'子菜单',2,15,'','/admin/sys/subtab_list','',0,1696470077,1696470077),(28,'添加vs编辑',2,16,'','/admin/sys/role_addupdate','',0,1696470286,1696470286),(29,'删除',2,16,'','/admin/sys/role_del','',0,1696470305,1696470305),(30,'多媒体',0,0,'&#xe725','media-data','',0,1728633467,1728633640),(31,'文章',1,30,'','/admin/media/article_list','/admin/media/article_list',0,1728634003,1728635141),(32,'视频',1,30,'','/admin/media/video_list','/admin/media/video_list',0,1728634532,1728635166),(33,'音频',1,30,'','/admin/media/music_list','/admin/media/music_list',0,1728634560,1728635178),(34,'图片',1,30,'','/admin/media/pic_list','/admin/media/pic_list',0,1728634577,1728635193);
/*!40000 ALTER TABLE `bl_sys_tab` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-22  4:01:55
