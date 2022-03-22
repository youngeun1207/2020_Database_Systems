-- MariaDB dump 10.18  Distrib 10.5.7-MariaDB, for osx10.15 (x86_64)
--
-- Host: localhost    Database: MUSIC
-- ------------------------------------------------------
-- Server version	10.5.7-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `MUSIC`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `MUSIC` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `MUSIC`;

--
-- Table structure for table `ALBUM`
--

DROP TABLE IF EXISTS `ALBUM`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ALBUM` (
  `Album_Code` int(11) NOT NULL,
  `Album_Name` varchar(20) NOT NULL,
  `Lable` varchar(20) NOT NULL,
  `Album_Type` varchar(10) NOT NULL,
  `Introduction` varchar(500) DEFAULT NULL,
  `Release_Date` date NOT NULL,
  `Nation` varchar(15) NOT NULL,
  PRIMARY KEY (`Album_Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ALBUM`
--

LOCK TABLES `ALBUM` WRITE;
/*!40000 ALTER TABLE `ALBUM` DISABLE KEYS */;
INSERT INTO `ALBUM` VALUES (0,'에잇','카카오M','싱글','앞서 선보인 곡들이 내가 청자에게 직접적으로 말을 거는 수필 형식의 이야기였다면 ‘에잇’은 ‘너’ 라는 가상의 인물과 여러 비유를 사용해 나의 스물여덟을 고백한 짧은 소설과 같다. 나의 개인적인 정서로부터 오는 것인지 재해로 인해 함께 힘든 시기를 견디고 있는 사회 전반적인 분위기로부터 오는 것인지 혹은 둘 모두인지 확신할 수는 없지만 나의 스물여덟은 반복되는 무력감과 무기력함 그리고 ‘우리’가 슬프지 않았고 자유로울 수 있었던 ‘오렌지 섬’에 대한 그리움으로 기억될 것 같다.','2020-05-06','대한민국'),(1,'Love poem','카카오M','EP','모든 문학에는 정답이 없다지만 그중 해석의 제한에서 가장 자유로운 것은 시가 아닐까 한다. 작품자의 순정만 담겨 있다면 어떤 형태든 그 안에선 모든 것이 시적 허용된다. ‘시인’이라든가 ‘예술’이라든가 ‘영감’이라든가 ‘작품’과 같이 본인 입으로 얘기하기에는 왠지 좀 민망한 표현들에 대해 약간의 울렁증을 가지고 있는 내가 앨범명을 뻔뻔하게 ‘사랑시’라고 지어 놓고도 하나도 부끄럽지 않은 이유는 여기 담은 것들이 전부 진심이기 때문이다.','2019-11-18','대한민국'),(2,'삐삐','카카오M','싱글','모두들 안녕. 내 걱정은 마세요. 난 언제나 잘해 나갈 테니까','2018-10-10','대한민국'),(3,'THE ALBUM','YG PLUS','정규','2016년 ’SQUARE ONE’으로 데뷔하여 글로벌 아티스트로 성장한 블랙핑크의 첫 정규 앨범 ‘The Album’이 10월 2일 발매된다.','2020-10-02','대한민국'),(4,'Ice Cream','YG PLUS','싱글','‘Ice Cream’은 블랙핑크와 팝스타 셀레나 고메즈가 콜라보한 무더운 여름과 잘 어울리는 경쾌하고 청량한 사운드가 돋보이는 댄스-팝 곡이다. 겉으로는 차가워 보이지만 알고보면 달콤하다는 의미를 아이스크림에 비유한 톡톡 튀는 가사가 눈에 띈다.','2020-08-28','대한민국'),(5,'Black Mamba','SM ENTERTAINMENT','싱글','SM 신인 걸그룹 aespa 데뷔 싱글 ‘Black Mamba’ 공개! \n파워풀한 댄스곡! 주문 외우는 듯한 훅으로 중독성 UP!','2020-11-17','대한민국'),(6,'Young And Beautiful','Universal music','싱글','우아함 속에 빛나는 관능적인 아름다움, 라나 델 레이의 신곡 Young And Beautiful','2013-04-23','미국');
/*!40000 ALTER TABLE `ALBUM` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ALBUM_OF`
--

