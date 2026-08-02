# 💰 Smart Fee Management System

A secure **web-based fee management system** built using **Flask** and **MySQL** to simplify and automate fee collection in educational institutions. The system provides separate portals for **administrators** and **students**, enabling efficient fee tracking, installment management, payment recording, and scholarship management.

---

## 📖 Overview

Managing student fee records manually is time-consuming and prone to errors. The **Smart Fee Management System** automates the entire fee management process, from student registration to installment generation and payment tracking.

The application offers role-based access, allowing administrators to manage student records and fee collections, while students can securely view their fee details, payment history, and scholarship information.

---

## ✨ Features

### 👨‍💼 Admin Module

- Secure administrator login
- Add, edit, and delete student records
- Manage courses and fee structures
- Assign students to courses
- Automatic installment generation
- Record student fee payments
- Scholarship management
- Dashboard with real-time statistics
- View recent payments
- Monitor pending installments

---

### 👨‍🎓 Student Module

- Secure student login
- View personal profile
- Check course details
- View payment history
- Track installment status
- View scholarship information
- Check remaining fee balance

---

## ⚙️ Automatic Installment Generation

When a new student is registered:

- The selected course fee is automatically divided into **two installments**
- Installment records are created automatically
- Due dates are generated
- Initial status is marked as **Pending**

This eliminates manual installment creation and improves accuracy.

---

## 📊 Dashboard

The administrator dashboard provides an overview of:

- 👨‍🎓 Total Students
- 📚 Total Courses
- 💰 Total Fee Collected
- ⏳ Pending Installments
- 💳 Recent Payments
- 📈 Collection Statistics

---

## 🛠️ Tech Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Python
- Flask

### Database

- MySQL

### Libraries

- Flask
- Flask-MySQLdb

---

## 🗄️ Database Design

The system uses the following database tables:

- Students
- Courses
- Installments
- Payments
- Scholarships
- Admin

---

## 🔄 Workflow

1. Administrator logs into the system.
2. Courses are created.
3. Students are registered.
4. A course is assigned.
5. Installments are automatically generated.
6. Payments are recorded.
7. Installment status is updated automatically.
8. Students log in to track payments, installments, and scholarships.
9. Dashboard provides fee collection insights.

## 🔒 Authentication

The application provides **role-based authentication**.

### Administrator

- Complete system access
- Student management
- Course management
- Payment recording
- Dashboard analytics

### Student

- View personal information
- Track installments
- View payment history
- Scholarship details

Session management ensures only authorized users can access protected pages.

---

## 🚀 Future Improvements

- Online payment gateway integration
- Email and SMS payment reminders
- PDF receipt generation
- Attendance integration
- Student analytics dashboard
- Mobile application
- Multi-institute support
- Export reports to Excel and PDF

---

## 💡 Learning Outcomes

Through this project, I gained practical experience in:

- Flask web development
- MySQL database design
- CRUD operations
- Session-based authentication
- Relational database management
- MVC architecture
- Dashboard development
- Form validation

---

## 👩‍💻 Author

**Aastha Chaudhari**
**Dnyaneshwari Ghorpade**


- GitHub: https://github.com/aastha2206
- LinkedIn: https://www.linkedin.com/in/aastha-c

---

## 📄 License

This project is licensed under the MIT License.
