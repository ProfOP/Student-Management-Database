# 📚 Student Management Database

<p align="center">
  <b>A structured SQL-based system to efficiently manage student, course, and academic data</b>
</p>

---

## 🚀 Overview

The **Student Management Database** is a relational database project designed to demonstrate efficient data organization, normalization, and querying techniques.

It models a real-world academic system where students enroll in courses, receive grades, and maintain academic records — making it a great learning resource for SQL and database design.

---

## ✨ Features

✅ Structured and normalized database design  
✅ Efficient management of student records  
✅ Course and enrollment tracking  
✅ Grade storage and performance analysis  
✅ Use of primary and foreign keys for relational integrity  
✅ Supports complex queries and reporting  

---

## 🗂️ Database Schema

### 📌 Core Tables

#### 👨‍🎓 Students
- `student_id` *(Primary Key)*
- `name`
- `email`
- `phone`
- `date_of_birth`

#### 📘 Courses
- `course_id` *(Primary Key)*
- `course_name`
- `credits`

#### 📝 Enrollments
- `enrollment_id` *(Primary Key)*
- `student_id` *(Foreign Key → Students)*
- `course_id` *(Foreign Key → Courses)*
- `enrollment_date`

#### 📊 Grades
- `grade_id` *(Primary Key)*
- `student_id` *(Foreign Key → Students)*
- `course_id` *(Foreign Key → Courses)*
- `grade`

---

## ⚙️ Tech Stack

- 💾 SQL (Structured Query Language)
- 🗄️ RDBMS (MySQL / PostgreSQL / SQLite)

---
