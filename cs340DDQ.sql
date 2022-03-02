-- phpMyAdmin SQL Dump
-- version 5.1.3-2.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 24, 2022 at 11:19 PM
-- Server version: 10.6.5-MariaDB-log
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_paoluccr`
--

-- --------------------------------------------------------

--
-- Table structure for table `Gyms`
--

CREATE TABLE `Gyms` (
  `gymId` int(11) NOT NULL,
  `gymName` varchar(255) NOT NULL,
  `leaderName` varchar(255) NOT NULL,
  `regionId` int(11) NOT NULL,
  `typeId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Gyms`
--

INSERT INTO `Gyms` (`gymId`, `gymName`, `leaderName`, `regionId`, `typeId`) VALUES
(1, 'Pewter City Gym', 'Brock', 1, 12);

-- --------------------------------------------------------

--
-- Table structure for table `Pokemon`
--

CREATE TABLE `Pokemon` (
  `pokemonId` int(11) NOT NULL,
  `pokemonName` varchar(255) NOT NULL,
  `pokemonGender` varchar(255) NOT NULL,
  `regionId` int(11) NOT NULL,
  `pokemonTypeId1` int(11) NOT NULL,
  `pokemonTypeId2` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Pokemon`
--

INSERT INTO `Pokemon` (`pokemonId`, `pokemonName`, `pokemonGender`, `regionId`, `pokemonTypeId1`, `pokemonTypeId2`) VALUES
(1, 'Bulbasaur', 'Male', 1, 3, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `PokemonTypes`
--

CREATE TABLE `PokemonTypes` (
  `pokemonTypeId` int(11) NOT NULL primary key AUTO_INCREMENT,
  `pokemonId` int(11) NOT NULL,
  `typeId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- --------------------------------------------------------

--
-- Table structure for table `Regions`
--

CREATE TABLE `Regions` (
  `regionId` int(11) NOT NULL,
  `regionName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Regions`
--

INSERT INTO `Regions` (`regionId`, `regionName`) VALUES
(1, 'Kanto'),
(2, 'Johto'),
(3, 'Hoenn'),
(4, 'Sinnoh'),
(5, 'Unova'),
(6, 'Kalos'),
(7, 'Alola'),
(8, 'Galar');

-- --------------------------------------------------------

--
-- Table structure for table `Types`
--

CREATE TABLE `Types` (
  `typeId` int(11) NOT NULL,
  `typeName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Types`
--

INSERT INTO `Types` (`typeId`, `typeName`) VALUES
(1, 'Normal'),
(2, 'Fire'),
(3, 'Water'),
(4, 'Grass'),
(5, 'Electric'),
(6, 'Ice'),
(7, 'Fighting'),
(8, 'Poison'),
(9, 'Ground'),
(10, 'Flying'),
(11, 'Psychic'),
(12, 'Bug'),
(13, 'Rock'),
(14, 'Ghost'),
(15, 'Dark'),
(16, 'Dragon'),
(17, 'Steel'),
(18, 'Fairy');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Gyms`
--
ALTER TABLE `Gyms`
  ADD PRIMARY KEY (`gymId`),
  ADD KEY `gyms_fk_1` (`regionId`),
  ADD KEY `gyms_fk_2` (`typeId`);

--
-- Indexes for table `Pokemon`
--
ALTER TABLE `Pokemon`
  ADD PRIMARY KEY (`pokemonId`),
  ADD KEY `pokemon_fk_1` (`regionId`),
  ADD KEY `pokemon_fk_2` (`pokemonTypeId1`),
  ADD KEY `pokemon_fk_3` (`pokemonTypeId2`);

--
-- Indexes for table `PokemonTypes`
--
ALTER TABLE `PokemonTypes`
  ADD KEY `pokemonTypes_fk_1` (`pokemonId`),
  ADD KEY `pokemonTypes_fk_2` (`typeId`);

--
-- Indexes for table `Regions`
--
ALTER TABLE `Regions`
  ADD PRIMARY KEY (`regionId`);

--
-- Indexes for table `Types`
--
ALTER TABLE `Types`
  ADD PRIMARY KEY (`typeId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Gyms`
--
ALTER TABLE `Gyms`
  MODIFY `gymId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `Regions`
--
ALTER TABLE `Regions`
  MODIFY `regionId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `Types`
--
ALTER TABLE `Types`
  MODIFY `typeId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Gyms`
--
ALTER TABLE `Gyms`
  ADD CONSTRAINT `gyms_fk_1` FOREIGN KEY (`regionId`) REFERENCES `Regions` (`regionId`),
  ADD CONSTRAINT `gyms_fk_2` FOREIGN KEY (`typeId`) REFERENCES `Types` (`typeId`);

--
-- Constraints for table `Pokemon`
--
ALTER TABLE `Pokemon`
  ADD CONSTRAINT `pokemon_fk_1` FOREIGN KEY (`regionId`) REFERENCES `Regions` (`regionId`);

--
-- Constraints for table `PokemonTypes`
--
ALTER TABLE `PokemonTypes`
  ADD CONSTRAINT `pokemonTypes_fk_1` FOREIGN KEY (`pokemonId`) REFERENCES `Pokemon` (`pokemonId`),
  ADD CONSTRAINT `pokemonTypes_fk_2` FOREIGN KEY (`typeId`) REFERENCES `Types` (`typeId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
