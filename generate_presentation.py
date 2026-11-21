import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Palette
    C_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
    C_BLUE = RGBColor(37, 99, 235)       # #2563EB
    C_CYAN = RGBColor(14, 165, 233)      # #0EA5E9
    C_DARK = RGBColor(15, 23, 42)        # #0F172A
    C_SLATE = RGBColor(51, 65, 85)       # #334155
    C_MUTED = RGBColor(100, 116, 139)    # #64748B
    C_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
    C_WHITE = RGBColor(255, 255, 255)    # #FFFFFF
    C_GREEN = RGBColor(22, 163, 74)      # #16A34A
    C_RED = RGBColor(220, 38, 38)        # #DC2626
    C_BORDER = RGBColor(203, 213, 225)   # #CBD5E1

    blank_layout = prs.slide_layouts[6]
    
    screenshots_dir = r"C:\Users\Dell\.gemini\antigravity\Capstone\classroom_portal\screenshots"

    def add_header(slide, title_text, category="CLASSROOMPORTAL CAPSTONE DEFENSE"):
        # Top banner background
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = C_NAVY
        top_bar.line.fill.background()

        # Accent line under top bar
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
        accent.fill.solid()
        accent.fill.fore_color.rgb = C_CYAN
        accent.line.fill.background()

        # Category text
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_CYAN
        p_cat.font.name = "Segoe UI"

        # Main Title text
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.65))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE
        p_t.font.name = "Segoe UI"

        # Footer
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.15), Inches(11.733), Inches(0.3))
        tf_f = footer_box.text_frame
        p_f = tf_f.paragraphs[0]
        p_f.text = "ClassroomPortal | Confidential Academic Management System | External Evaluation 2026"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = C_MUTED
        p_f.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = C_NAVY
    bg1.line.fill.background()

    # Subtle inner accent card
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(11.333), Inches(5.9))
    card1.fill.solid()
    card1.fill.fore_color.rgb = RGBColor(23, 37, 84) # Darker blue
    card1.line.color.rgb = C_CYAN
    card1.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.5), Inches(1.2), Inches(10.333), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CAPSTONE PROJECT FINAL DEFENSE"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "ClassroomPortal"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.font.name = "Segoe UI"
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "A Secure, Role-Based Teaching-Learning Portal with IDOR-Protected Confidential Assignment Submissions"
    p.font.size = Pt(17)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.font.name = "Segoe UI"
    p.space_after = Pt(28)

    p = tf.add_paragraph()
    p.text = "• Core Innovation: Dual-Key Gatekeeper Authorization (Strict Peer-to-Peer Privacy Enforcement)"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(191, 219, 254)
    p.font.name = "Segoe UI"

    p = tf.add_paragraph()
    p.text = "• Architecture: Python 3.14/3.15, Flask WSGI Framework, SQLite3 ACID Relational Engine"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(191, 219, 254)
    p.font.name = "Segoe UI"

    p = tf.add_paragraph()
    p.text = "• Presentation Scope: Architecture, Security Validation, Database Design, Real UI Screenshots & Live Defense"
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(191, 219, 254)
    p.font.name = "Segoe UI"
    p.space_after = Pt(28)

    p = tf.add_paragraph()
    p.text = "Presented by: Capstone Project Team  |  Academic Year: 2026  |  Evaluator: External Examination Committee"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.font.name = "Segoe UI"

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Problem Statement & Project Motivation", "BACKGROUND & CHALLENGES")

    # Card 1: Enterprise LMS bloat
    c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(3.6), Inches(5.2))
    c1.fill.solid(); c1.fill.fore_color.rgb = C_LIGHT; c1.line.color.rgb = C_BORDER
    tf1 = c1.text_frame; tf1.word_wrap = True; tf1.margin_left = Inches(0.25); tf1.margin_right = Inches(0.25)
    p = tf1.paragraphs[0]; p.text = "1. Enterprise LMS Bloat"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(12)
    p = tf1.add_paragraph(); p.text = "• Overly Complex Setup:\nPlatforms like Moodle and Blackboard require specialized sysadmin overhead.\n\n• High Cognitive Load:\nTeachers struggle with complex multi-level menus just to post a single homework assignment.\n\n• Resource Heavy:\nSluggish response on low-bandwidth school networks."; p.font.size = Pt(12); p.font.color.rgb = C_SLATE

    # Card 2: Privacy Leaks & IDOR
    c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.5), Inches(3.7), Inches(5.2))
    c2.fill.solid(); c2.fill.fore_color.rgb = RGBColor(254, 242, 242); c2.line.color.rgb = RGBColor(248, 113, 113)
    tf2 = c2.text_frame; tf2.word_wrap = True; tf2.margin_left = Inches(0.25); tf2.margin_right = Inches(0.25)
    p = tf2.paragraphs[0]; p.text = "2. Severe IDOR Privacy Flaws"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_RED; p.space_after = Pt(12)
    p = tf2.add_paragraph(); p.text = "• Insecure Direct Object References:\nMost ad-hoc school portals expose sequential URL IDs (e.g. /files/sub_4.pdf).\n\n• Academic Dishonesty & Plagiarism:\nMalicious students manipulate URL query params to download classmates' un-graded homework.\n\n• Inadequate Role Segregation:\nLack of granular endpoint authorization."; p.font.size = Pt(12); p.font.color.rgb = C_DARK

    # Card 3: ClassroomPortal Solution
    c3 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.9), Inches(1.5), Inches(3.6), Inches(5.2))
    c3.fill.solid(); c3.fill.fore_color.rgb = RGBColor(240, 253, 244); c3.line.color.rgb = RGBColor(134, 239, 172)
    tf3 = c3.text_frame; tf3.word_wrap = True; tf3.margin_left = Inches(0.25); tf3.margin_right = Inches(0.25)
    p = tf3.paragraphs[0]; p.text = "3. The ClassroomPortal Vision"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_GREEN; p.space_after = Pt(12)
    p = tf3.add_paragraph(); p.text = "• Zero-Leakage Architecture:\nDual-Key Gatekeeper enforces HTTP 403 Forbidden for any unauthorized student access.\n\n• Frictionless Classroom Cohorts:\nInstant class creation with 6-character Join Codes (e.g. BIO101).\n\n• Fast & Transparent Workflow:\nDirect grading, feedback delivery, and real-time student task tracking."; p.font.size = Pt(12); p.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & TECH STACK
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "System Architecture & Comprehensive Tech Stack", "TECHNICAL SPECIFICATIONS")

    # Left Column: Tech Stack Cards
    stack_items = [
        ("Backend Web Engine", "Python 3.14/3.15 + Flask WSGI", "Lightweight, decoupled MVC pattern with modular route dispatching and clean RESTful design."),
        ("Security Engine", "Werkzeug Security (PBKDF2-SHA256)", "Salted password hashing (600,000 rounds) + HTTP-only encrypted session cookies."),
        ("Relational Database", "SQLite3 with Foreign Key Enforcement", "ACID-compliant relational engine with WAL journaling and zero server daemon maintenance."),
        ("File Storage & Sanitizer", "Werkzeug secure_filename + UUID", "Defends against path traversal (../) attacks; prevents filename collisions on server storage."),
        ("Responsive UI & Templates", "HTML5, Jinja2, Bootstrap 5", "Modern responsive web portal rendering cleanly across desktop, tablet, and mobile browsers.")
    ]

    for i, (title, tech, desc) in enumerate(stack_items):
        y_pos = 1.45 + (i * 1.05)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y_pos), Inches(6.8), Inches(0.95))
        box.fill.solid(); box.fill.fore_color.rgb = C_LIGHT; box.line.color.rgb = C_BORDER
        t_frame = box.text_frame; t_frame.word_wrap = True; t_frame.margin_top = Inches(0.08); t_frame.margin_left = Inches(0.2)
        p = t_frame.paragraphs[0]; p.text = f"{title}:  {tech}"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = t_frame.add_paragraph(); p2.text = desc; p2.font.size = Pt(10.5); p2.font.color.rgb = C_SLATE

    # Right Column: Architectural Flow Diagram Card
    diag_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(1.45), Inches(4.5), Inches(5.2))
    diag_box.fill.solid(); diag_box.fill.fore_color.rgb = RGBColor(238, 242, 255); diag_box.line.color.rgb = C_BLUE
    dtf = diag_box.text_frame; dtf.word_wrap = True; dtf.margin_left = Inches(0.25); dtf.margin_right = Inches(0.25)
    p = dtf.paragraphs[0]; p.text = "Architectural Tier Separation"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(10)
    
    tiers = [
        ("Presentation Layer", "Client Browser (Edge/Chrome/Firefox)\nBootstrap 5 responsive UI & Jinja2 Templates"),
        ("Application Layer", "Flask Routing & Decorators\n@login_required & @role_required gatekeepers"),
        ("Business Logic Layer", "Classroom cohort manager, assignment file handler, and confidential submission reviewer"),
        ("Security Gatekeeper", "Dual-Key IDOR verification logic & Werkzeug secure file upload interceptor"),
        ("Data Persistence Layer", "SQLite3 relational database + local server-side confidential upload repository")
    ]
    for name, detail in tiers:
        p = dtf.add_paragraph(); p.text = f"▶ {name}"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_BLUE
        p = dtf.add_paragraph(); p.text = detail; p.font.size = Pt(10); p.font.color.rgb = C_DARK; p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: SECURITY ARCHITECTURE - DUAL-KEY GATEKEEPER
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Security Architecture: Dual-Key Gatekeeper Authorization", "CORE INNOVATION")

    # Top Explanation Card
    top_c = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.45), Inches(11.733), Inches(1.5))
    top_c.fill.solid(); top_c.fill.fore_color.rgb = RGBColor(254, 242, 242); top_c.line.color.rgb = RGBColor(239, 68, 68)
    tt = top_c.text_frame; tt.word_wrap = True; tt.margin_left = Inches(0.3); tt.margin_right = Inches(0.3)
    p = tt.paragraphs[0]; p.text = "Defending Against IDOR (Insecure Direct Object Reference) - OWASP Top 10 A01"; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = C_RED; p.space_after = Pt(4)
    p = tt.add_paragraph(); p.text = "In typical web portals, endpoints like /download/submission/4 blindly stream files if the user is authenticated. In ClassroomPortal, the Dual-Key Gatekeeper algorithm interrogates the database relationship before sending a single byte. If neither authorization key matches, the request is instantly rejected with HTTP 403 Forbidden."; p.font.size = Pt(11); p.font.color.rgb = C_DARK

    # Key 1 Card
    k1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.2), Inches(3.6), Inches(3.5))
    k1.fill.solid(); k1.fill.fore_color.rgb = C_LIGHT; k1.line.color.rgb = C_BLUE
    kt1 = k1.text_frame; kt1.word_wrap = True; kt1.margin_left = Inches(0.25); kt1.margin_right = Inches(0.25)
    p = kt1.paragraphs[0]; p.text = "KEY 1: TEACHER PRIVILEGE"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_BLUE; p.space_after = Pt(10)
    p = kt1.add_paragraph(); p.text = "• Role Verification:\nUser must hold role == 'teacher'.\n\n• Cohort Ownership Check:\nTeacher ID must strictly match groups.teacher_id for the parent class.\n\n• Permitted Operations:\nInspect homework files, assign numerical marks (0-100), and submit detailed feedback."; p.font.size = Pt(11); p.font.color.rgb = C_SLATE

    # Key 2 Card
    k2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(3.2), Inches(3.6), Inches(3.5))
    k2.fill.solid(); k2.fill.fore_color.rgb = C_LIGHT; k2.line.color.rgb = C_GREEN
    kt2 = k2.text_frame; kt2.word_wrap = True; kt2.margin_left = Inches(0.25); kt2.margin_right = Inches(0.25)
    p = kt2.paragraphs[0]; p.text = "KEY 2: STUDENT AUTHORSHIP"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_GREEN; p.space_after = Pt(10)
    p = kt2.add_paragraph(); p.text = "• Role Verification:\nUser holds role == 'student'.\n\n• Authorship Proof:\nCurrent session user_id must match submissions.student_id exactly.\n\n• Permitted Operations:\nUpload solution, replace submission prior to deadline, and review personal grade & teacher feedback."; p.font.size = Pt(11); p.font.color.rgb = C_SLATE

    # Rejection Card
    k3 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(3.2), Inches(3.7), Inches(3.5))
    k3.fill.solid(); k3.fill.fore_color.rgb = RGBColor(254, 242, 242); k3.line.color.rgb = C_RED
    kt3 = k3.text_frame; kt3.word_wrap = True; kt3.margin_left = Inches(0.25); kt3.margin_right = Inches(0.25)
    p = kt3.paragraphs[0]; p.text = "ALL OTHERS: IMMEDIATE 403"; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_RED; p.space_after = Pt(10)
    p = kt3.add_paragraph(); p.text = "• Peer Students Rejected:\nClassmates enrolled in the same group CANNOT view or download another peer's submission.\n\n• Unrelated Teachers Rejected:\nTeachers who do not own this specific group are blocked.\n\n• Zero Information Leak:\nZero file metadata or headers sent to client."; p.font.size = Pt(11); p.font.color.rgb = C_DARK

    # =========================================================================
    # SLIDE 5: DATABASE DESIGN & RELATIONAL INTEGRITY
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Relational Database Schema (3NF Normalized)", "DATA PERSISTENCE & INTEGRITY")

    tables = [
        ("users", "Primary Authentication & Identity", ["id (PK, INTEGER AUTOINCREMENT)", "username (VARCHAR, UNIQUE)", "email (VARCHAR, UNIQUE)", "password_hash (VARCHAR, PBKDF2)", "role (ENUM: 'teacher' | 'student')", "created_at (TIMESTAMP)"]),
        ("groups", "Teacher-Curated Classroom Cohorts", ["id (PK, INTEGER AUTOINCREMENT)", "name (VARCHAR(100))", "subject (VARCHAR(100))", "join_code (VARCHAR(10), UNIQUE)", "teacher_id (FK -> users.id)", "created_at (TIMESTAMP)"]),
        ("group_members", "Student Enrollment Mapping (M:N)", ["id (PK, INTEGER AUTOINCREMENT)", "group_id (FK -> groups.id)", "student_id (FK -> users.id)", "UNIQUE(group_id, student_id)", "joined_at (TIMESTAMP)"]),
        ("assignments", "Teacher Tasks & Worksheets", ["id (PK, INTEGER AUTOINCREMENT)", "group_id (FK -> groups.id)", "title (VARCHAR(200))", "description (TEXT)", "file_path (VARCHAR(255))", "due_date (DATETIME)"]),
        ("submissions", "Confidential Student Homework", ["id (PK, INTEGER AUTOINCREMENT)", "assignment_id (FK -> assignments.id)", "student_id (FK -> users.id)", "file_path (VARCHAR(255))", "grade (INTEGER), feedback (TEXT)", "submitted_at (TIMESTAMP)"])
    ]

    for i, (tname, tdesc, fields) in enumerate(tables):
        col = i % 3
        row = i // 3
        x = 0.8 + (col * 3.95)
        y = 1.45 + (row * 2.7)
        w = 3.8
        h = 2.5 if row == 0 else 2.5
        if i == 4: # span wider for submissions
            w = 7.75

        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        box.fill.solid(); box.fill.fore_color.rgb = C_LIGHT; box.line.color.rgb = C_BLUE if "submissions" not in tname else C_RED
        btf = box.text_frame; btf.word_wrap = True; btf.margin_top = Inches(0.1); btf.margin_left = Inches(0.2)
        p = btf.paragraphs[0]; p.text = f"TABLE: {tname.upper()}"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = btf.add_paragraph(); p2.text = tdesc; p2.font.size = Pt(9.5); p2.font.italic = True; p2.font.color.rgb = C_MUTED; p2.space_after = Pt(4)
        for f in fields:
            pf = btf.add_paragraph(); pf.text = f"• {f}"; pf.font.size = Pt(9.5); pf.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 6: TEACHER WORKFLOW & USER INTERFACE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Teacher Experience: Cohort Creation & Assessment Lifecycle", "LIVE UI SHOWCASE: TEACHER")

    # Screenshot 1: Teacher Dashboard
    p1 = os.path.join(screenshots_dir, "04_teacher_dashboard.png")
    if os.path.exists(p1):
        s6.shapes.add_picture(p1, Inches(0.8), Inches(1.5), width=Inches(3.7))
        lbl1 = s6.shapes.add_textbox(Inches(0.8), Inches(4.35), Inches(3.7), Inches(0.6))
        lbl1.text_frame.word_wrap = True
        p = lbl1.text_frame.paragraphs[0]; p.text = "Fig 1: Teacher Dashboard"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = lbl1.text_frame.add_paragraph(); p2.text = "Cohorts list & unique Join Code (BIO101)"; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Screenshot 2: Create Assignment
    p2_img = os.path.join(screenshots_dir, "06_create_assignment.png")
    if os.path.exists(p2_img):
        s6.shapes.add_picture(p2_img, Inches(4.8), Inches(1.5), width=Inches(3.7))
        lbl2 = s6.shapes.add_textbox(Inches(4.8), Inches(4.35), Inches(3.7), Inches(0.6))
        lbl2.text_frame.word_wrap = True
        p = lbl2.text_frame.paragraphs[0]; p.text = "Fig 2: Create Assignment Modal"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = lbl2.text_frame.add_paragraph(); p2.text = "Due dates, instructions & reference worksheet upload"; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Screenshot 3: Submissions & Grading
    p3_img = os.path.join(screenshots_dir, "07_teacher_submissions_grading.png")
    if os.path.exists(p3_img):
        s6.shapes.add_picture(p3_img, Inches(8.8), Inches(1.5), width=Inches(3.7))
        lbl3 = s6.shapes.add_textbox(Inches(8.8), Inches(4.35), Inches(3.7), Inches(0.6))
        lbl3.text_frame.word_wrap = True
        p = lbl3.text_frame.paragraphs[0]; p.text = "Fig 3: Confidential Grading Roster"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = lbl3.text_frame.add_paragraph(); p2.text = "Download homework, enter grades & feedback"; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Bottom Summary Box
    bot_box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.8))
    bot_box.fill.solid(); bot_box.fill.fore_color.rgb = C_LIGHT; bot_box.line.color.rgb = C_BLUE
    btf = bot_box.text_frame; btf.word_wrap = True; btf.margin_left = Inches(0.25); btf.margin_right = Inches(0.25)
    p = btf.paragraphs[0]; p.text = "Key Teacher Workflow Highlights:"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(4)
    p = btf.add_paragraph(); p.text = "1. Immediate Group Formation: Generates a human-friendly unique 6-character Join Code (e.g. BIO101) for students.\n2. Assignment Management: Uploads syllabus documents and instructions with server-side validation.\n3. Confidential Submission Review: Real-time table displaying student submission status, file download links, and instant grade updating."; p.font.size = Pt(11); p.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 7: STUDENT WORKFLOW & USER INTERFACE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Student Experience: Enrollment, Upload & Feedback", "LIVE UI SHOWCASE: STUDENT")

    # Screenshot 1: Student Dashboard
    s1_img = os.path.join(screenshots_dir, "08_student_dashboard.png")
    if os.path.exists(s1_img):
        s7.shapes.add_picture(s1_img, Inches(0.8), Inches(1.5), width=Inches(3.7))
        lbl1 = s7.shapes.add_textbox(Inches(0.8), Inches(4.35), Inches(3.7), Inches(0.6))
        lbl1.text_frame.word_wrap = True
        p = lbl1.text_frame.paragraphs[0]; p.text = "Fig 4: Student Dashboard"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = lbl1.text_frame.add_paragraph(); p2.text = "Enrolled classes, upcoming homework & status"; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Screenshot 2: Join Group
    s2_img = os.path.join(screenshots_dir, "09_student_join_group.png")
    if os.path.exists(s2_img):
        s7.shapes.add_picture(s2_img, Inches(4.8), Inches(1.5), width=Inches(3.7))
        lbl2 = s7.shapes.add_textbox(Inches(4.8), Inches(4.35), Inches(3.7), Inches(0.6))
        lbl2.text_frame.word_wrap = True
        p = lbl2.text_frame.paragraphs[0]; p.text = "Fig 5: Join Group Dialog"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = lbl2.text_frame.add_paragraph(); p2.text = "Enter 6-char code provided by teacher"; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Screenshot 3: Student Assignment Detail & Upload
    s3_img = os.path.join(screenshots_dir, "10_student_assignment_detail.png")
    if os.path.exists(s3_img):
        s7.shapes.add_picture(s3_img, Inches(8.8), Inches(1.5), width=Inches(3.7))
        lbl3 = s7.shapes.add_textbox(Inches(8.8), Inches(4.35), Inches(3.7), Inches(0.6))
        lbl3.text_frame.word_wrap = True
        p = lbl3.text_frame.paragraphs[0]; p.text = "Fig 6: Submission & Feedback View"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p2 = lbl3.text_frame.add_paragraph(); p2.text = "File upload, student notes, assigned grade & remarks"; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Bottom Summary Box
    bot_box2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.8))
    bot_box2.fill.solid(); bot_box2.fill.fore_color.rgb = C_LIGHT; bot_box2.line.color.rgb = C_GREEN
    btf2 = bot_box2.text_frame; btf2.word_wrap = True; btf2.margin_left = Inches(0.25); btf2.margin_right = Inches(0.25)
    p = btf2.paragraphs[0]; p.text = "Key Student Workflow Highlights:"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_GREEN; p.space_after = Pt(4)
    p = btf2.add_paragraph(); p.text = "1. Simple Self-Enrollment: Join classes immediately without awaiting administrator invitation links.\n2. Robust Assignment Submissions: Uploads homework files (PDF, DOCX, ZIP) with optional comments.\n3. Private Assessment Loop: Only the student can view their individual grade and teacher feedback; other students cannot see it."; p.font.size = Pt(11); p.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 8: SECURITY VERIFICATION & 403 DEMONSTRATION
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Security Verification: Live HTTP 403 Forbidden Rejection", "DEFENSE AGAINST TAMPERING")

    # Left: Screenshot of 403 Access Denied
    s403_img = os.path.join(screenshots_dir, "11_access_denied_403.png")
    if os.path.exists(s403_img):
        s8.shapes.add_picture(s403_img, Inches(0.8), Inches(1.5), width=Inches(5.5))
        lbl_sec = s8.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(5.5), Inches(0.6))
        p = lbl_sec.text_frame.paragraphs[0]; p.text = "Fig 7: Live HTTP 403 Forbidden Rejection Response"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_RED
        p2 = lbl_sec.text_frame.add_paragraph(); p2.text = "URL parameter tampering (/download/submission/1) blocked by Dual-Key Gatekeeper."; p2.font.size = Pt(9.5); p2.font.color.rgb = C_MUTED

    # Right: Test scenario explanation card
    r_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.5), Inches(5.933), Inches(5.2))
    r_card.fill.solid(); r_card.fill.fore_color.rgb = RGBColor(254, 242, 242); r_card.line.color.rgb = C_RED
    rtf = r_card.text_frame; rtf.word_wrap = True; rtf.margin_left = Inches(0.3); rtf.margin_right = Inches(0.3)
    p = rtf.paragraphs[0]; p.text = "Penetration Testing Test Case TC-06"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_RED; p.space_after = Pt(10)

    test_steps = [
        ("Simulated Threat Actor", "Student 'student_jane' logged in with legitimate student credentials."),
        ("Attack Vector", "Jane inspects network requests, discovers submission ID #1 belongs to classmate 'student_john', and attempts to directly navigate to /download/submission/1."),
        ("Vulnerable Behavior in Typical Systems", "Server fetches row #1 and streams file, leaking John's homework."),
        ("ClassroomPortal Defense Mechanism", "Dual-Key Gatekeeper queries database:\n1. Is Jane the teacher of Biology 101? (False)\n2. Is Jane the author of submission #1? (False)\nResult: abort(403) triggered before file read."),
        ("Audit & Integrity Result", "Zero data leaked. The attempt terminates with an Access Denied error page.")
    ]
    for title, desc in test_steps:
        p = rtf.add_paragraph(); p.text = f"• {title}:"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_DARK
        p = rtf.add_paragraph(); p.text = f"  {desc}"; p.font.size = Pt(10.5); p.font.color.rgb = C_SLATE; p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 9: QUALITY ASSURANCE & TEST MATRIX
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Quality Assurance: Verification & Test Matrix", "VERIFICATION RESULTS")

    # Table of Test Cases
    rows, cols = 8, 4
    left, top, width, height = Inches(0.8), Inches(1.5), Inches(11.733), Inches(4.4)
    table_shape = s9.shapes.add_table(rows, cols, left, top, width, height)
    tbl = table_shape.table

    tbl.columns[0].width = Inches(1.2)   # Test ID
    tbl.columns[1].width = Inches(3.2)   # Test Scenario
    tbl.columns[2].width = Inches(5.8)   # Expected vs Actual Behavior
    tbl.columns[3].width = Inches(1.533) # Status

    headers = ["Test ID", "Test Scenario", "Verification & Enforcement Mechanism", "Result"]
    for col_idx, text in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = C_NAVY
        p = cell.text_frame.paragraphs[0]; p.text = text; p.font.bold = True; p.font.size = Pt(11); p.font.color.rgb = C_WHITE

    test_data = [
        ("TC-01", "User Registration & Role Assignment", "Werkzeug salted hash generated; role saved as teacher/student", "100% PASS"),
        ("TC-02", "Unique Join Code Enrollment", "Enrolls student into group; duplicate enrollment blocked via UNIQUE constraint", "100% PASS"),
        ("TC-03", "Assignment Creation & File Upload", "Saves task metadata and uploads reference worksheet to server repository", "100% PASS"),
        ("TC-04", "Student Homework Submission", "Student uploads homework file with notes; replaces prior submission cleanly", "100% PASS"),
        ("TC-05", "Teacher Grading & Feedback", "Teacher assigns marks (0-100) and saves feedback; instantly visible to student", "100% PASS"),
        ("TC-06", "Unauthorized Peer Download (IDOR)", "Student tampering with peer's submission ID receives HTTP 403 Forbidden", "100% PASS"),
        ("TC-07", "Unauthenticated Route Protection", "Visiting protected URLs without session redirects to /login immediately", "100% PASS")
    ]

    for row_idx, row in enumerate(test_data, start=1):
        for col_idx, val in enumerate(row):
            cell = tbl.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_LIGHT if row_idx % 2 == 1 else C_WHITE
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(10)
            if col_idx == 0:
                p.font.bold = True; p.font.color.rgb = C_NAVY
            elif col_idx == 3:
                p.font.bold = True; p.font.color.rgb = C_GREEN
            else:
                p.font.color.rgb = C_SLATE

    # Bottom summary
    sb = s9.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.8))
    stf = sb.text_frame; stf.word_wrap = True
    p = stf.paragraphs[0]; p.text = "Summary: All 7 critical validation scenarios passed with 0 security regressions. Endpoints strictly enforce RBAC and IDOR mitigation."; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 10: DEPLOYMENT & NETWORK ACCESSIBILITY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Multi-Tier Deployment & Network Accessibility", "NETWORKING MODES")

    deploy_modes = [
        ("Tier 1: Local Development", "127.0.0.1:5000", C_BLUE, [
            "Standalone loopback server.",
            "Instant hot-reload for UI/backend debugging.",
            "Integrated SQLite database file."
        ]),
        ("Tier 2: Classroom LAN Access", "192.168.18.8:5000", C_CYAN, [
            "Bound to host 0.0.0.0 on local Wi-Fi router.",
            "Teachers and students connect on campus.",
            "Zero cloud latency, highly accessible."
        ]),
        ("Tier 3: Secure Global WAN", "Ngrok TLS Reverse Proxy", C_GREEN, [
            "Encrypted HTTPS public tunnel (*.ngrok-free.app).",
            "Enables remote student submissions and grading.",
            "End-to-end SSL/TLS encryption."
        ])
    ]

    for i, (title, addr, color, points) in enumerate(deploy_modes):
        x = 0.8 + (i * 3.95)
        box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.5), Inches(3.8), Inches(3.2))
        box.fill.solid(); box.fill.fore_color.rgb = C_LIGHT; box.line.color.rgb = color
        box.line.width = Pt(1.5)
        btf = box.text_frame; btf.word_wrap = True; btf.margin_left = Inches(0.25); btf.margin_right = Inches(0.25)
        p = btf.paragraphs[0]; p.text = title; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(2)
        p = btf.add_paragraph(); p.text = f"URL / Host: {addr}"; p.font.size = Pt(10.5); p.font.bold = True; p.font.color.rgb = color; p.space_after = Pt(10)
        for pt_item in points:
            p = btf.add_paragraph(); p.text = f"• {pt_item}"; p.font.size = Pt(10.5); p.font.color.rgb = C_SLATE; p.space_after = Pt(4)

    # Production Recommendations Card
    prod_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(11.733), Inches(1.9))
    prod_card.fill.solid(); prod_card.fill.fore_color.rgb = RGBColor(238, 242, 255); prod_card.line.color.rgb = C_NAVY
    ptf = prod_card.text_frame; ptf.word_wrap = True; ptf.margin_left = Inches(0.25); ptf.margin_right = Inches(0.25)
    p = ptf.paragraphs[0]; p.text = "Production Scaling & Hardening Architecture:"; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = C_NAVY; p.space_after = Pt(4)
    p = ptf.add_paragraph(); p.text = "• Production WSGI Server: Replace Flask dev server with Waitress (Windows) or Gunicorn (Linux) running 4 worker processes.\n• Reverse Proxy & SSL Termination: Place Nginx at port 443 with Let's Encrypt automated TLS certificates.\n• Object Storage Migration: Transition local uploads/ folder to S3/Cloud Storage pre-signed URLs for high-volume enterprise deployments."; p.font.size = Pt(10.5); p.font.color.rgb = C_SLATE

    # =========================================================================
    # SLIDE 11: CONCLUSION & FUTURE WORK
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Project Conclusion & Future Roadmap", "SUMMARY & OUTLOOK")

    # Left: Deliverables summary
    d_box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.2))
    d_box.fill.solid(); d_box.fill.fore_color.rgb = RGBColor(240, 253, 244); d_box.line.color.rgb = C_GREEN
    dtf = d_box.text_frame; dtf.word_wrap = True; dtf.margin_left = Inches(0.25); dtf.margin_right = Inches(0.25)
    p = dtf.paragraphs[0]; p.text = "Project Deliverables Completed"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_GREEN; p.space_after = Pt(10)

    delivs = [
        ("Full-Stack Portal Application", "Fully operational Flask web application supporting both Teacher and Student personas."),
        ("Dual-Key Gatekeeper Authorization", "100% verified defense against IDOR parameter tampering and unauthorized file access."),
        ("34-Page Academic Documentation PDF", "Comprehensive capstone report generated with ReportLab, containing 10 chapters, tables, and 11 real UI screenshots."),
        ("Automated Edge UI Capture Suite", "Selenium Headless Edge automation script for repeatable UI screenshot rendering."),
        ("Git Version Controlled Codebase", "Structured repository initialized with .gitignore and prepared for remote synchronization.")
    ]
    for dtitle, ddesc in delivs:
        p = dtf.add_paragraph(); p.text = f"✔ {dtitle}"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p = dtf.add_paragraph(); p.text = f"   {ddesc}"; p.font.size = Pt(10); p.font.color.rgb = C_SLATE; p.space_after = Pt(4)

    # Right: Future Roadmap
    f_box = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.2))
    f_box.fill.solid(); f_box.fill.fore_color.rgb = C_LIGHT; f_box.line.color.rgb = C_BLUE
    ftf = f_box.text_frame; ftf.word_wrap = True; ftf.margin_left = Inches(0.25); ftf.margin_right = Inches(0.25)
    p = ftf.paragraphs[0]; p.text = "Future Technical Roadmap"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = C_BLUE; p.space_after = Pt(10)

    roadmap = [
        ("Automated Plagiarism Detection", "Integrate cosine similarity and n-gram analysis across student submissions within the same group."),
        ("Real-time Push Notifications", "Integrate WebSockets / Flask-SocketIO for instant notification when a teacher grades homework."),
        ("Auto-Graded Quizzes & MCQs", "Expand assignment model to support online timed multiple-choice assessments with automatic score calculation."),
        ("Cloud Object Storage Integration", "Support Amazon S3 or Google Cloud Storage pre-signed URLs for scalable enterprise storage.")
    ]
    for rtitle, rdesc in roadmap:
        p = ftf.add_paragraph(); p.text = f"🚀 {rtitle}"; p.font.size = Pt(11); p.font.bold = True; p.font.color.rgb = C_NAVY
        p = ftf.add_paragraph(); p.text = f"   {rdesc}"; p.font.size = Pt(10); p.font.color.rgb = C_SLATE; p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 12: QUESTIONS & ANSWERS (FINAL DEFENSE SLIDE)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg12.fill.solid(); bg12.fill.fore_color.rgb = C_NAVY; bg12.line.fill.background()

    card12 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    card12.fill.solid(); card12.fill.fore_color.rgb = RGBColor(23, 37, 84)
    card12.line.color.rgb = C_CYAN; card12.line.width = Pt(1.5)

    tf12 = card12.text_frame; tf12.word_wrap = True
    p = tf12.paragraphs[0]; p.text = "Thank You!"; p.font.size = Pt(44); p.font.bold = True; p.font.color.rgb = C_WHITE; p.font.name = "Segoe UI"; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(14)
    p = tf12.add_paragraph(); p.text = "ClassroomPortal Capstone Project Defense"; p.font.size = Pt(20); p.font.color.rgb = C_CYAN; p.font.name = "Segoe UI"; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(24)
    p = tf12.add_paragraph(); p.text = "Questions & Answers from the External Examination Committee"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = RGBColor(226, 232, 240); p.font.name = "Segoe UI"; p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(24)
    p = tf12.add_paragraph(); p.text = "Project Artifacts & Source Code:\n• 34-Page Comprehensive Capstone Documentation PDF\n• 12-Slide Executive Project Defense Presentation (.pptx)\n• Fully Tested Flask & SQLite Source Repository with Automated Test Suite"; p.font.size = Pt(12); p.font.color.rgb = RGBColor(191, 219, 254); p.font.name = "Segoe UI"; p.alignment = PP_ALIGN.CENTER

    out_path = r"C:\Users\Dell\.gemini\antigravity\Capstone\classroom_portal\ClassroomPortal_Presentation.pptx"
    prs.save(out_path)
    print(f"Presentation successfully created at: {out_path}")

if __name__ == "__main__":
    create_deck()
