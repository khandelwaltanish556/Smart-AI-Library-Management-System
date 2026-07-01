-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 01, 2026 at 02:26 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smart_library1`
--

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `position` varchar(100) DEFAULT NULL,
  `resume` varchar(255) DEFAULT NULL,
  `applied_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `attendance_id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `attendance_date` date DEFAULT NULL,
  `status` enum('Present','Absent','Leave') DEFAULT NULL,
  `check_in_time` time DEFAULT NULL,
  `check_out_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`attendance_id`, `member_id`, `attendance_date`, `status`, `check_in_time`, `check_out_time`) VALUES
(12, 1, '2026-06-28', 'Present', '14:32:00', '06:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `book_id` int(11) NOT NULL,
  `book_name` varchar(255) NOT NULL,
  `author` varchar(255) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT 1,
  `available_quantity` int(11) DEFAULT 1,
  `added_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `title` varchar(255) DEFAULT NULL,
  `available_qty` int(20) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`book_id`, `book_name`, `author`, `category`, `quantity`, `available_quantity`, `added_date`, `title`, `available_qty`, `image`) VALUES
(1, 'Python Programming', 'Eric Matthes', 'Programming', 20, 18, '2026-06-30 16:38:43', NULL, NULL, 'python.jpg'),
(2, 'Java Complete Reference', 'Herbert Schildt', 'Programming', 15, 12, '2026-06-30 16:38:43', NULL, NULL, 'java.jpg'),
(3, 'C Programming Language', 'Dennis Ritchie', 'Programming', 18, 15, '2026-06-30 16:38:43', NULL, NULL, 'c.jpg'),
(4, 'Machine Learning Basics', 'Andrew Ng', 'AI', 10, 8, '2026-06-30 16:38:43', NULL, NULL, 'ml.jpg'),
(5, 'Deep Learning Guide', 'Ian Goodfellow', 'AI', 12, 10, '2026-06-30 16:38:43', NULL, NULL, 'deep.jpg'),
(6, 'Data Science Handbook', 'Jake VanderPlas', 'Data Science', 14, 11, '2026-06-30 16:38:43', NULL, NULL, 'data science.jpg'),
(7, 'Flask Web Development', 'Miguel Grinberg', 'Web Development', 10, 9, '2026-06-30 16:38:43', NULL, NULL, 'flask.jpg'),
(8, 'Django for Beginners', 'William S. Vincent', 'Web Development', 16, 13, '2026-06-30 16:38:43', NULL, NULL, 'uploads/books/django.jpg'),
(9, 'Learning SQL', 'Alan Beaulieu', 'Database', 20, 17, '2026-06-30 16:38:43', NULL, NULL, 'sql.jpg'),
(10, 'HTML & CSS Design', 'Jon Duckett', 'Web Development', 25, 22, '2026-06-30 16:38:43', NULL, NULL, 'web.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `book_rating`
--

CREATE TABLE `book_rating` (
  `rating_id` int(11) NOT NULL,
  `book_id` int(11) DEFAULT NULL,
  `member_id` int(11) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `review` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `chatbot_history`
--

CREATE TABLE `chatbot_history` (
  `chat_id` int(11) NOT NULL,
  `question` text DEFAULT NULL,
  `answer` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `course_progress`
--

CREATE TABLE `course_progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `course_name` varchar(100) DEFAULT NULL,
  `progress` int(11) DEFAULT 0,
  `completed` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fees`
--

CREATE TABLE `fees` (
  `fee_id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `admission_no` varchar(50) DEFAULT NULL,
  `member_name` varchar(100) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  `payment_method` enum('Cash','UPI','Card','Net Banking') DEFAULT NULL,
  `status` enum('Paid','Pending') DEFAULT 'Paid'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `issued_books`
--

CREATE TABLE `issued_books` (
  `issue_id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `return_date` date DEFAULT NULL,
  `status` enum('Issued','Returned','Late') DEFAULT 'Issued',
  `fine_amount` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` int(11) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `experience` varchar(50) DEFAULT NULL,
  `skills` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `members`
--

CREATE TABLE `members` (
  `member_id` int(11) NOT NULL,
  `admission_no` varchar(50) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `course` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `join_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `members`
--

INSERT INTO `members` (`member_id`, `admission_no`, `full_name`, `email`, `phone`, `gender`, `course`, `address`, `join_date`) VALUES
(1, 'ADM2026001', 'Aarav Sharma', 'aarav.sharma@gmail.com', '9876543210', 'Male', 'BCA', 'Jaipur, Rajasthan', '2026-01-10'),
(2, 'ADM2026002', 'Priya Verma', 'priya.verma@gmail.com', '9876543211', 'Female', 'B.Tech', 'Delhi', '2026-01-12'),
(3, 'ADM2026003', 'Rohan Mehta', 'rohan.mehta@gmail.com', '9876543212', 'Male', 'MCA', 'Indore', '2026-01-15'),
(4, 'ADM2026004', 'Sneha Patel', 'sneha.patel@gmail.com', '9876543213', 'Female', 'BCA', 'Ahmedabad', '2026-01-18'),
(5, 'ADM2026005', 'Aditya Singh', 'aditya.singh@gmail.com', '9876543214', 'Male', 'B.Sc IT', 'Lucknow', '2026-01-20'),
(6, 'ADM2026006', 'Neha Gupta', 'neha.gupta@gmail.com', '9876543215', 'Female', 'MBA', 'Noida', '2026-01-22'),
(7, 'ADM2026007', 'Rahul Yadav', 'rahul.yadav@gmail.com', '9876543216', 'Male', 'B.Com', 'Bhopal', '2026-01-25'),
(8, 'ADM2026008', 'Pooja Joshi', 'pooja.joshi@gmail.com', '9876543217', 'Female', 'BBA', 'Pune', '2026-01-28'),
(9, 'ADM2026009', 'Vikas Kumar', 'vikas.kumar@gmail.com', '9876543218', 'Male', 'M.Tech', 'Chandigarh', '2026-02-01'),
(10, 'ADM2026010', 'Anjali Mishra', 'anjali.mishra@gmail.com', '9876543219', 'Female', 'BCA', 'Kota, Rajasthan', '2026-02-05');

-- --------------------------------------------------------

--
-- Table structure for table `notices`
--

CREATE TABLE `notices` (
  `notice_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `message` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notices`
--

INSERT INTO `notices` (`notice_id`, `title`, `message`, `created_at`, `date`) VALUES
(1, 'Intractive Sesstion', 'All Student 26-06-2026 in 6:00 pm interactive sesstion in online meeting to please join the sesstion at a time attendance complusory.', '2026-06-24 10:55:28', '2026-06-26');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','student') DEFAULT 'student',
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password`, `role`, `address`, `created_at`) VALUES
(1, 'tanish', 'tanish@gmail.com', 'Admin@123', 'admin', 'Jaipur, Rajasthan', '2026-06-28 06:04:26'),
(2, 'aarav', 'aarav@gmail.com', 'Aarav@101', 'student', 'Delhi', '2026-06-28 06:04:26'),
(3, 'priya', 'priya@gmail.com', 'Priya@202', 'student', 'Mumbai', '2026-06-28 06:04:26'),
(4, 'rohan', 'rohan@gmail.com', 'Rohan@303', 'student', 'Indore', '2026-06-28 06:04:26'),
(5, 'sneha', 'sneha@gmail.com', 'Sneha@404', 'student', 'Pune', '2026-06-28 06:04:26'),
(6, 'aditya', 'aditya@gmail.com', 'Aditya@505', 'admin', 'Lucknow', '2026-06-28 06:04:26'),
(7, 'neha', 'neha@gmail.com', 'Neha@606', 'student', 'Ahmedabad', '2026-06-28 06:04:26'),
(8, 'rahul', 'rahul@gmail.com', 'Rahul@707', 'student', 'Noida', '2026-06-28 06:04:26'),
(9, 'pooja', 'pooja@gmail.com', 'Pooja@808', 'student', 'Bhopal', '2026-06-28 06:04:26'),
(10, 'karan', 'karan@gmail.com', 'Karan@909', 'admin', 'Chandigarh', '2026-06-28 06:04:26');

-- --------------------------------------------------------

--
-- Table structure for table `user_book_history`
--

CREATE TABLE `user_book_history` (
  `history_id` int(11) NOT NULL,
  `member_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  `action_type` enum('view','issue','return','search') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`attendance_id`),
  ADD KEY `member_id` (`member_id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`book_id`);

--
-- Indexes for table `book_rating`
--
ALTER TABLE `book_rating`
  ADD PRIMARY KEY (`rating_id`);

--
-- Indexes for table `chatbot_history`
--
ALTER TABLE `chatbot_history`
  ADD PRIMARY KEY (`chat_id`);

--
-- Indexes for table `course_progress`
--
ALTER TABLE `course_progress`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fees`
--
ALTER TABLE `fees`
  ADD PRIMARY KEY (`fee_id`),
  ADD KEY `member_id` (`member_id`);

--
-- Indexes for table `issued_books`
--
ALTER TABLE `issued_books`
  ADD PRIMARY KEY (`issue_id`),
  ADD KEY `member_id` (`member_id`),
  ADD KEY `book_id` (`book_id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `members`
--
ALTER TABLE `members`
  ADD PRIMARY KEY (`member_id`),
  ADD UNIQUE KEY `admission_no` (`admission_no`);

--
-- Indexes for table `notices`
--
ALTER TABLE `notices`
  ADD PRIMARY KEY (`notice_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `user_book_history`
--
ALTER TABLE `user_book_history`
  ADD PRIMARY KEY (`history_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `book_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `book_rating`
--
ALTER TABLE `book_rating`
  MODIFY `rating_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `chatbot_history`
--
ALTER TABLE `chatbot_history`
  MODIFY `chat_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `course_progress`
--
ALTER TABLE `course_progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `fees`
--
ALTER TABLE `fees`
  MODIFY `fee_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `issued_books`
--
ALTER TABLE `issued_books`
  MODIFY `issue_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `members`
--
ALTER TABLE `members`
  MODIFY `member_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `notices`
--
ALTER TABLE `notices`
  MODIFY `notice_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_book_history`
--
ALTER TABLE `user_book_history`
  MODIFY `history_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE;

--
-- Constraints for table `fees`
--
ALTER TABLE `fees`
  ADD CONSTRAINT `fees_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE;

--
-- Constraints for table `issued_books`
--
ALTER TABLE `issued_books`
  ADD CONSTRAINT `issued_books_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `members` (`member_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `issued_books_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
