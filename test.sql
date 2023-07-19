-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 19, 2023 at 05:19 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `categoria`
--

CREATE TABLE `categoria` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `categoria`
--

INSERT INTO `categoria` (`id`, `nombre`, `fecha_creacion`, `ultima_modificacion`, `activo`) VALUES
(1, 'Pizza mediana', '2023-06-06 14:38:02', '2023-06-06 14:38:02', 1),
(2, 'Eliminado', '2023-06-06 14:38:02', '2023-06-06 14:38:02', 0),
(3, 'Bebestible', '2023-06-09 12:11:26', '2023-06-20 11:48:29', 1),
(4, 'Ensalada', '2023-06-09 12:56:40', '2023-06-20 11:48:34', 1),
(5, 'Pizza familiar', '2023-06-13 21:34:26', '2023-06-13 21:34:26', 1),
(6, 'Postre', '2023-06-14 13:37:57', '2023-06-20 11:48:37', 1),
(7, 'Bebestibles', '2023-06-20 11:58:48', '2023-06-20 11:58:48', 1);

-- --------------------------------------------------------

--
-- Table structure for table `ingrediente`
--

CREATE TABLE `ingrediente` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `unidadmedida_id` int(11) DEFAULT NULL,
  `precio` int(11) NOT NULL DEFAULT 1000,
  `alerta_stock` int(11) NOT NULL DEFAULT 1000,
  `extra_mediana` int(11) NOT NULL DEFAULT 100,
  `extra_familiar` int(11) NOT NULL DEFAULT 100
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `ingrediente`
--

INSERT INTO `ingrediente` (`id`, `nombre`, `cantidad`, `activo`, `fecha_creacion`, `ultima_modificacion`, `unidadmedida_id`, `precio`, `alerta_stock`, `extra_mediana`, `extra_familiar`) VALUES
(1, 'Salsa de tomate', 601095, 1, '2023-06-06 14:41:38', '2023-07-14 17:12:25', 1, 0, 1000, 100, 150),
(2, 'Bolas de masa', 93, 1, '2023-06-09 12:12:25', '2023-07-18 22:04:11', 3, 0, 100, 100, 150),
(3, 'Queso Cheddar', 78649, 1, '2023-06-09 12:13:19', '2023-07-14 17:12:42', 1, 1500, 1000, 100, 150),
(4, 'Queso Mozzarella', 17600, 1, '2023-06-09 12:13:29', '2023-07-14 17:12:46', 1, 1500, 1000, 100, 150),
(5, 'Orégano', 61759, 1, '2023-06-09 12:13:59', '2023-06-09 12:13:59', 1, 1000, 1000, 100, 150),
(6, 'Tomate picado', 51573, 1, '2023-06-09 12:15:52', '2023-07-14 17:12:37', 1, 0, 1000, 100, 150),
(7, 'Jamón', 887995, 1, '2023-06-09 12:16:19', '2023-06-09 12:16:36', 1, 1000, 1000, 100, 150),
(8, 'Camarón', 1800, 1, '2023-06-20 18:54:24', '2023-06-20 18:54:24', 3, 1000, 1000, 100, 150),
(9, 'Aceituna', 52, 1, '2023-06-20 18:54:47', '2023-07-15 23:03:59', 3, 1000, 100, 10, 15),
(10, 'Piña', 349900, 1, '2023-06-20 18:55:15', '2023-06-20 18:55:31', 1, 1000, 1000, 100, 150),
(11, 'Tocino', 50000, 1, '2023-06-20 18:55:43', '2023-06-20 18:55:43', 1, 1000, 1000, 100, 150),
(12, 'Choclo', 70000, 1, '2023-06-20 18:56:33', '2023-06-20 18:56:33', 1, 1000, 1000, 100, 150),
(13, 'Cebolla morada', 601000, 1, '2023-06-20 18:56:54', '2023-06-20 18:56:54', 1, 1000, 1000, 100, 150),
(14, 'Salsa de tomate', 0, 0, '2023-06-20 18:57:08', '2023-06-20 18:57:08', 1, 1000, 1000, 100, 150),
(15, 's', 0, 0, '2023-06-28 01:50:15', '2023-06-28 01:50:15', 1, 1000, 1000, 100, 150);

-- --------------------------------------------------------

--
-- Table structure for table `metodopago`
--

