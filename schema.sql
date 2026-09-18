-- ATM Demo — database schema
-- Run this once against your MySQL server before starting the app:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS atm_db;
USE atm_db;

CREATE TABLE IF NOT EXISTS users (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100)   NOT NULL,
    account_number  VARCHAR(20)    NOT NULL UNIQUE,
    pin             VARCHAR(255)   NOT NULL,   -- stores a hashed PIN, not plaintext
    balance         DECIMAL(12,2)  NOT NULL DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS transactions (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    user_id           INT NOT NULL,
    transaction_type  ENUM('DEPOSIT', 'WITHDRAW') NOT NULL,
    amount            DECIMAL(12,2) NOT NULL,
    transaction_date  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sample login for testing:
--   Account number: 1234567890
--   PIN:             1234
-- The value below is werkzeug's generate_password_hash('1234') — NOT the
-- plaintext PIN. Use seed_user.py to create additional users with your
-- own PINs correctly hashed.
INSERT INTO users (name, account_number, pin, balance)
VALUES (
    'Test User',
    '1234567890',
    'scrypt:32768:8:1$WkflH1NvkqU3RCPa$72e5ae65a05eb2897a24ff5d9b8cb3b096158b085aa6102cbc1e342b01d989484614a09506debdaf2d32124d70f3cb35d849ceb57b2b7d58f45ddfa1ef689cac',
    5000.00
);
