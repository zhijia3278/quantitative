/*
Navicat MySQL Data Transfer

Source Server         : 192.168.0.115
Source Server Version : 50650
Source Host           : 192.168.0.115:50004
Source Database       : zhijia

Target Server Type    : MYSQL
Target Server Version : 50650
File Encoding         : 65001

Date: 2020-11-03 20:29:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for stock_buy_sell
-- ----------------------------
DROP TABLE IF EXISTS `stock_buy_sell`;
CREATE TABLE `stock_buy_sell` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` int(10) DEFAULT NULL,
  `k` decimal(10,6) DEFAULT NULL,
  `d` decimal(10,6) DEFAULT NULL,
  `j` decimal(10,6) DEFAULT NULL,
  `buy` decimal(7,2) DEFAULT NULL,
  `sell` decimal(7,2) DEFAULT NULL,
  `money` decimal(10,2) DEFAULT NULL,
  `num` decimal(10,2) DEFAULT NULL,
  `flag` smallint(1) DEFAULT NULL COMMENT '买入、卖出的标志位',
  `validdate` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
