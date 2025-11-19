-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: sgmcl
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `alertas`
--

DROP TABLE IF EXISTS `alertas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alertas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tipo` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `mensaje` text COLLATE utf8mb4_general_ci,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertas`
--

LOCK TABLES `alertas` WRITE;
/*!40000 ALTER TABLE `alertas` DISABLE KEYS */;
/*!40000 ALTER TABLE `alertas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipos`
--

DROP TABLE IF EXISTS `equipos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `id_tipo` int NOT NULL,
  `marca` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `modelo` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `numero_serie` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `categoria` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `estado` enum('Operativo','En mantenimiento','Con falla','Fuera de servicio') COLLATE utf8mb4_general_ci DEFAULT 'Operativo',
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_tipo` (`id_tipo`),
  CONSTRAINT `equipos_ibfk_1` FOREIGN KEY (`id_tipo`) REFERENCES `tipos_equipo` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipos`
--

LOCK TABLES `equipos` WRITE;
/*!40000 ALTER TABLE `equipos` DISABLE KEYS */;
INSERT INTO `equipos` VALUES (1,'PC-01 ',1,'HP','ProDesk 400','SN001','Hardware','Operativo','2025-11-12 15:41:01'),(2,'PC-02',1,'HP','ProDesk 400','SN002','Hardware','Operativo','2025-11-12 15:41:01'),(4,'Switch-01',2,'Cisco','SG95-08','SW001','Red','Operativo','2025-11-12 15:41:01'),(5,'Switch-02',2,'TP-Link','TL-SG1008D','SW002','Red','Operativo','2025-11-12 15:41:01'),(6,'Proyector-01',3,'Epson','X100','PR001','Periférico','Operativo','2025-11-12 15:41:01'),(7,'Cable Cat6 Azul',4,'Belden','Cat6','CB001','Infraestructura','Operativo','2025-11-12 15:41:01'),(35,'PC-03',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(36,'PC-04',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(37,'PC-05',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(38,'PC-06',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(39,'PC-07',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(40,'PC-08',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(41,'PC-09',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(42,'PC-10',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(43,'PC-11',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(44,'PC-12',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(45,'PC-13',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(46,'PC-14',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(47,'PC-15',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(48,'PC-16',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(49,'PC-17',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(50,'PC-18',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(51,'PC-19',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(52,'PC-20',1,'HP','ProDesk 400',NULL,'Computadora','Operativo','2025-11-18 21:28:45'),(53,'Pantalla LED 65\"',6,'Samsung','QN65Q80A',NULL,'Audio/Video','Operativo','2025-11-18 21:28:45'),(54,'Barra de Sonido',10,'LG','SN6Y',NULL,'Audio/Video','Operativo','2025-11-18 21:28:45'),(55,'Proyector Epson',3,'Epson','PowerLite X49',NULL,'Proyección','Operativo','2025-11-18 21:28:45'),(56,'Canaleta Metálica Principal',7,'Panduit','Tipo F5',NULL,'Cableado','Operativo','2025-11-18 21:28:45'),(57,'Canaleta PVC Perimetral',7,'Bticino','SL-50',NULL,'Cableado','Operativo','2025-11-18 21:28:45'),(58,'Switch de Red 24 Puertos',2,'TP-Link','TL-SG1024',NULL,'Red','Operativo','2025-11-18 21:28:45'),(59,'Router Principal',8,'Cisco','RV340',NULL,'Red','Operativo','2025-11-18 21:28:45'),(60,'No Break 1500VA',9,'APC','BX1500M',NULL,'Energía','Operativo','2025-11-18 21:28:45'),(61,'Regleta de 8 Entradas',9,'Tripp Lite','PS4816',NULL,'Energía','Operativo','2025-11-18 21:28:45');
/*!40000 ALTER TABLE `equipos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fallas`
--

DROP TABLE IF EXISTS `fallas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fallas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_equipo` int NOT NULL,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `fecha_reporte` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_equipo` (`id_equipo`),
  CONSTRAINT `fallas_ibfk_1` FOREIGN KEY (`id_equipo`) REFERENCES `equipos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fallas`
--

LOCK TABLES `fallas` WRITE;
/*!40000 ALTER TABLE `fallas` DISABLE KEYS */;
INSERT INTO `fallas` VALUES (1,1,'No inicia, prende pero solo se esuchan pitidos','2025-11-12 16:12:15'),(2,2,'No enciende','2025-11-12 18:46:06'),(3,1,'No enciende','2025-11-12 18:52:03'),(4,1,'No enciende','2025-11-12 19:02:56'),(5,2,'Falla','2025-11-12 19:14:47'),(6,4,'Falla','2025-11-12 19:16:52'),(7,6,'no enciende','2025-11-17 05:08:25'),(8,4,'no funciona','2025-11-18 19:05:29');
/*!40000 ALTER TABLE `fallas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial`
--

DROP TABLE IF EXISTS `historial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_tarea` int NOT NULL,
  `fecha_cierre` datetime DEFAULT CURRENT_TIMESTAMP,
  `descripcion` text COLLATE utf8mb4_general_ci,
  `repuesto_usado` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_tarea` (`id_tarea`),
  CONSTRAINT `historial_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `tareas` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial`
--

LOCK TABLES `historial` WRITE;
/*!40000 ALTER TABLE `historial` DISABLE KEYS */;
INSERT INTO `historial` VALUES (1,1,'2025-11-12 16:39:21','Tarea completada correctamente para equipo ID 1',NULL),(2,2,'2025-11-12 18:51:49','Tarea completada correctamente para equipo ID 2',NULL),(3,3,'2025-11-12 18:52:23','Tarea completada correctamente para equipo ID 1',NULL),(4,4,'2025-11-12 19:14:38','Tarea completada correctamente para equipo ID 1',NULL),(5,6,'2025-11-16 19:35:05','Tarea completada correctamente para equipo ID 4',NULL),(6,5,'2025-11-16 19:35:11','Tarea completada correctamente para equipo ID 2',NULL),(7,5,'2025-11-16 21:23:35','Tarea completada para equipo ID 2',NULL),(8,6,'2025-11-18 19:23:11','Tarea completada para equipo ID 4',NULL);
/*!40000 ALTER TABLE `historial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `repuestos`
--

DROP TABLE IF EXISTS `repuestos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `repuestos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `tipo` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cantidad` int DEFAULT '0',
  `stock_minimo` int DEFAULT '1',
  `fecha_actualizacion` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `repuestos`
--

LOCK TABLES `repuestos` WRITE;
/*!40000 ALTER TABLE `repuestos` DISABLE KEYS */;
INSERT INTO `repuestos` VALUES (1,'Fuente de poder 500W','Componente PC',5,2,'2025-11-12 15:41:01'),(2,'Cable HDMI 2m','Conector',10,3,'2025-11-12 15:41:01'),(3,'Ventilador CPU','Componente PC',8,2,'2025-11-12 15:41:01'),(4,'Switch 8 puertos TP-Link','Equipo de red',2,1,'2025-11-12 15:41:01'),(6,'Disco duro 1TB','Componente PC',10,2,'2025-11-16 20:32:49'),(7,'Módulo RAM DDR4 8GB','Memoria PC',15,5,'2025-11-18 21:28:45'),(8,'Tarjeta de Red Gigabit PCIe','Componente PC',3,1,'2025-11-18 21:28:45'),(9,'Teclado USB estándar','Periférico',10,4,'2025-11-18 21:28:45'),(10,'Mouse USB óptico','Periférico',12,4,'2025-11-18 21:28:45'),(11,'Monitor 24 pulgadas LED','Pantalla',0,1,'2025-11-19 03:34:36'),(12,'Conector RJ45 Cat6','Cableado de Red',50,10,'2025-11-18 21:28:45'),(13,'Patch Cord Cat6 1m','Cableado de Red',30,10,'2025-11-18 21:28:45'),(14,'Patch Cord Cat6 3m','Cableado de Red',25,10,'2025-11-18 21:28:45'),(15,'Cable HDMI 2.0 2m','Audio/Video',20,5,'2025-11-18 21:28:45'),(16,'Cable VGA 1.5m','Audio/Video',10,3,'2025-11-18 21:28:45'),(17,'Adaptador HDMI a VGA','Audio/Video',8,2,'2025-11-18 21:28:45'),(18,'Cable de alimentación C13','Conector Eléctrico',25,5,'2025-11-18 21:28:45'),(19,'Extensión eléctrica 3m','Energía',15,5,'2025-11-18 21:28:45'),(20,'Batería UPS 12V/7Ah','Energía',8,2,'2025-11-18 21:28:45'),(21,'Control Remoto Pantalla','Audiovisual',4,2,'2025-11-18 21:28:45'),(22,'Soporte de Pared Universal TV 65\"','Audiovisual',2,1,'2025-11-18 21:28:45'),(23,'Tapa Canaleta 50mm (Metro)','Cableado',10,5,'2025-11-18 21:28:45'),(24,'Codos y Derivaciones Canaleta PVC','Cableado',15,5,'2025-11-18 21:28:45');
/*!40000 ALTER TABLE `repuestos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tareas`
--

DROP TABLE IF EXISTS `tareas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tareas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_falla` int NOT NULL,
  `id_tecnico` int DEFAULT NULL,
  `prioridad` enum('Alta','Media','Baja') COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP,
  `fecha_limite` datetime DEFAULT NULL,
  `estado` enum('Pendiente','En proceso','Completada') COLLATE utf8mb4_general_ci DEFAULT 'Pendiente',
  `observaciones` text COLLATE utf8mb4_general_ci,
  PRIMARY KEY (`id`),
  KEY `id_falla` (`id_falla`),
  KEY `id_tecnico` (`id_tecnico`),
  CONSTRAINT `tareas_ibfk_1` FOREIGN KEY (`id_falla`) REFERENCES `fallas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `tareas_ibfk_2` FOREIGN KEY (`id_tecnico`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tareas`
--

LOCK TABLES `tareas` WRITE;
/*!40000 ALTER TABLE `tareas` DISABLE KEYS */;
INSERT INTO `tareas` VALUES (1,1,2,'Media','2025-11-12 16:12:15','2025-11-26 16:12:16','Completada',''),(2,2,2,'Media','2025-11-12 18:46:06','2025-11-26 18:46:06','Completada',''),(3,3,2,'Media','2025-11-12 18:52:03','2025-11-26 18:52:03','Completada',''),(4,4,2,'Alta','2025-11-12 19:02:56','2025-11-14 19:02:57','Completada',''),(5,5,2,'Alta','2025-11-12 19:14:47','2025-11-14 19:14:48','Pendiente',''),(6,6,2,'Alta','2025-11-12 19:16:52','2025-11-14 19:16:53','Completada',''),(7,7,2,'Alta','2025-11-17 05:08:25','2025-11-19 05:08:26','Pendiente',NULL),(8,8,3,'Alta','2025-11-18 19:05:29','2025-11-20 19:05:30','Pendiente',NULL);
/*!40000 ALTER TABLE `tareas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_equipo`
--

DROP TABLE IF EXISTS `tipos_equipo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_equipo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_equipo`
--

LOCK TABLES `tipos_equipo` WRITE;
/*!40000 ALTER TABLE `tipos_equipo` DISABLE KEYS */;
INSERT INTO `tipos_equipo` VALUES (1,'Computadora','Equipo de cómputo personal o de escritorio'),(2,'Switch','Equipo de red para conexión de PCs'),(3,'Proyector','Dispositivo de proyección'),(4,'Cable UTP','Infraestructura de red y energía'),(5,'Impresora','Equipo periférico de impresión'),(6,'Pantalla / Audio-Video','Dispositivos de visualización y salida audiovisual'),(7,'Cableado','Canaletas, accesorios y materiales de cableado'),(8,'Router','Equipo de enrutamiento y administración de red'),(9,'Energía','Sistemas de respaldo y distribución eléctrica'),(10,'Audio','Barras de sonido y dispositivos de salida de audio');
/*!40000 ALTER TABLE `tipos_equipo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `usuario` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `contrasena` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `rol` enum('Administrador','Técnico') COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_registro` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Administrador General','admin','admin123','Administrador','2025-11-12 15:41:01'),(2,'Técnico Juan','juan','tecnico123','Técnico','2025-11-12 15:41:01'),(3,'Técnico 2','tecnico2','1234','Técnico','2025-11-18 18:55:09'),(4,'Técnico 3','tecnico3','1234','Técnico','2025-11-18 18:55:09');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-19  5:17:00
