#!/usr/bin/env python3
"""
Oil Shop Management System - Setup Script
This script helps automate the initial setup process
"""

import os
import sys
import subprocess
import getpass
import mysql.connector
from mysql.connector import Error

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        sys.exit(1)
    
    print("✓ Python version is compatible")

def install_requirements():
    """Install required Python packages"""
    print_header("Installing Python Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies. Please install manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

def test_mysql_connection(host, user, password):
    """Test MySQL connection"""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        conn.close()
        return True
    except Error:
        return False

def setup_database():
    """Setup MySQL database"""
    print_header("Database Setup")
    
    print("Please provide your MySQL credentials:")
    db_host = input("MySQL Host [localhost]: ").strip() or "localhost"
    db_user = input("MySQL User [root]: ").strip() or "root"
    db_password = getpass.getpass("MySQL Password: ")
    
    # Test connection
    print("\nTesting MySQL connection...")
    if not test_mysql_connection(db_host, db_user, db_password):
        print("❌ Error: Could not connect to MySQL. Please check your credentials.")
        return None
    
    print("✓ MySQL connection successful")
    
    # Create database
    try:
        print("\nCreating database...")
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor = conn.cursor()
        
        # Read and execute database init script
        with open('database_init.sql', 'r') as f:
            sql_script = f.read()
        
        # Execute SQL statements
        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✓ Database created and initialized successfully")
        
        return {
            'host': db_host,
            'user': db_user,
            'password': db_password
        }
        
    except Error as e:
        print(f"❌ Error creating database: {e}")
        print("\nYou can manually run the database_init.sql script:")
        print(f"   mysql -u {db_user} -p < database_init.sql")
        return None

def create_env_file(db_config):
    """Create .env file with configuration"""
    print_header("Creating Configuration File")
    
    if db_config is None:
        print("Skipping .env creation due to database setup issues.")
        return
    
    env_content = f"""# Database Configuration
DB_HOST={db_config['host']}
DB_USER={db_config['user']}
DB_PASSWORD={db_config['password']}
DB_NAME=oil_shop_db

# Flask Configuration
SECRET_KEY={os.urandom(24).hex()}
FLASK_ENV=development
DEBUG=True

# Server Configuration
HOST=0.0.0.0
PORT=5000
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Configuration file (.env) created successfully")
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def update_app_config(db_config):
    """Update app.py with database configuration"""
    print_header("Updating Application Configuration")
    
    if db_config is None:
        print("⚠ Warning: Please manually update DB_CONFIG in app.py")
        return
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Update DB_CONFIG
        new_config = f"""DB_CONFIG = {{
    'host': '{db_config['host']}',
    'user': '{db_config['user']}',
    'password': '{db_config['password']}',
    'database': 'oil_shop_db'
}}"""
        
        # Replace the DB_CONFIG section
        import re
        pattern = r"DB_CONFIG = \{[^}]+\}"
        content = re.sub(pattern, new_config, content, flags=re.DOTALL)
        
        with open('app.py', 'w') as f:
            f.write(content)
        
        print("✓ Application configuration updated successfully")
    except Exception as e:
        print(f"❌ Error updating app.py: {e}")
        print("Please manually update the DB_CONFIG section in app.py")

def create_directories():
    """Create required directories"""
    print_header("Creating Required Directories")
    
    directories = ['templates', 'static', 'static/uploads']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def print_completion_message():
    """Print setup completion message"""
    print_header("Setup Complete!")
    
    print("✓ Oil Shop Management System has been set up successfully!")

def main():
    """Main setup function"""
    print("Configeuring System...")
    
    try:
        # Check Python version
        check_python_version()
        
        # Install requirements
        install_requirements()
        
        # Setup database
        db_config = setup_database()
        
        # Create .env file
        create_env_file(db_config)
        
        # Update app.py configuration
        update_app_config(db_config)
        
        # Create required directories
        create_directories()
        
        # Print completion message
        print_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please check the error and try again, or set up manually using README.md")
        sys.exit(1)

if __name__ == "__main__":
    main()