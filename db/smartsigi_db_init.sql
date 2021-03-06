-- Adminer 4.7.9 MySQL dump

SET NAMES utf8;
SET time_zone = 'Europe/Vienna';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `smartsigi`;
CREATE DATABASE `smartsigi` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `smartsigi`;

DROP TABLE IF EXISTS `alarms`;
CREATE TABLE `alarms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` text NOT NULL,
  `label_id` text NOT NULL,
  `datetime` datetime NOT NULL,
  `temp` float NOT NULL,
  `expo_push_token` text NOT NULL,
  `notified` char(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `custom_labels`;
CREATE TABLE `custom_labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label_id` text NOT NULL,
  `uid` text NOT NULL,
  `custom_label_name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `labels`;
CREATE TABLE `labels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label_id` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


DROP TABLE IF EXISTS `snapshots`;
CREATE TABLE `snapshots` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `label_id` text NOT NULL,
  `datetime` datetime NOT NULL,
  `temp` float NOT NULL,
  `debug` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`debug`)),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- 2021-02-26 16:10:05