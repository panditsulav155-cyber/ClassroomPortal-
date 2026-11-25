import os
import io
import shutil
import tempfile
import unittest
from app import app
from database import create_connection, init_db

class ClassroomPortalTestCase(unittest.TestCase):
    def setUp(self):
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
        conn = create_connection(self.db_path)
        row = conn.execute(sql, args).fetchone()
        conn.close()
        return row

    def register(self, username, email, password, role, full_name, confirm_password=None):
        if confirm_password is None:
            confirm_password = password
        return self.client.post('/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
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

    def test_registration_validation_rules(self):
        """Verify strict mandatory fields and validation rules."""
        # 1. Non-Gmail rejection
        res_non_gmail = self.register('prof_smith', 'smith@school.edu', 'secret123', 'teacher', 'Professor Smith')
        self.assertIn(b'Email must be a valid Gmail address', res_non_gmail.data)

        # 2. Name starting with number rejection
        res_bad_name = self.register('prof_smith', 'smith@gmail.com', 'secret123', 'teacher', '123Professor Smith')
        self.assertIn(b'Full Name must start with an alphabet letter', res_bad_name.data)

        # 3. Username starting with number rejection
        res_bad_uname = self.register('123smith', 'smith@gmail.com', 'secret123', 'teacher', 'Professor Smith')
        self.assertIn(b'Username must start with an alphabet letter', res_bad_uname.data)

        # 4. Short password rejection
        res_short_pw = self.register('prof_smith', 'smith@gmail.com', '123', 'teacher', 'Professor Smith')
        self.assertIn(b'Password must be at least 6 characters long', res_short_pw.data)

        # 5. Password mismatch rejection
        res_mismatch = self.register('prof_smith', 'smith@gmail.com', 'secret123', 'teacher', 'Professor Smith', confirm_password='different123')
        self.assertIn(b'Passwords do not match', res_mismatch.data)

        # 6. Invalid role rejection
        res_bad_role = self.register('prof_smith', 'smith@gmail.com', 'secret123', 'admin', 'Professor Smith')
        self.assertIn(b'Please choose whether you are registering as a Student or Teacher', res_bad_role.data)

        # 7. Valid registration succeeds
        res_valid = self.register('prof_smith', 'smith@gmail.com', 'secret123', 'teacher', 'Professor Smith')
        self.assertIn(b'Registration successful', res_valid.data)

    def test_group_and_mandatory_fields(self):
        """Test teacher group creation and mandatory field enforcement."""
        self.register('mr_jones', 'jones@gmail.com', 'pass123', 'teacher', 'Mr. Jones')
        self.login('jones@gmail.com', 'pass123')

        # Empty description rejection
        bad_create = self.client.post('/teacher/groups/create', data={
            'name': 'Physics 101',
            'subject': 'Physics',
            'description': ''
        }, follow_redirects=True)
        self.assertIn(b'mandatory', bad_create.data)

        # Successful creation with subject and description
        create_res = self.client.post('/teacher/groups/create', data={
            'name': 'Physics 101',
            'subject': 'Physical Sciences',
            'description': 'Classical mechanics and wave kinetics.'
        }, follow_redirects=True)
        self.assertIn(b'created successfully', create_res.data)

        group = self.query_row('SELECT * FROM groups WHERE name = ?', ('Physics 101',))
        self.assertIsNotNone(group)
        self.assertEqual(group['subject'], 'Physical Sciences')
        self.assertEqual(len(group['join_code']), 6)

    def test_announcements_and_csv_export(self):
        """Test announcement creation and gradebook CSV export."""
        self.register('prof_davis', 'davis@gmail.com', 'pass123', 'teacher', 'Professor Davis')
        self.login('davis@gmail.com', 'pass123')

        # Create group
        self.client.post('/teacher/groups/create', data={
            'name': 'Chemistry 101',
            'subject': 'Chemical Sciences',
            'description': 'Organic synthesis lab.'
        }, follow_redirects=True)
        group = self.query_row('SELECT * FROM groups WHERE name = ?', ('Chemistry 101',))

        # Create announcement
        ann_res = self.client.post(f'/teacher/groups/{group["id"]}/announcements/create', data={
            'title': 'Safety Goggles Required',
            'content': 'All students must bring approved goggles to lab.',
            'is_pinned': '1'
        }, follow_redirects=True)
        self.assertIn(b'Announcement published', ann_res.data)

        ann = self.query_row('SELECT * FROM announcements WHERE group_id = ?', (group['id'],))
        self.assertIsNotNone(ann)
        self.assertEqual(ann['title'], 'Safety Goggles Required')

        # Test CSV export endpoint
        csv_res = self.client.get(f'/teacher/groups/{group["id"]}/export-csv')
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn('text/csv', csv_res.headers.get('Content-Type', ''))
        self.assertIn(b'Student ID,Student Name', csv_res.data)

    def test_critical_submission_file_privacy_and_access_control(self):
        """
        CRITICAL IDOR MITIGATION TEST:
        Ensure that student files are strictly private:
        - Accessible ONLY by the group teacher and the student who submitted it.
        - Denied (403 Forbidden) for other students in the same group.
        - Denied (403 Forbidden) for teachers of other groups.
        """
        # 1. Register Teacher 1
        self.register('teach1', 'teach1@gmail.com', 'pass123', 'teacher', 'Teacher One')
        self.login('teach1@gmail.com', 'pass123')
        self.client.post('/teacher/groups/create', data={
            'name': 'Biology 101',
            'subject': 'Life Sciences',
            'description': 'Cellular biology fundamentals.'
        }, follow_redirects=True)

        group = self.query_row('SELECT * FROM groups WHERE name = ?', ('Biology 101',))
        join_code = group['join_code']

        # Teacher creates assignment
        self.client.post(f'/teacher/groups/{group["id"]}/assignments/create', data={
            'title': 'Cell Structure Lab',
            'description': 'Draw and label an animal cell.',
            'due_date': '2026-12-30 23:59',
            'max_points': 100
        }, follow_redirects=True)

        assignment = self.query_row('SELECT * FROM assignments WHERE group_id = ?', (group['id'],))
        self.logout()

        # 2. Register Student 1 (Alice) and submit file
        self.register('alice', 'alice@gmail.com', 'pass123', 'student', 'Alice Scott')
        self.login('alice@gmail.com', 'pass123')
        self.client.post('/student/groups/join', data={'join_code': join_code}, follow_redirects=True)

        fake_file_content = b"ALICE CONFIDENTIAL HOMEWORK LAB - PRIVATE"
        submit_res = self.client.post(
            f'/student/assignments/{assignment["id"]}',
            data={
                'file': (io.BytesIO(fake_file_content), 'alice_cell_lab.pdf'),
                'notes': 'Complete lab conclusions'
            },
            content_type='multipart/form-data',
            follow_redirects=True
        )
        self.assertIn(b'Assignment submitted successfully', submit_res.data)

        submission = self.query_row('SELECT * FROM submissions WHERE assignment_id = ?', (assignment['id'],))
        sub_id = submission['id']

        # Alice CAN download her own file
        alice_dl = self.client.get(f'/submissions/{sub_id}/download')
        self.assertEqual(alice_dl.status_code, 200)
        self.assertEqual(alice_dl.data, fake_file_content)
        self.logout()

        # 3. Register Student 2 (Bob) in the SAME group
        self.register('bob', 'bob@gmail.com', 'pass123', 'student', 'Bob Scott')
        self.login('bob@gmail.com', 'pass123')
        self.client.post('/student/groups/join', data={'join_code': join_code}, follow_redirects=True)

        # Bob CANNOT download Alice's submission (MUST RETURN 403 FORBIDDEN!)
        bob_dl = self.client.get(f'/submissions/{sub_id}/download')
        self.assertEqual(bob_dl.status_code, 403, "CRITICAL: Bob must be rejected with 403 Forbidden!")
        self.logout()

        # 4. Teacher 1 grades Alice's work
        self.login('teach1@gmail.com', 'pass123')
        grade_res = self.client.post(f'/teacher/submissions/{sub_id}/grade', data={
            'grade': '98.5',
            'feedback': 'Outstanding microscopy analysis!'
        }, follow_redirects=True)
        self.assertIn(b'Grade and evaluative feedback saved successfully', grade_res.data)

        # Teacher 1 assignment CSV export
        asgn_csv = self.client.get(f'/teacher/assignments/{assignment["id"]}/export-csv')
        self.assertEqual(asgn_csv.status_code, 200)
        self.assertIn(b'Alice Scott', asgn_csv.data)
        self.assertIn(b'98.5', asgn_csv.data)

if __name__ == '__main__':
    unittest.main()
