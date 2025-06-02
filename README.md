# 🎓 Student Grade Management System

A simple command-line based Student Grade Management System written in Python using MySQL as the backend database. This system allows an admin to register students, assign/update grades, and view student data, while students can log in to view their grades securely.

---

## 📌 Features

- 👨‍🏫 Admin Panel:
  - Add/Register new students
  - Add or update student grades
  - View all registered students and their grades

- 👩‍🎓 Student Panel:
  - Secure login using email and password
  - View grades per subject

- 🔐 Secure practices:
  - Uses parameterized queries to prevent SQL injection
  - Passwords handled using `getpass` for hidden input (consider hashing for improved security)

---

## 💻 Technologies Used

- **Python 3.x**
- **MySQL**
- **PyMySQL** (MySQL connector for Python)

---

## 🛠️ Installation & Setup

1. **Clone this repository:**
   ```bash
   git clone https://github.com/your-username/student-grade-management.git
   cd student-grade-management
