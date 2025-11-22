#!/usr/bin/env python3
"""
Simple Admin User Creator
Just edit the password below and run this script
"""

import mysql.connector
from werkzeug.security import generate_password_hash

# ============================================
# EDIT THESE SETTINGS
# ============================================
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"  #CHANGE 
MYSQL_DATABASE = "oil_shop_db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # Change if you want a different password
# ============================================

def create_admin():
    print("\n" + "="*60)
    print("Creating Admin User for Oil Shop Management System")
    print("="*60 + "\n")
    
    print(f"Settings:")
    print(f"  MySQL Host: {MYSQL_HOST}")
    print(f"  MySQL User: {MYSQL_USER}")
    print(f"  MySQL Database: {MYSQL_DATABASE}")
    print(f"  Admin Username: {ADMIN_USERNAME}")
    print(f"  Admin Password: {ADMIN_PASSWORD}")
    print()
    
    try:
        # Connect to database
        print("Step 1: Connecting to MySQL...")
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        print("✓ Connected successfully!\n")
        
        cursor = conn.cursor()
        
        # Check if admin exists
        print("Step 2: Checking for existing admin user...")
        cursor.execute("SELECT id FROM employees WHERE username = %s", (ADMIN_USERNAME,))
        existing = cursor.fetchone()
        
        if existing:
            print(f"✓ Found existing admin user (ID: {existing[0]})")
            print("  Deleting old admin user...")
            cursor.execute("DELETE FROM employees WHERE username = %s", (ADMIN_USERNAME,))
            print("✓ Old admin user deleted\n")
        else:
            print("✓ No existing admin user found\n")
        
        # Create new admin
        print("Step 3: Creating new admin user...")
        hashed_password = generate_password_hash(ADMIN_PASSWORD)
        print(f"✓ Password hashed: {hashed_password[:40]}...\n")
        
        cursor.execute(
            "INSERT INTO employees (username, password, role) VALUES (%s, %s, %s)",
            (ADMIN_USERNAME, hashed_password, 'admin')
        )
        
        conn.commit()
        admin_id = cursor.lastrowid
        print(f"✓ Admin user created successfully! (ID: {admin_id})\n")
        
        # Verify creation
        print("Step 4: Verifying admin user...")
        cursor.execute("SELECT id, username, role FROM employees WHERE username = %s", (ADMIN_USERNAME,))
        result = cursor.fetchone()
        
        if result:
            print(f"✓ Verification successful!")
            print(f"  ID: {result[0]}")
            print(f"  Username: {result[1]}")
            print(f"  Role: {result[2]}")
            print()
        
        cursor.close()
        conn.close()
        
        # Success message
        print("="*60)
        print("✓✓✓ SUCCESS! ✓✓✓")
        print("="*60)
        print(f"\nYou can now login to the Oil Shop Management System:\n")
        print(f"  URL:      http://localhost:5000")
        print(f"  Username: {ADMIN_USERNAME}")
        print(f"  Password: {ADMIN_PASSWORD}")
        print()
        print("="*60)
        print("\nNext steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
        print("3. Login with the credentials above")
        print("4. Change your password after first login!")
        print()
        
    except mysql.connector.Error as e:
        print("\n" + "="*60)
        print("❌ DATABASE ERROR")
        print("="*60)
        print(f"\nError: {e}\n")
        
        if "Access denied" in str(e):
            print("Problem: Wrong MySQL password")
            print("Solution: Edit this file and update MYSQL_PASSWORD")
            print(f"         Current value: {MYSQL_PASSWORD}")
            print()
        elif "Unknown database" in str(e):
            print("Problem: Database doesn't exist")
            print("Solution: Run these commands first:")
            print("  mysql -u root -p")
            print("  CREATE DATABASE oil_shop_db;")
            print("  EXIT;")
            print("  mysql -u root -p oil_shop_db < database_init.sql")
            print()
        elif "Can't connect" in str(e):
            print("Problem: MySQL server is not running")
            print("Solution: Start MySQL service:")
            print("  Windows: net start MySQL80")
            print("  Or check Services app")
            print()
        
    except ImportError as e:
        print("\n❌ Missing Python package")
        print(f"Error: {e}")
        print("\nSolution: Install required packages:")
        print("  pip install mysql-connector-python werkzeug")
        print()
        
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        print("\nPlease check:")
        print("1. MySQL is running")
        print("2. Database oil_shop_db exists")
        print("3. Your MySQL password is correct")
        print()

if __name__ == "__main__":
    print("\n" + "⚠"*30)
    print("BEFORE RUNNING:")
    print("Edit this file and change MYSQL_PASSWORD to your actual MySQL password!")
    print("⚠"*30 + "\n")
    
    response = input("Have you updated MYSQL_PASSWORD? (yes/no): ").strip().lower()
    
    if response in ['yes', 'y']:
        create_admin()
    else:
        print("\nPlease edit this file first:")
        print("1. Open: create_admin_simple.py")
        print("2. Find: MYSQL_PASSWORD = \"YOUR_MYSQL_PASSWORD_HERE\"")
        print("3. Change it to your actual MySQL password")
        print("4. Save and run again")
        print()