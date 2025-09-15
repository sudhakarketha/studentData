# Student Management System

A web application for managing student details with features like attendance tracking, SMS notifications, PDF export, and search filters.

## Features

1. **Teacher Authentication**
   - Login and registration system for teachers
   - Secure password hashing

2. **Student Management**
   - Add, edit, and delete student records
   - Track student details: name, father's name, address, class, phone number
   - Attendance status tracking (present/absent)

3. **Attendance Notifications**
   - SMS notifications when a student is marked absent
   - Integration with Twilio API for sending SMS

4. **Reporting**
   - Export student data to PDF
   - Comprehensive student list with all details

5. **Search and Filtering**
   - Search students by name
   - Filter students by class

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd studentData
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Configure environment variables:
   - Create a `.env` file in the project root (or edit the existing one)
   - Add the following variables:
     ```
     SECRET_KEY=your_secret_key_here
     DATABASE_URL=sqlite:///students.db
     
     # For Twilio SMS (optional)
     TWILIO_ACCOUNT_SID=your_account_sid
     TWILIO_AUTH_TOKEN=your_auth_token
     TWILIO_PHONE_NUMBER=your_twilio_phone_number
     ```

6. Run the application:
   ```
   python app.py
   ```

7. Access the application at `http://localhost:5000`

## Deployment on Render

1. Create a new Web Service on Render

2. Connect your GitHub repository

3. Configure the service:
   - **Name**: student-management-system (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

4. Add environment variables:
   - `SECRET_KEY`: A secure random string
   - `DATABASE_URL`: Your PostgreSQL database URL (Render provides this if you create a PostgreSQL database)
   - Twilio credentials (if using SMS functionality)

5. Deploy the application

## Database Setup for Production

For production deployment on Render, it's recommended to use PostgreSQL instead of SQLite:

1. Create a PostgreSQL database on Render

2. Update the `DATABASE_URL` environment variable to use the PostgreSQL connection string

3. The application will automatically use the PostgreSQL database when deployed

## SMS Notification Setup

To enable SMS notifications for absent students:

1. Create a Twilio account at [twilio.com](https://www.twilio.com)

2. Get your Account SID, Auth Token, and a Twilio phone number

3. Add these credentials to your environment variables

4. Uncomment the Twilio code in the `send_sms` function in `app.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.