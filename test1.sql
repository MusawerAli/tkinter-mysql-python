-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 16, 2023 at 04:49 PM
-- Server version: 10.11.2-MariaDB-1
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test1`
--

-- --------------------------------------------------------

--
-- Table structure for table `transition`
--

CREATE TABLE `transition` (
  `id` int(11) NOT NULL,
  `amount` float NOT NULL,
  `type` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transition`
--

INSERT INTO `transition` (`id`, `amount`, `type`, `user_id`, `date`) VALUES
(1, 100, 'deposit', 1, '2023-06-15 16:28:36'),
(2, 100, 'deposit', 1, '2023-06-15 16:39:56'),
(3, 200, 'deposit', 1, '2023-06-15 16:41:15'),
(4, 500, 'deposit', 2, '2023-06-15 17:45:11'),
(5, 100, 'withdraw', 2, '2023-06-15 17:45:26');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `account_number` varchar(50) NOT NULL,
  `pin` varchar(50) NOT NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 1,
  `balance` float DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `account_number`, `pin`, `is_admin`, `balance`) VALUES
(1, 'admin', 'admin', 'admin123', 1, 400),
(2, 'test', 'test', 'test', 0, 500);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transition`
--
ALTER TABLE `transition`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `transition`
--
ALTER TABLE `transition`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
