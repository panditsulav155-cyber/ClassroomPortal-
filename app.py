import os
import re
import secrets
import uuid
from functools import wraps
from datetime import datetime

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, abort, send_from_directory, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from database import create_connection, init_db, DATABASE_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATERIALS_FOLDER = os.path.join(BASE_DIR, 'uploads', 'materials')
SUBMISSIONS_FOLDER = os.path.join(BASE_DIR, 'uploads', 'submissions')

os.makedirs(MATERIALS_FOLDER, exist_ok=True)
os.makedirs(SUBMISSIONS_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'classroom-secret-key-2026')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max upload
app.config['DATABASE_PATH'] = DATABASE_PATH
app.config['MATERIALS_FOLDER'] = MATERIALS_FOLDER
app.config['SUBMISSIONS_FOLDER'] = SUBMISSIONS_FOLDER

def get_submissions_folder():
    folder = app.config.get('SUBMISSIONS_FOLDER', SUBMISSIONS_FOLDER)
    os.makedirs(folder, exist_ok=True)
    return folder

def get_materials_folder():
    folder = app.config.get('MATERIALS_FOLDER', MATERIALS_FOLDER)
    os.makedirs(folder, exist_ok=True)
    return folder


# Initialize database if not already created
if not os.path.exists(DATABASE_PATH):
    init_db()

def get_db():
    """Returns a per-request SQLite database connection from Flask context."""
    db = getattr(g, '_database', None)
    if db is None:
        db_file = app.config.get('DATABASE_PATH', DATABASE_PATH)
        db = g._database = create_connection(db_file)
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the SQLite database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_current_user():
    """Fetches currently logged-in user from the database."""
    if 'user_id' not in session:
        return None
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    return user


