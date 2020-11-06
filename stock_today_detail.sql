/*
Navicat MySQL Data Transfer

Source Server         : 192.168.0.115
Source Server Version : 50650
Source Host           : 192.168.0.115:50004
Source Database       : zhijia

Target Server Type    : MYSQL
Target Server Version : 50650
File Encoding         : 65001

Date: 2020-11-03 20:30:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for stock_today_detail
-- ----------------------------
DROP TABLE IF EXISTS `stock_today_detail`;
CREATE TABLE `stock_today_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` char(6) DEFAULT NULL,
  `name` varchar(20) COLLATE utf8_bin DEFAULT NULL,
  `changepercent` decimal(7,2) DEFAULT NULL,
  `trade` decimal(7,2) DEFAULT NULL,
  `open` decimal(7,2) DEFAULT NULL,
  `high` decimal(7,2) DEFAULT NULL,
  `low` decimal(7,2) DEFAULT NULL,
  `settlement` decimal(7,2) DEFAULT NULL,
  `volume` decimal(12,2) DEFAULT NULL,
  `activate` smallint(1) DEFAULT NULL COMMENT '该股票是否仍然存活',
  `flag` smallint(1) DEFAULT NULL COMMENT '该股票是否加入监控队列',
  `validdate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4077 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
