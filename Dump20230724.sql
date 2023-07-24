CREATE DATABASE  IF NOT EXISTS `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `test`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: test
-- ------------------------------------------------------
-- Server version	8.0.34

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
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (1,'Pizza mediana','2023-07-22 14:32:28','2023-07-22 14:32:28',1),(2,'Pizza familiar','2023-07-22 14:32:28','2023-07-22 14:32:28',1),(3,'Bebestibles','2023-07-22 14:32:28','2023-07-22 14:32:28',1),(4,'Comida rápida','2023-07-22 14:32:28','2023-07-22 14:32:28',1),(5,'Sandwiches','2023-07-22 14:32:28','2023-07-22 14:32:28',1);
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingrediente`
--

DROP TABLE IF EXISTS `ingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingrediente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `cantidad` int NOT NULL,
  `precio` int NOT NULL,
  `alerta_stock` int NOT NULL,
  `extra_mediana` int NOT NULL,
  `extra_familiar` int NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `unidadmedida_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `unidadmedida_id` (`unidadmedida_id`),
  CONSTRAINT `ingrediente_ibfk_1` FOREIGN KEY (`unidadmedida_id`) REFERENCES `unidadmedida` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingrediente`
--

LOCK TABLES `ingrediente` WRITE;
/*!40000 ALTER TABLE `ingrediente` DISABLE KEYS */;
INSERT INTO `ingrediente` VALUES (1,'Tocino',50000,1000,100,1000,1000,1,'2023-07-20 21:03:49','2023-07-20 21:04:02',1),(2,'Salame',50000,1000,100,10,10,1,'2023-07-20 21:04:29','2023-07-20 21:05:39',4),(3,'Pepperoni',50000,1000,100,10,10,1,'2023-07-20 21:05:29','2023-07-20 21:05:36',3),(4,'Atún',50000,1000,10000,100,100,1,'2023-07-20 21:06:09','2023-07-20 21:10:44',1),(5,'Jamón',50000,1000,100,100,100,1,'2023-07-20 21:06:26','2023-07-20 21:06:26',1),(6,'Chorizo',50000,1000,100,100,100,1,'2023-07-20 21:06:37','2023-07-20 21:06:37',1),(7,'Salchicha',50000,1000,100,100,100,1,'2023-07-20 21:06:50','2023-07-20 21:06:50',1),(8,'Pollo',50000,1000,100,100,100,1,'2023-07-20 21:07:30','2023-07-20 21:07:30',1),(9,'Carne',50000,1000,100,100,100,1,'2023-07-20 21:07:39','2023-07-20 21:07:39',1),(10,'Camarón',50000,1000,100,100,100,1,'2023-07-20 21:07:49','2023-07-20 21:07:49',1),(11,'Piña',50000,1000,100,100,100,1,'2023-07-20 21:10:22','2023-07-20 21:10:22',1),(12,'Jamón Serrano',50000,1000,100,100,100,1,'2023-07-20 21:10:32','2023-07-20 21:10:32',1),(13,'Cebolla morada',50000,1000,10000,100,100,1,'2023-07-20 21:11:20','2023-07-20 21:11:20',1),(14,'Choclo',50000,1000,10000,100,100,1,'2023-07-20 21:12:09','2023-07-20 21:12:09',1),(15,'Jalapeño',50000,1000,10000,100,100,1,'2023-07-20 21:12:27','2023-07-20 21:12:27',1),(16,'Palmito',50000,1000,1000,100,100,1,'2023-07-20 21:12:49','2023-07-20 21:12:49',1),(17,'Espárragos',50000,1000,10000,100,100,1,'2023-07-20 21:13:11','2023-07-20 21:13:11',1),(18,'Alcaparras',50000,1000,10000,100,100,1,'2023-07-20 21:13:23','2023-07-20 21:13:23',1),(19,'Champiñón',50000,1000,10000,100,100,1,'2023-07-20 21:15:50','2023-07-20 21:15:50',1),(20,'Aceituna',50000,1000,10000,100,100,1,'2023-07-20 21:16:03','2023-07-20 21:16:03',1),(21,'Albahaca',50000,1000,10000,100,100,1,'2023-07-20 21:16:24','2023-07-20 21:16:38',1),(22,'Tomate natural',50000,1000,10000,100,100,1,'2023-07-20 21:19:36','2023-07-20 21:19:36',1),(23,'Pimentón',50000,1000,10000,100,100,1,'2023-07-20 21:19:45','2023-07-20 21:19:45',1),(24,'Masa',40000,0,10000,0,0,1,'2023-07-22 13:48:52','2023-07-23 22:15:21',1),(25,'test',1,1000,1,1,1,0,'2023-07-22 18:51:44','2023-07-22 18:51:44',1),(26,'Salsa de tomate',59000,0,10000,0,0,1,'2023-07-22 21:29:35','2023-07-22 21:29:35',1),(27,'Queso despunte',60000,1000,10000,100,100,1,'2023-07-22 21:37:16','2023-07-22 21:37:16',1);
/*!40000 ALTER TABLE `ingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metodopago`
--

DROP TABLE IF EXISTS `metodopago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metodopago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metodopago`
--

LOCK TABLES `metodopago` WRITE;
/*!40000 ALTER TABLE `metodopago` DISABLE KEYS */;
INSERT INTO `metodopago` VALUES (1,'Efectivo',1),(2,'Transferencia',1),(3,'Tarjeta de crédito',1),(4,'Tarjeta de débito',1),(5,'Cheque',0);
/*!40000 ALTER TABLE `metodopago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int NOT NULL AUTO_INCREMENT,
  `persona_id` int DEFAULT NULL,
  `estado_id` int NOT NULL,
  `metodopago_id` int DEFAULT NULL,
  `delivery` tinyint(1) NOT NULL,
  `nombre_cliente` varchar(50) NOT NULL,
  `notificacion` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_id` (`persona_id`),
  KEY `estado_id` (`estado_id`),
  KEY `metodopago_id` (`metodopago_id`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`estado_id`) REFERENCES `pedido_estado` (`id`),
  CONSTRAINT `pedido_ibfk_3` FOREIGN KEY (`metodopago_id`) REFERENCES `metodopago` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,1,1,3,1,'Test',0,'2023-07-22 18:09:49','2023-07-22 18:09:49');
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_detalle`
--

