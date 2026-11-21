import os
import time
import threading
from app import app
from seed_demo import seed
from database import create_connection

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def run_flask():
    app.run(host='127.0.0.1', port=5058, debug=False, use_reloader=False)

def capture_all():
    seed()
    db = create_connection()
    group_id = db.execute("SELECT id FROM groups WHERE name = 'Grade 10 Biology'").fetchone()['id']
    assignment_id = db.execute("SELECT id FROM assignments WHERE group_id = ?", (group_id,)).fetchone()['id']
    sub_id = db.execute("SELECT id FROM submissions WHERE assignment_id = ?", (assignment_id,)).fetchone()['id']
    db.close()

    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    time.sleep(2)

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1280,850')
    options.add_argument('--disable-gpu')
    driver = webdriver.Edge(options=options)

    base_url = 'http://127.0.0.1:5058'

    try:
        # 1. Landing Page
        driver.get(f'{base_url}/')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '01_landing_page.png'))
        print("Captured 01_landing_page.png")

        # 2. Registration Page
        driver.get(f'{base_url}/register')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '02_registration_page.png'))
        print("Captured 02_registration_page.png")

        # 3. Login Page
        driver.get(f'{base_url}/login')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '03_login_page.png'))
        print("Captured 03_login_page.png")

        # 4. Teacher Dashboard
        driver.find_element(By.ID, 'login_input').send_keys('sarah@school.edu')
        driver.find_element(By.ID, 'password').send_keys('password123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '04_teacher_dashboard.png'))
        print("Captured 04_teacher_dashboard.png")

        # 5. Teacher Group Detail
        driver.get(f'{base_url}/teacher/groups/{group_id}')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '05_teacher_group_detail.png'))
        print("Captured 05_teacher_group_detail.png")

        # 6. Create Assignment
        driver.get(f'{base_url}/teacher/groups/{group_id}/assignments/create')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '06_create_assignment.png'))
        print("Captured 06_create_assignment.png")

        # 7. Teacher Submissions Review & Grading Table
        driver.get(f'{base_url}/teacher/assignments/{assignment_id}/submissions')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '07_teacher_submissions_grading.png'))
        print("Captured 07_teacher_submissions_grading.png")

        # 8. Student Dashboard (Alex)
        driver.get(f'{base_url}/logout')
        time.sleep(1)
        driver.get(f'{base_url}/login')
        driver.find_element(By.ID, 'login_input').send_keys('alex@school.edu')
        driver.find_element(By.ID, 'password').send_keys('password123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '08_student_dashboard.png'))
        print("Captured 08_student_dashboard.png")

        # 9. Student Join Group
        driver.get(f'{base_url}/student/groups/join')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '09_student_join_group.png'))
        print("Captured 09_student_join_group.png")

        # 10. Student Assignment Detail & Submission View
        driver.get(f'{base_url}/student/assignments/{assignment_id}')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '10_student_assignment_detail.png'))
        print("Captured 10_student_assignment_detail.png")

        # 11. Security Protection: Student Emma attempts to download Alex's file -> 403 Forbidden
        driver.get(f'{base_url}/logout')
        time.sleep(1)
        driver.get(f'{base_url}/login')
        driver.find_element(By.ID, 'login_input').send_keys('emma@school.edu')
        driver.find_element(By.ID, 'password').send_keys('password123')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(1)
        driver.get(f'{base_url}/submissions/{sub_id}/download')
        time.sleep(1)
        driver.save_screenshot(os.path.join(SCREENSHOTS_DIR, '11_access_denied_403.png'))
        print("Captured 11_access_denied_403.png")

    finally:
        driver.quit()
        print("All 11 real UI screenshots captured successfully!")

if __name__ == '__main__':
    capture_all()
