import os
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json
import os
import pymysql
from dotenv import load_dotenv

# Configure PyMySQL as the driver for MySQL
pymysql.install_as_MySQLdb()

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')

# Configure database URI
database_url = os.environ.get('DATABASE_URL')

# If running on Render, adjust the database URL if needed
if 'RENDER' in os.environ:
    # Use the DATABASE_URL from environment variables
    pass
else:
    # Use the DATABASE_URL from .env file or fallback to SQLite
    if not database_url:
        database_url = 'sqlite:///students.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after initializing db to avoid circular imports
from models import Teacher, Student

@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        teacher = Teacher.query.filter_by(email=email).first()
        
        if teacher and check_password_hash(teacher.password, password):
            login_user(teacher)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        existing_teacher = Teacher.query.filter_by(email=email).first()
        if existing_teacher:
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_teacher = Teacher(name=name, email=email, password=hashed_password)
        
        db.session.add(new_teacher)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    students = Student.query.all()
    
    # Count students by status
    present_count = Student.query.filter_by(status='present').count()
    absent_count = Student.query.filter_by(status='absent').count()
    
    return render_template('dashboard.html', 
                           students=students, 
                           present_count=present_count, 
                           absent_count=absent_count, 
                           status_filter='all')

@app.route('/add_student', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        name = request.form.get('name')
        father_name = request.form.get('father_name')
        address = request.form.get('address')
        class_name = request.form.get('class_name')
        phone = request.form.get('phone')
        
        new_student = Student(
            name=name,
            father_name=father_name,
            address=address,
            class_name=class_name,
            phone=phone,
            status='present',
            teacher_id=current_user.id
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    
    if request.method == 'POST':
        student.name = request.form.get('name')
        student.father_name = request.form.get('father_name')
        student.address = request.form.get('address')
        student.class_name = request.form.get('class_name')
        student.phone = request.form.get('phone')
        
        db.session.commit()
        
        flash('Student updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_student.html', student=student)

@app.route('/delete_student/<int:id>')
@login_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    
    db.session.delete(student)
    db.session.commit()
    
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update_status/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    student = Student.query.get_or_404(id)
    status = request.form.get('status')
    
    student.status = status
    db.session.commit()
    
    if status == 'absent':
        # Send SMS notification for absent students
        sms_sent = send_sms(student.phone, f"Student {student.name} is marked absent today.")
        if sms_sent:
            flash(f'Status updated and SMS sent to {student.phone}', 'info')
        else:
            flash(f'Status updated but SMS notification failed', 'warning')
    else:
        flash('Status updated successfully!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query', '')
    filter_by = request.args.get('filter_by', 'name')
    status_filter = request.args.get('status_filter', 'all')
    
    # Start with base query
    student_query = Student.query
    
    # Apply status filter if not 'all'
    if status_filter != 'all':
        student_query = student_query.filter(Student.status == status_filter)
    
    # Apply search filter
    if query:
        if filter_by == 'name':
            student_query = student_query.filter(Student.name.contains(query))
        elif filter_by == 'class':
            student_query = student_query.filter(Student.class_name.contains(query))
    
    # Get results
    students = student_query.all()
    
    # Count students by status for the current filter
    present_count = Student.query.filter_by(status='present').count()
    absent_count = Student.query.filter_by(status='absent').count()
    
    return render_template('dashboard.html', 
                           students=students, 
                           query=query, 
                           filter_by=filter_by, 
                           status_filter=status_filter,
                           present_count=present_count,
                           absent_count=absent_count)

@app.route('/export_pdf')
@login_required
def export_pdf():
    from io import BytesIO
    from flask import send_file
    
    # Get filter parameters from request
    status_filter = request.args.get('status_filter', 'all')
    
    # Apply status filter if not 'all'
    if status_filter != 'all':
        students = Student.query.filter(Student.status == status_filter).all()
    else:
        students = Student.query.all()
    
    # Create a PDF file
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Create table data
    data = [
        ['ID', 'Name', 'Father\'s Name', 'Class', 'Phone', 'Status']
    ]
    
    for student in students:
        data.append([
            student.id,
            student.name,
            student.father_name,
            student.class_name,
            student.phone,
            student.status
        ])
    
    # Create table
    table = Table(data)
    
    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    table.setStyle(style)
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name='students.pdf',
        mimetype='application/pdf'
    )

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Helper function to send SMS using Twilio
def send_sms(phone_number, message):
    import os
    from twilio.rest import Client
    import re
    
    # Get Twilio credentials from environment variables
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_PHONE_NUMBER')
    
    # Check if Twilio credentials are configured
    if not all([account_sid, auth_token, twilio_number]):
        print(f"SMS to {phone_number}: {message} (Twilio not configured)")
        flash('SMS notification failed: Twilio not configured', 'warning')
        return False
    
    # Format phone number to E.164 format
    # Remove any non-digit characters
    digits_only = re.sub(r'\D', '', phone_number)
    
    # If the number doesn't start with +, add the country code
    # Assuming India country code (91) if not specified
    if not phone_number.startswith('+'):
        # If the number already has a country code (e.g., starts with 91), just add +
        if len(digits_only) > 10:
            formatted_number = '+' + digits_only
        else:
            # Add +91 for Indian numbers
            formatted_number = '+91' + digits_only
    else:
        formatted_number = phone_number
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        client.messages.create(
            body=message,
            from_=twilio_number,
            to=formatted_number
        )
        
        print(f"SMS sent to {formatted_number} (original: {phone_number}): {message}")
        return True
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        flash(f'SMS notification failed: {str(e)}', 'danger')
        return False

# Create database tables
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)