"""
ClassroomPortal Production WSGI Entry Point
For deployment on Gunicorn, Waitress, uWSGI, or AWS Elastic Beanstalk / Render / Railway.
"""
from app import app

if __name__ == "__main__":
    app.run()
