#!/usr/bin/env python3
"""
Automated update script for Discuss platform.
This script performs all necessary steps to update the application.

Usage:
    python utils/update.py [--backup] [--restart]

Options:
    --backup  : Create database backup before updating
    --restart : Restart the application server after updating
"""

import os
import sys
import subprocess
import argparse
import datetime
from pathlib import Path


def run_command(command, description=None, exit_on_error=True):
    """Run a shell command and print its output."""
    if description:
        print(f"\n[+] {description}...")
    
    try:
        process = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            text=True,
            capture_output=True
        )
        if process.stdout.strip():
            print(process.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing command: {command}")
        print(f"[-] {e.stderr.strip() if e.stderr else e}")
        if exit_on_error:
            sys.exit(1)
        return False


def create_backup():
    """Create a backup of the database."""
    # Ensure backup directory exists
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Get current date and time
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    
    # Create backup filename
    backup_file = backup_dir / f"discuss_backup_{timestamp}.sql"
    
    # Check if we have database configuration
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Look for .env file
        if Path('.env').exists():
            with open('.env', 'r') as f:
                for line in f:
                    if line.startswith('DATABASE_URL='):
                        database_url = line.strip().split('=', 1)[1]
                        break
    
    if not database_url:
        print("[-] DATABASE_URL not found in environment or .env file.")
        print("[-] Cannot create database backup.")
        return False
    
    # Parse database URL
    # Format: postgresql://username:password@hostname:port/database
    try:
        db_parts = database_url.replace('postgresql://', '').split('@')
        db_user_pass = db_parts[0].split(':')
        db_host_port_name = db_parts[1].split('/')
        
        db_user = db_user_pass[0]
        db_password = db_user_pass[1]
        db_host_port = db_host_port_name[0].split(':')
        db_host = db_host_port[0]
        db_port = db_host_port[1] if len(db_host_port) > 1 else '5432'
        db_name = db_host_port_name[1]
        
        # Create pg_dump command
        os.environ['PGPASSWORD'] = db_password
        command = f"pg_dump -h {db_host} -p {db_port} -U {db_user} -d {db_name} -f {backup_file}"
        
        run_command(command, f"Creating database backup to {backup_file}")
        print(f"[+] Backup created: {backup_file}")
        return True
    
    except Exception as e:
        print(f"[-] Error parsing DATABASE_URL: {e}")
        print("[-] Cannot create database backup.")
        return False


def update_application(restart=False):
    """Update the application code and database."""
    # Check for git
    if run_command("git --version", "Checking for Git", exit_on_error=False):
        # Pull latest code
        run_command("git pull", "Pulling latest code from repository")
    else:
        print("[-] Git not found. Manual code update required.")
    
    # Install dependencies
    run_command("pip install -e .", "Updating dependencies")
    
    # Run migrations
    run_command("python manage.py migrate", "Running database migrations")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Restart server if requested
    if restart:
        # Check if Gunicorn is running
        if run_command("pgrep -f 'gunicorn.*discuss'", exit_on_error=False):
            # Restart Gunicorn
            run_command("pkill -HUP -f 'gunicorn.*discuss'", "Restarting Gunicorn")
            print("[+] Gunicorn server restarted.")
        else:
            # Use systemctl if available
            if run_command("systemctl status gunicorn_discuss", exit_on_error=False):
                run_command("sudo systemctl restart gunicorn_discuss", "Restarting Gunicorn service")
                print("[+] Gunicorn service restarted.")
            else:
                print("[+] Gunicorn not detected. Manual restart required.")
    

def main():
    parser = argparse.ArgumentParser(description='Update Discuss platform')
    parser.add_argument('--backup', action='store_true', help='Create database backup before updating')
    parser.add_argument('--restart', action='store_true', help='Restart the application server after updating')
    args = parser.parse_args()
    
    print("=" * 50)
    print("Discuss Platform Update")
    print("=" * 50)
    
    # Create backup if requested
    if args.backup:
        create_backup()
    
    # Update application
    update_application(args.restart)
    
    print("\n[+] Update completed successfully.")
    if not args.restart:
        print("[+] Remember to restart your application server to apply the changes.")


if __name__ == '__main__':
    main()