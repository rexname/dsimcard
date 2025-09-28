#!/usr/bin/env python3
"""
Script to create the first admin user for the SMS Dashboard application.
Run this script once after setting up the database to create an initial admin account.
"""

import sys
import os
from getpass import getpass

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app, db
from app.models import User

def create_admin_user():
    """Create the first admin user."""
    app = create_app()

    with app.app_context():
        # Check if any admin user already exists
        existing_admin = User.query.filter_by(is_admin=True).first()
        if existing_admin:
            print("An admin user already exists!")
            print(f"Username: {existing_admin.username}")
            return

        print("Creating first admin user...")
        print("Please provide the following information:")

        # Get username
        while True:
            username = input("Username: ").strip()
            if not username:
                print("Username cannot be empty.")
                continue
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print("Username already exists. Please choose a different username.")
                continue
            break

        # Get password
        while True:
            password = getpass("Password: ")
            if len(password) < 6:
                print("Password must be at least 6 characters long.")
                continue
            confirm_password = getpass("Confirm Password: ")
            if password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue
            break

        # Create admin user
        admin_user = User(username=username, is_admin=True)
        admin_user.set_password(password)

        db.session.add(admin_user)
        db.session.commit()

        print("\nAdmin user created successfully!")
        print(f"Username: {username}")
        print("You can now log in to the application with these credentials.")

if __name__ == "__main__":
    create_admin_user()