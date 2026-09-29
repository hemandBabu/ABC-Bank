-- Create and use the database
CREATE DATABASE IF NOT EXISTS banking_management;
USE banking_management;

-- 1. Customer Table
CREATE TABLE Customer (
    Customer_ID VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    address TEXT,
    phone VARCHAR(20)
);

-- 2. Branch Table
CREATE TABLE Branch (
    Branch_ID VARCHAR(50) PRIMARY KEY,
    Branch_Name VARCHAR(100) NOT NULL,
    Location VARCHAR(100)
);

-- 3. Employee Table
CREATE TABLE Employee (
    Employee_ID VARCHAR(50) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(50),
    Branch_ID VARCHAR(50),
    FOREIGN KEY (Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE SET NULL
);

-- 4. Account Table
CREATE TABLE Account (
    Account_Number VARCHAR(50) PRIMARY KEY,
    Balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    Account_Type VARCHAR(50) NOT NULL,
    Customer_ID VARCHAR(50) NOT NULL,
    FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_ID) ON DELETE CASCADE
);

-- 5. Transaction Table
CREATE TABLE Transaction (
    Transaction_ID VARCHAR(50) PRIMARY KEY,
    date DATETIME NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    Type VARCHAR(20) NOT NULL, -- 'Credit' or 'Debit'
    Account_Number VARCHAR(50) NOT NULL,
    FOREIGN KEY (Account_Number) REFERENCES Account(Account_Number) ON DELETE CASCADE
);