DROP TABLE IF EXISTS `ALBUM_OF`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ALBUM_OF` (
  `A_ID` int(11) NOT NULL,
  `Album_ID` int(11) NOT NULL,
  PRIMARY KEY (`A_ID`,`Album_ID`),
  KEY `FK_albumID` (`Album_ID`),
  CONSTRAINT `FK_albumID` FOREIGN KEY (`Album_ID`) REFERENCES `ALBUM` (`Album_Code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_artistID` FOREIGN KEY (`A_ID`) REFERENCES `Artist` (`Artist_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ALBUM_OF`
--

LOCK TABLES `ALBUM_OF` WRITE;
/*!40000 ALTER TABLE `ALBUM_OF` DISABLE KEYS */;
INSERT INTO `ALBUM_OF` VALUES (0,0),(0,1),(0,2),(1,3),(1,4),(4,5),(6,6);
/*!40000 ALTER TABLE `ALBUM_OF` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Artist`
--

DROP TABLE IF EXISTS `Artist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Artist` (
  `Artist_ID` int(11) NOT NULL,
  `Real_Name` varchar(20) NOT NULL,
  `Nick_Name` varchar(20) NOT NULL,
  `Agency` varchar(20) DEFAULT NULL,
  `Debut` date DEFAULT NULL,
  PRIMARY KEY (`Artist_ID`),
  UNIQUE KEY `uqName` (`Nick_Name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Artist`
--

LOCK TABLES `Artist` WRITE;
/*!40000 ALTER TABLE `Artist` DISABLE KEYS */;
INSERT INTO `Artist` VALUES (0,'이지은','아이유','Edam','2008-09-18'),(1,'블랙핑크','블랙핑크','YG','2016-08-08'),(4,'에스파','Aespa','SM엔터테인먼트','2020-11-17'),(6,'Elizabeth W Grant','Lana Del Rey','CAA','2008-10-21'),(7,'레드벨벳','레드벨벳','SM앤터테인먼트','2014-08-04');
/*!40000 ALTER TABLE `Artist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CONTAIN`
--

DROP TABLE IF EXISTS `CONTAIN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTAIN` (
  `Constructor_ID` varchar(20) NOT NULL,
  `L_No` int(11) NOT NULL,
  `M_ICN` int(11) NOT NULL,
  `Music_No` int(11) NOT NULL,
  PRIMARY KEY (`Constructor_ID`,`L_No`,`Music_No`),
  KEY `Contain_M_FK` (`M_ICN`),
  CONSTRAINT `Contain_M_FK` FOREIGN KEY (`M_ICN`) REFERENCES `MUSIC` (`ICN`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Playlist_FK` FOREIGN KEY (`Constructor_ID`, `L_No`) REFERENCES `PLAYLIST` (`Constructor_ID`, `List_No`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONTAIN`
--

LOCK TABLES `CONTAIN` WRITE;
/*!40000 ALTER TABLE `CONTAIN` DISABLE KEYS */;
INSERT INTO `CONTAIN` VALUES ('user6',0,0,1),('user1',0,1,1),('user6',0,1,2),('user1',0,2,2),('user1',1,2,1),('user6',0,2,3),('user1',1,10,2);
/*!40000 ALTER TABLE `CONTAIN` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MEMBER_OF`
--

DROP TABLE IF EXISTS `MEMBER_OF`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MEMBER_OF` (
  `Group_ID` int(11) NOT NULL,
  `Member_Name` varchar(15) NOT NULL,
  PRIMARY KEY (`Group_ID`,`Member_Name`),
  CONSTRAINT `group_FK` FOREIGN KEY (`Group_ID`) REFERENCES `Artist` (`Artist_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MEMBER_OF`
--

LOCK TABLES `MEMBER_OF` WRITE;
/*!40000 ALTER TABLE `MEMBER_OF` DISABLE KEYS */;
INSERT INTO `MEMBER_OF` VALUES (1,'로제'),(1,'리사'),(1,'제니'),(1,'지수'),(4,'닝닝'),(4,'윈터'),(4,'지젤'),(4,'카리나'),(7,'슬기'),(7,'아이린'),(7,'예리'),(7,'웬디'),(7,'조이');
/*!40000 ALTER TABLE `MEMBER_OF` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MUSIC`
--

DROP TABLE IF EXISTS `MUSIC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MUSIC` (
  `ICN` int(11) NOT NULL,
  `Music_Name` varchar(20) NOT NULL,
  `Album_ID` int(11) NOT NULL,
  `Track_No` int(11) NOT NULL DEFAULT 1,
  `Age_Limit` int(11) NOT NULL,
  `Link` varchar(100) NOT NULL,
  `IsTitle` tinyint(1) DEFAULT 0,
  `Times_Of_Played` int(11) DEFAULT NULL,
  `Genre` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`ICN`),
  KEY `FK_M_MGR` (`Album_ID`),
  CONSTRAINT `FK_album` FOREIGN KEY (`Album_ID`) REFERENCES `ALBUM` (`Album_Code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MUSIC`
--

LOCK TABLES `MUSIC` WRITE;
/*!40000 ALTER TABLE `MUSIC` DISABLE KEYS */;
INSERT INTO `MUSIC` VALUES (0,'에잇',0,1,0,'./mp3/Eight.mp3',1,38,'록/메탈'),(1,'블루밍',1,1,0,'./mp3/Blueming.mp3',1,15,'록/메탈'),(2,'Love Poem',1,2,0,'./mp3/LovePoem.mp3',0,48,'발라드'),(3,'그 사람',1,3,0,'./mp3/TheVisitor.mp3',0,1,'R&B/Soul'),(4,'시간의 바깥',1,4,0,'./mp3/AboveTheTime.mp3',0,2,'발라드'),(10,'삐삐',2,1,0,'./mp3/BbiBbi.mp3',1,17,'R&B/Soul'),(100,'Lovesick Girls',3,1,0,'./mp3/LovesickGirls.mp3',1,32,'댄스'),(101,'Pretty Savage',3,2,0,'./mp3/PrettySavage.mp3',0,9,'댄스'),(102,'Bet You Wanna',3,3,0,'./mp3/BetYouWanna.mp3',0,2,'댄스'),(103,'Love To Hate Me',3,4,1,'./mp3/LoveToHateMe.mp3',0,4,'댄스'),(104,'You Never Know',3,5,0,'./mp3/YouNeverKnow.mp3',0,7,'댄스'),(110,'Ice Cream',4,1,0,'./mp3/IceCream.mp3',1,4,'댄스'),(111,'Black Mamba',5,1,0,'./mp3/BlackMamba.mp3',1,36,'댄스'),(112,'Hi',4,2,0,'./mp3/IceCream.mp3',0,0,'댄스'),(113,'Young And Beautiful',6,0,0,'./mp3/YoungAndBeautiful.mp3',1,2,'발라드');
/*!40000 ALTER TABLE `MUSIC` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MUSIC_MANAGER`
--

DROP TABLE IF EXISTS `MUSIC_MANAGER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MUSIC_MANAGER` (
  `M_ID` varchar(20) NOT NULL,
  `M_Pw` varchar(20) NOT NULL,
  `M_Name` varchar(10) NOT NULL,
  `M_Ssn` char(13) NOT NULL,
  `M_Right` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`M_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MUSIC_MANAGER`
--

LOCK TABLES `MUSIC_MANAGER` WRITE;
/*!40000 ALTER TABLE `MUSIC_MANAGER` DISABLE KEYS */;
INSERT INTO `MUSIC_MANAGER` VALUES ('root','1234','root','9812072000000',1),('root1','1234','root','0201044000000',1);
/*!40000 ALTER TABLE `MUSIC_MANAGER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MUSIC_OF`
--

DROP TABLE IF EXISTS `MUSIC_OF`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MUSIC_OF` (
  `A_ID` int(11) NOT NULL,
  `M_ICN` int(11) NOT NULL,
  `isMain` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`A_ID`,`M_ICN`),
  KEY `FK_ICN` (`M_ICN`),
  CONSTRAINT `FK_AID` FOREIGN KEY (`A_ID`) REFERENCES `Artist` (`Artist_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_ICN` FOREIGN KEY (`M_ICN`) REFERENCES `MUSIC` (`ICN`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MUSIC_OF`
--

LOCK TABLES `MUSIC_OF` WRITE;
/*!40000 ALTER TABLE `MUSIC_OF` DISABLE KEYS */;
INSERT INTO `MUSIC_OF` VALUES (0,0,1),(0,1,1),(0,2,1),(0,3,1),(0,4,1),(0,10,1),(1,100,1),(1,101,1),(1,102,1),(1,103,1),(1,104,1),(1,110,1),(1,112,0),(4,111,1),(4,112,0),(6,113,1);
/*!40000 ALTER TABLE `MUSIC_OF` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PLAYLIST`
--

DROP TABLE IF EXISTS `PLAYLIST`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PLAYLIST` (
  `Constructor_ID` varchar(20) NOT NULL,
  `List_No` int(11) NOT NULL,
  `List_Name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Constructor_ID`,`List_No`),
  CONSTRAINT `CONSTRUCT_FK` FOREIGN KEY (`Constructor_ID`) REFERENCES `STREAMING_SUBSCRIBER` (`S_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PLAYLIST`
--

LOCK TABLES `PLAYLIST` WRITE;
/*!40000 ALTER TABLE `PLAYLIST` DISABLE KEYS */;
INSERT INTO `PLAYLIST` VALUES ('user1',0,'list1'),('user1',1,'iu_love'),('user6',0,'IU조아');
/*!40000 ALTER TABLE `PLAYLIST` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `QnA`
--

DROP TABLE IF EXISTS `QnA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `QnA` (
  `solved` tinyint(1) DEFAULT 0,
  `txt` varchar(200) DEFAULT NULL,
  `mgr_ID` varchar(20) NOT NULL,
  `asker_ID` varchar(20) NOT NULL,
  `answer` varchar(200) DEFAULT NULL,
  `Q_Title` varchar(30) DEFAULT NULL,
  `ask_No` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ask_No`),
  KEY `mgrOf` (`mgr_ID`),
  KEY `askOf` (`asker_ID`),
  CONSTRAINT `askOf` FOREIGN KEY (`asker_ID`) REFERENCES `STREAMING_SUBSCRIBER` (`S_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mgrOf` FOREIGN KEY (`mgr_ID`) REFERENCES `MUSIC_MANAGER` (`M_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `QnA`
--

LOCK TABLES `QnA` WRITE;
/*!40000 ALTER TABLE `QnA` DISABLE KEYS */;
INSERT INTO `QnA` VALUES (1,'노래가 이해요','root','user6','이상하면 치과에..','hihi',5),(0,'힘들어요','root','user6',NULL,'심해요',6),(0,'왜 없어졌냐','root','user1',NULL,'이상하다',7),(0,'노래가 좀 이상한디여 관리자 취향 반영ㄷㄷ','root','user1',NULL,'안녕하세요',8);
/*!40000 ALTER TABLE `QnA` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `STREAMING_SUBSCRIBER`
--

DROP TABLE IF EXISTS `STREAMING_SUBSCRIBER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `STREAMING_SUBSCRIBER` (
  `S_ID` varchar(20) NOT NULL,
  `S_Pw` varchar(20) NOT NULL,
  `S_Name` varchar(10) NOT NULL,
  `S_Ssn` char(13) NOT NULL,
  `Email` varchar(30) DEFAULT NULL,
  `BirthDate` date NOT NULL,
  `S_Mgr_ID` varchar(20) NOT NULL,
  `S_Right` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`S_ID`),
  KEY `MGR_FK` (`S_Mgr_ID`),
  CONSTRAINT `MGR_FK` FOREIGN KEY (`S_Mgr_ID`) REFERENCES `MUSIC_MANAGER` (`M_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `STREAMING_SUBSCRIBER`
--

LOCK TABLES `STREAMING_SUBSCRIBER` WRITE;
/*!40000 ALTER TABLE `STREAMING_SUBSCRIBER` DISABLE KEYS */;
INSERT INTO `STREAMING_SUBSCRIBER` VALUES ('user1','1111','주희','1210154000000','juhee@gmail.com','2012-10-15','root',1),('user4','4444','영으닝','9901072000000','user4@email.com','1999-01-07','root',0),('user5','5555','sangwook','7001011000000','dbs@hanyang.ac.kr','1970-01-01','root',0),('user6','6666','임규민','9711041000000','babo@gmail.com','1997-11-04','root',1),('yes','0000','youngeun','9812072000000','youngeun@hanyang.ac.kr','1998-12-07','root',1);
/*!40000 ALTER TABLE `STREAMING_SUBSCRIBER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SUBSCRIPTION_INFO`
--

DROP TABLE IF EXISTS `SUBSCRIPTION_INFO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SUBSCRIPTION_INFO` (
  `Subs_ID` varchar(20) NOT NULL,
  `Payment_No` int(11) NOT NULL,
  `PaymentMethod` varchar(20) DEFAULT NULL,
  `Price` int(11) DEFAULT 0,
  `PaymentDate` date DEFAULT NULL,
  PRIMARY KEY (`Payment_No`,`Subs_ID`),
  KEY `SUBS_FK` (`Subs_ID`),
  CONSTRAINT `SUBS_FK` FOREIGN KEY (`Subs_ID`) REFERENCES `STREAMING_SUBSCRIBER` (`S_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SUBSCRIPTION_INFO`
--

LOCK TABLES `SUBSCRIPTION_INFO` WRITE;
/*!40000 ALTER TABLE `SUBSCRIPTION_INFO` DISABLE KEYS */;
INSERT INTO `SUBSCRIPTION_INFO` VALUES ('user1',0,'1111222233334444',6000,'2020-09-28'),('user6',0,'0000111122223333',6000,'2020-12-05'),('yes',0,'9999888877776666',6000,'2020-11-29'),('user1',1,'1010202030304040',6000,'2020-11-28');
/*!40000 ALTER TABLE `SUBSCRIPTION_INFO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `album_intro`
--

DROP TABLE IF EXISTS `album_intro`;
/*!50001 DROP VIEW IF EXISTS `album_intro`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `album_intro` (
  `Album_Name` tinyint NOT NULL,
  `Album_Type` tinyint NOT NULL,
  `Lable` tinyint NOT NULL,
  `Release_Date` tinyint NOT NULL,
  `Nation` tinyint NOT NULL,
  `Introduction` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Album_Code` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `artist_album`
--

DROP TABLE IF EXISTS `artist_album`;
/*!50001 DROP VIEW IF EXISTS `artist_album`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `artist_album` (
  `Artist_ID` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Album_Code` tinyint NOT NULL,
  `Album_Name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `member_list`
--

DROP TABLE IF EXISTS `member_list`;
/*!50001 DROP VIEW IF EXISTS `member_list`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `member_list` (
  `Artist_ID` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Member_Name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `music_album`
--

DROP TABLE IF EXISTS `music_album`;
/*!50001 DROP VIEW IF EXISTS `music_album`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `music_album` (
  `ICN` tinyint NOT NULL,
  `Music_Name` tinyint NOT NULL,
  `Album_Code` tinyint NOT NULL,
  `Album_Name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `music_artist`
--

DROP TABLE IF EXISTS `music_artist`;
/*!50001 DROP VIEW IF EXISTS `music_artist`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `music_artist` (
  `ICN` tinyint NOT NULL,
  `Music_Name` tinyint NOT NULL,
  `Times_Of_Played` tinyint NOT NULL,
  `Artist_ID` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Genre` tinyint NOT NULL,
  `isTitle` tinyint NOT NULL,
  `isMain` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `music_artist_album`
--

DROP TABLE IF EXISTS `music_artist_album`;
/*!50001 DROP VIEW IF EXISTS `music_artist_album`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `music_artist_album` (
  `ICN` tinyint NOT NULL,
  `Music_Name` tinyint NOT NULL,
  `Times_Of_Played` tinyint NOT NULL,
  `Artist_ID` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Album_Code` tinyint NOT NULL,
  `Album_Name` tinyint NOT NULL,
  `Nation` tinyint NOT NULL,
  `IsTitle` tinyint NOT NULL,
  `isMain` tinyint NOT NULL,
  `Link` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `playlist_inst`
--

DROP TABLE IF EXISTS `playlist_inst`;
/*!50001 DROP VIEW IF EXISTS `playlist_inst`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `playlist_inst` (
  `ICN` tinyint NOT NULL,
  `Music_Name` tinyint NOT NULL,
  `Album_ID` tinyint NOT NULL,
  `Track_No` tinyint NOT NULL,
  `Age_Limit` tinyint NOT NULL,
  `Link` tinyint NOT NULL,
  `IsTitle` tinyint NOT NULL,
  `Times_Of_Played` tinyint NOT NULL,
  `Genre` tinyint NOT NULL,
  `L_No` tinyint NOT NULL,
  `Constructor_ID` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Music_No` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `statistics`
--

DROP TABLE IF EXISTS `statistics`;
/*!50001 DROP VIEW IF EXISTS `statistics`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `statistics` (
  `Music_Name` tinyint NOT NULL,
  `Times_Of_Played` tinyint NOT NULL,
  `Nick_Name` tinyint NOT NULL,
  `Genre` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Current Database: `MUSIC`
--

USE `MUSIC`;

--
-- Final view structure for view `album_intro`
--

/*!50001 DROP TABLE IF EXISTS `album_intro`*/;
/*!50001 DROP VIEW IF EXISTS `album_intro`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`album_intro` AS select `music`.`album`.`Album_Name` AS `Album_Name`,`music`.`album`.`Album_Type` AS `Album_Type`,`music`.`album`.`Lable` AS `Lable`,`music`.`album`.`Release_Date` AS `Release_Date`,`music`.`album`.`Nation` AS `Nation`,`music`.`album`.`Introduction` AS `Introduction`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`album`.`Album_Code` AS `Album_Code` from ((`music`.`album` join `music`.`album_of`) join `music`.`artist`) where `music`.`album_of`.`A_ID` = `music`.`artist`.`Artist_ID` and `music`.`album_of`.`Album_ID` = `music`.`album`.`Album_Code` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `artist_album`
--

/*!50001 DROP TABLE IF EXISTS `artist_album`*/;
/*!50001 DROP VIEW IF EXISTS `artist_album`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`artist_album` AS select `music`.`artist`.`Artist_ID` AS `Artist_ID`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`album`.`Album_Code` AS `Album_Code`,`music`.`album`.`Album_Name` AS `Album_Name` from ((`music`.`album` join `music`.`artist`) join `music`.`album_of`) where `music`.`album_of`.`A_ID` = `music`.`artist`.`Artist_ID` and `music`.`album_of`.`Album_ID` = `music`.`album`.`Album_Code` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `member_list`
--

/*!50001 DROP TABLE IF EXISTS `member_list`*/;
/*!50001 DROP VIEW IF EXISTS `member_list`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`member_list` AS select `music`.`artist`.`Artist_ID` AS `Artist_ID`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`member_of`.`Member_Name` AS `Member_Name` from (`music`.`member_of` join `music`.`artist`) where `music`.`member_of`.`Group_ID` = `music`.`artist`.`Artist_ID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `music_album`
--

/*!50001 DROP TABLE IF EXISTS `music_album`*/;
/*!50001 DROP VIEW IF EXISTS `music_album`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`music_album` AS select `music`.`music`.`ICN` AS `ICN`,`music`.`music`.`Music_Name` AS `Music_Name`,`music`.`album`.`Album_Code` AS `Album_Code`,`music`.`album`.`Album_Name` AS `Album_Name` from (`music`.`album` join `music`.`music`) where `music`.`music`.`Album_ID` = `music`.`album`.`Album_Code` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `music_artist`
--

/*!50001 DROP TABLE IF EXISTS `music_artist`*/;
/*!50001 DROP VIEW IF EXISTS `music_artist`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`music_artist` AS select `music`.`music`.`ICN` AS `ICN`,`music`.`music`.`Music_Name` AS `Music_Name`,`music`.`music`.`Times_Of_Played` AS `Times_Of_Played`,`music`.`artist`.`Artist_ID` AS `Artist_ID`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`music`.`Genre` AS `Genre`,`music`.`music`.`IsTitle` AS `isTitle`,`music`.`music_of`.`isMain` AS `isMain` from ((`music`.`artist` join `music`.`music`) join `music`.`music_of`) where `music`.`music`.`ICN` = `music`.`music_of`.`M_ICN` and `music`.`music_of`.`A_ID` = `music`.`artist`.`Artist_ID` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `music_artist_album`
--

/*!50001 DROP TABLE IF EXISTS `music_artist_album`*/;
/*!50001 DROP VIEW IF EXISTS `music_artist_album`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`music_artist_album` AS select `music`.`music`.`ICN` AS `ICN`,`music`.`music`.`Music_Name` AS `Music_Name`,`music`.`music`.`Times_Of_Played` AS `Times_Of_Played`,`music`.`artist`.`Artist_ID` AS `Artist_ID`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`album`.`Album_Code` AS `Album_Code`,`music`.`album`.`Album_Name` AS `Album_Name`,`music`.`album`.`Nation` AS `Nation`,`music`.`music`.`IsTitle` AS `IsTitle`,`music`.`music_of`.`isMain` AS `isMain`,`music`.`music`.`Link` AS `Link` from (((`music`.`artist` join `music`.`music`) join `music`.`music_of`) join `music`.`album`) where `music`.`music`.`ICN` = `music`.`music_of`.`M_ICN` and `music`.`music_of`.`A_ID` = `music`.`artist`.`Artist_ID` and `music`.`music`.`Album_ID` = `music`.`album`.`Album_Code` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `playlist_inst`
--

/*!50001 DROP TABLE IF EXISTS `playlist_inst`*/;
/*!50001 DROP VIEW IF EXISTS `playlist_inst`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`playlist_inst` AS select `music`.`music`.`ICN` AS `ICN`,`music`.`music`.`Music_Name` AS `Music_Name`,`music`.`music`.`Album_ID` AS `Album_ID`,`music`.`music`.`Track_No` AS `Track_No`,`music`.`music`.`Age_Limit` AS `Age_Limit`,`music`.`music`.`Link` AS `Link`,`music`.`music`.`IsTitle` AS `IsTitle`,`music`.`music`.`Times_Of_Played` AS `Times_Of_Played`,`music`.`music`.`Genre` AS `Genre`,`music`.`contain`.`L_No` AS `L_No`,`music`.`contain`.`Constructor_ID` AS `Constructor_ID`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`contain`.`Music_No` AS `Music_No` from (((`music`.`contain` join `music`.`music`) join `music`.`music_of`) join `music`.`artist`) where `music`.`contain`.`M_ICN` = `music`.`music`.`ICN` and `music`.`music_of`.`A_ID` = `music`.`artist`.`Artist_ID` and `music`.`music`.`ICN` = `music`.`music_of`.`M_ICN` and `music`.`music_of`.`isMain` = 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `statistics`
--

/*!50001 DROP TABLE IF EXISTS `statistics`*/;
/*!50001 DROP VIEW IF EXISTS `statistics`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `music`.`statistics` AS select `music`.`music`.`Music_Name` AS `Music_Name`,`music`.`music`.`Times_Of_Played` AS `Times_Of_Played`,`music`.`artist`.`Nick_Name` AS `Nick_Name`,`music`.`music`.`Genre` AS `Genre` from ((`music`.`artist` join `music`.`music`) join `music`.`music_of`) where `music`.`music`.`ICN` = `music`.`music_of`.`M_ICN` and `music`.`music_of`.`A_ID` = `music`.`artist`.`Artist_ID` and `music`.`music_of`.`isMain` = 1 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-05 14:32:38
