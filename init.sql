
USE `sb_bots`;

/* CREATE 
   note:
   no point in having card_type reference table,
   lookup card_type from enum in app
*/

CREATE TABLE IF NOT EXISTS `cah_card` (
  `card_id` BIGINT(20) UNSIGNED NOT NULL,
  `card_type` TINYINT(4) UNSIGNED NOT NULL,
  `message` VARCHAR(255) NOT NULL COLLATE 'utf8_unicode_ci',
  PRIMARY KEY (`card_id`),
  INDEX `card_id` (`card_id`)
) COLLATE='utf8_unicode_ci' ENGINE=InnoDB;

/* Insert 
   Test Data
   
   6 Test Questions
   20 Test Answers
*/

INSERT INTO sb_bots.cah_card 
VALUES 
	('1','2','Question 1'),
	('2','2','Question 2'),
	('3','2','Question 3'),
	('4','2','Question 4'),
	('5','2','Question 5'),
	('6','2','Question 6'),
	('7','1','Answer 1'),
	('8','1','Answer 2'),
	('9','1','Answer 3'),
	('10','1','Answer 4'),
	('11','1','Answer 5'),
	('12','1','Answer 6'),
	('13','1','Answer 7'),
	('14','1','Answer 8'),
	('15','1','Answer 9'),
	('16','1','Answer 10'),
	('17','1','Answer 11'),
	('18','1','Answer 12'),
	('19','1','Answer 13'),
	('20','1','Answer 14'),
	('21','1','Answer 15'),
	('22','1','Answer 16'),
	('23','1','Answer 17'),
	('24','1','Answer 18'),
	('25','1','Answer 19'),
	('26','1','Answer 20')
