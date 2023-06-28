-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 28, 2023 at 08:28 AM
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
(1, 'Salsa de tomate', 599834, 1, '2023-06-06 14:41:38', '2023-06-28 02:18:30', 1, 1000, 1000, 100, 100),
(2, 'Bolas de masa', 1010, 1, '2023-06-09 12:12:25', '2023-06-28 02:06:28', 3, 1000, 1000, 100, 100),
(3, 'Queso Cheddar', 82350, 1, '2023-06-09 12:13:19', '2023-06-09 12:13:19', 1, 1000, 1000, 100, 100),
(4, 'Queso Mozzarella', 6000, 1, '2023-06-09 12:13:29', '2023-06-09 12:13:39', 1, 1000, 1000, 100, 100),
(5, 'Orégano', 66250, 1, '2023-06-09 12:13:59', '2023-06-09 12:13:59', 1, 1000, 1000, 100, 100),
(6, 'Tomate picado', 57000, 1, '2023-06-09 12:15:52', '2023-06-09 12:15:52', 1, 1000, 1000, 100, 100),
(7, 'Jamón', 895500, 1, '2023-06-09 12:16:19', '2023-06-09 12:16:36', 1, 1000, 1000, 100, 100),
(8, 'Camarón', 3000, 1, '2023-06-20 18:54:24', '2023-06-20 18:54:24', 3, 1000, 1000, 100, 100),
(9, 'Aceituna', 800, 1, '2023-06-20 18:54:47', '2023-06-20 18:54:47', 3, 1000, 1000, 100, 100),
(10, 'Piña', 350000, 1, '2023-06-20 18:55:15', '2023-06-20 18:55:31', 1, 1000, 1000, 100, 100),
(11, 'Tocino', 50000, 1, '2023-06-20 18:55:43', '2023-06-20 18:55:43', 1, 1000, 1000, 100, 100),
(12, 'Choclo', 70000, 1, '2023-06-20 18:56:33', '2023-06-20 18:56:33', 1, 1000, 1000, 100, 100),
(13, 'Cebolla morada', 600000, 1, '2023-06-20 18:56:54', '2023-06-20 18:56:54', 1, 1000, 1000, 100, 100),
(14, 'Salsa de tomate', 0, 0, '2023-06-20 18:57:08', '2023-06-20 18:57:08', 1, 1000, 1000, 100, 100),
(15, 's', 0, 0, '2023-06-28 01:50:15', '2023-06-28 01:50:15', 1, 1000, 1000, 100, 100);

-- --------------------------------------------------------

--
-- Table structure for table `pedido`
--

