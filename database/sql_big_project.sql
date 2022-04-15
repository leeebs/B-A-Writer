## create database test7; #데이터베이스 생성

## use test7; #데이터베이스 사용
# autoincrement 지정
# primarykey지정 
############################################## 테이블 생성 ################################
DROP TABLE IF EXISTS `member`;

CREATE TABLE `member` (
	`member_no`	int	NOT NULL AUTO_INCREMENT	PRIMARY KEY,
	`member_id`	varchar(20)	NOT NULL,
	`member_password`	varchar(30)	NOT NULL,
	`member_email`	varchar(30)	NOT NULL,
	`member_name`	varchar(20)	NOT NULL,
	`member_type`	tinyint	NOT NULL	DEFAULT 0	COMMENT '일반사용자:0, 관리자:1'
);

DROP TABLE IF EXISTS `storybook`;

CREATE TABLE `storybook` (
	`book_no`	int	NOT NULL AUTO_INCREMENT	PRIMARY KEY,
	`book_con`	longtext	NOT NULL,
	`book_date`	datetime	NOT NULL	DEFAULT now(),
	`member_no`	int	NOT NULL
);

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
	`rating_no`	int	NOT NULL AUTO_INCREMENT,
	`member_no`	int	NOT NULL,
	`book_no`	int	NOT NULL,
	`rating`	int	NOT NULL,
    PRIMARY KEY(`rating_no`, `member_no`, `book_no`)
);

DROP TABLE IF EXISTS `image`;

CREATE TABLE `image` (
	`img_no`	int	NOT NULL AUTO_INCREMENT,
	`book_no`	int	NOT NULL,
	`img_path`	varchar(500)	NOT NULL,
    PRIMARY KEY(`img_no`, `book_no`)
);

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
	`question_no`	int	NOT NULL AUTO_INCREMENT	PRIMARY KEY,
	`ques_title` varchar(50) NOT NULL,
	`ques_con`	varchar(1000)	NOT NULL,
	`ques_date`	datetime	NOT NULL	DEFAULT now(),
	`member_no`	int	NOT NULL
);

DROP TABLE IF EXISTS `question_comment`;

CREATE TABLE `question_comment` (
	`comment_no`	int	NOT NULL AUTO_INCREMENT,
	`member_no`	int	NOT NULL,
	`question_no`	int	NOT NULL,
	`comment_con`	varchar(200)	NOT NULL,
	`comment_date`	datetime	NOT NULL	DEFAULT now(),
    PRIMARY KEY(`comment_no`, `member_no`, `question_no`)
);


commit;

##############################더미데이터 삽입###################################

select * from member;
select * from storybook;
select * from rating;
select * from image;
select * from question;
select * from question_comment;

-- 프로시저 삭제 코드
DROP PROCEDURE IF EXISTS loopInsert_member;
DROP PROCEDURE IF EXISTS loopInsert_storybook;
DROP PROCEDURE IF EXISTS loopInsert_rating;
DROP PROCEDURE IF EXISTS loopInsert_image;
DROP PROCEDURE IF EXISTS loopInsert_question;
DROP PROCEDURE IF EXISTS loopInsert_question_comment;

#멤버더미
DELIMITER $$
 
CREATE PROCEDURE loopInsert_member()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO member(member_id, member_password , member_email, member_name)
          VALUES(concat('id',i), concat('pass',i), concat('email',i), concat('이름',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE loopInsert_storybook()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO storybook(book_con, book_date, member_no)
          VALUES(concat('con',i), now(), i/2);
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

#평점더미
DELIMITER $$
 
CREATE PROCEDURE loopInsert_rating()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO rating(member_no, book_no, rating)
          VALUES(i/2, i/2, i%5);
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


# 이미지더미
DELIMITER $$
CREATE PROCEDURE loopInsert_image()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO image(book_no, img_path)
          VALUES(i/2, concat('경로',i));
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


# 문의더미
DELIMITER $$
CREATE PROCEDURE loopInsert_question()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO question(ques_title, ques_con, ques_date, member_no)
          VALUES(concat('제목',i), concat('문의내용',i), now(), i/2);
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;


# 문의댓글더미
DELIMITER $$
CREATE PROCEDURE loopInsert_question_comment()
BEGIN
    DECLARE i INT DEFAULT 1;
        
    WHILE i <= 50 DO
        INSERT INTO question_comment(member_no, question_no, comment_con, comment_date)
          VALUES(i/2, i/2, concat('댓글내용',i), now() );
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

CALL loopInsert_member;
CALL loopInsert_storybook;
CALL loopInsert_rating;
CALL loopInsert_image;
CALL loopInsert_question;
CALL loopInsert_question_comment;

select * from member;
select * from storybook;
select * from rating;
select * from image;
select * from question;
select * from question_comment;

############################################### cascade 적용 ####################################
###########################################################################################

ALTER TABLE `storybook` ADD CONSTRAINT `FK_member_TO_storybook_1` FOREIGN KEY (
	`member_no`
)
REFERENCES `member` (
	`member_no`
)on delete cascade;

ALTER TABLE `rating` ADD CONSTRAINT `FK_storybook_TO_rating_1` FOREIGN KEY (
	`book_no`
)
REFERENCES `storybook` (
	`book_no`
)on delete cascade;

ALTER TABLE `rating` ADD CONSTRAINT `FK_member_TO_rating_1` FOREIGN KEY (
	`member_no`
)
REFERENCES `member` (
	`member_no`
)on delete cascade;

ALTER TABLE `image` ADD CONSTRAINT `FK_storybook_TO_image_1` FOREIGN KEY (
	`book_no`
)
REFERENCES `storybook` (
	`book_no`
)on delete cascade;

ALTER TABLE `question` ADD CONSTRAINT `FK_member_TO_question_1` FOREIGN KEY (
	`member_no`
)
REFERENCES `member` (
	`member_no`
)on delete cascade;

ALTER TABLE `question_comment` ADD CONSTRAINT `FK_member_TO_question_comment_1` FOREIGN KEY (
	`member_no`
)
REFERENCES `member` (
	`member_no`
)on delete cascade;


ALTER TABLE `question_comment` ADD CONSTRAINT `FK_question_TO_question_comment_1` FOREIGN KEY (
	`question_no`
)
REFERENCES `question` (
	`question_no`
)on delete cascade;

commit;


######################################################test code #################################

delete from question_comment where comment_no = 1;

select * from member;
select * from storybook;
select * from rating;
select * from image;
select * from question;

select * from question_comment;


delete from question where question_no = 1;
