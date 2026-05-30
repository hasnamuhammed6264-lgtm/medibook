# MediBook - Cloud-Based Healthcare Booking System

A secure, scalable healthcare appointment booking web application built with Flask and deployed using DevSecOps best practices on AWS Cloud.

## Live Features
- Patient registration and login with role-based access
- Browse doctors by specialty
- Book, view and cancel appointments
- Admin dashboard with full control
- Security hardened with rate limiting, CSP headers, bcrypt hashing

## Tech Stack
- Backend: Python, Flask
- Database: SQLite (local), MySQL RDS (AWS)
- Frontend: HTML, Bootstrap 5
- Security: Flask-Talisman, Flask-Limiter, Bcrypt
- DevOps: Git, GitHub Actions CI/CD, Docker
- Cloud: AWS VPC, EC2, RDS, S3, CloudFront
- Server: Nginx, Waitress

## Local Setup
- git clone https://github.com/hasnamuhammed6264-lgtm/medibook.git
- cd medibook
- python -m venv venv
- source venv/Scripts/activate
- pip install -r requirements.txt
- python run.py

## Security Features
- Bcrypt password hashing
- Rate limiting on login and register
- Content Security Policy headers
- Session security with HTTPOnly cookies
- Input sanitization with Bleach
- SQL injection prevention via SQLAlchemy ORM
- Role-based access control

## AWS Architecture
- Internet → CloudFront CDN → ALB → EC2 (Nginx + Flask) → RDS MySQL → S3

## CI/CD Pipeline
- GitHub Actions automatically tests, builds Docker image, runs security scan

## Test Accounts
- Admin: admin@medibook.com / admin123
- Doctor: arjun@medibook.com / doctor123

## Developer
Hasna Muhammed - Summer Internship Capstone Project
IPSR Solutions Ltd
