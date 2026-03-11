CREATE DATABASE smart_fee_management;
USE smart_fee_management;

-- Create Students Table
CREATE TABLE Students (
    Student_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(15),
    Course_ID INT,
    DOB DATE,
    Age INT,
    Gender ENUM('Male','Female','Other'),
    Address VARCHAR(255),
    Admission_Date DATE,
    Status VARCHAR(20) DEFAULT 'Active'
);

-- Create Courses Table
CREATE TABLE Courses (
    Course_ID INT AUTO_INCREMENT PRIMARY KEY,
    Course_Name VARCHAR(100) NOT NULL,
    Fee DECIMAL(10,2),
    Duration INT NOT NULL
);

-- Create Payments Table
CREATE TABLE Payments (
    Payment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Installment_No INT NOT NULL,
    Amount_Paid DECIMAL(10,2) NOT NULL,
    Payment_Date DATE NOT NULL,
    Payment_Mode VARCHAR(20) NOT NULL,
    Remaining_Balance DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);


-- Create Installments Table

CREATE TABLE Installments (
    Installment_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT NOT NULL,
    Installment_No INT NOT NULL,
    Due_Date DATE NOT NULL,
    Installment_Amount DECIMAL(10,2) NOT NULL,
    Paid_Amount DECIMAL(10,2) DEFAULT 0,
    Fine_Amount DECIMAL(10,2) DEFAULT 0,
    Status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (Student_ID) REFERENCES Students(Student_ID)
);

-- Create Scholarships Table

CREATE TABLE Scholarships (
    Scholarship_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID INT,
    Applied VARCHAR(10),
    Eligibility VARCHAR(20),
    Percentage DECIMAL(5,2),
    Approval_Status VARCHAR(20),
    Amount_Released DECIMAL(10,2),
   Approval_Date  DATE
);

CREATE TABLE Admin(
	Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Phone VARCHAR(15)
);

INSERT INTO Students (Name, Email, Password, Phone, Course_ID, DOB, Age, Gender, Address, Admission_Date, Status)
VALUES
('Rahul Sharma', 'rahul@email.com', 'hashedpwd1', '9876543210', 101, '2004-05-10', 21, 'Male', '123 MG Road, Delhi', '2026-01-05', 'Active'),
('Priya Singh', 'priya@email.com', 'hashedpwd2', '9876543211', 102, '2003-08-22', 22, 'Female', '45 Nehru Street, Pune', '2026-01-10', 'Active'),
('Aman Verma', 'aman@email.com', 'hashedpwd3', '9876543212', 101, '2005-02-15', 21, 'Male', '12 Park Lane, Mumbai', '2026-01-12', 'Active');

INSERT INTO Courses (Course_Name, Fee, Duration)
VALUES('BCA', 23000, 36),
('MCA', 31500, 24),
('BBA', 20000, 36);

INSERT INTO Payments (Student_ID, Installment_No, Amount_Paid, Payment_Date, Payment_Mode, Remaining_Balance)
VALUES
(1, 1, 10000, '2026-01-10', 'Cash', 13000),
(1, 2, 13000, '2026-02-10', 'Online', 0),
(2, 1, 15000, '2026-01-15', 'Cash', 16500);

INSERT INTO Installments (Student_ID, Installment_No, Due_Date, Installment_Amount, Paid_Amount, Fine_Amount, Status)
VALUES
(1, 1, '2026-01-10', 10000, 10000, 0, 'Paid'),
(1, 2, '2026-02-10', 13000, 13000, 0, 'Paid'),
(2, 1, '2026-01-15', 15000, 15000, 0, 'Paid');

INSERT INTO Scholarships (Student_ID, Applied, Eligibility, Percentage, Approval_Status, Amount_Released, Approval_Date)
VALUES
(1, 'Yes', 'Eligible', 5, 'Approved', 1150, '2026-02-01'),
(2, 'Yes', 'Eligible', 10, 'Pending', 0, NULL),
(3, 'No', 'Not Eligible', 0, 'Pending', 0, NULL);

INSERT INTO Admin (Name, Email, Password, Phone)
VALUES
('Admin One', 'admin1@email.com', 'adminpwd1', '9876500001'),
('Admin Two', 'admin2@email.com', 'adminpwd2', '9876500002'),
('Admin Three', 'admin3@email.com', 'adminpwd3', '9876500003');

SELECT * FROM Students;
SELECT * FROM Courses;
SELECT * FROM Payments;
SELECT * FROM Installments;
SELECT * FROM Scholarships;
SELECT * FROM Admin;

DELETE FROM Students
WHERE Student_ID = 6;

DELETE FROM Payments
WHERE Student_ID = 6;

DELETE FROM Installments
WHERE Student_ID = 6;

DELETE FROM Students
WHERE Student_ID = 6;

DELETE FROM Payments
WHERE Payment_ID = 6;

UPDATE Students SET Course_ID = 1 WHERE Student_ID = 1;
UPDATE Students SET Course_ID = 1 WHERE Student_ID = 2;
UPDATE Students SET Course_ID = 2 WHERE Student_ID = 3;

SELECT s.Student_ID, s.Name, c.Course_Name FROM Students s JOIN Courses c ON s.Course_ID = c.Course_ID;
SELECT Student_ID, SUM(Amount_Paid) AS Total_Paid FROM Payments GROUP BY Student_ID;
DESCRIBE installments;
SELECT Student_ID, Percentage, Approval_Status FROM Scholarships WHERE Approval_Status='Approved';
SELECT Student_ID, Installment_No, Due_Date FROM Installments WHERE Due_Date < CURDATE();
SELECT SUM(Amount_Paid) AS Total_Revenue FROM Payments;