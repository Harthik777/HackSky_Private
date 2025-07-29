-- MySQL initialization script for HackSky ICS Monitoring
-- This script will run when the MySQL container starts for the first time

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ics_monitoring;

-- Use the database
USE ics_monitoring;

-- Grant all privileges to the hacksky user
GRANT ALL PRIVILEGES ON ics_monitoring.* TO 'hacksky'@'%';
FLUSH PRIVILEGES;

-- Optional: Create some initial configuration
SET time_zone = '+00:00';
SET sql_mode = 'NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
