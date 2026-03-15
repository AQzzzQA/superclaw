-- MySQL初始化脚本

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS dsp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（如果不存在）
CREATE USER IF NOT EXISTS 'dsp_user'@'%' IDENTIFIED BY '${MYSQL_PASSWORD}';

-- 授予权限
GRANT ALL PRIVILEGES ON dsp_db.* TO 'dsp_user'@'%';
FLUSH PRIVILEGES;

-- 使用数据库
USE dsp_db;

-- 创建初始表结构（示例）
CREATE TABLE IF NOT EXISTS migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(255) NOT NULL UNIQUE,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入初始迁移记录
INSERT INTO migrations (version) VALUES ('initial') ON DUPLICATE KEY UPDATE version=version;
