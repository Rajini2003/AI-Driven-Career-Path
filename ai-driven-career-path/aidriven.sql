-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 25, 2025 at 01:56 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `aidriven`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `ID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`ID`, `Username`, `Password`) VALUES
(1, 'Admin', 'admin'),
(2, 'admin1', 'admin1');

-- --------------------------------------------------------

--
-- Table structure for table `apply_details`
--

CREATE TABLE `apply_details` (
  `job_id` varchar(50) NOT NULL,
  `job_name` varchar(255) DEFAULT NULL,
  `branch` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `mob` varchar(15) DEFAULT NULL,
  `email_id` varchar(255) DEFAULT NULL,
  `usn_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `apply_details`
--

INSERT INTO `apply_details` (`job_id`, `job_name`, `branch`, `name`, `mob`, `email_id`, `usn_number`) VALUES
('3', 'adgfa', 'is', 'Punith', '8618424197', 'punithsuresh1234@gmail.com', '1'),
('3', 'adgfa', 'is', 'test6', '1234567899', 'driveformovies01111@gmail.com', '5');

-- --------------------------------------------------------

--
-- Table structure for table `candidate_details`
--

CREATE TABLE `candidate_details` (
  `ID` int(11) NOT NULL,
  `FirstName` varchar(50) DEFAULT NULL,
  `MiddleName` varchar(50) DEFAULT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `MobileNumber` varchar(15) DEFAULT NULL,
  `EmailID` varchar(100) DEFAULT NULL,
  `TenthPercentage` float DEFAULT NULL,
  `TwelfthPercentage` float DEFAULT NULL,
  `Branch` varchar(50) DEFAULT NULL,
  `USNNumber` varchar(20) DEFAULT NULL,
  `Password` varchar(50) DEFAULT NULL,
  `skills` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidate_details`
--

INSERT INTO `candidate_details` (`ID`, `FirstName`, `MiddleName`, `LastName`, `Gender`, `MobileNumber`, `EmailID`, `TenthPercentage`, `TwelfthPercentage`, `Branch`, `USNNumber`, `Password`, `skills`) VALUES
(1, 'test6', 'test6', 'test6', 'male', '1234567899', 'driveformovies01111@gmail.com', 1, 1, 'CS', '5', '9j1vzhDS', 'Python,Java,C++'),
(2, 'Punith', 's', 'S', 'male', '8618424197', 'punithsuresh1234@gmail.com', 1, 1, 'CS', '1', 'Aasdf1234', 'Python,Java,C++'),
(3, 'Punith1', 's2', 'S3', 'Male', '8618424197', 'punithsuresh21234@gmail.com', 1, 2, 'CS', '2', 'Asdf1234', 'Python,Java,C++');

-- --------------------------------------------------------

--
-- Table structure for table `company_details`
--

CREATE TABLE `company_details` (
  `ID` int(11) NOT NULL,
  `CompanyName` varchar(100) NOT NULL,
  `Address` varchar(255) NOT NULL,
  `EmailID` varchar(100) NOT NULL,
  `Website` varchar(100) DEFAULT NULL,
  `ContactNumber` varchar(15) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `company_details`
--

INSERT INTO `company_details` (`ID`, `CompanyName`, `Address`, `EmailID`, `Website`, `ContactNumber`, `Username`, `Password`) VALUES
(1, 'asdad', 'bangalore', '123@gmail.com', 'abcd', '08618424197', 'User', 'TT'),
(2, 'test1', 'tests', '3rdyear1122334@gmail.com', 'tests', '9632490935', 'test2', 'O3IJOtym');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `email`, `message`) VALUES
(1, 'aa@gmail.com', 'agasrfghsha');

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `job_id` int(11) NOT NULL,
  `job_name` varchar(100) NOT NULL,
  `job_location` varchar(100) NOT NULL,
  `number_of_posts` int(11) NOT NULL,
  `branch` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`job_id`, `job_name`, `job_location`, `number_of_posts`, `branch`) VALUES
(3, 'adgfa', 'afgda', 2342, 'is');

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` int(11) NOT NULL,
  `branch` varchar(255) NOT NULL,
  `message` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notification`
--

INSERT INTO `notification` (`id`, `branch`, `message`) VALUES
(7, 'CS', 'test cs'),
(8, 'IS', 'test is'),
(9, 'IS', 'test IS'),
(10, 'CS', 'test cs\r\n'),
(11, 'IS', 'test IS');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `candidate_details`
--
ALTER TABLE `candidate_details`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `USNNumber` (`USNNumber`);

--
-- Indexes for table `company_details`
--
ALTER TABLE `company_details`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `EmailID` (`EmailID`),
  ADD UNIQUE KEY `Username` (`Username`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`job_id`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `candidate_details`
--
ALTER TABLE `candidate_details`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `company_details`
--
ALTER TABLE `company_details`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `notification`
--
ALTER TABLE `notification`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
