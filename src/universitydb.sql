-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: university
-- ------------------------------------------------------
-- Server version	8.0.39

CREATE DATABASE IF NOT EXISTS university`;
USE university;

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
-- Table structure for table `autochecker`
--

DROP TABLE IF EXISTS `autochecker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `autochecker` (
  `coursework_id` int NOT NULL,
  `marking_scheme_id` int NOT NULL,
  `autochecker_marks` int DEFAULT NULL,
  PRIMARY KEY (`coursework_id`,`marking_scheme_id`),
  KEY `marking_scheme_id` (`marking_scheme_id`),
  CONSTRAINT `autochecker_ibfk_1` FOREIGN KEY (`coursework_id`) REFERENCES `courseworks` (`coursework_id`),
  CONSTRAINT `autochecker_ibfk_2` FOREIGN KEY (`marking_scheme_id`) REFERENCES `markingschemes` (`marking_scheme_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autochecker`
--

LOCK TABLES `autochecker` WRITE;
/*!40000 ALTER TABLE `autochecker` DISABLE KEYS */;
/*!40000 ALTER TABLE `autochecker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courseworks`
--

DROP TABLE IF EXISTS `courseworks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `courseworks` (
  `coursework_id` int NOT NULL,
  `module_id` int NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`coursework_id`),
  KEY `module_id` (`module_id`),
  CONSTRAINT `courseworks_ibfk_1` FOREIGN KEY (`module_id`) REFERENCES `modules` (`module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courseworks`
--

LOCK TABLES `courseworks` WRITE;
/*!40000 ALTER TABLE `courseworks` DISABLE KEYS */;
INSERT INTO `courseworks` VALUES (101,1,'Database Assignment 1'),(102,1,'Database Assignment 2'),(103,1,'Database Assignment 3'),(104,1,'Database Assignment 4'),(105,1,'Database Assignment 5'),(106,1,'Database Assignment 6'),(107,1,'Database Assignment 7'),(108,1,'Database Assignment 8'),(109,1,'Database Assignment 9'),(110,1,'Database Assignment 10'),(201,2,'Software Design 1'),(202,2,'Software Design 2'),(203,2,'Software Design 3'),(204,2,'Software Design 4'),(205,2,'Software Design 5'),(206,2,'Software Design 6'),(207,2,'Software Design 7'),(208,2,'Software Design 8'),(209,2,'Software Design 9'),(210,2,'Software Design 10'),(301,3,'ML Basics 1'),(302,3,'ML Basics 2'),(303,3,'ML Basics 3'),(304,3,'ML Basics 4'),(305,3,'ML Basics 5'),(306,3,'ML Basics 6'),(307,3,'ML Basics 7'),(308,3,'ML Basics 8'),(309,3,'ML Basics 9'),(310,3,'ML Basics 10'),(401,4,'Security Principles 1'),(402,4,'Security Principles 2'),(403,4,'Security Principles 3'),(404,4,'Security Principles 4'),(405,4,'Security Principles 5'),(406,4,'Security Principles 6'),(407,4,'Security Principles 7'),(408,4,'Security Principles 8'),(409,4,'Security Principles 9'),(410,4,'Security Principles 10'),(501,5,'Usability Test 1'),(502,5,'Usability Test 2'),(503,5,'Usability Test 3'),(504,5,'Usability Test 4'),(505,5,'Usability Test 5'),(506,5,'Usability Test 6'),(507,5,'Usability Test 7'),(508,5,'Usability Test 8'),(509,5,'Usability Test 9'),(510,5,'Usability Test 10');
/*!40000 ALTER TABLE `courseworks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `markingschemes`
--

DROP TABLE IF EXISTS `markingschemes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `markingschemes` (
  `marking_scheme_id` int NOT NULL,
  `coursework_id` int NOT NULL,
  `Description` text,
  PRIMARY KEY (`marking_scheme_id`),
  KEY `coursework_id` (`coursework_id`),
  CONSTRAINT `markingschemes_ibfk_1` FOREIGN KEY (`coursework_id`) REFERENCES `courseworks` (`coursework_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `markingschemes`
--

LOCK TABLES `markingschemes` WRITE;
/*!40000 ALTER TABLE `markingschemes` DISABLE KEYS */;
INSERT INTO `markingschemes` VALUES (1,101,'Accuracy and completeness'),(2,102,'Clarity and formatting'),(3,103,'Code efficiency'),(4,104,'Documentation quality'),(5,105,'Problem-solving skills');
/*!40000 ALTER TABLE `markingschemes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moduleleaders`
--

DROP TABLE IF EXISTS `moduleleaders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `moduleleaders` (
  `module_leader_id` int NOT NULL,
  `module_leader_name` varchar(100) NOT NULL,
  PRIMARY KEY (`module_leader_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moduleleaders`
--

LOCK TABLES `moduleleaders` WRITE;
/*!40000 ALTER TABLE `moduleleaders` DISABLE KEYS */;
INSERT INTO `moduleleaders` VALUES (1,'Dr. Alice Johnson'),(2,'Dr. Bob Smith'),(3,'Dr. Clara Davis'),(4,'Dr. Daniel Brown'),(5,'Dr. Emily Wilson');
/*!40000 ALTER TABLE `moduleleaders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modules`
--

DROP TABLE IF EXISTS `modules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modules` (
  `module_id` int NOT NULL,
  `module_name` varchar(50) NOT NULL,
  `module_leader_id` int DEFAULT NULL,
  PRIMARY KEY (`module_id`),
  KEY `module_leader_id` (`module_leader_id`),
  CONSTRAINT `modules_ibfk_1` FOREIGN KEY (`module_leader_id`) REFERENCES `moduleleaders` (`module_leader_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modules`
--

LOCK TABLES `modules` WRITE;
/*!40000 ALTER TABLE `modules` DISABLE KEYS */;
INSERT INTO `modules` VALUES (1,'Database Systems',1),(2,'Software Engineering',2),(3,'Machine Learning',3),(4,'Networks and Security',4),(5,'Human-Computer Interaction',5);
/*!40000 ALTER TABLE `modules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` int NOT NULL,
  `student_name` varchar(100) NOT NULL,
  PRIMARY KEY (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` VALUES (1,'Alice'),(2,'Bob'),(3,'Charlie'),(4,'Diana'),(5,'Eve'),(6,'Frank'),(7,'Grace'),(8,'Hannah'),(9,'Ivan'),(10,'Jack');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `studentscoursework`
--

DROP TABLE IF EXISTS `studentscoursework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `studentscoursework` (
  `student_id` int NOT NULL,
  `coursework_id` int NOT NULL,
  `coursework_marks` int DEFAULT NULL,
  `teacher_id` int DEFAULT NULL,
  PRIMARY KEY (`student_id`,`coursework_id`),
  KEY `coursework_id` (`coursework_id`),
  KEY `teacher_id` (`teacher_id`),
  CONSTRAINT `studentscoursework_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `studentscoursework_ibfk_2` FOREIGN KEY (`coursework_id`) REFERENCES `courseworks` (`coursework_id`),
  CONSTRAINT `studentscoursework_ibfk_3` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `studentscoursework`
--

LOCK TABLES `studentscoursework` WRITE;
/*!40000 ALTER TABLE `studentscoursework` DISABLE KEYS */;
INSERT INTO `studentscoursework` VALUES (1,101,85,1),(1,201,89,2),(1,301,88,3),(2,102,90,1),(2,202,87,2),(2,302,86,3),(3,103,88,1),(3,203,85,2),(3,303,84,3),(4,104,92,1),(4,204,90,2),(4,304,91,3),(5,105,NULL,1),(5,205,NULL,2),(5,305,NULL,3),(6,106,75,1),(6,206,78,2),(6,306,77,3),(7,107,80,1),(7,207,82,2),(7,307,81,3),(8,108,85,1),(8,208,91,2),(8,308,87,3),(9,109,NULL,1),(9,209,76,2),(9,309,90,3),(10,110,88,1),(10,210,NULL,2),(10,310,NULL,3);
/*!40000 ALTER TABLE `studentscoursework` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `teacher_id` int NOT NULL,
  `teacher_name` varchar(100) NOT NULL,
  PRIMARY KEY (`teacher_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` VALUES (1,'Prof. John Miller'),(2,'Prof. Susan Lee'),(3,'Prof. Michael Scott');
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacherscoursework`
--

DROP TABLE IF EXISTS `teacherscoursework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacherscoursework` (
  `teacher_id` int NOT NULL,
  `coursework_id` int NOT NULL,
  `student_id` int NOT NULL,
  `marks` int DEFAULT NULL,
  PRIMARY KEY (`teacher_id`,`coursework_id`,`student_id`),
  KEY `coursework_id` (`coursework_id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `teacherscoursework_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`),
  CONSTRAINT `teacherscoursework_ibfk_2` FOREIGN KEY (`coursework_id`) REFERENCES `courseworks` (`coursework_id`),
  CONSTRAINT `teacherscoursework_ibfk_3` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherscoursework`
--

LOCK TABLES `teacherscoursework` WRITE;
/*!40000 ALTER TABLE `teacherscoursework` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacherscoursework` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-28  1:58:11
