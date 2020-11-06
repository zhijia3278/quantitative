/*
Navicat MySQL Data Transfer

Source Server         : 192.168.0.115
Source Server Version : 50650
Source Host           : 192.168.0.115:50004
Source Database       : zhijia

Target Server Type    : MYSQL
Target Server Version : 50650
File Encoding         : 65001

Date: 2020-11-03 20:29:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for stock_history_detail
-- ----------------------------
DROP TABLE IF EXISTS `stock_history_detail`;
CREATE TABLE `stock_history_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` char(6) DEFAULT NULL,
  `open` decimal(7,2) DEFAULT NULL,
  `high` decimal(7,2) DEFAULT NULL,
  `close` decimal(7,2) DEFAULT NULL,
  `low` decimal(7,2) DEFAULT NULL,
  `volume` decimal(10,2) DEFAULT NULL,
  `record_date` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  `validdate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
