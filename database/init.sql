-- 草药问答系统数据库初始化脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS caoyao_qa DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE caoyao_qa;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    avatar VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 题目表
CREATE TABLE IF NOT EXISTS questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    option_a VARCHAR(255) NOT NULL,
    option_b VARCHAR(255) NOT NULL,
    option_c VARCHAR(255) NOT NULL,
    option_d VARCHAR(255) NOT NULL,
    correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
    explanation TEXT,
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_difficulty (difficulty),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 答题记录表
CREATE TABLE IF NOT EXISTS answer_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    user_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
    is_correct BOOLEAN NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_question_id (question_id),
    INDEX idx_answered_at (answered_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 用户统计表
CREATE TABLE IF NOT EXISTS user_statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    total_questions INT DEFAULT 0,
    correct_answers INT DEFAULT 0,
    accuracy_rate DECIMAL(5,2) DEFAULT 0.00,
    last_study_date DATE,
    continuous_days INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入示例题目数据
INSERT INTO questions (question_text, option_a, option_b, option_c, option_d, correct_answer, explanation, difficulty, category) VALUES
('人参的主要功效是什么？', '清热解毒', '大补元气', '活血化瘀', '止咳平喘', 'B', '人参具有大补元气、复脉固脱、补脾益肺、生津养血、安神益智的功效。', 'easy', '补益药'),
('以下哪种草药具有清热解毒的功效？', '当归', '黄芪', '金银花', '枸杞', 'C', '金银花性寒，味甘，具有清热解毒、疏散风热的功效。', 'easy', '清热药'),
('枸杞子主要归哪条经？', '肝、肾经', '心、肺经', '脾、胃经', '肝、脾经', 'A', '枸杞子归肝、肾经，具有滋补肝肾、益精明目的功效。', 'medium', '补益药'),
('黄芪的性味是？', '寒、苦', '温、甘', '平、辛', '凉、酸', 'B', '黄芪性温，味甘，归脾、肺经，具有补气升阳、固表止汗的功效。', 'medium', '补益药'),
('以下哪种草药不适合阴虚火旺体质？', '麦冬', '百合', '附子', '沙参', 'C', '附子性大热，阴虚火旺者禁用，否则会加重阴虚症状。', 'hard', '温里药'),
('甘草在中药配伍中常起什么作用？', '君药', '佐药', '使药', '引药', 'C', '甘草常作为使药，具有调和诸药、缓急止痛的作用。', 'medium', '补益药'),
('当归的主要功效不包括以下哪项？', '补血活血', '调经止痛', '润肠通便', '清热解毒', 'D', '当归具有补血活血、调经止痛、润肠通便的功效，但不具有清热解毒作用。', 'easy', '补血药'),
('板蓝根主要用于治疗？', '风寒感冒', '风热感冒', '虚寒咳嗽', '脾虚腹泻', 'B', '板蓝根清热解毒，凉血利咽，主要用于治疗风热感冒、温病发热等。', 'easy', '清热药'),
('三七的主要功效是？', '补气', '止血化瘀', '温阳', '养阴', 'B', '三七具有止血、化瘀、定痛的功效，是止血化瘀的良药。', 'medium', '止血药'),
('以下哪种草药孕妇应慎用？', '黄芪', '红枣', '红花', '山药', 'C', '红花具有活血化瘀的作用，孕妇使用可能导致流产，应慎用。', 'hard', '活血药');

-- 插入测试用户（密码: test123，实际使用时应该是加密后的密码）
INSERT INTO users (username, password_hash, nickname) VALUES
('testuser', 'pbkdf2:sha256:260000$test$hashed_password', '测试用户');

-- 为测试用户创建统计记录
INSERT INTO user_statistics (user_id, total_questions, correct_answers, accuracy_rate) VALUES
(1, 0, 0, 0.00);
