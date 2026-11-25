# ClassroomPortal - Enterprise Academic Learning & Assessment Management System

ClassroomPortal is a production-ready, role-based educational management and assessment platform engineered for secure teaching and learning activities. Built with Python, Flask, and an ACID-compliant relational persistence layer, the portal provides complete cohort segregation, automated join code enrollment, syllabus distribution, notice board bulletins, and strict confidential submission review protected by Dual-Key Gatekeeper authorization.

---

## Architecture & Security Highlights

### Zero-Leakage Peer Privacy (IDOR Defense)
Student homework files are stored outside the public document root in a protected server repository. Access to any submission file (`/submissions/<id>/download`) is strictly guarded by the **Dual-Key Gatekeeper**:
- **Key 1 (Instructor Privilege)**: User must hold the Instructor role and own the parent classroom cohort.
- **Key 2 (Student Authorship)**: User must hold the Student role and be the exact author of that submission.

Any attempt by an unauthorized peer or unauthenticated entity to tamper with sequential submission IDs is immediately terminated with an **HTTP 403 Forbidden Access Denied** response.

### Mandatory Field Enforcement
Across all portal endpoints, every input field is strictly mandatory:
- **Registration**: Full Name (starts with A-Z letter), Username (starts with A-Z letter), Email (must end with `@gmail.com`), Password (min 6 characters), Confirm Password (must match), and Account Role.
- **Cohort Creation**: Group Name, Subject/Discipline, and Description.
- **Assignment Creation**: Title, Instructions, Due Date & Time, and Max Points.
- **Student Submission**: Homework solution file and student submission notes.
- **Instructor Evaluation**: Numerical score (0 to max) and constructive feedback remarks.

### Light & Dark Theme System
A theme engine supporting both Light and Dark modes with instant local persistence (`localStorage`), zero flash of unstyled content, and responsive SVG icons.

---

## Market-Ready Features

1. **Classroom Notice Board**: Instructors can publish announcements with pinning capabilities to notify enrolled students of schedule changes and laboratory protocols.
2. **Gradebook CSV Export**: One-click export of individual assignment rosters and cohort-wide gradebooks to CSV for registrars and examination committees.
3. **Submission Timeliness Detection**: Automatic comparison between submission timestamps and due dates, labeling entries as `On Time` or `Late Submission`.
4. **Live Search & Filtering**: Instant client-side search across cohort groups, assignments, and student rosters without page reloads.
5. **Role-Segregated Workspaces**: Dedicated Instructor Workspace and Student Learning Hub with customized analytical metric cards.

---

## Production Deployment Guide

ClassroomPortal is architected for immediate cloud or on-premises production deployment.

### 1. Cross-Platform Production Server (Waitress WSGI)
Runs out of the box on Windows, Linux, and macOS with multi-threaded request dispatching:
```bash
python run_production.py
```
*(Default: bound to `0.0.0.0:5000` with 6 worker threads)*

### 2. Linux Production Deployment (Gunicorn WSGI)
```bash
gunicorn wsgi:app --workers 4 --threads 2 --bind 0.0.0.0:5000
```

### 3. Containerized Deployment (Docker & Docker Compose)
```bash
docker compose up --build -d
```
The Docker image is built on `python:3.11-slim`, includes health check probes, and mounts persistent volumes for the SQLite database and upload storage.

### 4. Cloud Platform Deployment (Render / Heroku / Railway)
- **Procfile**: `web: gunicorn wsgi:app --workers 4 --threads 2 --bind 0.0.0.0:$PORT`
- **render.yaml**: Pre-configured infrastructure blueprint with persistent disk mounting.

---

## Getting Started (Local Development)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Populate Demo Data
```bash
python seed_demo.py
```

**Pre-configured Accounts:**
- **Instructor**: `sarah.connor@gmail.com` (username: `teacher_sarah`) | Password: `password123`
- **Student 1**: `alex.rivera@gmail.com` (username: `student_alex`) | Password: `password123`
- **Student 2**: `emma.watson@gmail.com` (username: `student_emma`) | Password: `password123`

### 3. Run Development Server
```bash
python app.py
```
Access via browser at: **http://127.0.0.1:5000**

---

## Automated Test Verification
```bash
python test_app.py
```
Executes complete automated test matrix verifying registration validation, role segregation, group creation, assignment submission, grading, CSV export, and 403 Forbidden IDOR mitigation.

---

## Deliverables & Documentation
- **ClassroomPortal_Capstone_Project_Report.pdf**: 34-Page Comprehensive Academic Documentation Report.
- **ClassroomPortal_Presentation.pptx**: 12-Slide Widescreen Project Defense Presentation.