@app.before_request
def load_user():
    g.user = get_current_user()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user['role'] != 'teacher':
            flash('Access restricted to teachers only.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or g.user['role'] != 'student':
            flash('Access restricted to students only.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def generate_join_code():
    """Generates a clean 6-character uppercase join code."""
    alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return ''.join(secrets.choice(alphabet) for _ in range(6))

# --- Public & Auth Routes ---

@app.route('/')
def index():
    if g.user:
        if g.user['role'] == 'teacher':
            return redirect(url_for('teacher_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()

        # 1. Mandatory Fields Check ("mail paspost ko nessasary")
        if not full_name:
            flash('Full Name is required.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        if not username:
            flash('Username is required.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        if not email:
            flash('Email address is required.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        if not password:
            flash('Password is required.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        # 2. Role Validation ("teacher student xuttini gari rakha")
        if role not in ('teacher', 'student'):
            flash('Please choose whether you are registering as a Student or Teacher.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        # 3. Name Validation ("name latter bata huna paryo")
        # Full name must start with an alphabet letter (A-Z)
        if not re.match(r'^[A-Za-z]', full_name):
            flash('Full Name must start with an alphabet letter (A-Z). Numbers or symbols are not allowed at the beginning.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        if not re.match(r"^[A-Za-z][A-Za-z\s.\'-]{1,49}$", full_name):
            flash('Full Name must contain only alphabet letters, spaces, and valid name characters (2-50 characters).', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        # Username must start with an alphabet letter (A-Z)
        if not re.match(r'^[A-Za-z]', username):
            flash('Username must start with an alphabet letter (A-Z). Numbers or symbols are not allowed at the beginning.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        if not re.match(r'^[A-Za-z][A-Za-z0-9_]{2,29}$', username):
            flash('Username must start with a letter and contain only letters, numbers, or underscores (3-30 characters).', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        # 4. Email Validation ("mail ma gmail.com")
        if not re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email):
            flash('Email must be a valid Gmail address ending with @gmail.com (e.g., yourname@gmail.com).', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        # 5. Password Validation ("paspost ko nessasary")
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        if password != confirm_password:
            flash('Passwords do not match. Please re-enter your password.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        db = get_db()
        existing = db.execute(
            'SELECT id FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?',
            (username.lower(), email)
        ).fetchone()

        if existing:
            flash('Username or Gmail address is already registered. Please log in or use another.', 'danger')
            return render_template('auth/register.html', full_name=full_name, username=username, email=email, role=role)

        password_hash = generate_password_hash(password)
        with db:
            db.execute(
                '''INSERT INTO users (username, email, password_hash, role, full_name)
                   VALUES (?, ?, ?, ?, ?)''',
                (username, email, password_hash, role, full_name)
            )

        role_label = '👨‍🏫 Teacher' if role == 'teacher' else '👨‍🎓 Student'
        flash(f'Registration successful as {role_label}! You can now log in with your Gmail or username.', 'success')
        return redirect(url_for('login'))

    return render_template('auth/register.html', role='student')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('index'))

    if request.method == 'POST':
        login_input = request.form.get('login_input', '').strip().lower()
        password = request.form.get('password', '')

        if not login_input or not password:
            flash('Please enter both your Gmail/username and password.', 'danger')
            return render_template('auth/login.html')

        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?',
            (login_input, login_input)
        ).fetchone()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            role_label = '👨‍🏫 Teacher' if user['role'] == 'teacher' else '👨‍🎓 Student'
            flash(f"Welcome back, {user['full_name']}! ({role_label})", 'success')
            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            flash('Invalid username/Gmail or password.', 'danger')

    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# --- Teacher Routes ---

@app.route('/teacher/dashboard')
@teacher_required
def teacher_dashboard():
    db = get_db()
    groups = db.execute(
        '''SELECT g.*, 
                  (SELECT COUNT(*) FROM group_memberships m WHERE m.group_id = g.id) AS student_count,
                  (SELECT COUNT(*) FROM assignments a WHERE a.group_id = g.id) AS assignment_count
           FROM groups g 
           WHERE g.teacher_id = ? 
           ORDER BY g.created_at DESC''',
        (g.user['id'],)
    ).fetchall()
    return render_template('teacher/dashboard.html', groups=groups)

@app.route('/teacher/groups/create', methods=['GET', 'POST'])
@teacher_required
def teacher_create_group():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not name:
            flash('Group name is required.', 'danger')
            return render_template('teacher/create_group.html')

        db = get_db()
        join_code = generate_join_code()
        # Ensure code uniqueness
        while db.execute('SELECT id FROM groups WHERE join_code = ?', (join_code,)).fetchone():
            join_code = generate_join_code()

        with db:
            db.execute(
                '''INSERT INTO groups (name, description, join_code, teacher_id)
                   VALUES (?, ?, ?, ?)''',
                (name, description, join_code, g.user['id'])
            )

        flash(f'Group "{name}" created successfully with join code: {join_code}', 'success')
        return redirect(url_for('teacher_dashboard'))

    return render_template('teacher/create_group.html')

@app.route('/teacher/groups/<int:group_id>')
@teacher_required
def teacher_group_detail(group_id):
    db = get_db()
    group = db.execute(
        'SELECT * FROM groups WHERE id = ? AND teacher_id = ?',
        (group_id, g.user['id'])
    ).fetchone()

    if not group:
        flash('Group not found or access unauthorized.', 'danger')
        return redirect(url_for('teacher_dashboard'))

    assignments = db.execute(
        '''SELECT a.*,
                  (SELECT COUNT(*) FROM submissions s WHERE s.assignment_id = a.id) AS submission_count,
                  (SELECT COUNT(*) FROM group_memberships m WHERE m.group_id = a.group_id) AS total_students
           FROM assignments a
           WHERE a.group_id = ?
           ORDER BY a.created_at DESC''',
        (group_id,)
    ).fetchall()

    members = db.execute(
        '''SELECT u.id, u.full_name, u.email, u.username, m.joined_at
           FROM group_memberships m
           JOIN users u ON m.student_id = u.id
           WHERE m.group_id = ?
           ORDER BY u.full_name ASC''',
        (group_id,)
    ).fetchall()

    return render_template('teacher/group_detail.html', group=group, assignments=assignments, members=members)

@app.route('/teacher/groups/<int:group_id>/assignments/create', methods=['GET', 'POST'])
@teacher_required
def teacher_create_assignment(group_id):
    db = get_db()
    group = db.execute(
        'SELECT * FROM groups WHERE id = ? AND teacher_id = ?',
        (group_id, g.user['id'])
    ).fetchone()

    if not group:
        flash('Group not found or access unauthorized.', 'danger')
        return redirect(url_for('teacher_dashboard'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date = request.form.get('due_date', '').strip()
        max_points = request.form.get('max_points', 100)

        if not title or not description:
            flash('Assignment title and description are required.', 'danger')
            return render_template('teacher/create_assignment.html', group=group)

        try:
            max_points = int(max_points)
        except ValueError:
            max_points = 100

        attachment_filename = None
        original_attachment_name = None

        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                orig_name = secure_filename(file.filename)
                if orig_name:
                    stored_name = f"mat_{uuid.uuid4().hex}_{orig_name}"
                    file.save(os.path.join(get_materials_folder(), stored_name))
                    attachment_filename = stored_name
                    original_attachment_name = file.filename

        with db:
            db.execute(
                '''INSERT INTO assignments (group_id, title, description, due_date, max_points, attachment_filename, original_attachment_name)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (group_id, title, description, due_date, max_points, attachment_filename, original_attachment_name)
            )

        flash(f'Assignment "{title}" published successfully!', 'success')
        return redirect(url_for('teacher_group_detail', group_id=group_id))

    return render_template('teacher/create_assignment.html', group=group)

@app.route('/teacher/assignments/<int:assignment_id>/submissions')
@teacher_required
def teacher_assignment_submissions(assignment_id):
    db = get_db()
    assignment = db.execute(
        '''SELECT a.*, g.name AS group_name, g.teacher_id
           FROM assignments a
           JOIN groups g ON a.group_id = g.id
           WHERE a.id = ? AND g.teacher_id = ?''',
        (assignment_id, g.user['id'])
    ).fetchone()

    if not assignment:
        flash('Assignment not found or access unauthorized.', 'danger')
        return redirect(url_for('teacher_dashboard'))

    # Retrieve all enrolled students along with their submissions (if any)
    students = db.execute(
        '''SELECT u.id AS student_id, u.full_name, u.email,
                  s.id AS submission_id, s.stored_filename, s.original_filename,
                  s.notes, s.submitted_at, s.grade, s.feedback, s.graded_at
           FROM group_memberships m
           JOIN users u ON m.student_id = u.id
           LEFT JOIN submissions s ON s.assignment_id = ? AND s.student_id = u.id
           WHERE m.group_id = ?
           ORDER BY u.full_name ASC''',
        (assignment_id, assignment['group_id'])
    ).fetchall()

    return render_template('teacher/submissions.html', assignment=assignment, students=students)

@app.route('/teacher/submissions/<int:submission_id>/grade', methods=['POST'])
@teacher_required
def teacher_grade_submission(submission_id):
    db = get_db()
    submission = db.execute(
        '''SELECT s.*, a.max_points, a.id AS assignment_id, g.teacher_id
           FROM submissions s
           JOIN assignments a ON s.assignment_id = a.id
           JOIN groups g ON a.group_id = g.id
           WHERE s.id = ? AND g.teacher_id = ?''',
        (submission_id, g.user['id'])
    ).fetchone()

    if not submission:
        flash('Submission not found or access unauthorized.', 'danger')
        return redirect(url_for('teacher_dashboard'))

    grade_input = request.form.get('grade', '').strip()
    feedback = request.form.get('feedback', '').strip()

    try:
        grade = float(grade_input) if grade_input else None
    except ValueError:
        flash('Invalid grade number.', 'danger')
        return redirect(url_for('teacher_assignment_submissions', assignment_id=submission['assignment_id']))

    with db:
        db.execute(
            '''UPDATE submissions 
               SET grade = ?, feedback = ?, graded_at = CURRENT_TIMESTAMP
               WHERE id = ?''',
            (grade, feedback, submission_id)
        )

    flash('Grade and feedback saved successfully.', 'success')
    return redirect(url_for('teacher_assignment_submissions', assignment_id=submission['assignment_id']))

# --- Student Routes ---

@app.route('/student/dashboard')
@student_required
def student_dashboard():
    db = get_db()
    enrolled_groups = db.execute(
        '''SELECT g.*, u.full_name AS teacher_name,
                  (SELECT COUNT(*) FROM assignments a WHERE a.group_id = g.id) AS assignment_count
           FROM group_memberships m
           JOIN groups g ON m.group_id = g.id
           JOIN users u ON g.teacher_id = u.id
           WHERE m.student_id = ?
           ORDER BY m.joined_at DESC''',
        (g.user['id'],)
    ).fetchall()

    # Active upcoming assignments
    pending_assignments = db.execute(
        '''SELECT a.*, g.name AS group_name, u.full_name AS teacher_name,
                  s.id AS submission_id, s.grade, s.graded_at
           FROM group_memberships m
           JOIN assignments a ON m.group_id = a.group_id
           JOIN groups g ON a.group_id = g.id
           JOIN users u ON g.teacher_id = u.id
           LEFT JOIN submissions s ON s.assignment_id = a.id AND s.student_id = ?
           WHERE m.student_id = ?
           ORDER BY a.due_date ASC, a.created_at DESC''',
        (g.user['id'], g.user['id'])
    ).fetchall()

    return render_template('student/dashboard.html', groups=enrolled_groups, assignments=pending_assignments)

@app.route('/student/groups/join', methods=['GET', 'POST'])
@student_required
def student_join_group():
    if request.method == 'POST':
        join_code = request.form.get('join_code', '').strip().upper()
        if not join_code:
            flash('Please enter a group join code.', 'danger')
            return render_template('student/join_group.html')

        db = get_db()
        group = db.execute('SELECT * FROM groups WHERE UPPER(join_code) = ?', (join_code,)).fetchone()

        if not group:
            flash('No group found with that join code. Please verify with your teacher.', 'danger')
            return render_template('student/join_group.html')

        # Check if already joined
        membership = db.execute(
            'SELECT id FROM group_memberships WHERE group_id = ? AND student_id = ?',
            (group['id'], g.user['id'])
        ).fetchone()

        if membership:
            flash(f'You are already enrolled in "{group["name"]}".', 'info')
            return redirect(url_for('student_group_detail', group_id=group['id']))

        with db:
            db.execute(
                'INSERT INTO group_memberships (group_id, student_id) VALUES (?, ?)',
                (group['id'], g.user['id'])
            )

        flash(f'Successfully joined group "{group["name"]}"!', 'success')
        return redirect(url_for('student_group_detail', group_id=group['id']))

    return render_template('student/join_group.html')

@app.route('/student/groups/<int:group_id>')
@student_required
def student_group_detail(group_id):
    db = get_db()
    membership = db.execute(
        'SELECT * FROM group_memberships WHERE group_id = ? AND student_id = ?',
        (group_id, g.user['id'])
    ).fetchone()

    if not membership:
        flash('You are not enrolled in this group.', 'danger')
        return redirect(url_for('student_dashboard'))

    group = db.execute(
        '''SELECT g.*, u.full_name AS teacher_name, u.email AS teacher_email
           FROM groups g
           JOIN users u ON g.teacher_id = u.id
           WHERE g.id = ?''',
        (group_id,)
    ).fetchone()

    assignments = db.execute(
        '''SELECT a.*,
                  s.id AS submission_id, s.submitted_at, s.grade, s.feedback
           FROM assignments a
           LEFT JOIN submissions s ON s.assignment_id = a.id AND s.student_id = ?
           WHERE a.group_id = ?
           ORDER BY a.created_at DESC''',
        (g.user['id'], group_id)
    ).fetchall()

    return render_template('student/group_detail.html', group=group, assignments=assignments)

@app.route('/student/assignments/<int:assignment_id>', methods=['GET', 'POST'])
@student_required
def student_assignment_detail(assignment_id):
    db = get_db()
    assignment = db.execute(
        '''SELECT a.*, g.name AS group_name, g.id AS group_id, u.full_name AS teacher_name
           FROM assignments a
           JOIN groups g ON a.group_id = g.id
           JOIN users u ON g.teacher_id = u.id
           JOIN group_memberships m ON m.group_id = g.id
           WHERE a.id = ? AND m.student_id = ?''',
        (assignment_id, g.user['id'])
    ).fetchone()

    if not assignment:
        flash('Assignment not found or you are not enrolled in this group.', 'danger')
        return redirect(url_for('student_dashboard'))

    submission = db.execute(
        'SELECT * FROM submissions WHERE assignment_id = ? AND student_id = ?',
        (assignment_id, g.user['id'])
    ).fetchone()

    if request.method == 'POST':
        notes = request.form.get('notes', '').strip()

        if 'file' not in request.files or not request.files['file'].filename:
            if not submission:
                flash('Please select a file to submit.', 'danger')
                return render_template('student/assignment_detail.html', assignment=assignment, submission=submission)
            # If already submitted and only updating notes
            with db:
                db.execute(
                    'UPDATE submissions SET notes = ? WHERE id = ?',
                    (notes, submission['id'])
                )
            flash('Submission notes updated successfully.', 'success')
            return redirect(url_for('student_assignment_detail', assignment_id=assignment_id))

        file = request.files['file']
        orig_name = secure_filename(file.filename)
        if not orig_name:
            flash('Invalid file name.', 'danger')
            return render_template('student/assignment_detail.html', assignment=assignment, submission=submission)

        stored_name = f"sub_{uuid.uuid4().hex}_{orig_name}"
        submissions_dir = get_submissions_folder()
        file.save(os.path.join(submissions_dir, stored_name))

        with db:
            if submission:
                # Remove old file from disk if desired or overwrite record
                try:
                    old_path = os.path.join(submissions_dir, submission['stored_filename'])
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass

                db.execute(
                    '''UPDATE submissions 
                       SET stored_filename = ?, original_filename = ?, notes = ?, submitted_at = CURRENT_TIMESTAMP
                       WHERE id = ?''',
                    (stored_name, file.filename, notes, submission['id'])
                )
                flash('Assignment resubmitted successfully! Your teacher can view your updated file.', 'success')
            else:
                db.execute(
                    '''INSERT INTO submissions (assignment_id, student_id, stored_filename, original_filename, notes)
                       VALUES (?, ?, ?, ?, ?)''',
                    (assignment_id, g.user['id'], stored_name, file.filename, notes)
                )
                flash('Assignment submitted successfully! Your teacher can now review your file.', 'success')

        return redirect(url_for('student_assignment_detail', assignment_id=assignment_id))

    return render_template('student/assignment_detail.html', assignment=assignment, submission=submission)

# --- STRICT ACCESS-CONTROLLED FILE DOWNLOADS ---

@app.route('/submissions/<int:submission_id>/download')
@login_required
def download_submission_file(submission_id):
    """
    CRITICAL SECURITY ENDPOINT:
    Only the assigned teacher of the group OR the submitting student
    is authorized to download this file.
    All other students or unauthorized users are strictly denied (HTTP 403).
    """
    db = get_db()
    sub_info = db.execute(
        '''SELECT s.id, s.stored_filename, s.original_filename, s.student_id,
                  g.teacher_id, a.title AS assignment_title, u.full_name AS student_name
           FROM submissions s
           JOIN assignments a ON s.assignment_id = a.id
           JOIN groups g ON a.group_id = g.id
           JOIN users u ON s.student_id = u.id
           WHERE s.id = ?''',
        (submission_id,)
    ).fetchone()

    if not sub_info:
        abort(404, "Submission record not found.")

    # Authorization Check
    is_teacher = (g.user['role'] == 'teacher' and g.user['id'] == sub_info['teacher_id'])
    is_owner_student = (g.user['role'] == 'student' and g.user['id'] == sub_info['student_id'])

    if not (is_teacher or is_owner_student):
        # Strictly forbidden
        abort(403, "Access Denied: Student files can only be accessed by the teacher of this group or the student who submitted it.")

    sub_dir = get_submissions_folder()
    file_path = os.path.join(sub_dir, sub_info['stored_filename'])
    if not os.path.exists(file_path):
        abort(404, "Requested file does not exist on disk.")

    return send_from_directory(
        sub_dir,
        sub_info['stored_filename'],
        as_attachment=True,
        download_name=sub_info['original_filename']
    )

@app.route('/assignments/<int:assignment_id>/attachment')
@login_required
def download_assignment_attachment(assignment_id):
    """Allows enrolled students or the group teacher to download assignment materials."""
    db = get_db()
    assignment = db.execute(
        '''SELECT a.*, g.teacher_id,
                  (SELECT id FROM group_memberships m WHERE m.group_id = a.group_id AND m.student_id = ?) AS membership_id
           FROM assignments a
           JOIN groups g ON a.group_id = g.id
           WHERE a.id = ?''',
        (g.user['id'], assignment_id)
    ).fetchone()

    if not assignment or not assignment['attachment_filename']:
        abort(404, "Attachment not found.")

    # Authorization: Either teacher of group OR enrolled student
    is_teacher = (g.user['role'] == 'teacher' and g.user['id'] == assignment['teacher_id'])
    is_enrolled = (g.user['role'] == 'student' and assignment['membership_id'] is not None)

    if not (is_teacher or is_enrolled):
        abort(403, "Access Denied: You must be the teacher or enrolled in this group to access course materials.")

    mat_dir = get_materials_folder()
    file_path = os.path.join(mat_dir, assignment['attachment_filename'])
    if not os.path.exists(file_path):
        abort(404, "File not found on server.")

    return send_from_directory(
        mat_dir,
        assignment['attachment_filename'],
        as_attachment=True,
        download_name=assignment['original_attachment_name'] or assignment['attachment_filename']
    )

if __name__ == '__main__':
    print("ClassroomPortal is running!")
    print("  Local (Only this PC): http://127.0.0.1:5000")
    print("  Network (Same Wi-Fi): http://0.0.0.0:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
