-- MariaDB dump 10.19-11.3.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: distribuidos1
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS `distribuidos1`;
USE `distribuidos1`;

--
-- Table structure for table `db1`
--

DROP TABLE IF EXISTS `db1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` mediumtext NOT NULL,
  `autor` varchar(150) DEFAULT NULL,
  `tipo` varchar(150) DEFAULT NULL,
  `nodo` varchar(100) NOT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db1`
--

LOCK TABLES `db1` WRITE;
/*!40000 ALTER TABLE `db1` DISABLE KEYS */;
INSERT INTO `db1` VALUES
(1,'Cambios Fasicos','Juan Perez','tesis','slaveTesis','2024-04-22 16:01:49'),
(2,'Fisica Cuantica','Pedro Perez','tesis','slaveTesis','2024-04-22 16:01:49'),
(3,'Cuantica de los fluidos','Tesla','tesis','slaveTesis','2024-04-22 16:01:49');
/*!40000 ALTER TABLE `db1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db2`
--

DROP TABLE IF EXISTS `db2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` mediumtext NOT NULL,
  `autor` varchar(150) DEFAULT NULL,
  `tipo` varchar(150) DEFAULT NULL,
  `nodo` varchar(100) NOT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db2`
--

LOCK TABLES `db2` WRITE;
/*!40000 ALTER TABLE `db2` DISABLE KEYS */;
INSERT INTO `db2` VALUES
(1,'Hola Mundo!','Mundo','general','slaveGeneral','2024-04-23 15:10:51'),
(2,'Cotizacion gaming','Pedro Pedro','general','slaveGeneral','2024-04-23 15:10:51'),
(3,'Tazas por el mundo','Edgardo Ramos','general','slaveGeneral','2024-04-23 15:10:51');
/*!40000 ALTER TABLE `db2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db3`
--

DROP TABLE IF EXISTS `db3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` mediumtext NOT NULL,
  `autor` varchar(150) DEFAULT NULL,
  `tipo` varchar(150) DEFAULT NULL,
  `nodo` varchar(100) NOT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db3`
--

LOCK TABLES `db3` WRITE;
/*!40000 ALTER TABLE `db3` DISABLE KEYS */;
/*!40000 ALTER TABLE `db3` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `db4`
--

DROP TABLE IF EXISTS `db4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `db4` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` mediumtext NOT NULL,
  `autor` varchar(150) DEFAULT NULL,
  `tipo` varchar(150) DEFAULT NULL,
  `nodo` varchar(100) NOT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `db4`
--

LOCK TABLES `db4` WRITE;
/*!40000 ALTER TABLE `db2` DISABLE KEYS */;
INSERT INTO `db4` VALUES
(1,'Conferencia PC Gaming','Juan Perez','audio','slaveAudio','2024-04-23 15:10:51'),
(2,'Audio Whatsapp 12345','Anonymous','audio','slaveAudio','2024-04-23 15:10:51');
/*!40000 ALTER TABLE `db2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos`
--

DROP TABLE IF EXISTS `tipos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipos` (
  `idTipos` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `nodoDestino` varchar(100) NOT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp(),
  `nodo` varchar(100) NOT NULL,
  `updatedAt` datetime DEFAULT NULL,
  PRIMARY KEY (`idTipos`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos`
--

LOCK TABLES `tipos` WRITE;
/*!40000 ALTER TABLE `tipos` DISABLE KEYS */;
INSERT INTO `tipos` VALUES
(1,'tesis','localhost:5001','2024-04-22 15:59:04','master','2024-04-24 12:46:00'),
(2,'libros','localhost:5003','2024-04-23 14:15:53','master','2024-04-24 12:46:00'),
(3,'general','localhost:5002','2024-04-23 14:15:53','master','2024-04-24 12:46:00'),
(4,'audio','localhost:5004','2024-04-23 14:15:53','master','2024-04-24 12:46:00');
/*!40000 ALTER TABLE `tipos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-25 16:46:23
