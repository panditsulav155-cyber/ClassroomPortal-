import os
from werkzeug.security import generate_password_hash
from database import create_connection, init_db, DATABASE_PATH

def seed():
    init_db()
    db = create_connection()

    # Clear existing demo data if any
    with db:
        db.execute("DELETE FROM submissions")
        db.execute("DELETE FROM assignments")
        db.execute("DELETE FROM group_memberships")
        db.execute("DELETE FROM groups")
        db.execute("DELETE FROM users")

    # 1. Create Teacher
    pw_hash = generate_password_hash('password123')
    with db:
        cur = db.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (?, ?, ?, ?, ?)
        ''', ('teacher_sarah', 'sarah.connor@gmail.com', pw_hash, 'teacher', 'Sarah Connor'))
        teacher_id = cur.lastrowid

        # 2. Create Group
        cur = db.execute('''
            INSERT INTO groups (name, description, join_code, teacher_id)
            VALUES (?, ?, ?, ?)
        ''', ('Grade 10 Biology', 'Cellular biology, genetics, and lab exercises.', 'BIO101', teacher_id))
        group_id = cur.lastrowid

        # 3. Create Assignment
        cur = db.execute('''
            INSERT INTO assignments (group_id, title, description, due_date, max_points)
            VALUES (?, ?, ?, ?, ?)
        ''', (group_id, 'Assignment 1: Cell Membrane Lab', 'Draw and label the fluid mosaic model. Explain the phospholipid bilayer and proteins.', '2026-10-15 23:59', 100))
        assignment_id = cur.lastrowid

        # 4. Create Students
        cur = db.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (?, ?, ?, ?, ?)
        ''', ('student_alex', 'alex.rivera@gmail.com', pw_hash, 'student', 'Alex Rivera'))
        alex_id = cur.lastrowid

        cur = db.execute('''
            INSERT INTO users (username, email, password_hash, role, full_name)
            VALUES (?, ?, ?, ?, ?)
        ''', ('student_emma', 'emma.watson@gmail.com', pw_hash, 'student', 'Emma Watson'))
        emma_id = cur.lastrowid

        # 5. Enroll Students in Group
        db.execute('INSERT INTO group_memberships (group_id, student_id) VALUES (?, ?)', (group_id, alex_id))
        db.execute('INSERT INTO group_memberships (group_id, student_id) VALUES (?, ?)', (group_id, emma_id))

        # 6. Create Alex's Submission
        submissions_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', 'submissions')
        os.makedirs(submissions_dir, exist_ok=True)
        demo_filename = 'sub_demo_alex_cell_model.txt'
        demo_filepath = os.path.join(submissions_dir, demo_filename)
        with open(demo_filepath, 'w', encoding='utf-8') as f:
            f.write("Alex Rivera's Homework Submission:\n\nThe fluid mosaic model describes the cell membrane as a tapestry of phospholipids, cholesterol, and proteins.")

        db.execute('''
            INSERT INTO submissions (assignment_id, student_id, stored_filename, original_filename, notes, grade, feedback, graded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (assignment_id, alex_id, demo_filename, 'cell_membrane_diagram.txt', 'Completed after Friday lab!', 95.0, 'Very good diagram and explanation!'))

    print("=" * 60)
    print("ClassroomPortal demo database seeded successfully!")
    print("=" * 60)
    print("Teacher Account:")
    print("  Full Name: Sarah Connor (starts with letter S)")
    print("  Username: teacher_sarah  (or email: sarah.connor@gmail.com)")
    print("  Password: password123")
    print("  Role: Teacher")
    print("  Group: Grade 10 Biology (Join Code: BIO101)")
    print("-" * 60)
    print("Student 1 (Has Submitted Homework):")
    print("  Full Name: Alex Rivera (starts with letter A)")
    print("  Username: student_alex  (or email: alex.rivera@gmail.com)")
    print("  Password: password123")
    print("  Role: Student")
    print("-" * 60)
    print("Student 2 (Pending Submission):")
    print("  Full Name: Emma Watson (starts with letter E)")
    print("  Username: student_emma  (or email: emma.watson@gmail.com)")
    print("  Password: password123")
    print("  Role: Student")
    print("=" * 60)

if __name__ == '__main__':
    seed()
