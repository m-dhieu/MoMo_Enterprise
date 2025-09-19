--------------------------------------------------------------------------------
-- Script Name: database_setup.sql
-- Description: Creates and documents the MTN Mobile Money transaction database schema. 
--              Includes table creation, constraints, comments, indexes, and sample data.
-- Author: Thierry Gabin & Janviere Munezero
-- Date:   2025-09-18
-- Usage:  Executed by a DBMS
--------------------------------------------------------------------------------

-- Users Table
CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Auto-generated ID for each user to internally track and link records',
    PhoneNumber VARCHAR(20) NOT NULL UNIQUE COMMENT 'This is User’s phone number to serves as their unique identifier across transactions',
    Name VARCHAR(255) COMMENT 'User full name',
    UserType ENUM('sender', 'receiver', 'agent') NOT NULL COMMENT 'Role of user in transaction'
) COMMENT='User table to store mobile money account owners and contacts involved in transactions';

-- Inserted sample data into User
INSERT INTO User (PhoneNumber, Name, UserType) VALUES
('+250780123456', 'Jane Smith', 'sender'),
('+250781234567', 'Samuel Carter', 'receiver'),
('+250782345678', 'Alice Johnson', 'agent'),
('+250793456789', 'Michael Brown', 'sender'),
('+250784567890', 'Emily Davis', 'receiver');

-- Index phone number for quick lookup
CREATE INDEX idx_user_phonenumber ON User(PhoneNumber);

-- Categories(Transaction) Table
CREATE TABLE TransactionCategory (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique identifier for transaction category',
    CategoryName VARCHAR(50) NOT NULL UNIQUE COMMENT 'Category name to store deposit, payment, transfer, and ...',
    Description TEXT COMMENT 'Description about the category'
) COMMENT='TransactionCategory table for categorizing transactions for reporting and analytics';

-- Inserted sample data into TransactionCategory
INSERT INTO TransactionCategory (CategoryName, Description) VALUES
('deposit', 'Money added to account'),
('payment', 'Payment for goods or services'),
('transfer', 'Transfer between accounts'),
('withdrawal', 'Cash withdrawn from account'),
('fee', 'Transaction fee charged');

-- Transactions Table
CREATE TABLE Transaction (
    TransactionID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique transaction record identifier',
    TransactionType VARCHAR(50) NOT NULL COMMENT 'Type of transaction, e.g., deposit, payment',
    Amount DECIMAL(15, 2) NOT NULL CHECK (Amount >= 0) COMMENT 'Transaction amount',
    Currency VARCHAR(10) NOT NULL COMMENT 'Currency code like RWF,UGX,USD, ...',
    DateTime DATETIME NOT NULL COMMENT 'Timestamp of the transaction',
    ReferenceNumber VARCHAR(100) COMMENT 'Payment token or voucher number',
    BalanceAfterTransaction DECIMAL(15, 2) COMMENT 'Account balance after transaction',
    Status ENUM('confirmed', 'failed', 'pending') NOT NULL COMMENT 'Transaction status',
    MessageText TEXT COMMENT 'Full original SMS message content',
    CategoryID INT COMMENT 'Category for transaction',
    FOREIGN KEY (CategoryID) REFERENCES TransactionCategory(CategoryID)
) COMMENT='Mobile money transaction records';

-- Inserted sample data into Transaction
INSERT INTO Transaction (TransactionType, Amount, Currency, DateTime, ReferenceNumber, BalanceAfterTransaction, Status, MessageText, CategoryID) VALUES
('deposit', 100000.00, 'RWF', '2025-09-10 14:30:00', 'REF12345', 150000.00, 'confirmed', 'Deposit of 100000 RWF successful', 1),
('payment', 50000.00, 'RWF', '2025-09-11 09:15:00', 'PAY54321', 100000.00, 'confirmed', 'Payment of 50000 RWF to merchant', 2),
('transfer', 20000.00, 'RWF', '2025-09-12 16:45:00', 'TRF67890', 80000.00, 'confirmed', 'Transferred 20000 RWF to +250781234567', 3),
('withdrawal', 30000.00, 'RWF', '2025-09-13 11:00:00', 'WDL11223', 50000.00, 'pending', 'Withdrawal request of 30000 RWF', 4),
('fee', 1000.00, 'RWF', '2025-09-14 08:00:00', NULL, 49000.00, 'confirmed', 'Transaction fee charged: 1000 RWF', 5);

-- Index date and time for query performance
CREATE INDEX idx_transaction_datetime ON Transaction(DateTime);




