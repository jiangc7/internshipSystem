SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for company
-- ----------------------------
DROP TABLE IF EXISTS `company`;
CREATE TABLE `company`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `street` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `city` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `region` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `website` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 17 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of company
-- ----------------------------
INSERT INTO company VALUES (1, 'Deloitte', 'Cambridge Terrace', 'Christchurch', 'NZ', 'www.Deloitte.com');
INSERT INTO company VALUES (2, 'PWC', 'Raptor Street', 'Christchurch', 'NZ', 'www.PWC.com');
INSERT INTO company VALUES (3, 'ABC Technologies', '123 Main Street', 'Auckland', 'NZ', 'www.abctech.com');
INSERT INTO company VALUES (4, 'XYZ Solutions', '456 Elm Street', 'Wellington', 'NZ', 'www.xyzsolutions.com');
INSERT INTO company VALUES (5, 'Tech Innovators', '789 Oak Street', 'Hamilton', 'NZ', 'www.techinnovators.com');
INSERT INTO company VALUES (6, 'Digital Systems', '321 Maple Street', 'Tauranga', 'NZ', 'www.digitalsystems.com');
INSERT INTO company VALUES (7, 'Infinite Tech', '654 Pine Street', 'Dunedin', 'NZ', 'www.infinitetech.com');
INSERT INTO company VALUES (8, 'Byte Wizards', '987 Cedar Street', 'Palmerston North', 'NZ', 'www.bytewizards.com');
INSERT INTO company VALUES (9, 'TechGenius', '159 Birch Street', 'Nelson', 'NZ', 'www.techgenius.com');
INSERT INTO company VALUES (10, 'IT Solutions', '753 Walnut Street', 'Rotorua', 'NZ', 'www.itsolutions.com');
INSERT INTO company VALUES (11, 'Code Masters', '246 Chestnut Street', 'New Plymouth', 'NZ', 'www.codemasters.com');
INSERT INTO company VALUES (12, 'Innovative Tech', '579 Hickory Street', 'Invercargill', 'NZ', 'www.innovativetech.com');

