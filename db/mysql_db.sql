DROP TABLE IF EXISTS `sources`;
DROP TABLE IF EXISTS `trends`;
DROP TABLE IF EXISTS `entries`;

-- SOURCES TABLE --
CREATE TABLE `sources` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT UC_Source_Name UNIQUE(name)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- TRENDS TABLE --
CREATE TABLE `trends` (
  `id` int NOT NULL AUTO_INCREMENT,
  `topic` varchar(255) NOT NULL,
  `trend_date` date NOT NULL,
  `entry_id` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`entry_id`) REFERENCES `entries`(id)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- ENTRIES TABLE ---
CREATE TABLE `entries` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `fiability` BOOLEAN NOT NULL,
  `search_count` int NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`source_id`) REFERENCES `sources`(id),
  CONSTRAINT UC_Entry_Data UNIQUE(source_id, title)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;