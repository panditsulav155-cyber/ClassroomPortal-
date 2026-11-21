# 🎓 ClassroomPortal - Teaching & Learning Activities Hub

A secure, role-based academic learning and assessment management platform designed for modern teaching and learning activities. Teachers can organize subject groups, distribute assignments with reference materials, and evaluate confidential student submissions. Students can register, join classes via unique 6-character Join Codes, submit homework solutions, and receive grades and qualitative feedback.

---

## 🔒 Security Architecture: Zero-Leakage Peer Privacy
Student homework files are stored in a protected repository isolated from public web routing. **Only the teacher who owns the group and the specific student who submitted the file can access or download it.** Any attempt by an unauthorized peer or unauthenticated user to tamper with submission IDs (e.g., Insecure Direct Object Reference - IDOR) is immediately rejected with an **HTTP 403 Forbidden Access Denied** response.

---

## 🚀 Key Features

- **Role-Based Access Control (RBAC)**:
  - Secure registration and authentication using Werkzeug salted password hashing (`PBKDF2-HMAC-SHA256`).
  - Strict separation of Teacher and Student privileges.
- **Teacher Workspace**:
  - Create and manage subject groups / classrooms.
  - Automatic generation of human-readable, unique 6-character Join Codes (e.g., `BIO101`).
  - Create assignments with deadlines, instructions, and syllabus/worksheet attachments.
  - Review all student submissions, download homework files securely, assign numerical grades (0–100), and provide feedback.
- **Student Workspace**:
  - Self-enroll into teacher cohorts using Join Codes.
  - View real-time course roster and upcoming deadlines.
  - Submit homework files (PDF, Word DOCX, ZIP, TXT) with student notes.
  - Update or resubmit solutions before grading.
  - Access personal grades and teacher comments in complete confidentiality.
- **Dual-Key Gatekeeper Authorization**:
  - File downloads are intercepted by `/download/submission/<id>` verifying both Teacher Group Ownership and Student Submission Authorship before streaming bytes.

---

## 📁 Repository Structure & Deliverables

- **`ClassroomPortal_Capstone_Project_Report.pdf`**: Complete 34-Page Academic Documentation Report prepared for the External Examination Committee (featuring 10 chapters, database schema, OWASP analysis, test matrix, and 11 real UI screenshots).
- **`ClassroomPortal_Presentation.pptx`**: 12-Slide Widescreen (16:9) Project Defense PowerPoint Presentation for external defense.
- **`app.py`**: Main Flask web application core logic and route dispatchers.
- **`database.py`**: SQLite3 database initialization and schema setup.
- **`test_app.py`**: Automated test suite executing test cases TC-01 through TC-07.
- **`capture_portal_screenshots.py`**: Selenium Headless Edge automation script for portal screenshots.
- **`generate_final_report.py`**: ReportLab script generating the 34-page documentation PDF.
- **`generate_presentation.py`**: `python-pptx` script generating the defense presentation.
- **`screenshots/`**: Directory containing 11 UI screenshots covering teacher, student, and security test workflows.

---

## 🛠️ Getting Started

### 1. Requirements
- Python 3.10+ (Tested on Python 3.14 & 3.15)
- Standard web browser (Chrome, Edge, Firefox)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Populate Demo Data (Optional)
To test immediately with pre-configured accounts:
```bash
python seed_demo.py
```

**Pre-seeded Demo Accounts:**
- **Teacher**:
  - Username: `teacher_sarah` (or email: `sarah@school.edu`)
  - Password: `password123`
  - Group: Grade 10 Biology (Join Code: `BIO101`)
- **Student 1** (Submitted Homework):
  - Username: `student_alex` (or email: `alex@school.edu`)
  - Password: `password123`
- **Student 2** (Pending Submission):
  - Username: `student_emma` (or email: `emma@school.edu`)
  - Password: `password123`

### 4. Run the Web Server
```bash
python app.py
```
Open your browser and navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🌐 Network Access & Remote Hosting

### Local Area Network (LAN):
To allow other devices (mobiles/tablets) on the same Wi-Fi network to access the portal:
```bash
python app.py
```
*(The server binds to `0.0.0.0:5000` — access via `http://<YOUR_LAN_IP>:5000`)*

### Secure Global WAN Tunnel (Ngrok):
```bash
ngrok http 5000
```
Open the generated HTTPS URL (e.g., `https://xxxx.ngrok-free.app`) from any external network.

---

## 🧪 Running Automated Tests
```bash
python test_app.py
```
All test cases (TC-01 through TC-07) will run and verify user registration, role authorization, submission uploads, teacher grading, and IDOR 403 Forbidden protection.