CREATE TABLE `pedido` (
  `id` int(11) NOT NULL,
  `persona_id` int(11) DEFAULT NULL,
  `estado_id` int(11) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `pedido`
--

INSERT INTO `pedido` (`id`, `persona_id`, `estado_id`, `fecha_creacion`, `ultima_modificacion`) VALUES
(1, 1, 3, '2023-06-13 21:45:51', '2023-06-13 21:45:51'),
(2, 1, 2, '2023-06-14 15:03:43', '2023-06-14 15:03:43'),
(3, 1, 2, '2023-06-14 19:11:26', '2023-06-14 19:11:26'),
(4, 1, 2, '2023-06-16 15:49:23', '2023-06-16 15:49:23'),
(5, 1, 1, '2023-06-20 00:31:08', '2023-06-20 00:31:08'),
(6, 1, 1, '2023-06-20 00:31:08', '2023-06-20 00:31:08'),
(7, 1, 1, '2023-06-20 18:41:16', '2023-06-20 18:41:16'),
(8, 3, 1, '2023-06-26 23:04:01', '2023-06-26 23:04:01');

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `pedido_detalle`
--

INSERT INTO `pedido_detalle` (`id`, `pedido_id`, `producto_id`, `cantidad`, `fecha_creacion`, `ultima_modificacion`) VALUES
(1, 1, 9, 1, '2023-06-14 13:37:57', '2023-06-14 13:37:57'),
(2, 1, 1, 1, '2023-06-14 13:37:57', '2023-06-14 13:37:57'),
(3, 1, 9, 1, '2023-06-14 13:37:57', '2023-06-14 13:37:57'),
(4, 2, 1, 3, '2023-06-14 15:19:34', '2023-06-14 15:19:34'),
(5, 2, 9, 111, '2023-06-14 15:19:34', '2023-06-14 15:19:34'),
(10, 3, 9, 1, '2023-06-16 14:50:00', '2023-06-16 14:50:00'),
(26, 4, 1, 7, '2023-06-19 20:46:05', '2023-06-19 20:46:05'),
(30, 4, 9, 6, '2023-06-19 21:28:52', '2023-06-19 21:28:52'),
(32, 3, 10, 2, '2023-06-19 21:28:52', '2023-06-19 21:28:52'),
(36, 4, 10, 5, '2023-06-19 22:22:51', '2023-06-19 22:22:51'),
(37, 3, 1, 1, '2023-06-19 22:39:14', '2023-06-19 22:39:14'),
(62, 5, 9, 1, '2023-06-20 12:01:25', '2023-06-20 12:01:25'),
(64, 7, 9, 1, '2023-06-20 18:41:16', '2023-06-20 18:41:16'),
(72, 7, 10, 1, '2023-06-20 18:41:16', '2023-06-20 18:41:16'),
(91, 5, 10, 1, '2023-06-21 14:46:03', '2023-06-21 14:46:03'),
(93, 5, 1, 1, '2023-06-21 14:46:03', '2023-06-21 14:46:03'),
(95, 8, 9, 2, '2023-06-26 23:04:01', '2023-06-26 23:04:01'),
(96, 8, 1, 1, '2023-06-26 23:04:01', '2023-06-26 23:04:01');

-- --------------------------------------------------------

--
-- Table structure for table `pedido_detalle_ingrediente`
--

CREATE TABLE `pedido_detalle_ingrediente` (
  `id` int(11) NOT NULL,
  `pedido_detalle_id` int(11) DEFAULT NULL,
  `ingrediente_id` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `pedido_detalle_ingrediente`
--

INSERT INTO `pedido_detalle_ingrediente` (`id`, `pedido_detalle_id`, `ingrediente_id`, `cantidad`) VALUES
(1, 91, 1, 777),
(2, 91, 1, 777),
(3, 91, 1, 777),
(4, 91, 1, 777),
(5, 91, 1, 777),
(6, 91, 1, 45),
(7, 91, 2, 1),
(8, 91, 4, 6000),
(9, 91, 4, 6000),
(10, 91, 2, 1),
(11, 91, 1, 1),
(12, 96, 1, 23),
(13, 96, 1, 2),
(14, 96, 1, 555);

-- --------------------------------------------------------

--
-- Table structure for table `pedido_estado`
--

CREATE TABLE `pedido_estado` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
(1, 1, '20704339-7', 'Luis', 'Gálvez', 'González', '935257778', '2023-06-06 14:04:04', '2023-06-21 14:52:24', 1),
(2, 2, '6753719‑k', 'Juditza', 'Álvarez', 'Ramírez', '9', '2023-06-21 15:02:17', '2023-06-21 15:02:17', 1),
(3, 3, '67537319‑k', 'Mario', 'Lopez', 'González', '345657', '2023-06-26 23:04:01', '2023-06-26 23:04:01', 1);

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
  `activo` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `producto`
--

INSERT INTO `producto` (`id`, `imagen`, `codigo_barra`, `nombre`, `descripcion`, `precio`, `stock`, `tiene_receta`, `categoria_id`, `fecha_creacion`, `ultima_modificacion`, `activo`) VALUES
(1, '/productos/pizzeria-valencia-blasco-ibanez-la-fratelli-pizza-tropical.jpg', '53', 'La Fratelli', 'Salsa de tomate, albahaca, champiñones, queso Taleggio, pimiento, cebolla, espinacas, bacon y orégano.', 7500, NULL, 1, 1, '2023-06-07 19:56:38', '2023-06-21 14:23:05', 1),
(9, '/productos/8975035.jpg', '34', 'Coca-Cola Sin Azucar 350ml', 'Bebida en lata, 350ml', 1400, 400, 0, 3, '2023-06-09 12:42:08', '2023-06-27 23:51:29', 1),
(10, '/productos/pizzeria-valencia-blasco-ibanez-la-fratelli-pizza-caprichosa.jpg', '35', 'Caprichosa', '', 7500, NULL, 1, 1, '2023-06-19 21:31:42', '2023-06-19 21:28:52', 1);

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
(10, 10, '2023-06-19 21:28:52', '2023-06-19 21:28:52');

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
(5, 300, 1, 3, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(6, 250, 1, 5, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(7, 200, 1, 6, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(8, 300, 1, 7, '2023-06-09 12:11:26', '2023-06-09 12:11:26', 0),
(12, 1, 10, 2, '2023-06-19 21:28:52', '2023-06-19 21:28:52', 0),
(13, 350, 10, 3, '2023-06-19 21:28:52', '2023-06-19 21:28:52', 0),
(16, 1, 1, 2, '2023-06-26 23:04:01', '2023-06-26 23:04:01', 0),
(17, 100, 1, 9, '2023-06-26 23:04:01', '2023-06-26 23:04:01', 0);

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
(5, 'Empleado', 1, '2023-06-07 19:51:30', '2023-06-07 19:51:30');

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
(3, 'Unidad(es)', 1, '2023-06-16 17:15:12', '2023-06-16 17:15:12');

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
(1, 'galvezluis', 'galvezluis72@gmail.com', '$2b$12$NJ/4JWBugLVU0pJjIfMcne9NqDk/.zLpotKLUAqXUes4FG7GZ/..O', 1, '2023-06-06 14:04:05', '2023-06-21 14:52:24', 1),
(2, 'admin', 'admin@fratelli.cl', '$2b$12$4iPqNtgn6dwMZEJnbgIVkuNRmivp/gFnGSs6/JuPqi7bOkdIvBw1S', 2, '2023-06-21 15:02:17', '2023-06-21 15:02:17', 1),
(3, 'marito', 'marito@pizzeria.cl', '$2b$12$O54gYmqoqaqTkHJXiowTaucqFLhvijIbIaFRY9ArmwDJNoOP1WF7S', 1, '2023-06-26 23:04:01', '2023-06-26 23:04:01', 1);

-- --------------------------------------------------------

--
-- Table structure for table `venta`
--

CREATE TABLE `venta` (
  `id` int(11) NOT NULL,
  `id_pedido` int(11) DEFAULT NULL,
  `precio` int(11) DEFAULT NULL,
  `activo` tinyint(1) NOT NULL,
  `fecha_creacion` datetime NOT NULL,
  `ultima_modificacion` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
-- Indexes for table `pedido`
--
ALTER TABLE `pedido`
  ADD PRIMARY KEY (`id`),
  ADD KEY `persona_id` (`persona_id`),
  ADD KEY `estado_id` (`estado_id`);

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
  ADD KEY `id_pedido` (`id_pedido`);

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
-- AUTO_INCREMENT for table `pedido`
--
ALTER TABLE `pedido`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `pedido_detalle`
--
ALTER TABLE `pedido_detalle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT for table `pedido_detalle_ingrediente`
--
ALTER TABLE `pedido_detalle_ingrediente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `receta`
--
ALTER TABLE `receta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `receta_detalle`
--
ALTER TABLE `receta_detalle`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `unidadmedida`
--
ALTER TABLE `unidadmedida`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `venta`
--
ALTER TABLE `venta`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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
  ADD CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`estado_id`) REFERENCES `pedido_estado` (`id`);

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
  ADD CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
