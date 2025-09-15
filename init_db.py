import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

# Add the current directory to the path so we can import our app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our app and models
from app import app, db
from models import Teacher, Student

def init_db():
    """Initialize the database with sample data"""
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if we already have data
        if Teacher.query.count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        # Create a sample teacher
        teacher = Teacher(
            name="Demo Teacher",
            email="teacher@example.com",
            password=generate_password_hash("password123")
        )
        db.session.add(teacher)
        db.session.commit()
        
        # Create sample students
        students = [
            Student(
                name="John Smith",
                father_name="David Smith",
                address="123 Main St, Anytown",
                class_name="10A",
                phone="1234567890",
                status="present",
                teacher_id=teacher.id
            ),
            Student(
                name="Emily Johnson",
                father_name="Robert Johnson",
                address="456 Oak Ave, Somewhere",
                class_name="10A",
                phone="2345678901",
                status="present",
                teacher_id=teacher.id
            ),
            Student(
                name="Michael Brown",
                father_name="James Brown",
                address="789 Pine Rd, Nowhere",
                class_name="10B",
                phone="3456789012",
                status="absent",
                teacher_id=teacher.id
            ),
            Student(
                name="Sarah Davis",
                father_name="Thomas Davis",
                address="321 Elm St, Anywhere",
                class_name="10B",
                phone="4567890123",
                status="present",
                teacher_id=teacher.id
            ),
            Student(
                name="Alex Wilson",
                father_name="Charles Wilson",
                address="654 Maple Dr, Everywhere",
                class_name="11A",
                phone="5678901234",
                status="present",
                teacher_id=teacher.id
            )
        ]
        
        for student in students:
            db.session.add(student)
        
        db.session.commit()
        print("Database initialized with sample data!")
        print(f"Teacher login: teacher@example.com / password123")

if __name__ == "__main__":
    init_db()