-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: boekenkast v2
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `bibliotheek`
--

DROP TABLE IF EXISTS `bibliotheek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bibliotheek` (
  `idbibliotheek` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) NOT NULL,
  `locatie` varchar(145) NOT NULL,
  `website` varchar(145) DEFAULT NULL,
  PRIMARY KEY (`idbibliotheek`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bibliotheek`
--

LOCK TABLES `bibliotheek` WRITE;
/*!40000 ALTER TABLE `bibliotheek` DISABLE KEYS */;
/*!40000 ALTER TABLE `bibliotheek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `boek`
--

DROP TABLE IF EXISTS `boek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `boek` (
  `idboek` int NOT NULL AUTO_INCREMENT,
  `naam` varchar(145) NOT NULL,
  `idauthor` int DEFAULT NULL,
  `RFID` varchar(45) DEFAULT NULL,
  `idbibliotheek` int NOT NULL,
  `inleverdatum` date DEFAULT NULL,
  PRIMARY KEY (`idboek`),
  KEY `fk_boek_bibliotheek_idx` (`idbibliotheek`),
  CONSTRAINT `fk_boek_bibliotheek` FOREIGN KEY (`idbibliotheek`) REFERENCES `bibliotheek` (`idbibliotheek`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `boek`
--

LOCK TABLES `boek` WRITE;
/*!40000 ALTER TABLE `boek` DISABLE KEYS */;
/*!40000 ALTER TABLE `boek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hystoriek`
--

DROP TABLE IF EXISTS `hystoriek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hystoriek` (
  `idhystoriek` int NOT NULL,
  `idsensor/actuator` int DEFAULT NULL,
  `waarde` varchar(45) DEFAULT NULL,
  `tijdstip` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idhystoriek`),
  KEY `fk_hystoriek_sensor/actuator1_idx` (`idsensor/actuator`),
  CONSTRAINT `fk_hystoriek_sensor/actuator1` FOREIGN KEY (`idsensor/actuator`) REFERENCES `sensor/actuator` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hystoriek`
--

LOCK TABLES `hystoriek` WRITE;
/*!40000 ALTER TABLE `hystoriek` DISABLE KEYS */;
INSERT INTO `hystoriek` VALUES (1,1,'100','2021-05-28 11:42:23'),(2,2,'134','2021-05-28 11:42:23'),(3,3,'127','2021-05-28 11:42:23'),(4,4,'501','2021-05-28 11:42:23'),(5,5,'134','2021-05-28 11:42:23'),(6,5,'604','2021-05-28 11:42:23'),(7,6,'1','2021-05-28 11:42:23'),(8,6,'0','2021-05-28 11:42:23'),(9,5,'103','2021-05-28 11:42:23'),(10,2,'558','2021-05-28 11:42:23');
/*!40000 ALTER TABLE `hystoriek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `positie boekenkast`
--

DROP TABLE IF EXISTS `positie boekenkast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `positie boekenkast` (
  `idpositie` int NOT NULL,
  `idboek` int DEFAULT NULL,
  `kleur ledstrip` varchar(45) NOT NULL,
  PRIMARY KEY (`idpositie`),
  KEY `fk_positie boekenkast_boek1_idx` (`idboek`),
  CONSTRAINT `fk_positie boekenkast_boek1` FOREIGN KEY (`idboek`) REFERENCES `boek` (`idboek`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `positie boekenkast`
--

LOCK TABLES `positie boekenkast` WRITE;
/*!40000 ALTER TABLE `positie boekenkast` DISABLE KEYS */;
/*!40000 ALTER TABLE `positie boekenkast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor/actuator`
--

DROP TABLE IF EXISTS `sensor/actuator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor/actuator` (
  `id` int NOT NULL,
  `naam` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor/actuator`
--

LOCK TABLES `sensor/actuator` WRITE;
/*!40000 ALTER TABLE `sensor/actuator` DISABLE KEYS */;
INSERT INTO `sensor/actuator` VALUES (1,'ldr1'),(2,'ldr2'),(3,'ldr3'),(4,'ldr4'),(5,'ldr5'),(6,'infrarood sensor'),(7,'rfid'),(8,'led strip');
/*!40000 ALTER TABLE `sensor/actuator` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-28 17:34:56
