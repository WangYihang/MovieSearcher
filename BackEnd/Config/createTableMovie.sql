CREATE TABLE `movies` (
  `movieID` int(16) NOT NULL AUTO_INCREMENT,
  `movieTitle` text NOT NULL,
  `movieDescribe` text NOT NULL,
  `movieTime` text NOT NULL,
  `movieClickTimes` text NOT NULL,
  `movieDownloadLink` text NOT NULL,
  `movieKey` text NOT NULL,
  PRIMARY KEY (`movieID`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8

CREATE TABLE `queue` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `keyword` text NOT NULL,
  `status` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8


create database 'bigdata' default character set utf8;