-- ----------------------------
-- Table structure for external_student
-- ----------------------------
DROP TABLE IF EXISTS `external_student`;
CREATE TABLE `external_student`  (
  `student_id_no` int NOT NULL AUTO_INCREMENT,
  `ifCurrentlyEnrolled` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '0- not enrolled, 1- enrolled',
  PRIMARY KEY (`student_id_no`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12345 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of external_student
-- ----------------------------
INSERT INTO `external_student` VALUES (12346, '0');
INSERT INTO `external_student` VALUES (12341, '1');
INSERT INTO `external_student` VALUES (12340, '1');
INSERT INTO `external_student` VALUES (12345, '1');

-- ----------------------------
-- Table structure for interviews
-- ----------------------------
DROP TABLE IF EXISTS `interviews`;
CREATE TABLE `interviews`  (
  `project_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  `interview_date` datetime NULL DEFAULT NULL,
  `interview_type` tinyint(1) NULL DEFAULT NULL COMMENT '0-online, 1- in site',
  `interview_status` tinyint(1) NULL DEFAULT NULL COMMENT '0-initial, 1- interview failed, 2-  interview passed, 3- offer sent, 4- offer accepted, 5- offer rejected',
  `interviewer` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`project_id`, `student_id`) USING BTREE,
  INDEX `student_id`(`student_id`) USING BTREE,
  INDEX `interviewer`(`interviewer`) USING BTREE,
  CONSTRAINT `interviews_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `interviews_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `interviews_ibfk_3` FOREIGN KEY (`interviewer`) REFERENCES `mentor` (`mentor_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of interviews
-- ----------------------------

-- ----------------------------
-- Table structure for mentor
-- ----------------------------
DROP TABLE IF EXISTS `mentor`;
CREATE TABLE `mentor`  (
  `mentor_id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `summary` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `company_id` bigint NULL DEFAULT NULL,
  INDEX `mentor_id`(`mentor_id`) USING BTREE,
  INDEX `company_id`(`company_id`) USING BTREE,
  CONSTRAINT `mentor_ibfk_1` FOREIGN KEY (`mentor_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mentor_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 171 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mentor
-- ----------------------------
INSERT INTO mentor VALUES (1, '0232345333', 'Patient and experienced', 1);
INSERT INTO mentor VALUES (2, '023145512', 'Good in business analysis', 2);
INSERT INTO mentor VALUES (3, '0208847125', 'Strong background and experience', 3);
INSERT INTO mentor VALUES (4, '0279284775', 'Skilled in UX and UI', 4);
INSERT INTO mentor VALUES (5, '0214567890', 'Expert in software development', 5);
INSERT INTO mentor VALUES (6, '0229876543', 'Specializes in data science', 6);
INSERT INTO mentor VALUES (7, '0277766554', 'Experienced in cybersecurity', 7);
INSERT INTO mentor VALUES (8, '0212345678', 'Knowledgeable in cloud computing', 8);
INSERT INTO mentor VALUES (9, '0209123456', 'Proficient in mobile app development', 9);
INSERT INTO mentor VALUES (10, '0228765432', 'Skilled in project management', 10);

-- ----------------------------
-- Table structure for mentor_student
-- ----------------------------
DROP TABLE IF EXISTS `mentor_student`;
CREATE TABLE `mentor_student`  (
  `student_id` bigint NOT NULL,
  `mentor_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`student_id`) USING BTREE,
  INDEX `mentor_id`(`mentor_id`) USING BTREE,
  CONSTRAINT `mentor_student_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `mentor_student_ibfk_2` FOREIGN KEY (`mentor_id`) REFERENCES `mentor` (`mentor_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of mentor_student
-- ----------------------------

-- ----------------------------
-- Table structure for project
-- ----------------------------
DROP TABLE IF EXISTS `project`;
CREATE TABLE `project`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `project_title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `number_of_student` int NULL DEFAULT NULL,
  `project_type` bigint NULL DEFAULT NULL,
  `start_date` datetime NULL DEFAULT NULL COMMENT 'to indicate if the project is current',
  `end_date` datetime NULL DEFAULT NULL COMMENT 'to indicate if the project is current',
  `remain_number_of_student` int NULL DEFAULT NULL COMMENT 'remain number of place',
  `mentor_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id`(`id`) USING BTREE,
  INDEX `project_type`(`project_type`) USING BTREE,
  INDEX `mentor_id`(`mentor_id`) USING BTREE,
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`project_type`) REFERENCES `project_type` (`type_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_ibfk_2` FOREIGN KEY (`mentor_id`) REFERENCES `mentor` (`mentor_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project
-- ----------------------------
INSERT INTO `project` VALUES (1, 'testProject', 'a good project', 2, 4, NULL, NULL, NULL, 20);
INSERT INTO `project` VALUES (2, 'Consultant', 'Technology Strategy and Transformation ', 5, 1, '2023-07-17 00:00:00', '2023-10-10 00:00:00', 3, 2);
INSERT INTO `project` VALUES (3, 'System Engineering Intern', 'Spend this summer helping transform the construction industry', 3, 2, '2023-07-17 00:00:00', '2023-10-10 00:00:00', 1, 2);
INSERT INTO `project` VALUES (4, 'Web Development Internship', 'Gain hands-on experience in web development and design', 3, 1, '2023-07-01 00:00:00', '2023-09-30 00:00:00', 3, 1);
INSERT INTO `project` VALUES (5, 'Data Analysis Project', 'Work on analyzing and interpreting large datasets for insights', 4, 2, '2023-07-05 00:00:00', '2023-10-15 00:00:00', 4, 2);
INSERT INTO `project` VALUES (6, 'Software Testing and Quality Assurance', 'Learn about testing methodologies and ensure software quality', 2, 1, '2023-07-10 00:00:00', '2023-09-20 00:00:00', 2, 3);
INSERT INTO `project` VALUES (7, 'IT Project Management', 'Assist in managing and coordinating IT projects', 5, 2, '2023-08-15 00:00:00', '2023-10-31 00:00:00', 5, 2);
INSERT INTO `project` VALUES (8, 'Network Infrastructure Optimization', 'Optimize network performance and troubleshoot issues', 4, 1, '2023-07-20 00:00:00', '2023-10-10 00:00:00', 4, 1);
INSERT INTO `project` VALUES (9, 'Cybersecurity Intern', 'Contribute to enhancing security measures and detecting vulnerabilities', 3, 2, '2023-08-01 00:00:00', '2023-09-30 00:00:00', 3, 3);
INSERT INTO `project` VALUES (10, 'Mobile App Development Project', 'Develop mobile applications for iOS and Android platforms', 5, 1, '2023-07-15 00:00:00', '2023-10-20 00:00:00', 5, 2);
INSERT INTO `project` VALUES (11, 'Database Management Internship', 'Assist in managing and optimizing databases for efficient data storage', 2, 2, '2023-07-25 00:00:00', '2023-09-15 00:00:00', 2, 1);
INSERT INTO `project` VALUES (12, 'IT Help Desk Support', 'Provide technical support and assist users with IT-related issues', 4, 1, '2023-08-10 00:00:00', '2023-10-31 00:00:00', 4, 3);
INSERT INTO `project` VALUES (13, 'Artificial Intelligence Project', 'Explore AI technologies and develop intelligent systems', 3, 2, '2023-07-10 00:00:00', '2023-09-30 00:00:00', 3, 2);
INSERT INTO `project` VALUES (14, 'Web Design Internship', 'Create visually appealing and user-friendly websites', 5, 1, '2023-07-30 00:00:00', '2023-10-15 00:00:00', 5, 1);
INSERT INTO `project` VALUES (15, 'IT Consulting Project', 'Provide consulting services and solutions for IT-related challenges', 4, 2, '2023-07-05 00:00:00', '2023-09-20 00:00:00', 4, 2);
INSERT INTO `project` VALUES (16, 'Cloud Computing Intern', 'Gain experience in managing and deploying cloud-based solutions', 6, 1, '2023-08-20 00:00:00', '2023-10-10 00:00:00', 6, 3);
INSERT INTO `project` VALUES (17, 'IT Infrastructure Management', 'Assist in managing and maintaining IT infrastructure components', 2, 2, '2023-07-15 00:00:00', '2023-09-30 00:00:00', 2, 2);
INSERT INTO `project` VALUES (18, 'Software Development Internship', 'Participate in developing software applications and solutions', 4, 1, '2023-07-10 00:00:00', '2023-10-31 00:00:00', 4, 1);
INSERT INTO `project` VALUES (19, 'UI/UX Design Project', 'Create intuitive user interfaces and optimize user experiences', 4, 1, '2023-07-10 00:00:00', '2023-10-31 00:00:00', 4, 1);

-- ----------------------------
-- Table structure for project_mentor
-- ----------------------------
DROP TABLE IF EXISTS `project_mentor`;
CREATE TABLE `project_mentor`  (
  `project_id` bigint NOT NULL,
  `mentor_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`project_id`) USING BTREE,
  INDEX `mentor_id`(`mentor_id`) USING BTREE,
  CONSTRAINT `project_mentor_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_mentor_ibfk_2` FOREIGN KEY (`mentor_id`) REFERENCES `mentor` (`mentor_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project_mentor
-- ----------------------------

-- ----------------------------
-- Table structure for project_skills
-- ----------------------------
DROP TABLE IF EXISTS `project_skills`;
CREATE TABLE `project_skills`  (
  `project_id` bigint NOT NULL,
  `skill_id` bigint NULL DEFAULT NULL,
  PRIMARY KEY (`project_id`) USING BTREE,
  INDEX `skill_id`(`skill_id`) USING BTREE,
  CONSTRAINT `project_skills_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `techs_and_skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project_skills
-- ----------------------------
INSERT INTO `project_skills` VALUES (1, 1);

-- ----------------------------
-- Table structure for project_type
-- ----------------------------
DROP TABLE IF EXISTS `project_type`;
CREATE TABLE `project_type`  (
  `type_id` bigint NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`type_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of project_type
-- ----------------------------
INSERT INTO `project_type` VALUES (1, 'ETC');
INSERT INTO `project_type` VALUES (2, 'computer science');
INSERT INTO `project_type` VALUES (3, 'business');
INSERT INTO `project_type` VALUES (4, 'agricultule');
INSERT INTO `project_type` VALUES (5, 'art');

-- ----------------------------
-- Table structure for question
-- ----------------------------
DROP TABLE IF EXISTS `question`;
CREATE TABLE `question`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of question
-- ----------------------------
INSERT INTO `question` VALUES (1, '\r{\"title\": \"Have you studied or are you currently studying COMP639 Studio Project with Pat Anthony?\",\r\"type\": \"1\",\r\"option\": [\r\"Yes - I am studying COMP639 this semester\", \"Yes - I completed and passed COMP639 in a previous semester\", \"I studied COMP639 but did not pass \", \"No - I have not started COMP639 yet \"\r]\r}\r');
INSERT INTO `question` VALUES (2, '{\r\"title\": \"Would you like us to help you find a match for a potential industry project?\",\r\"type\": \"1\",\r\"option\": [\"a.Yes - I will enter my details on the following pages\",\"b.No - I will exit the survey now\"]\r}');
INSERT INTO `question` VALUES (3, '{\r\"title\": \"Your location during your industry project (if not listed above)?\",\r\"type\": \"0\",\r\"option\": []\r}');
INSERT INTO `question` VALUES (4, '{\"title\": \"Where will you be located during the completion of your industry project?\",\r\"type\": \"1\",\r\"option\": [\"Christchurch\", \"Auckland\", \"Hamilton\", \"Wellinton\"]\r}');
INSERT INTO `question` VALUES (5, '{\"title\": \"Will you be attending the Christchurch industry speed networking event at Lincoln at 4pm on Thursday 25 May?\",\r	\"type\": \"1\",\r\"option\": [\"a.Yes \",\"b.No\"]\r}');
INSERT INTO `question` VALUES (6, '{\r\"title\": \"Have you submitted your CV and updated it?\",\r\"type\": \"1\",\r\"option\": [\"I have submitted my CV and it was approved\",\"I have submitted my CV and I have made the requested updates\",\"I have submitted my CV but I have not yet made the requested updates\",\"I have not yet submitted my CV\"]\r}');
INSERT INTO `question` VALUES (7, '{\n\"title\": \"Please click on the electives that you have studied or that you are currently studying.\",\n \"type\": \"2\",\n \"option\": [\"COMP627 Neural Networks\",\"COMP637 User Engagement and Business Analysis\",\"COMP640 User Experience\",\"COMP 642 Advanced Programming\",\"COMP 643 Advanced Database Management\",\"Geographic Information Systems (GIS)\",\"Other - please specify below\"]\n}');
INSERT INTO `question` VALUES (8, '{\r\"title\": \"Which of the following types of project would you like to work on?  (Choose all that apply).\",\r \"type\": \"2\",\r \"option\": [\"Technical Project - software development, testing, database, systems administration, GIS development\",\"Human-Centered project - business analysis, user experience, GIS analysis\"]\r}');
INSERT INTO `question` VALUES (9, '{\r\"title\": \"Please describe your background prior to starting the Master of Applied Computing, including your work experience, volunteering, and other studies.\",\r \"type\": \"3\",\r \"option\": []\r}');
INSERT INTO `question` VALUES (10, '{\r\"title\": \"Please describe your goals for after completing your studies, including the type of organisation you\'d like to work in.\",\r \"type\": \"3\",\r \"option\": []\r}');

-- ----------------------------
-- Table structure for question_answer
-- ----------------------------
DROP TABLE IF EXISTS `question_answer`;
CREATE TABLE `question_answer`  (
  `student_id` bigint NOT NULL,
  `question_id` bigint NOT NULL,
  `question_answer` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`student_id`, `question_id`) USING BTREE,
  INDEX `question_id`(`question_id`) USING BTREE,
  CONSTRAINT `question_answer_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `question_answer_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of question_answer
-- ----------------------------
INSERT INTO `question_answer` VALUES (166, 1, '0');
INSERT INTO `question_answer` VALUES (166, 2, '0');
INSERT INTO `question_answer` VALUES (166, 3, '111');
INSERT INTO `question_answer` VALUES (166, 4, '0');
INSERT INTO `question_answer` VALUES (166, 5, '0');
INSERT INTO `question_answer` VALUES (166, 6, '0');
INSERT INTO `question_answer` VALUES (166, 7, '1');
INSERT INTO `question_answer` VALUES (166, 8, '1');
INSERT INTO `question_answer` VALUES (166, 9, '1');
INSERT INTO `question_answer` VALUES (166, 10, '1');
INSERT INTO `question_answer` VALUES (167, 5, '0');
INSERT INTO `question_answer` VALUES (167, 6, '0');
INSERT INTO `question_answer` VALUES (167, 7, '[0,1,2]');
INSERT INTO `question_answer` VALUES (167, 8, '[0,1]');
INSERT INTO `question_answer` VALUES (167, 9, 'I am a good programmer with a lot of skills');
INSERT INTO `question_answer` VALUES (167, 10, 'I want find a job ASAP');
INSERT INTO `question_answer` VALUES (171, 1, '2');
INSERT INTO `question_answer` VALUES (171, 2, '0');
INSERT INTO `question_answer` VALUES (171, 4, '0');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `id` bigint NOT NULL,
  `student_id_no` int NULL DEFAULT NULL,
  `alternative_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `preferred_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `cv` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'a link of student cv',
  `project_preference` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `personal_statements` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `placement_status` tinyint(1) NULL DEFAULT NULL COMMENT '0- seeking oppurtunities,1- offer accepted,2- not available',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '0- male, 1- female, 2- neutral',
  `dateofbirth` date NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `student_ibfk_2`(`student_id_no`) USING BTREE,
  CONSTRAINT `student_ibfk_2` FOREIGN KEY (`student_id_no`) REFERENCES `external_student` (`student_id_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_ibfk_3` FOREIGN KEY (`id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (166, 123456, 'John Doe', 'John', '0212345678', 'www.example.com/cv', 'Web Development, Data Analysis', 'I am passionate about technology and eager to gain practical experience.', 0, 0, '1998-05-15');
INSERT INTO `student` VALUES (167, 987654, 'Jane Smith', 'Jane', '0223456789', 'www.example.com/cv', 'Software Engineering, Machine Learning', 'I am a dedicated learner and enjoy solving complex problems.', 0, 1, '1999-09-20');
INSERT INTO `student` VALUES (171, 654321, 'Alex Johnson', 'Alex', '0219876543', 'www.example.com/cv', 'UI/UX Design, Front-end Development', 'I have a keen eye for aesthetics and strive to create user-friendly interfaces.', 1, 1, '1997-12-10');


-- ----------------------------
-- Table structure for student_project
-- ----------------------------
DROP TABLE IF EXISTS `student_project`;
CREATE TABLE `student_project`  (
  `project_id` bigint NOT NULL,
  `student_id` bigint NULL DEFAULT NULL,
  `rank` tinyint NULL DEFAULT NULL,
  PRIMARY KEY (`project_id`) USING BTREE,
  INDEX `student_id`(`student_id`) USING BTREE,
  CONSTRAINT `student_project_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_project_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of student_project
-- ----------------------------
INSERT INTO `student_project` VALUES (1, 171, 1);
INSERT INTO `student_project` VALUES (2, 171, 0);
INSERT INTO `student_project` VALUES (3, 171, 2);

-- ----------------------------
-- Table structure for student_skills
-- ----------------------------
DROP TABLE IF EXISTS `student_skills`;
CREATE TABLE `student_skills`  (
  `student_id` bigint NOT NULL,
  `skill_id` bigint NOT NULL,
  PRIMARY KEY (`student_id`, `skill_id`) USING BTREE,
  INDEX `skill_id`(`skill_id`) USING BTREE,
  CONSTRAINT `student_skills_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `student_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `techs_and_skills` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of student_skills
-- ----------------------------

-- ----------------------------
-- Table structure for techs_and_skills
-- ----------------------------
DROP TABLE IF EXISTS `techs_and_skills`;
CREATE TABLE `techs_and_skills`  (
  `id` bigint NOT NULL,
  `skill_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of techs_and_skills
-- ----------------------------
INSERT INTO `techs_and_skills` VALUES (1, 'JAVA');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` bigint NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'formal first name',
  `last_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'formal last name',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'encrypted',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'email',
  `role` tinyint(1) NULL DEFAULT NULL COMMENT '0-staff, 1- mentor, 2- student',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 173 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (1, 'Jack', 'Ma', 'e10adc3949ba59abbe56e057f20f883e', 'jack.ma@jm.com', 1);
INSERT INTO `user` VALUES (2, 'Jim', 'Zhang', 'e10adc3949ba59abbe56e057f20f883e', 'jimZhang@jz.com', 1);
INSERT INTO `user` VALUES (3, 'Karen', 'Fiel', 'e10adc3949ba59abbe56e057f20f883e', 'kaFile@jzsd.com', 1);
INSERT INTO `user` VALUES (20, 'newUser', 'lasnamennnnki,ol', 'e10adc3949ba59abbe56e057f20f883e', 'aMentor', 1);
INSERT INTO `user` VALUES (21, '1', '1', 'e10adc3949ba59abbe56e057f20f883e', 'staff@c.com', 0);
INSERT INTO `user` VALUES (32, 'newUser', 'lasnamennnnki,ol', 'e10adc3949ba59abbe56e057f20f883e', 'liuwerwe32432@qwe.com123123', 0);
INSERT INTO `user` VALUES (127, 'Yang', 'Liu', 'e10adc3949ba59abbe56e057f20f883e', '123@123.com', 1);
INSERT INTO `user` VALUES (166, 'John Doe', 'John', 'e10adc3949ba59abbe56e057f20f883e', 'leon846666@gmail.com', 2);
INSERT INTO `user` VALUES (167, 'Jane Smith', 'Jane', 'e10adc3949ba59abbe56e057f20f883e', '123123@123.com', 2);
INSERT INTO `user` VALUES (171, 'Alex Johnson', 'Alex', 'e10adc3949ba59abbe56e057f20f883e', '273618706@qq.com', 2);


-- ----------------------------
-- Table structure for wishlist
-- ----------------------------
DROP TABLE IF EXISTS `wishlist`;
CREATE TABLE `wishlist`  (
  `project_id` bigint NOT NULL,
  `student_id` bigint NOT NULL,
  PRIMARY KEY (`project_id`, `student_id`) USING BTREE,
  INDEX `student_id`(`student_id`) USING BTREE,
  CONSTRAINT `wishlist_ibfk_1` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `wishlist_ibfk_2` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of wishlist
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;


