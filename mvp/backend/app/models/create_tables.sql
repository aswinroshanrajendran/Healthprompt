-- SQL script to create tables for users and activity_log

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
	lastname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    isadmin BOOLEAN DEFAULT FALSE
);

-- Create the activity_log table
CREATE TABLE activity_logs (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    detail TEXT,
    source_language TEXT,
    recognized_text TEXT,
    ner_result TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- creating a table to store clinical notes
CREATE TABLE clinical_notes (
    id SERIAL PRIMARY KEY,
    nct_id VARCHAR(255) UNIQUE NOT NULL,
    note_type VARCHAR(255),
    note_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Create the feedback table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    feedback JSON NOT NULL
);