--- Create Database
CREATE DATABASE aug_zerctech

--- Drop Database
USE [master]
DROP DATABASE aug_zerctech;

--- Create Table
USE [aug_zerctech]
CREATE TABLE employee(
employee_id CHAR(5) NOT NULL,
First_name VARCHAR(20) NOT NULL,
Last_name VARCHAR(20) NOT NULL,
DOB DATE NOT NULL,
Sex CHAR(1) NOT NULL,
Years_of_Service INT NULL
)

--- Drop Table
DROP TABLE employee;

--- Add column
ALTER TABLE employee
ADD State_of_Employee VARCHAR(20);

--- Drop Column
ALTER TABLE employee
DROP COLUMN State_of_Employee