CREATE TABLE `metodopago` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `metodopago`
--

INSERT INTO `metodopago` (`id`, `nombre`, `activo`) VALUES
(1, 'Efectivo', 1),
(2, 'Transferencia', 1),
(3, 'Tarjeta de crédito', 1),
(4, 'Tarjeta de débito', 1),
(5, 'Cheque', 0);

-- --------------------------------------------------------

--
-- Table structure for table `pedido`
--

CREATE TABLE `pedido` (
  `id` int(11) NOT NULL,
  `persona_id` int(11) DEFAULT NULL,
  `estado_id` int(11) NOT NULL,
  `metodopago_id` int(11) DEFAULT NULL,
  `delivery` tinyint(1) NOT NULL,
  `nombre_cliente` varchar(50) NOT NULL,
  `notificacion` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pedido`
--

INSERT INTO `pedido` (`id`, `persona_id`, `estado_id`, `metodopago_id`, `delivery`, `nombre_cliente`, `notificacion`, `fecha_creacion`, `ultima_modificacion`) VALUES
(1, 2, 2, 3, 1, 'Luis', 0, '2023-07-17 17:11:58', '2023-07-17 17:11:58'),
(2, 2, 2, 2, 0, 'Mario', 0, '2023-07-17 19:24:30', '2023-07-17 19:24:30'),
(3, 2, 2, 1, 0, 'Pancho', 0, '2023-07-17 19:34:48', '2023-07-17 19:34:48'),
(4, 2, 2, 4, 0, 'Luis G', 0, '2023-07-18 10:21:49', '2023-07-18 10:21:49'),
(5, 2, 2, 3, 1, 'Jorge', 0, '2023-07-18 14:01:48', '2023-07-18 14:01:48'),
(6, 2, 2, 3, 1, 'Su Jie', 0, '2023-07-18 21:26:09', '2023-07-18 21:26:09'),
(7, 2, 2, NULL, 0, 'No definido', 0, '2023-07-18 21:26:09', '2023-07-18 21:26:09'),
(8, 2, 2, 2, 1, 'Pedro', 0, '2023-07-19 11:17:06', '2023-07-19 11:17:06');

-- --------------------------------------------------------

--
-- Table structure for table `pedido_detalle`
--

CREATE TABLE `pedido_detalle` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) DEFAULT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pedido_detalle`
--

INSERT INTO `pedido_detalle` (`id`, `pedido_id`, `producto_id`, `cantidad`, `fecha_creacion`, `ultima_modificacion`) VALUES
(11, 1, 1, 1, '2023-07-17 21:38:52', '2023-07-17 21:38:52'),
(12, 3, 9, 2, '2023-07-17 21:38:52', '2023-07-17 21:38:52'),
(13, 3, 1, 1, '2023-07-17 21:38:52', '2023-07-17 21:38:52'),
(14, 1, 9, 1, '2023-07-18 09:43:51', '2023-07-18 09:43:51'),
(15, 4, 1, 1, '2023-07-18 10:21:49', '2023-07-18 10:21:49'),
(17, 2, 1, 1, '2023-07-18 17:07:22', '2023-07-18 17:07:22'),
(18, 5, 21, 1, '2023-07-18 17:07:22', '2023-07-18 17:07:22'),
(19, 5, 21, 1, '2023-07-18 17:07:22', '2023-07-18 17:07:22'),
(20, 5, 16, 1, '2023-07-18 17:07:22', '2023-07-18 17:07:22'),
(21, 6, 21, 1, '2023-07-18 21:26:09', '2023-07-18 21:26:09'),
(22, 6, 9, 2, '2023-07-18 21:26:09', '2023-07-18 21:26:09'),
(23, 7, 24, 1, '2023-07-18 22:04:05', '2023-07-18 22:04:05'),
(24, 7, 21, 1, '2023-07-19 11:05:08', '2023-07-19 11:05:08'),
(25, 8, 24, 1, '2023-07-19 11:17:06', '2023-07-19 11:17:06'),
(26, 8, 21, 1, '2023-07-19 11:17:06', '2023-07-19 11:17:06');

-- --------------------------------------------------------

--
-- Table structure for table `pedido_detalle_ingrediente`
--

CREATE TABLE `pedido_detalle_ingrediente` (
  `id` int(11) NOT NULL,
  `pedido_detalle_id` int(11) DEFAULT NULL,
  `ingrediente_id` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pedido_detalle_ingrediente`
--

INSERT INTO `pedido_detalle_ingrediente` (`id`, `pedido_detalle_id`, `ingrediente_id`, `cantidad`) VALUES
(8, 18, 3, 150),
(9, 21, 4, 150),
(10, 26, 3, 150);

-- --------------------------------------------------------

--
-- Table structure for table `pedido_estado`
--

CREATE TABLE `pedido_estado` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pedido_estado`
--

INSERT INTO `pedido_estado` (`id`, `nombre`) VALUES
(3, 'Anulado'),
(1, 'En proceso'),
(2, 'Finalizado');

-- --------------------------------------------------------

--
-- Table structure for table `persona`
--

CREATE TABLE `persona` (
  `id` int(11) NOT NULL,
  `usuario_id` int(11) DEFAULT NULL,
  `rut` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `nombre` varchar(30) NOT NULL,
  `apellido_paterno` varchar(30) NOT NULL,
  `apellido_materno` varchar(30) NOT NULL,
  `celular` varchar(22) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `persona`
--

INSERT INTO `persona` (`id`, `usuario_id`, `rut`, `nombre`, `apellido_paterno`, `apellido_materno`, `celular`, `fecha_creacion`, `ultima_modificacion`, `activo`) VALUES
(1, 1, '20704339-7', 'Luis', 'Gálvez', 'González', '935257777', '2023-06-06 14:04:04', '2023-07-19 11:07:53', 1),
(2, 2, '6753719‑k', 'Juditza', 'Álvarez', 'Ramírez', '9', '2023-06-21 15:02:17', '2023-07-14 17:21:25', 1),
(3, 3, '67537319‑k', 'Mario', 'Lopez', 'González', '345657', '2023-06-26 23:04:01', '2023-07-04 01:26:49', 1);

-- --------------------------------------------------------

--
-- Table structure for table `producto`
--

CREATE TABLE `producto` (
  `id` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `codigo_barra` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` int(11) NOT NULL,
  `stock` int(11) DEFAULT NULL,
  `tiene_receta` tinyint(1) NOT NULL,
  `categoria_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `alerta_stock` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `producto`
--

INSERT INTO `producto` (`id`, `imagen`, `codigo_barra`, `nombre`, `descripcion`, `precio`, `stock`, `tiene_receta`, `categoria_id`, `fecha_creacion`, `ultima_modificacion`, `activo`, `alerta_stock`) VALUES
(1, '/productos/pizzeria-valencia-blasco-ibanez-restaurante-italiano-pizza-la-fratelli.jpg', '53', 'La Fratelli', 'Salsa de tomate, albahaca, champiñones, queso Taleggio, pimiento, cebolla, espinacas, bacon y orégano.', 8800, 0, 1, 1, '2023-06-07 19:56:38', '2023-07-18 13:04:51', 1, 100),
(9, '/productos/DeqpCw5SazLzEFbZq-Bebida-Coca-Cola-sin-azucar-350-ml_1.jpeg', '34', 'Coca-Cola Sin Azucar 350ml', 'Bebida en lata, 350ml', 1400, 96, 0, 3, '2023-06-09 12:42:08', '2023-07-15 23:18:00', 1, 100),
(10, '/productos/pizzeria-valencia-blasco-ibanez-la-fratelli-pizza-caprichosa.jpg', '35', 'Caprichosa', '', 8800, 0, 1, 1, '2023-06-19 21:31:42', '2023-07-18 12:50:08', 1, 90),
(14, NULL, '36', 'Caprichosa', '', 11500, 0, 1, 5, '2023-07-18 12:41:22', '2023-07-18 12:41:45', 0, 90),
(15, NULL, '354', 'Caprichosa', '', 7500, 0, 1, 1, '2023-07-18 12:44:50', '2023-07-18 12:44:40', 0, 90),
(16, '/productos/pizzeria-valencia-blasco-ibanez-restaurante-italiano-pizza-la-fratelli.jpg', '54', 'La Fratelli', 'Salsa de tomate, albahaca, champiñones, queso Taleggio, pimiento, cebolla, espinacas, bacon y orégano.', 11500, 0, 1, 5, '2023-07-18 12:48:38', '2023-07-18 13:04:59', 1, 100),
(17, '/productos/pizzeria-valencia-blasco-ibanez-la-fratelli-pizza-caprichosa.jpg', '37', 'Caprichosa', '', 10800, 0, 1, 5, '2023-07-18 12:50:39', '2023-07-18 12:48:12', 1, 90),
(18, '/productos/pizzeria-valencia-blasco-ibanez-la-fratelli-pizza-tropical.jpg', '1', 'Tropical', 'Queso, Jamón, Piña', 8300, NULL, 1, 1, '2023-07-18 13:04:27', '2023-07-18 12:48:12', 1, 100),
(19, '/productos/pizzeria-valencia-blasco-ibanez-la-fratelli-pizza-tropical.jpg', '2', 'Tropical', 'Queso, Jamón, Piña', 10300, 0, 1, 5, '2023-07-18 13:05:26', '2023-07-18 13:05:34', 1, 100),
(20, '/productos/pizza_napolitana_32625_orig.jpg', '3', 'Bella Napoli', 'Queso, Jamón, Tomate', 8300, NULL, 1, 1, '2023-07-18 13:07:56', '2023-07-18 12:48:12', 1, 100),
(21, '/productos/pizza_napolitana_32625_orig.jpg', '4', 'Bella Napoli', 'Queso, Jamón, Tomate', 10300, 0, 1, 5, '2023-07-18 13:10:16', '2023-07-18 12:48:12', 1, 100),
(22, '/productos/ueq5XmkQudTS2DrtsyYD.jpg', '5', 'Siciliana', 'Queso, Carne, Cebolla Morada', 8700, 0, 1, 1, '2023-07-18 13:12:12', '2023-07-18 12:48:12', 1, 100),
(23, '/productos/ueq5XmkQudTS2DrtsyYD.jpg', '6', 'Siciliana', 'Queso, Carne, Cebolla Morada', 10700, 0, 1, 5, '2023-07-18 13:12:59', '2023-07-18 12:48:12', 1, 100),
(24, '/productos/Bebida-lata-350-ml.webp', '340', 'Sprite 350 ml', 'Bebida en lata, 350ml', 1050, 94, 0, 3, '2023-07-18 21:35:52', '2023-07-18 21:36:19', 1, 100),
(25, '/productos/Bebida-lata-350-ml.webp', '3400', 'Sprite 350 ml', 'Bebida en lata, 350ml', 1050, 960, 0, 3, '2023-07-18 21:38:18', '2023-07-18 21:26:09', 0, 100);

-- --------------------------------------------------------

--
-- Table structure for table `receta`
--

CREATE TABLE `receta` (
  `id` int(11) NOT NULL,
  `producto_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `receta`
--

INSERT INTO `receta` (`id`, `producto_id`, `fecha_creacion`, `ultima_modificacion`) VALUES
(1, 1, '2023-06-07 19:51:34', '2023-06-07 19:51:34'),
(10, 10, '2023-06-19 21:28:52', '2023-06-19 21:28:52'),
(14, 14, '2023-07-18 12:40:50', '2023-07-18 12:40:50'),
(16, 16, '2023-07-18 12:48:12', '2023-07-18 12:48:12'),
(17, 17, '2023-07-18 12:48:12', '2023-07-18 12:48:12'),
(20, 20, '2023-07-18 12:48:12', '2023-07-18 12:48:12'),
(21, 21, '2023-07-18 14:01:48', '2023-07-18 14:01:48');

-- --------------------------------------------------------

--
-- Table structure for table `receta_detalle`
--

CREATE TABLE `receta_detalle` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `receta_id` int(11) DEFAULT NULL,
  `ingrediente_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `receta_detalle`
--

INSERT INTO `receta_detalle` (`id`, `cantidad`, `receta_id`, `ingrediente_id`, `fecha_creacion`, `ultima_modificacion`, `activo`) VALUES
(6, 250, 1, 5, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(7, 200, 1, 6, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(8, 300, 1, 7, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(12, 1, 10, 2, '2023-06-19 21:28:52', '2023-06-19 21:28:52', 0),
(21, 1, 1, 2, '2023-07-06 18:12:10', '2023-07-06 18:12:10', 0),
(22, 10, 10, 9, '2023-07-15 21:02:38', '2023-07-15 21:02:38', 0),
(23, 2, 14, 2, '2023-07-18 12:40:50', '2023-07-18 12:40:50', 0),
(24, 2, 16, 2, '2023-07-18 12:48:12', '2023-07-18 12:48:12', 0),
(25, 2, 17, 2, '2023-07-18 12:48:12', '2023-07-18 12:48:12', 0),
(26, 1, 20, 2, '2023-07-18 12:48:12', '2023-07-18 12:48:12', 0),
(29, 110, 20, 3, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0),
(30, 110, 20, 7, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0),
(31, 110, 20, 6, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0),
(32, 2, 21, 2, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0),
(33, 150, 21, 3, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0),
(34, 150, 21, 7, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0),
(35, 130, 21, 6, '2023-07-18 14:01:48', '2023-07-18 14:01:48', 0);

-- --------------------------------------------------------

--
-- Table structure for table `rol`
--

CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `rol`
--

INSERT INTO `rol` (`id`, `nombre`, `activo`, `fecha_creacion`, `ultima_modificacion`) VALUES
(1, 'Administrador', 1, '2023-06-06 14:04:04', '2023-06-06 14:04:04'),
(2, 'Personal de caja', 1, '2023-06-06 14:04:04', '2023-06-06 14:04:04'),
(3, 'ELIMINADO', 0, '2023-06-06 14:04:04', '2023-06-07 19:41:30'),
(4, 'ELIMIANO', 0, '2023-06-07 19:39:12', '2023-06-07 19:39:12'),
(5, 'Personal de cocina', 1, '2023-06-07 19:51:30', '2023-07-14 17:21:46'),
(6, 'Empleado', 1, '2023-07-14 17:26:38', '2023-07-14 17:26:38');

-- --------------------------------------------------------

--
-- Table structure for table `unidadmedida`
--

CREATE TABLE `unidadmedida` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `unidadmedida`
--

INSERT INTO `unidadmedida` (`id`, `nombre`, `activo`, `fecha_creacion`, `ultima_modificacion`) VALUES
(1, 'gr', 1, '2023-06-16 17:15:12', '2023-06-16 17:15:12'),
(2, 'ml', 1, '2023-06-16 17:15:12', '2023-06-16 17:15:12'),
(3, 'Unidad/es', 1, '2023-06-16 17:15:12', '2023-07-04 17:20:02'),
(4, 'Unidad(es)', 1, '2023-07-04 18:21:14', '2023-07-04 18:21:14');

-- --------------------------------------------------------

--
-- Table structure for table `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `nombre_usuario` varchar(50) NOT NULL,
  `correo` varchar(255) NOT NULL,
  `contrasena` varchar(60) NOT NULL,
  `rol_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `usuario`
--

INSERT INTO `usuario` (`id`, `nombre_usuario`, `correo`, `contrasena`, `rol_id`, `fecha_creacion`, `ultima_modificacion`, `activo`) VALUES
(1, 'galvezluis', 'galvezluis72@gmail.com', '$2b$12$NJ/4JWBugLVU0pJjIfMcne9NqDk/.zLpotKLUAqXUes4FG7GZ/..O', 5, '2023-06-06 14:04:05', '2023-07-19 11:07:53', 1),
(2, 'admin', 'admin@fratelli.cl', '$2b$12$4iPqNtgn6dwMZEJnbgIVkuNRmivp/gFnGSs6/JuPqi7bOkdIvBw1S', 1, '2023-06-21 15:02:17', '2023-07-14 17:21:25', 1),
(3, 'marito', 'marito@pizzeria.cl', '$2b$12$O54gYmqoqaqTkHJXiowTaucqFLhvijIbIaFRY9ArmwDJNoOP1WF7S', 5, '2023-06-26 23:04:01', '2023-07-04 01:26:49', 0);

-- --------------------------------------------------------

--
-- Table structure for table `venta`
--

CREATE TABLE `venta` (
  `id` int(11) NOT NULL,
  `pedido_id` int(11) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `venta`
--

INSERT INTO `venta` (`id`, `pedido_id`, `total`, `activo`) VALUES
(1, 1, 10200, 1),
(2, 2, 8800, 1),
(3, 3, 11600, 1),
(4, 4, 8800, 1),
(5, 5, 33600, 1),
(6, 6, 14600, 1),
(7, 7, 11350, 1),
(8, 8, 12850, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `ingrediente`
--
ALTER TABLE `ingrediente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `unidadmedida_id` (`unidadmedida_id`);

--
-- Indexes for table `metodopago`
--
ALTER TABLE `metodopago`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `persona_id` (`persona_id`),
  ADD KEY `estado_id` (`estado_id`),
  ADD KEY `metodopago_id` (`metodopago_id`);

--
-- Indexes for table `pedido_detalle`
--
ALTER TABLE `pedido_detalle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indexes for table `pedido_detalle_ingrediente`
--
ALTER TABLE `pedido_detalle_ingrediente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_detalle_id` (`pedido_detalle_id`),
  ADD KEY `ingrediente_id` (`ingrediente_id`);

--
-- Indexes for table `pedido_estado`
--
ALTER TABLE `pedido_estado`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `persona`
--
ALTER TABLE `persona`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rut` (`rut`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indexes for table `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_barra` (`codigo_barra`),
  ADD KEY `categoria_id` (`categoria_id`);

--
-- Indexes for table `receta`
--
ALTER TABLE `receta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indexes for table `receta_detalle`
--
ALTER TABLE `receta_detalle`
  ADD PRIMARY KEY (`id`),
  ADD KEY `receta_id` (`receta_id`),
  ADD KEY `ingrediente_id` (`ingrediente_id`);

--
-- Indexes for table `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `unidadmedida`
--
ALTER TABLE `unidadmedida`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indexes for table `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `rol_id` (`rol_id`);

--
-- Indexes for table `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pedido_id` (`pedido_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categoria`
--
ALTER TABLE `categoria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `ingrediente`
--
ALTER TABLE `ingrediente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `metodopago`
--
ALTER TABLE `metodopago`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `pedido_detalle`
--
ALTER TABLE `pedido_detalle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `pedido_detalle_ingrediente`
--
ALTER TABLE `pedido_detalle_ingrediente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `pedido_estado`
--
ALTER TABLE `pedido_estado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `persona`
--
ALTER TABLE `persona`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `receta`
--
ALTER TABLE `receta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `receta_detalle`
--
ALTER TABLE `receta_detalle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `unidadmedida`
--
ALTER TABLE `unidadmedida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `venta`
--
ALTER TABLE `venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ingrediente`
--
ALTER TABLE `ingrediente`
  ADD CONSTRAINT `ingrediente_ibfk_1` FOREIGN KEY (`unidadmedida_id`) REFERENCES `unidadmedida` (`id`);

--
-- Constraints for table `pedido`
--
ALTER TABLE `pedido`
  ADD CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`persona_id`) REFERENCES `persona` (`id`),
  ADD CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`estado_id`) REFERENCES `pedido_estado` (`id`),
  ADD CONSTRAINT `pedido_ibfk_3` FOREIGN KEY (`metodopago_id`) REFERENCES `metodopago` (`id`);

--
-- Constraints for table `pedido_detalle`
--
ALTER TABLE `pedido_detalle`
  ADD CONSTRAINT `pedido_detalle_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`),
  ADD CONSTRAINT `pedido_detalle_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`);

--
-- Constraints for table `pedido_detalle_ingrediente`
--
ALTER TABLE `pedido_detalle_ingrediente`
  ADD CONSTRAINT `pedido_detalle_ingrediente_ibfk_1` FOREIGN KEY (`pedido_detalle_id`) REFERENCES `pedido_detalle` (`id`),
  ADD CONSTRAINT `pedido_detalle_ingrediente_ibfk_2` FOREIGN KEY (`ingrediente_id`) REFERENCES `ingrediente` (`id`);

--
-- Constraints for table `persona`
--
ALTER TABLE `persona`
  ADD CONSTRAINT `persona_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`);

--
-- Constraints for table `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`id`);

--
-- Constraints for table `receta`
--
ALTER TABLE `receta`
  ADD CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `producto` (`id`);

--
-- Constraints for table `receta_detalle`
--
ALTER TABLE `receta_detalle`
  ADD CONSTRAINT `receta_detalle_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `receta` (`id`),
  ADD CONSTRAINT `receta_detalle_ibfk_2` FOREIGN KEY (`ingrediente_id`) REFERENCES `ingrediente` (`id`);

--
-- Constraints for table `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);

--
-- Constraints for table `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedido` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
