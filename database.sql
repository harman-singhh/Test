-- ================================================
-- CodeCraft Academy - Programming & Tech Skills
-- Tutoring Hub Database
-- Import this file in phpMyAdmin
-- ================================================

CREATE DATABASE IF NOT EXISTS codecraft_academy_db;
USE codecraft_academy_db;

-- ------------------------------------------------
-- Table: admins
-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default admin -> email: admin@gmail.com | password: admin123
-- (password below is werkzeug generate_password_hash('admin123'))
INSERT INTO admins (username, email, password) VALUES
('admin', 'admin@gmail.com', 'pbkdf2:sha256:600000$2fL0z3s6DlYVGgKX$0000000000000000000000000000000000000000000000000000000000000');

-- NOTE: The placeholder hash above is a template. app.py automatically
-- re-hashes and repairs this row on first run via ensure_default_admin(),
-- so the login admin@gmail.com / admin123 always works out of the box.

-- ------------------------------------------------
-- Table: contact_messages
-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS contact_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(200),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------
-- Table: courses  (tech/coding tutoring courses)
-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    image VARCHAR(255),
    duration VARCHAR(100),
    price DECIMAL(10,2) DEFAULT 0.00,
    syllabus_link VARCHAR(255),
    demo_link VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------
-- Table: tutors
-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS tutors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    expertise VARCHAR(200) NOT NULL,
    bio TEXT,
    experience_years INT DEFAULT 0,
    email VARCHAR(150),
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------
-- Table: testimonials
-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(150) NOT NULL,
    course_taken VARCHAR(150),
    message TEXT NOT NULL,
    rating INT DEFAULT 5,
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------
-- Table: bookings (students booking a tutoring session)
-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    course_id INT,
    preferred_date DATE,
    preferred_time VARCHAR(50),
    message TEXT,
    status ENUM('Pending','Confirmed','Completed','Cancelled') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
);
