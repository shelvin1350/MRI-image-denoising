-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 09, 2024 at 03:51 AM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mri`
--

-- --------------------------------------------------------

--
-- Table structure for table `addprescription`
--

DROP TABLE IF EXISTS `addprescription`;
CREATE TABLE IF NOT EXISTS `addprescription` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `did` int NOT NULL,
  `details` varchar(100) NOT NULL,
  `prescription` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `addprescription`
--

INSERT INTO `addprescription` (`id`, `pid`, `did`, `details`, `prescription`) VALUES
(2, 9, 1, 'fever', 'paracetamol 500g'),
(3, 10, 2, 'Brain tumour', 'paracetamol'),
(4, 10, 1, 'fever', 'paracetamol');

-- --------------------------------------------------------

--
-- Table structure for table `doctorreg`
--

DROP TABLE IF EXISTS `doctorreg`;
CREATE TABLE IF NOT EXISTS `doctorreg` (
  `did` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phoneno` varchar(30) NOT NULL,
  `specification` varchar(30) NOT NULL,
  `qualification` varchar(30) NOT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctorreg`
--

INSERT INTO `doctorreg` (`did`, `name`, `email`, `phoneno`, `specification`, `qualification`) VALUES
(3, 'jeena', 'jeena@gmail.com', '1234567890', 'physio', 'mbbs');

-- --------------------------------------------------------

--
-- Table structure for table `labreg`
--

DROP TABLE IF EXISTS `labreg`;
CREATE TABLE IF NOT EXISTS `labreg` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phoneno` varchar(30) NOT NULL,
  `qualification` varchar(30) NOT NULL,
  PRIMARY KEY (`rid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `labreg`
--

INSERT INTO `labreg` (`rid`, `name`, `email`, `phoneno`, `qualification`) VALUES
(1, 'manju', 'manju@gmail.com', '2147483647', 'MBA'),
(2, 'nirog', 'nirog@gmail.com', '2147483647', 'nirog lab'),
(3, 'ivin', 'ivin@gmail.com', '9876543210', 'dpharm');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
CREATE TABLE IF NOT EXISTS `login` (
  `uname` varchar(50) NOT NULL,
  `password` varchar(30) NOT NULL,
  `usertype` varchar(20) NOT NULL,
  `status` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`uname`, `password`, `usertype`, `status`) VALUES
('admin@gmail.com', 'admin', 'admin', 'approved'),
('rijo@gmail.com', 'rijo', 'doctor', 'approved'),
('manju@gmail.com', 'manju', 'receptionist', 'approved'),
('prakash@gmail.com', '9999999999', 'doctor', 'approved'),
('arjun@gmail.com', 'arjun', 'doctor', 'approved'),
('a@gmail.com', '9900887889', 'doctor', 'approved'),
('anu@gmail.com', '9988899009', 'user', 'approved'),
('nirog@gmail.com', '9999999999', 'lab', 'approved'),
('shelvin@gmail.com', '9526423046', 'user', 'approved'),
('jeena@gmail.com', '1234567890', 'doctor', 'approved'),
('ivin@gmail.com', '9876543210', 'lab', 'approved');

-- --------------------------------------------------------

--
-- Table structure for table `mri`
--

DROP TABLE IF EXISTS `mri`;
CREATE TABLE IF NOT EXISTS `mri` (
  `mriid` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `did` int NOT NULL,
  `status` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`mriid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `mri`
--

INSERT INTO `mri` (`mriid`, `pid`, `did`, `status`, `image`) VALUES
(1, 12, 1, 'requested', '/media/images.jpg'),
(2, 13, 3, 'requested', '/media/noise_ler9HR8.jfif');

-- --------------------------------------------------------

--
-- Table structure for table `patientbooking`
--

DROP TABLE IF EXISTS `patientbooking`;
CREATE TABLE IF NOT EXISTS `patientbooking` (
  `pbid` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `did` int NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`pbid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patientbooking`
--

INSERT INTO `patientbooking` (`pbid`, `pid`, `did`, `status`) VALUES
(3, 9, 1, 'discharge'),
(4, 10, 2, ''),
(5, 10, 1, ''),
(6, 11, 2, 'booked'),
(7, 12, 1, 'mri'),
(8, 13, 3, 'mri');

-- --------------------------------------------------------

--
-- Table structure for table `patientreg`
--

DROP TABLE IF EXISTS `patientreg`;
CREATE TABLE IF NOT EXISTS `patientreg` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `phoneno` varchar(30) NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patientreg`
--

INSERT INTO `patientreg` (`pid`, `name`, `email`, `phoneno`) VALUES
(13, 'shelvin', 'shelvin@gmail.com', '9526423046');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
