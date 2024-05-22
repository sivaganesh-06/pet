-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: data
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
-- Table structure for table `adoption`
--

DROP TABLE IF EXISTS `adoption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adoption` (
  `name` varchar(100) NOT NULL,
  `species` text,
  `breed` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `location` varchar(100) NOT NULL,
  `description` text,
  `image_url` varchar(255) DEFAULT NULL,
  `shelter_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shelter_id` (`shelter_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `adoption_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `shelter_id` FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adoption`
--

LOCK TABLES `adoption` WRITE;
/*!40000 ALTER TABLE `adoption` DISABLE KEYS */;
INSERT INTO `adoption` VALUES ('ruby','cat','somali cat',3,'small','penamaluru','friendly','cat.jpg',10,3,12),('rab','rabbit','rabbit',3,'small','poranki','joyful','rab.jpeg',9,3,13),('parry','bird','parrot',2,'small','kanuru','naughty','parrot.jpg',9,3,14);
/*!40000 ALTER TABLE `adoption` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adoptionresources`
--

DROP TABLE IF EXISTS `adoptionresources`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adoptionresources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `content` text,
  `link` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adoptionresources`
--

LOCK TABLES `adoptionresources` WRITE;
/*!40000 ALTER TABLE `adoptionresources` DISABLE KEYS */;
/*!40000 ALTER TABLE `adoptionresources` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chat_messages`
--

DROP TABLE IF EXISTS `chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chat_messages` (
  `chat_id` int NOT NULL AUTO_INCREMENT,
  `sender_id` int DEFAULT NULL,
  `receiver_id` int DEFAULT NULL,
  `message` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `file_path` varchar(255) DEFAULT NULL,
  `pid` int DEFAULT NULL,
  PRIMARY KEY (`chat_id`),
  KEY `pid` (`pid`),
  CONSTRAINT `chat_messages_ibfk_1` FOREIGN KEY (`pid`) REFERENCES `petprofiles` (`pet_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chat_messages`
--

LOCK TABLES `chat_messages` WRITE;
/*!40000 ALTER TABLE `chat_messages` DISABLE KEYS */;
INSERT INTO `chat_messages` VALUES (15,2,10,'hi gudmrng','2024-05-18 05:07:32','3Ym4.jpg',12),(16,10,2,'hloooo have a nyc day','2024-05-18 05:08:26','0Gy6.jpg',12);
/*!40000 ALTER TABLE `chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `notes_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `description` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notes_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `petprofiles`
--

DROP TABLE IF EXISTS `petprofiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `petprofiles` (
  `name` varchar(100) NOT NULL,
  `species` text,
  `breed` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `location` text,
  `personality` text,
  `history` text,
  `image_url` varchar(255) DEFAULT NULL,
  `shelter_id` int NOT NULL,
  `pet_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`pet_id`),
  UNIQUE KEY `name` (`name`,`shelter_id`),
  KEY `shelter_id` (`shelter_id`),
  CONSTRAINT `petprofiles_ibfk_1` FOREIGN KEY (`shelter_id`) REFERENCES `shelters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `petprofiles`
--

LOCK TABLES `petprofiles` WRITE;
/*!40000 ALTER TABLE `petprofiles` DISABLE KEYS */;
INSERT INTO `petprofiles` VALUES ('ruby','cat','somali cat',3,'small','penamaluru','friendly','ruby.docx','cat.jpg',10,12),('parry','bird','parrot',2,'small','kanuru','naughty','Rab.docx','parrot.jpg',9,14),('abc','dog','breed',3,'2','hyderabad','abc','abc.webp','abc.webp',11,15);
/*!40000 ALTER TABLE `petprofiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `savedsearches`
--

DROP TABLE IF EXISTS `savedsearches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `savedsearches` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `search_name` varchar(100) DEFAULT NULL,
  `species` varchar(50) NOT NULL,
  `breed` varchar(100) DEFAULT NULL,
  `age` int DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `searched_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `s_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `s_id` (`s_id`),
  CONSTRAINT `s_id` FOREIGN KEY (`s_id`) REFERENCES `shelters` (`id`),
  CONSTRAINT `savedsearches_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `savedsearches`
--

LOCK TABLES `savedsearches` WRITE;
/*!40000 ALTER TABLE `savedsearches` DISABLE KEYS */;
INSERT INTO `savedsearches` VALUES (56,3,'cat','cat',NULL,NULL,NULL,NULL,'2024-05-18 15:45:45',NULL),(57,3,'cat','cat',NULL,NULL,NULL,NULL,'2024-05-18 15:48:30',NULL),(58,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 15:49:26',NULL),(59,3,'dog','dog',NULL,NULL,NULL,NULL,'2024-05-18 15:49:34',NULL),(60,3,'rabbit','rabbit',NULL,NULL,NULL,NULL,'2024-05-18 15:49:43',NULL),(61,3,'rabbit','rabbit',NULL,NULL,NULL,NULL,'2024-05-18 15:51:52',NULL),(62,3,'dog','dog',NULL,NULL,NULL,NULL,'2024-05-18 17:03:39',NULL),(63,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 17:03:47',NULL),(64,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 17:03:55',NULL),(65,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 17:04:26',NULL),(66,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 17:04:55',NULL),(67,3,'dog','dog',NULL,NULL,NULL,NULL,'2024-05-18 17:05:05',NULL),(68,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 17:06:19',NULL),(69,3,'cat','cat',NULL,NULL,NULL,NULL,'2024-05-18 17:06:35',NULL),(70,3,'rabbit','rabbit',NULL,NULL,NULL,NULL,'2024-05-18 17:07:17',NULL),(71,3,'parrot','parrot',NULL,NULL,NULL,NULL,'2024-05-18 17:07:37',NULL),(72,3,'bird','bird',NULL,NULL,NULL,NULL,'2024-05-18 17:08:09',NULL),(73,NULL,'cat','cat',NULL,NULL,NULL,NULL,'2024-05-20 11:07:58',10),(74,5,'d','d',NULL,NULL,NULL,NULL,'2024-05-22 12:30:14',NULL),(75,5,'dogs','dogs',NULL,NULL,NULL,NULL,'2024-05-22 12:30:25',NULL),(76,5,'cat','cat',NULL,NULL,NULL,NULL,'2024-05-22 12:30:43',NULL),(77,NULL,'dogs','dogs',NULL,NULL,NULL,NULL,'2024-05-22 12:41:47',11),(78,NULL,'dogs','dogs',NULL,NULL,NULL,NULL,'2024-05-22 12:52:16',11),(79,NULL,'dog','dog',NULL,NULL,NULL,NULL,'2024-05-22 12:52:23',11);
/*!40000 ALTER TABLE `savedsearches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `searchfilters`
--

DROP TABLE IF EXISTS `searchfilters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `searchfilters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `location` varchar(100) DEFAULT NULL,
  `pet_type` varchar(50) DEFAULT NULL,
  `size` varchar(20) DEFAULT NULL,
  `age` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `searchfilters`
--

LOCK TABLES `searchfilters` WRITE;
/*!40000 ALTER TABLE `searchfilters` DISABLE KEYS */;
INSERT INTO `searchfilters` VALUES (1,'vijayawada','dog','45',4),(2,'vijaywada','dog','4.5',3),(3,'vijayawada','dog','4.5',3),(4,'vijayawada','dog','4.5',3),(5,'vijayawada','dog','4.5',3),(6,'vijayawada','dog','4.5',3),(7,'vijayawada','dog','4.5',3),(8,'New York City','dog','large',5),(9,'New York City','dog','large',3),(10,'New York City','dog','large',3),(11,'vijayawada','parrot','medium',3),(12,'new york','dog','small',4),(13,'vijayawada','parrot','medium',5),(14,'penamaluru','gloden','4',10),(15,'penamaluru','gloden','small',3),(16,'penamaluru','gloden','small',3),(17,'dog','gloden','small',3),(18,'dog','gloden','small',3),(19,'','gloden','',3),(20,'','','',3),(21,'penamaluru','gloden','small',3),(22,'hyderabad','cat','5',2);
/*!40000 ALTER TABLE `searchfilters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelters`
--

DROP TABLE IF EXISTS `shelters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shelters` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `contact_person` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `website` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelters`
--

LOCK TABLES `shelters` WRITE;
/*!40000 ALTER TABLE `shelters` DISABLE KEYS */;
INSERT INTO `shelters` VALUES (9,'anusha','vijayawada','12121212','anusha@codegnan.com','1212121212',''),(10,'rishi','penamaluru','','rishithajarapala7@gmail.com','8187844367',''),(11,'harish','hyderabad','','lenkaharish22@gmail.com','1234567890','');
/*!40000 ALTER TABLE `shelters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'anusha','anusha@codegnan.com','1234');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `registration_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'anusha','anusha@codegnan.com','123','2024-03-29 08:52:43'),(3,'rishi','rishithajarapala7@gmail.com','12345','2024-05-15 04:23:09'),(4,'raja','jarapalarajanayak1@gmail.com','098','2024-05-20 14:38:56'),(5,'harish','lenkaharish22@gmail.com','1234','2024-05-22 06:35:14');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-22 17:38:16
