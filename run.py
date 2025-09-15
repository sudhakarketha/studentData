import os
from app import app, create_tables

if __name__ == '__main__':
    # Create database tables before running the app
    create_tables()
    
    # Get port from environment variable or use default 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)