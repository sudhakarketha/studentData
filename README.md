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
     
     # For SQLite (development)
     DATABASE_URL=sqlite:///students.db
     
     # For MySQL (production)
     # DATABASE_URL=mysql://username:password@host:port/database
     
     # For Twilio SMS (required for attendance notifications)
     TWILIO_ACCOUNT_SID=your_account_sid
     TWILIO_AUTH_TOKEN=your_auth_token
     TWILIO_PHONE_NUMBER=your_twilio_phone_number  # Must be in E.164 format (e.g., +12345678901)
     ```

6. Run the application:
   ```
   python run.py
   ```

7. Access the application at `http://localhost:5000`

## Deployment on Render

1. Create a new Web Service on Render

2. Connect your GitHub repository

3. The application includes a `render.yaml` file that will automatically configure the service with:
   - **Name**: student-management-system
   - **Environment**: Python 3.9.0
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`

4. The `render.yaml` file includes environment variables, but you should update:
   - `SECRET_KEY`: A secure random string (will be auto-generated)
   - `DATABASE_URL`: Already configured to use Clever Cloud MySQL
   - Twilio credentials (you need to add these in the Render dashboard)

5. Deploy the application

## Database Setup for Production

This application is configured to use MySQL on Clever Cloud:

1. The database connection string is already configured in the `.env` file and `render.yaml`

2. If you need to use your own MySQL database:
   - Update the `DATABASE_URL` in the `.env` file
   - Update the `DATABASE_URL` in the `render.yaml` file

3. The application will automatically use the MySQL database when deployed

## SMS Notification Setup

To enable SMS notifications for absent students:

1. Create a Twilio account at [twilio.com](https://www.twilio.com)

2. Get your Account SID, Auth Token, and a Twilio phone number

3. Add these credentials to your `.env` file and in the Render dashboard

4. Important notes about phone numbers:
   - Student phone numbers must be in E.164 format or will be automatically formatted
   - For Indian phone numbers, the country code (+91) will be added if missing
   - Example: "9990809882" will be formatted as "+919990809882"
   - In trial mode, you can only send SMS to verified numbers

## License

This project is licensed under the MIT License - see the LICENSE file for details.