DROP TABLE IF EXISTS `pedido_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `pedido_detalle_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`),
  CONSTRAINT `pedido_detalle_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_detalle`
--

LOCK TABLES `pedido_detalle` WRITE;
/*!40000 ALTER TABLE `pedido_detalle` DISABLE KEYS */;
INSERT INTO `pedido_detalle` VALUES (1,1,6,2,'2023-07-22 18:59:31','2023-07-22 18:59:31');
/*!40000 ALTER TABLE `pedido_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_detalle_ingrediente`
--

DROP TABLE IF EXISTS `pedido_detalle_ingrediente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalle_ingrediente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_detalle_id` int DEFAULT NULL,
  `ingrediente_id` int DEFAULT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_detalle_id` (`pedido_detalle_id`),
  KEY `ingrediente_id` (`ingrediente_id`),
  CONSTRAINT `pedido_detalle_ingrediente_ibfk_1` FOREIGN KEY (`pedido_detalle_id`) REFERENCES `pedido_detalle` (`id`),
  CONSTRAINT `pedido_detalle_ingrediente_ibfk_2` FOREIGN KEY (`ingrediente_id`) REFERENCES `ingrediente` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_detalle_ingrediente`
--

LOCK TABLES `pedido_detalle_ingrediente` WRITE;
/*!40000 ALTER TABLE `pedido_detalle_ingrediente` DISABLE KEYS */;
/*!40000 ALTER TABLE `pedido_detalle_ingrediente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_estado`
--

DROP TABLE IF EXISTS `pedido_estado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_estado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_estado`
--

LOCK TABLES `pedido_estado` WRITE;
/*!40000 ALTER TABLE `pedido_estado` DISABLE KEYS */;
INSERT INTO `pedido_estado` VALUES (3,'Anulado'),(1,'En proceso'),(2,'Finalizado');
/*!40000 ALTER TABLE `pedido_estado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona`
--

DROP TABLE IF EXISTS `persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persona` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int DEFAULT NULL,
  `rut` varchar(12) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido_paterno` varchar(30) NOT NULL,
  `apellido_materno` varchar(30) NOT NULL,
  `celular` varchar(12) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rut` (`rut`),
  UNIQUE KEY `celular` (`celular`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `persona_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona`
--

LOCK TABLES `persona` WRITE;
/*!40000 ALTER TABLE `persona` DISABLE KEYS */;
INSERT INTO `persona` VALUES (1,1,'1','Lorem','Ipsum','','','2023-07-22 14:32:28','2023-07-22 14:32:28',1);
/*!40000 ALTER TABLE `persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `imagen` varchar(255) DEFAULT NULL,
  `nombre` varchar(30) NOT NULL,
  `descripcion` text,
  `precio` int NOT NULL,
  `stock` int DEFAULT NULL,
  `alerta_stock` int DEFAULT NULL,
  `tiene_receta` tinyint(1) NOT NULL,
  `categoria_id` int DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `categoria_id` (`categoria_id`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (1,'/productos/Kebab.webp','Kebab','RICA MASA HECHA POR NOSOTROS CON UN RELLENO DE CARNE, POLLO, LECHUGA, TOMATE, CEBOLLA MORADA Y UNA MAYONESA CON AJO.',6000,0,100,1,5,'2023-07-20 22:14:32','2023-07-21 01:31:56',1),(2,'/productos/Palitos_de_ajo.webp','Palitos de ajo','MASA AL HORNO ESTILO MARGARITA, 8 UNIDADES.',4500,0,100,1,4,'2023-07-20 22:21:57','2023-07-21 01:32:05',1),(3,'/productos/Aros_de_cebolla.webp','Aros de cebolla','CEBOLLAS CORTADAS TRANSVERSALMENTE PARA QUE SE PUEDA COCINAR EN FORMA DE ANILLO, FRITOS EN ACEITE 10 UNIDADES.',3000,0,100,1,4,'2023-07-20 22:27:18','2023-07-21 01:31:51',1),(4,'/productos/Papas_fritas.webp','Papas fritas','PAPAS FRITAS CON QUESO CHEDDAR MÁS TOCINO CROCANTE MÁS TOPPING DE CEBOLLIN',6500,0,100,1,4,'2023-07-20 22:30:59','2023-07-21 01:32:12',1),(5,'/productos/Salchipapa.webp','Salchipapa','PAPAS FRITAS MÁS SALCHICHAS.',5990,0,100,1,4,'2023-07-20 22:33:37','2023-07-21 01:32:20',1),(6,'/productos/Coca-Cola_Original_1.5_L.webp','Coca-Cola Original 1.5 L',NULL,2500,29,100,0,3,'2023-07-21 01:19:13','2023-07-21 13:54:24',1),(7,'/productos/Fanta_en_lata_350_ml.webp','Fanta en lata 350 ml',NULL,1600,30,100,0,3,'2023-07-21 14:43:30','2023-07-21 15:06:20',1),(8,'/productos/Sprite_Original_1.5_L.webp','Sprite Original 1.5 L',NULL,2500,30,100,0,3,'2023-07-21 14:59:37','2023-07-21 14:56:04',1),(9,'/productos/Coca-Cola_en_Lata_350_ml.webp','Coca-Cola en Lata 350 ml',NULL,1600,30,100,0,3,'2023-07-21 15:01:46','2023-07-21 15:07:28',1),(10,'/productos/Sprite_normal_en_lata_1.5_L.webp','Sprite normal en lata 1.5 L',NULL,1600,30,100,0,3,'2023-07-21 15:03:01','2023-07-21 14:56:04',1),(11,'/productos/Fanta_Original_1.5_L.webp','Fanta Original 1.5 L',NULL,2500,30,100,0,3,'2023-07-21 15:04:20','2023-07-21 15:05:59',1),(12,'/productos/Tropical.webp','Tropical','Queso, jamón, piña',8300,NULL,100,1,1,'2023-07-21 15:23:49','2023-07-21 15:22:57',1),(13,'/productos/Bella_Napoli.webp','Bella Napoli','Queso, jamón tomate',8300,NULL,100,1,1,'2023-07-21 15:26:24','2023-07-21 15:22:57',1),(14,'/productos/Siciliana.webp','Siciliana','Queso, carne, cebolla morada',8700,NULL,100,1,1,'2023-07-21 15:28:29','2023-07-21 15:22:57',1),(15,'/productos/Caprichosa.webp','Caprichosa','Queso, jamón, champiñon',8500,NULL,100,1,1,'2023-07-21 15:29:44','2023-07-21 15:22:57',1),(16,'/productos/Romana.webp','Romana','Queso, pepperoni, pimentón',8800,NULL,100,1,1,'2023-07-21 15:32:55','2023-07-21 15:22:57',1),(17,'/productos/Toscana.webp','Toscana','Queso, pollo, choclo',8800,NULL,100,1,1,'2023-07-21 15:37:24','2023-07-21 15:22:57',1),(18,'/productos/Quatro_stagioni.webp','Quatro stagioni','Queso, jamón, champiñón, aceituna, palmitos',10400,NULL,100,1,1,'2023-07-21 15:40:14','2023-07-21 15:22:57',1),(19,'/productos/Cosa_nostra.webp','Cosa nostra','Queso, carne, tocino',8700,NULL,100,1,1,'2023-07-21 15:43:31','2023-07-21 15:22:57',1),(20,'/productos/Arrabiata.webp','Arrabiata','Queso, salame, choclo, jalapeño',8400,NULL,100,1,1,'2023-07-21 15:46:05','2023-07-21 15:22:57',1),(21,'/productos/Marina.webp','Marina','Queso, atún, cebolla morada, alcaparra',9500,NULL,100,1,1,'2023-07-21 15:49:43','2023-07-21 15:22:57',1),(22,'/productos/Mamma_mia.webp','Mamma mia','Queso, chorizo, carne, pimentón',9800,0,100,1,1,'2023-07-21 15:52:01','2023-07-22 12:17:31',1),(23,'/productos/Fratelli.webp','Fratelli','Queso, carne, pollo, tocino, salame',10800,NULL,100,1,1,'2023-07-21 15:53:27','2023-07-21 15:22:57',1),(24,'/productos/Vegetariana.webp','Vegetariana','Queso con tres vegetales a elección',8400,NULL,100,1,1,'2023-07-21 15:58:20','2023-07-21 15:22:57',1),(25,'/productos/Amore_mio.webp','Amore mio','Queso, jamón serrano, albahaca',12300,NULL,100,1,2,'2023-07-21 16:00:07','2023-07-21 15:22:57',1),(26,'/productos/Lucia.webp','Lucia','Queso, jamón, champiñon, camarón',9900,NULL,100,1,1,'2023-07-21 16:02:33','2023-07-21 15:22:57',1),(27,'/productos/Marinera_especial.webp','Marinera especial','Queso, camarón más dos vegetales a elección',9500,NULL,100,1,1,'2023-07-21 16:05:06','2023-07-21 15:22:57',1),(28,'/productos/Tropical.webp','Tropical','Queso, jamón, piña',10300,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(29,'/productos/Bella_Napoli.webp','Bella Napoli','Queso, jamón tomate',10300,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(30,'/productos/Siciliana.webp','Siciliana','Queso, carne, cebolla morada',10700,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(31,'/productos/Caprichosa.webp','Caprichosa','Queso, jamón, champiñon',10500,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(32,'/productos/Romana.webp','Romana','Queso, pepperoni, pimentón',10800,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(33,'/productos/Toscana.webp','Toscana','Queso, pollo, choclo',10800,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(34,'/productos/Quatro_stagioni.webp','Quatro stagioni','Queso, jamón, champiñón, aceituna, palmitos',12500,0,50,1,2,'2023-07-22 21:13:17','2023-07-22 21:17:18',1),(35,'/productos/Cosa_nostra.webp','Cosa nostra','Queso, carne, tocino',10800,0,50,1,2,'2023-07-22 21:13:17','2023-07-22 21:17:44',1),(36,'/productos/Arrabiata.webp','Arrabiata','Queso, salame, choclo, jalapeño',10400,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(37,'/productos/Marina.webp','Marina','Queso, atún, cebolla morada, alcaparra',11500,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(38,'/productos/Mamma_mia.webp','Mamma mia','Queso, chorizo, carne, pimentón',11900,0,50,1,2,'2023-07-22 21:13:17','2023-07-22 21:18:12',1),(39,'/productos/Fratelli.webp','Fratelli','Queso, carne, pollo, tocino, salame',12900,0,50,1,2,'2023-07-22 21:13:17','2023-07-22 21:19:13',1),(40,'/productos/Vegetariana.webp','Vegetariana','Queso con tres vegetales a elección',10400,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(41,'/productos/Lucia.webp','Lucia','Queso, jamón, champiñon, camarón',11900,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1),(42,'/productos/Marinera_especial.webp','Marinera especial','Queso, camarón más dos vegetales a elección',11500,NULL,NULL,1,2,'2023-07-22 21:13:17','2023-07-22 21:13:17',1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
INSERT INTO `receta` VALUES (1,1),(2,2),(3,3),(4,4),(5,5),(12,12),(13,13),(14,14),(15,15),(16,16),(17,17),(18,18),(19,19),(20,20),(21,21),(22,22),(23,23),(24,24),(25,25),(26,26),(27,27),(28,28),(29,29),(30,30),(31,31),(32,32),(33,33),(34,34),(35,35),(36,36),(37,37),(38,38),(39,39),(40,40),(41,41),(42,42);
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta_detalle`
--

DROP TABLE IF EXISTS `receta_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta_detalle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `receta_id` int DEFAULT NULL,
  `ingrediente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  KEY `ingrediente_id` (`ingrediente_id`),
  CONSTRAINT `receta_detalle_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `receta` (`id`),
  CONSTRAINT `receta_detalle_ibfk_2` FOREIGN KEY (`ingrediente_id`) REFERENCES `ingrediente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta_detalle`
--

LOCK TABLES `receta_detalle` WRITE;
/*!40000 ALTER TABLE `receta_detalle` DISABLE KEYS */;
INSERT INTO `receta_detalle` VALUES (1,99,12,26),(2,99,13,26),(3,99,14,26),(4,99,15,26),(5,99,16,26),(6,99,17,26),(7,99,18,26),(8,99,19,26),(9,99,20,26),(10,99,21,26),(11,99,22,26),(12,99,23,26),(13,99,24,26),(14,99,26,26),(15,99,27,26),(16,289,12,24),(17,289,13,24),(18,289,14,24),(19,289,15,24),(20,289,16,24),(21,289,17,24),(22,289,18,24),(23,289,19,24),(24,289,20,24),(25,289,21,24),(26,289,22,24),(27,289,23,24),(28,289,24,24),(29,289,26,24),(30,289,27,24),(31,120,12,27),(32,120,13,27),(33,120,14,27),(34,120,15,27),(35,120,16,27),(36,120,17,27),(37,120,18,27),(38,120,19,27),(39,120,20,27),(40,120,21,27),(41,120,22,27),(42,120,23,27),(43,120,24,27),(44,120,26,27),(45,120,27,27);
/*!40000 ALTER TABLE `receta_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Administrador',1,'2023-07-22 14:32:28','2023-07-22 14:32:28'),(2,'Personal de caja',1,'2023-07-22 14:32:28','2023-07-22 14:32:28'),(3,'Empleado',1,'2023-07-22 14:32:28','2023-07-22 14:32:28');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidadmedida`
--

DROP TABLE IF EXISTS `unidadmedida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidadmedida` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidadmedida`
--

LOCK TABLES `unidadmedida` WRITE;
/*!40000 ALTER TABLE `unidadmedida` DISABLE KEYS */;
INSERT INTO `unidadmedida` VALUES (1,'gr',1,'2023-07-22 14:32:28','2023-07-22 14:32:28'),(2,'ml',1,'2023-07-22 14:32:28','2023-07-22 14:32:28'),(3,'Unidad(es)',1,'2023-07-22 14:32:28','2023-07-22 14:32:28'),(4,'Rodajas',1,'2023-07-20 21:04:36','2023-07-20 21:04:36');
/*!40000 ALTER TABLE `unidadmedida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(30) NOT NULL,
  `correo` varchar(30) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol_id` int DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  UNIQUE KEY `correo` (`correo`),
  KEY `rol_id` (`rol_id`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'admin','admin@pizzeriafratelli.cl','$2b$12$NJ/4JWBugLVU0pJjIfMcne9NqDk/.zLpotKLUAqXUes4FG7GZ/..O',1,'2023-07-22 14:32:28','2023-07-22 14:32:28',1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int DEFAULT NULL,
  `total` int DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pedido_id` (`pedido_id`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-24 11:14:07
