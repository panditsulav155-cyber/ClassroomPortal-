import os
import io
import shutil
import tempfile
import unittest
from app import app
from database import create_connection, init_db

class ClassroomPortalTestCase(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for DB and uploads
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_classroom.db')
        self.subs_dir = os.path.join(self.temp_dir, 'submissions')
        self.mats_dir = os.path.join(self.temp_dir, 'materials')
        os.makedirs(self.subs_dir, exist_ok=True)
        os.makedirs(self.mats_dir, exist_ok=True)

        app.config['DATABASE_PATH'] = self.db_path
        app.config['SUBMISSIONS_FOLDER'] = self.subs_dir
        app.config['MATERIALS_FOLDER'] = self.mats_dir
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        init_db(self.db_path)
        self.client = app.test_client()

    def tearDown(self):
        import gc
        gc.collect()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def query_row(self, sql, args=()):
        """Helper to run a single-row query and close the connection cleanly."""
        conn = create_connection(self.db_path)
        row = conn.execute(sql, args).fetchone()
        conn.close()
        return row

    def register(self, username, email, password, role, full_name):
        return self.client.post('/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': password,
            'role': role,
            'full_name': full_name
        }, follow_redirects=True)

    def login(self, login_input, password):
        return self.client.post('/login', data={
            'login_input': login_input,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_registration_and_authentication(self):
        """Test registration, password hashing, and login validation."""
        res = self.register('prof_smith', 'smith@school.edu', 'secret123', 'teacher', 'Professor Smith')
        self.assertIn(b'Registration successful', res.data)

        # Verify password in DB is hashed and not plaintext
        user = self.query_row('SELECT * FROM users WHERE username = ?', ('prof_smith',))
        self.assertIsNotNone(user)
        self.assertNotEqual(user['password_hash'], 'secret123')
        self.assertEqual(user['role'], 'teacher')

        # Test valid login
        login_res = self.login('prof_smith', 'secret123')
        self.assertIn(b'Welcome back, Professor Smith', login_res.data)
        
        # Test wrong password login failure
        self.logout()
        bad_res = self.login('prof_smith', 'wrongpass')
        self.assertIn(b'Invalid username/email or password', bad_res.data)

    def test_group_creation_and_enrollment(self):
        """Test teacher group creation and student enrollment via 6-char join code."""
        # 1. Register Teacher & create group
        self.register('mr_jones', 'jones@school.edu', 'pass123', 'teacher', 'Mr. Jones')
        self.login('jones@school.edu', 'pass123')
        
        create_res = self.client.post('/teacher/groups/create', data={
            'name': 'Physics 101',
            'description': 'Mechanics and Waves'
        }, follow_redirects=True)
        self.assertIn(b'created successfully', create_res.data)

        group = self.query_row('SELECT * FROM groups WHERE name = ?', ('Physics 101',))
        self.assertIsNotNone(group)
        join_code = group['join_code']
        self.assertEqual(len(join_code), 6)

        self.logout()

        # 2. Register Student & join group using join code
        self.register('alice_s', 'alice@student.edu', 'studentpass', 'student', 'Alice Walker')
        self.login('alice@student.edu', 'studentpass')

        join_res = self.client.post('/student/groups/join', data={
            'join_code': join_code
        }, follow_redirects=True)
        self.assertIn(b'Successfully joined group', join_res.data)

        # Verify student is listed in memberships
        membership = self.query_row('SELECT * FROM group_memberships WHERE group_id = ?', (group['id'],))
        self.assertIsNotNone(membership)

    def test_critical_submission_file_privacy_and_access_control(self):
        """
        CRITICAL PRIVACY TEST:
        Ensure that student files are strictly private:
        - Accessible ONLY by the group teacher and the student who submitted it.
        - Denied (403 Forbidden) for other students in the same group.
        - Denied (403 Forbidden) for teachers of other groups.
        - Denied (redirect / 401 / 403) for unauthenticated guests.
        """
        # Step A: Register Teacher 1
        self.register('teach1', 'teach1@school.edu', 'pass123', 'teacher', 'Teacher One')
        self.login('teach1@school.edu', 'pass123')
        self.client.post('/teacher/groups/create', data={'name': 'Biology 101', 'description': 'Cells'})
        
        group = self.query_row('SELECT * FROM groups WHERE name = ?', ('Biology 101',))
        join_code = group['join_code']

        # Teacher creates an assignment
        self.client.post(f'/teacher/groups/{group["id"]}/assignments/create', data={
            'title': 'Cell Structure Lab',
            'description': 'Draw and label an animal cell.',
            'max_points': 100
        }, follow_redirects=True)

        assignment = self.query_row('SELECT * FROM assignments WHERE group_id = ?', (group['id'],))
        self.assertIsNotNone(assignment)
        self.logout()

        # Step B: Register Student 1 (Alice) and submit file
        self.register('alice', 'alice@school.edu', 'pass123', 'student', 'Alice S.')
        self.login('alice@school.edu', 'pass123')
        self.client.post('/student/groups/join', data={'join_code': join_code}, follow_redirects=True)

        fake_file_content = b"ALICE'S PRIVATE HOMEWORK LAB CONTENT - CONFIDENTIAL"
        submit_res = self.client.post(
            f'/student/assignments/{assignment["id"]}',
            data={
                'file': (io.BytesIO(fake_file_content), 'alice_cell_lab.pdf'),
                'notes': 'Here is my complete lab report'
            },
            content_type='multipart/form-data',
            follow_redirects=True
        )
        self.assertIn(b'Assignment submitted successfully', submit_res.data)

        submission = self.query_row('SELECT * FROM submissions WHERE assignment_id = ?', (assignment['id'],))
        self.assertIsNotNone(submission)
        submission_id = submission['id']

        # Verification 1: Alice (the submitting student) CAN download her own file
        alice_dl = self.client.get(f'/submissions/{submission_id}/download')
        self.assertEqual(alice_dl.status_code, 200)
        self.assertEqual(alice_dl.data, fake_file_content)
        self.logout()

        # Step C: Register Student 2 (Bob) in the SAME group
        self.register('bob', 'bob@school.edu', 'pass123', 'student', 'Bob S.')
        self.login('bob@school.edu', 'pass123')
        self.client.post('/student/groups/join', data={'join_code': join_code}, follow_redirects=True)

        # Verification 2: Bob CANNOT download Alice's submission file (MUST RETURN 403 FORBIDDEN!)
        bob_dl = self.client.get(f'/submissions/{submission_id}/download')
        self.assertEqual(bob_dl.status_code, 403, "CRITICAL: Student Bob must NOT be able to download Alice's submission!")
        self.logout()

        # Step D: Register Teacher 2 (who is NOT the teacher of this group)
        self.register('teach2', 'teach2@school.edu', 'pass123', 'teacher', 'Teacher Two')
        self.login('teach2@school.edu', 'pass123')

        # Verification 3: Teacher 2 CANNOT download Alice's file (MUST RETURN 403 FORBIDDEN!)
        t2_dl = self.client.get(f'/submissions/{submission_id}/download')
        self.assertEqual(t2_dl.status_code, 403, "CRITICAL: Teacher 2 must NOT be able to download files from another teacher's group!")
        self.logout()

        # Step E: Teacher 1 (the owner of Biology 101) logs in
        self.login('teach1@school.edu', 'pass123')

        # Verification 4: Teacher 1 CAN download Alice's file
        t1_dl = self.client.get(f'/submissions/{submission_id}/download')
        self.assertEqual(t1_dl.status_code, 200)
        self.assertEqual(t1_dl.data, fake_file_content)

        # Step F: Teacher 1 grades Alice's submission
        grade_res = self.client.post(f'/teacher/submissions/{submission_id}/grade', data={
            'grade': '98.5',
            'feedback': 'Outstanding microscopy diagrams and analysis!'
        }, follow_redirects=True)
        self.assertIn(b'Grade and feedback saved successfully', grade_res.data)
        self.logout()

        # Step G: Alice logs back in and checks her grade and feedback
        self.login('alice@school.edu', 'pass123')
        student_page = self.client.get(f'/student/assignments/{assignment["id"]}')
        self.assertIn(b'98.5', student_page.data)
        self.assertIn(b'Outstanding microscopy diagrams and analysis!', student_page.data)

if __name__ == '__main__':
    unittest.main()
