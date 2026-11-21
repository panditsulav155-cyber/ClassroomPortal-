import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw 'Page X of Y' and header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress header & footer on cover page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header
        self.drawString(54, 11 * 72 - 36, "ClassroomPortal — Teaching & Learning Activities Platform")
        self.drawRightString(8.5 * 72 - 54, 11 * 72 - 36, "System Documentation")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)

        # Running Footer
        self.line(54, 48, 8.5 * 72 - 54, 48)
        self.drawString(54, 34, "ClassroomPortal • Confidential Academic Application")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 34, page_str)

        self.restoreState()


def build_pdf(filename="ClassroomPortal_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    primary = colors.HexColor("#1E3A8A")     # Deep Navy
    secondary = colors.HexColor("#4F46E5")   # Modern Indigo
    dark_text = colors.HexColor("#0F172A")   # Slate 900
    muted_text = colors.HexColor("#475569")  # Slate 600
    card_bg = colors.HexColor("#F8FAFC")     # Clean Slate tint
    code_bg = colors.HexColor("#F1F5F9")     # Code background

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=primary,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12.5,
        leading=18,
        textColor=muted_text,
        spaceAfter=22
    )

    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=secondary,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=dark_text,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=dark_text,
        leftIndent=12,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'DocCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
        backColor=code_bg,
        borderPadding=8,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=dark_text
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=13,
        textColor=colors.HexColor("#065F46")
    )

    story = []

    # ==========================================
    # PAGE 1: COVER PAGE
    # ==========================================
    story.append(Spacer(1, 35))
    story.append(Paragraph(
        "<font color='#4F46E5'><b>ACADEMIC SOFTWARE SPECIFICATION &amp; TECHNICAL MANUAL</b></font>",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("ClassroomPortal", title_style))
    story.append(Paragraph(
        "A Secure Web Platform for Teaching &amp; Learning Activities with Isolated Groups, Assignment Workflows, and Strict Student File Confidentiality",
        subtitle_style
    ))

    story.append(HRFlowable(width="100%", thickness=2, color=secondary, spaceAfter=22))

    meta_data = [
        [Paragraph("<b>Project Title:</b>", body_style), Paragraph("ClassroomPortal (Teaching &amp; Learning Hub)", body_style)],
        [Paragraph("<b>Document Version:</b>", body_style), Paragraph("1.0.0 (Production Release)", body_style)],
        [Paragraph("<b>Technology Stack:</b>", body_style), Paragraph("Python 3.14 • Flask 3.1 • SQLite3 • Jinja2 • HTML5/CSS3", body_style)],
        [Paragraph("<b>Security Paradigm:</b>", body_style), Paragraph("Strict Role-Based Access Control (RBAC) &amp; Protected Storage Isolation", body_style)],
        [Paragraph("<b>Test Status:</b>", body_style), Paragraph("<font color='#059669'><b>100% Automated Unit &amp; Security Tests Passing</b></font>", body_style)],
        [Paragraph("<b>Platform Compatibility:</b>", body_style), Paragraph("Windows 10/11, macOS, Linux (Zero External Services Needed)", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[140, 364])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), card_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)

    story.append(Spacer(1, 30))

    callout_data = [[
        Paragraph(
            "<b>🔒 Critical Privacy Guarantee:</b><br/>"
            "This application guarantees that student assignment submissions are <b>strictly accessible only by the group teacher</b> "
            "and the student who submitted the file. Any unauthorized download attempts by peers or unauthorized teachers are blocked "
            "at the server level with an HTTP 403 Forbidden denial.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#ECFDF5")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#A7F3D0")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(callout_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: EXECUTIVE SUMMARY & ARCHITECTURE FLOW
    # ==========================================
    story.append(Paragraph("1. Executive Summary &amp; Core Objectives", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    story.append(Paragraph(
        "<b>ClassroomPortal</b> is a lightweight, responsive, and secure web application designed to facilitate "
        "teaching and learning activities. The platform acts as a digital bridge between educators and students, "
        "allowing teachers to organize curriculum into isolated groups (classes), publish assignments with downloadable "
        "instructional resources, and assess student submissions. Students enroll via simple 6-character access codes, "
        "download learning materials, and submit homework solutions securely.",
        body_style
    ))

    story.append(Paragraph("<b>Primary Goals &amp; Problem Resolution:</b>", h2_style))
    story.append(Paragraph("• <b>Streamlined Class Enrollment:</b> Eliminates manual administrative overhead. Teachers generate unique join codes (e.g. <code>BIO101</code>), and students enroll autonomously in seconds.", bullet_style))
    story.append(Paragraph("• <b>Confidential File Storage:</b> Conventional school file shares often leak student work to peers. ClassroomPortal enforces physical and route-level isolation so students can never access or download each other's submissions.", bullet_style))
    story.append(Paragraph("• <b>Comprehensive Assessment Cycle:</b> Teachers monitor roster submissions in real-time, inspect student work, record scores, and deliver constructive remarks.", bullet_style))
    story.append(Paragraph("• <b>Zero-Configuration Portability:</b> Powered by SQLite3 and Flask, the entire system runs locally with zero database setup or complex server dependencies.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("2. System Architecture &amp; User Flow", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    story.append(Paragraph(
        "The application follows the Model-View-Controller (MVC) architectural pattern. Static files (CSS styles) "
        "are cached, while all uploaded materials and student homework files are quarantined in dedicated protected folders.",
        body_style
    ))

    flow_data = [
        [
            Paragraph("<b>Stage</b>", table_header_style),
            Paragraph("<b>Teacher Operations</b>", table_header_style),
            Paragraph("<b>Student Operations</b>", table_header_style)
        ],
        [
            Paragraph("<b>1. Authentication</b>", table_body_style),
            Paragraph("Registers as Teacher; logs in with encrypted password.", table_body_style),
            Paragraph("Registers as Student; logs in with encrypted password.", table_body_style)
        ],
        [
            Paragraph("<b>2. Group Setup</b>", table_body_style),
            Paragraph("Creates Class/Group. System generates 6-character Join Code.", table_body_style),
            Paragraph("Enters Join Code on dashboard to enroll in teacher's group.", table_body_style)
        ],
        [
            Paragraph("<b>3. Assignments</b>", table_body_style),
            Paragraph("Creates assignment with instructions, deadline, max points, and optional worksheet file.", table_body_style),
            Paragraph("Views assignment instructions and downloads teacher's attached worksheet.", table_body_style)
        ],
        [
            Paragraph("<b>4. Submission</b>", table_body_style),
            Paragraph("Monitors submission roster (who submitted vs. who is pending).", table_body_style),
            Paragraph("Uploads solution file (PDF, Docx, Zip, Python, etc.) with notes.", table_body_style)
        ],
        [
            Paragraph("<b>5. Access &amp; Grading</b>", table_body_style),
            Paragraph("Securely downloads student's file, enters grade and feedback.", table_body_style),
            Paragraph("Views earned grade, teacher remarks, or downloads own submitted file.", table_body_style)
        ]
    ]

    flow_table = Table(flow_data, colWidths=[90, 205, 209])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(flow_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: DATABASE SPECIFICATION
    # ==========================================
    story.append(Paragraph("3. Database Schema &amp; Data Model (SQLite3)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    story.append(Paragraph(
        "The relational database schema is normalized to Third Normal Form (3NF), enforcing strict foreign key constraints "
        "and cascading deletes. SQLite connections are initialized with <code>PRAGMA foreign_keys = ON</code>.",
        body_style
    ))

    schema_data = [
        [
            Paragraph("<b>Table</b>", table_header_style),
            Paragraph("<b>Column</b>", table_header_style),
            Paragraph("<b>Type &amp; Constraints</b>", table_header_style),
            Paragraph("<b>Description</b>", table_header_style)
        ],
        # users
        [
            Paragraph("<b>users</b>", table_body_style),
            Paragraph("id<br/>username<br/>email<br/>password_hash<br/>role<br/>full_name", table_body_style),
            Paragraph("INTEGER PK AUTO<br/>TEXT UNIQUE NOT NULL<br/>TEXT UNIQUE NOT NULL<br/>TEXT NOT NULL<br/>CHECK('teacher','student')<br/>TEXT NOT NULL", table_body_style),
            Paragraph("Stores user profile, credentials hashed with PBKDF2/scrypt, and role assignment.", table_body_style)
        ],
        # groups
        [
            Paragraph("<b>groups</b>", table_body_style),
            Paragraph("id<br/>name<br/>description<br/>join_code<br/>teacher_id", table_body_style),
            Paragraph("INTEGER PK AUTO<br/>TEXT NOT NULL<br/>TEXT<br/>TEXT UNIQUE NOT NULL<br/>FK -> users(id)", table_body_style),
            Paragraph("Classes owned by teachers. Join code is a 6-character random alphanumeric string.", table_body_style)
        ],
        # group_memberships
        [
            Paragraph("<b>group_memberships</b>", table_body_style),
            Paragraph("id<br/>group_id<br/>student_id<br/>joined_at", table_body_style),
            Paragraph("INTEGER PK AUTO<br/>FK -> groups(id)<br/>FK -> users(id)<br/>TIMESTAMP DEFAULT", table_body_style),
            Paragraph("Associative table tracking enrolled students per group with UNIQUE(group_id, student_id).", table_body_style)
        ],
        # assignments
        [
            Paragraph("<b>assignments</b>", table_body_style),
            Paragraph("id<br/>group_id<br/>title<br/>description<br/>due_date<br/>max_points<br/>attachment_filename", table_body_style),
            Paragraph("INTEGER PK AUTO<br/>FK -> groups(id)<br/>TEXT NOT NULL<br/>TEXT NOT NULL<br/>TEXT<br/>INTEGER DEFAULT 100<br/>TEXT", table_body_style),
            Paragraph("Learning activities issued by teacher, with optional teacher resource attachments.", table_body_style)
        ],
        # submissions
        [
            Paragraph("<b>submissions</b>", table_body_style),
            Paragraph("id<br/>assignment_id<br/>student_id<br/>stored_filename<br/>notes<br/>grade<br/>feedback", table_body_style),
            Paragraph("INTEGER PK AUTO<br/>FK -> assignments(id)<br/>FK -> users(id)<br/>TEXT NOT NULL<br/>TEXT<br/>REAL<br/>TEXT", table_body_style),
            Paragraph("Protected student submissions. UUID-prefixed filename on disk with evaluation data.", table_body_style)
        ]
    ]

    schema_table = Table(schema_data, colWidths=[90, 110, 140, 164])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(schema_table)

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Relational Integrity &amp; Cascading Rules:</b>", h2_style))
    story.append(Paragraph("• <b>User Deletion:</b> If a teacher account is removed, all associated groups, assignments, and student submissions cascade delete automatically.", bullet_style))
    story.append(Paragraph("• <b>Group Deletion:</b> Deleting a group automatically purges all enrolled memberships and issued assignments.", bullet_style))
    story.append(Paragraph("• <b>Duplicate Protection:</b> A compound unique constraint on <code>(group_id, student_id)</code> prevents redundant student enrollments.", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: SECURITY & ACCESS CONTROL
    # ==========================================
    story.append(Paragraph("4. Security Architecture &amp; File Access Enforcement", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    story.append(Paragraph(
        "A critical vulnerability in web-based educational platforms is unauthorized student file downloads (known as "
        "Insecure Direct Object Reference, or IDOR). ClassroomPortal implements three concentric layers of defense to "
        "ensure student submissions remain 100% confidential:",
        body_style
    ))

    story.append(Paragraph("<b>Layer 1: Storage Quarantining</b>", h2_style))
    story.append(Paragraph(
        "Files submitted by students are stored in <code>uploads/submissions/</code>, located entirely outside the public "
        "<code>static/</code> directory. Web servers and browsers cannot access or browse these files via direct URLs.",
        body_style
    ))

    story.append(Paragraph("<b>Layer 2: Cryptographic Name Sanitization &amp; UUID Tokenization</b>", h2_style))
    story.append(Paragraph(
        "When an upload occurs, the original filename is sanitized with <code>secure_filename()</code> to defeat path traversal attacks, "
        "and is prepended with a cryptographically secure 128-bit UUID: <code>sub_&lt;uuid4&gt;_&lt;sanitized_name&gt;</code>. "
        "This completely eliminates filename collision and predictable guessing.",
        body_style
    ))

    story.append(Paragraph("<b>Layer 3: Dual-Key Authorization Gatekeeper</b>", h2_style))
    story.append(Paragraph(
        "Downloads are governed exclusively through an authenticated controller endpoint (<code>/submissions/&lt;id&gt;/download</code>). "
        "Before any byte stream is transmitted, the server executes strict ownership verification:",
        body_style
    ))

    code_block = (
        "@app.route('/submissions/&lt;int:submission_id&gt;/download')\n"
        "@login_required\n"
        "def download_submission_file(submission_id):\n"
        "    sub_info = db.query(submission, assignment, group)\n"
        "    is_teacher = (g.user['role'] == 'teacher' and g.user['id'] == sub_info['teacher_id'])\n"
        "    is_owner   = (g.user['role'] == 'student' and g.user['id'] == sub_info['student_id'])\n"
        "\n"
        "    if not (is_teacher or is_owner):\n"
        "        # Unauthorized peer or stranger -> Strictly Denied\n"
        "        abort(403, 'Access Denied: Only the teacher and submitter can access this file.')\n"
        "\n"
        "    return send_from_directory(sub_dir, sub_info['stored_filename'],\n"
        "                               as_attachment=True, download_name=sub_info['original_filename'])"
    )
    story.append(Paragraph(code_block.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style))

    story.append(Paragraph("<b>Password Cryptography &amp; Session Hygiene:</b>", h2_style))
    story.append(Paragraph("• <b>PBKDF2 / Scrypt Hashing:</b> Passwords are never stored in plaintext. They are salted and hashed using Werkzeug's cryptographic suite.", bullet_style))
    story.append(Paragraph("• <b>Session Isolation:</b> Sessions are cryptographically signed with a secure server key. Role guards (<code>@teacher_required</code>, <code>@student_required</code>) prevent privilege escalation.", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: APPLICATION ENDPOINTS & ROUTES
    # ==========================================
    story.append(Paragraph("5. Application Endpoints &amp; URL Routes", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    routes_data = [
        [
            Paragraph("<b>HTTP Method &amp; Route</b>", table_header_style),
            Paragraph("<b>Access Role</b>", table_header_style),
            Paragraph("<b>Function &amp; Responsibilities</b>", table_header_style)
        ],
        # Public
        [
            Paragraph("<code>GET /</code>", table_body_style),
            Paragraph("Public", table_body_style),
            Paragraph("Landing page; redirects authenticated users to their respective dashboards.", table_body_style)
        ],
        [
            Paragraph("<code>GET, POST /register</code>", table_body_style),
            Paragraph("Public", table_body_style),
            Paragraph("Registers Teacher or Student with role validation and password hashing.", table_body_style)
        ],
        [
            Paragraph("<code>GET, POST /login</code>", table_body_style),
            Paragraph("Public", table_body_style),
            Paragraph("Authenticates username/email and establishes session.", table_body_style)
        ],
        [
            Paragraph("<code>GET /logout</code>", table_body_style),
            Paragraph("Auth", table_body_style),
            Paragraph("Terminates session and redirects to login.", table_body_style)
        ],
        # Teacher
        [
            Paragraph("<code>GET /teacher/dashboard</code>", table_body_style),
            Paragraph("Teacher", table_body_style),
            Paragraph("Displays active teacher-owned groups, member tallies, and assignment counts.", table_body_style)
        ],
        [
            Paragraph("<code>GET, POST /teacher/groups/create</code>", table_body_style),
            Paragraph("Teacher", table_body_style),
            Paragraph("Creates new subject group and generates 6-character uppercase Join Code.", table_body_style)
        ],
        [
            Paragraph("<code>GET /teacher/groups/&lt;id&gt;</code>", table_body_style),
            Paragraph("Teacher (Owner)", table_body_style),
            Paragraph("Group detail page: displays join code, student roster, and assignments.", table_body_style)
        ],
        [
            Paragraph("<code>GET, POST .../assignments/create</code>", table_body_style),
            Paragraph("Teacher (Owner)", table_body_style),
            Paragraph("Publishes homework task with instructions, due date, max points, and resource file.", table_body_style)
        ],
        [
            Paragraph("<code>GET .../assignments/&lt;id&gt;/submissions</code>", table_body_style),
            Paragraph("Teacher (Owner)", table_body_style),
            Paragraph("Grading roster: lists all enrolled students, submission status, and download links.", table_body_style)
        ],
        [
            Paragraph("<code>POST /teacher/submissions/&lt;id&gt;/grade</code>", table_body_style),
            Paragraph("Teacher (Owner)", table_body_style),
            Paragraph("Saves numeric score and textual feedback on a student submission.", table_body_style)
        ],
        # Student
        [
            Paragraph("<code>GET /student/dashboard</code>", table_body_style),
            Paragraph("Student", table_body_style),
            Paragraph("Enrolled groups grid and global pending/completed assignments table.", table_body_style)
        ],
        [
            Paragraph("<code>GET, POST /student/groups/join</code>", table_body_style),
            Paragraph("Student", table_body_style),
            Paragraph("Validates 6-character Join Code and adds membership.", table_body_style)
        ],
        [
            Paragraph("<code>GET /student/groups/&lt;id&gt;</code>", table_body_style),
            Paragraph("Student (Enrolled)", table_body_style),
            Paragraph("Class overview with teacher details and group assignments.", table_body_style)
        ],
        [
            Paragraph("<code>GET, POST /student/assignments/&lt;id&gt;</code>", table_body_style),
            Paragraph("Student (Enrolled)", table_body_style),
            Paragraph("Task instructions, worksheet download, file uploader, notes, and grade display.", table_body_style)
        ],
        # Protected Downloads
        [
            Paragraph("<code>GET /submissions/&lt;id&gt;/download</code>", table_body_style),
            Paragraph("Teacher OR Submitter", table_body_style),
            Paragraph("<b>Protected File Download:</b> Returns file if authorized, otherwise HTTP 403.", table_body_style)
        ],
        [
            Paragraph("<code>GET /assignments/&lt;id&gt;/attachment</code>", table_body_style),
            Paragraph("Teacher OR Enrolled", table_body_style),
            Paragraph("Downloads teacher's course materials and worksheets.", table_body_style)
        ]
    ]

    routes_table = Table(routes_data, colWidths=[150, 94, 260])
    routes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(routes_table)

    story.append(PageBreak())

    # ==========================================
    # PAGE 6: TESTING & DEPLOYMENT GUIDE
    # ==========================================
    story.append(Paragraph("6. Quality Assurance &amp; Automated Testing", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    story.append(Paragraph(
        "ClassroomPortal is verified through automated test suites in <code>test_app.py</code> using isolated "
        "temporary databases and upload folders:",
        body_style
    ))

    test_data = [
        [
            Paragraph("<b>Test Case Name</b>", table_header_style),
            Paragraph("<b>Verification Scope</b>", table_header_style),
            Paragraph("<b>Result</b>", table_header_style)
        ],
        [
            Paragraph("<code>test_registration_and_authentication</code>", table_body_style),
            Paragraph("Verifies user creation, role assignment, PBKDF2 password hashing (never plaintext), valid authentication, and rejection of incorrect passwords.", table_body_style),
            Paragraph("<font color='#059669'><b>PASSED</b></font>", table_body_style)
        ],
        [
            Paragraph("<code>test_group_creation_and_enrollment</code>", table_body_style),
            Paragraph("Validates group creation by teacher, ensures 6-character uppercase join code generation, and verifies student enrollment via code.", table_body_style),
            Paragraph("<font color='#059669'><b>PASSED</b></font>", table_body_style)
        ],
        [
            Paragraph("<code>test_critical_submission_file_privacy</code>", table_body_style),
            Paragraph(
                "<b>Critical Privacy Verification:</b><br/>"
                "• Student A downloads own file &rarr; <b>200 OK</b><br/>"
                "• Student B attempts downloading Student A's file &rarr; <b>403 FORBIDDEN</b><br/>"
                "• Unrelated Teacher attempts downloading Student A's file &rarr; <b>403 FORBIDDEN</b><br/>"
                "• Group Owner Teacher downloads Student A's file &rarr; <b>200 OK</b><br/>"
                "• Teacher grades submission &rarr; Student verifies score &rarr; <b>PASSED</b>",
                table_body_style
            ),
            Paragraph("<font color='#059669'><b>PASSED</b></font>", table_body_style)
        ]
    ]

    test_table = Table(test_data, colWidths=[160, 280, 64])
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(test_table)

    story.append(Spacer(1, 8))
    story.append(Paragraph("7. Quick Start &amp; Deployment Manual", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary, spaceAfter=8))

    story.append(Paragraph("<b>Step 1: Navigate to Workspace Directory</b>", h2_style))
    story.append(Paragraph("<code>cd C:\\Users\\Dell\\.gemini\\antigravity\\scratch\\classroom_portal</code>", code_style))

    story.append(Paragraph("<b>Step 2: Install Python Dependencies</b>", h2_style))
    story.append(Paragraph("<code>py -m pip install -r requirements.txt</code>", code_style))

    story.append(Paragraph("<b>Step 3: Load Demo Database (Optional)</b>", h2_style))
    story.append(Paragraph("Populates teacher Sarah, students Alex and Emma, and sample biology assignments:", body_style))
    story.append(Paragraph("<code>py seed_demo.py</code>", code_style))

    story.append(Paragraph("<b>Step 4: Launch Web Server</b>", h2_style))
    story.append(Paragraph("<code>py app.py</code>", code_style))
    story.append(Paragraph("The portal binds to <code>0.0.0.0:5000</code>. Access locally at <b>http://127.0.0.1:5000</b> or over local Wi-Fi via your host IP.", body_style))

    # Pre-seeded Accounts Card
    creds_data = [
        [
            Paragraph("<b>Role / Person</b>", table_header_style),
            Paragraph("<b>Email / Username</b>", table_header_style),
            Paragraph("<b>Password</b>", table_header_style),
            Paragraph("<b>Group / Join Code</b>", table_header_style)
        ],
        [
            Paragraph("<b>Teacher</b>", table_body_style),
            Paragraph("<code>sarah@school.edu</code>", table_body_style),
            Paragraph("<code>password123</code>", table_body_style),
            Paragraph("Grade 10 Biology (Code: <b>BIO101</b>)", table_body_style)
        ],
        [
            Paragraph("<b>Student 1</b>", table_body_style),
            Paragraph("<code>alex@school.edu</code>", table_body_style),
            Paragraph("<code>password123</code>", table_body_style),
            Paragraph("Enrolled (Homework Submitted &amp; Graded)", table_body_style)
        ],
        [
            Paragraph("<b>Student 2</b>", table_body_style),
            Paragraph("<code>emma@school.edu</code>", table_body_style),
            Paragraph("<code>password123</code>", table_body_style),
            Paragraph("Enrolled (Pending Homework Submission)", table_body_style)
        ]
    ]

    creds_table = Table(creds_data, colWidths=[90, 140, 110, 164])
    creds_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 2))
    story.append(creds_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documentation PDF successfully created: {filename}")


if __name__ == '__main__':
    output_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ClassroomPortal_Documentation.pdf')
    build_pdf(output_pdf)
