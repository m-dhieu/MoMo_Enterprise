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


-- Participants(Transaction) Table
CREATE TABLE TransactionParticipant (
    ParticipantID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique participant entry identifier',
    TransactionID INT NOT NULL COMMENT 'Foreign key to transaction',
    UserID INT NOT NULL COMMENT 'Foreign key to user',
    Role ENUM('sender', 'receiver', 'agent') NOT NULL COMMENT 'Participant role in transaction',
    FOREIGN KEY (TransactionID) REFERENCES Transaction(TransactionID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
) COMMENT='Participants involved in each transaction';

-- Insert sample data into TransactionParticipant
INSERT INTO TransactionParticipant (TransactionID, UserID, Role) VALUES
(1, 4, 'sender'),
(1, 3, 'agent'),
(2, 1, 'sender'),
(2, 2, 'receiver'),
(3, 4, 'sender'),
(3, 2, 'receiver'),
(3, 3, 'agent'),
(4, 1, 'sender'),
(5, 4, 'sender');

-- SystemLog Table
CREATE TABLE SystemLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique system log identifier',
    Timestamp DATETIME NOT NULL COMMENT 'Log entry timestamp',
    LogLevel ENUM('info', 'warning', 'error') NOT NULL COMMENT 'Level of log severity',
    Message TEXT NOT NULL COMMENT 'Log message content'
) COMMENT='Logs related to system processes like ETL, validation, errors';

-- Index time stamp for log queries
CREATE INDEX idx_systemlog_timestamp ON SystemLog(Timestamp);

-- Insert sample data into SystemLog
INSERT INTO SystemLog (Timestamp, LogLevel, Message) VALUES
('2025-09-15 09:00:00', 'info', 'ETL process started'),
('2025-09-15 09:01:00', 'info', 'Transaction data loaded'),
('2025-09-15 09:02:00', 'warning', 'Missing reference number in transaction 4'),
('2025-09-15 09:03:00', 'error', 'Failed to process transaction 6'),
('2025-09-15 09:04:00', 'info', 'ETL process completed');

-- Promotions Table
CREATE TABLE Promotion (
    PromotionID INT PRIMARY KEY AUTO_INCREMENT COMMENT 'Unique promotion identifier',
    PromotionType VARCHAR(50) COMMENT 'Type of promotion or alert',
    Message TEXT COMMENT 'Promotion or alert message content',
    ValidFrom DATE COMMENT 'Promotion start date',
    ValidTo DATE COMMENT 'Promotion end date'
) COMMENT='Promotions or security alerts associated with transactions';

-- Insert sample data into Promotion
INSERT INTO Promotion (PromotionType, Message, ValidFrom, ValidTo) VALUES
('promotion', 'Double cashback on deposits', '2025-09-01', '2025-09-30'),
('security alert', 'Unauthorized login detected', '2025-09-12', '2025-09-18'),
('promotion', 'Fee waiver on first 3 transactions', '2025-09-05', '2025-09-20'),
('promotion', 'Refer a friend and earn 5000 RWF', '2025-09-10', '2025-10-10'),
('security alert', 'Password change required', '2025-09-14', '2025-09-21');



