#!/usr/bin/env python3
"""
Automated deployment script for Discuss platform.
This script performs all necessary steps to deploy the application.

Usage:
    python utils/deploy.py [--production]

Options:
    --production : Deploy in production mode (default: development mode)
"""

import os
import sys
import subprocess
import argparse
import getpass
from pathlib import Path

# Configuration
DEPLOYMENT_MODES = {
    'development': {
        'debug': 'True',
        'hosts': 'localhost,127.0.0.1',
        'port': 8000,
    },
    'production': {
        'debug': 'False',
        'hosts': None,  # Will prompt for domain names
        'port': 80,
    }
}


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


def collect_environment_info(mode):
    """Collect environment information for deployment."""
    env_vars = {}
    
    # Get database information
    if mode == 'production':
        print("\n=== Database Configuration ===")
        db_name = input("Enter database name [discuss]: ") or "discuss"
        db_user = input("Enter database username [discussuser]: ") or "discussuser"
        db_password = getpass.getpass("Enter database password: ")
        db_host = input("Enter database host [localhost]: ") or "localhost"
        db_port = input("Enter database port [5432]: ") or "5432"
        
        env_vars['DATABASE_URL'] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Get domain names
        print("\n=== Domain Configuration ===")
        domains = input("Enter comma-separated domain names (e.g., discuss.com,www.discuss.com): ")
        DEPLOYMENT_MODES['production']['hosts'] = domains
        
        # Secret key
        print("\n=== Security Configuration ===")
        use_generated = input("Generate a secure secret key? [Y/n]: ").lower() != 'n'
        if use_generated:
            # Generate a secure secret key
            import secrets
            env_vars['DJANGO_SECRET_KEY'] = secrets.token_urlsafe(50)
        else:
            env_vars['DJANGO_SECRET_KEY'] = getpass.getpass("Enter Django secret key: ")
            
        # Sentry configuration
        use_sentry = input("Configure Sentry for error tracking? [y/N]: ").lower() == 'y'
        if use_sentry:
            env_vars['SENTRY_DSN'] = input("Enter Sentry DSN: ")
    else:
        # Development mode defaults
        env_vars['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/discuss')
        env_vars['DJANGO_SECRET_KEY'] = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-development-key-change-in-production')
    
    env_vars['DEBUG'] = DEPLOYMENT_MODES[mode]['debug']
    env_vars['ALLOWED_HOSTS'] = DEPLOYMENT_MODES[mode]['hosts']
    
    return env_vars


def create_env_file(env_vars):
    """Create or update .env file with environment variables."""
    env_path = Path('.env')
    
    # Check if .env exists and backup if it does
    if env_path.exists():
        backup_path = Path('.env.backup')
        env_path.rename(backup_path)
        print(f"[+] Existing .env file backed up to {backup_path}")
    
    # Write new .env file
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            if value is not None:  # Only write non-None values
                f.write(f"{key}={value}\n")
    
    print(f"[+] Environment configuration saved to {env_path}")


def setup_database(env_vars, mode):
    """Set up the database for deployment."""
    if mode == 'production':
        # Instructions for manual database setup in production
        print("\n=== Database Setup Instructions ===")
        print("Run the following commands as the PostgreSQL superuser:")
        print(f"CREATE DATABASE {env_vars['DATABASE_URL'].split('/')[-1]};")
        print(f"CREATE USER {env_vars['DATABASE_URL'].split(':')[1].split('@')[0]} WITH PASSWORD '{env_vars['DATABASE_URL'].split(':')[2].split('@')[0]}';")
        print(f"ALTER ROLE {env_vars['DATABASE_URL'].split(':')[1].split('@')[0]} SET client_encoding TO 'utf8';")
        print("ALTER ROLE discussuser SET default_transaction_isolation TO 'read committed';")
        print("ALTER ROLE discussuser SET timezone TO 'UTC';")
        print(f"GRANT ALL PRIVILEGES ON DATABASE {env_vars['DATABASE_URL'].split('/')[-1]} TO {env_vars['DATABASE_URL'].split(':')[1].split('@')[0]};")
        
        proceed = input("\nHave you completed these steps? [y/N]: ").lower() == 'y'
        if not proceed:
            print("Deployment aborted. Please set up the database first.")
            sys.exit(1)
    
    # Run migrations
    run_command('python manage.py migrate', 'Running database migrations')


def deploy_development(env_vars):
    """Deploy in development mode."""
    # Create virtual environment if it doesn't exist
    if not Path('venv').exists():
        run_command('python -m venv venv', 'Creating virtual environment')
        
        # Determine the activate script based on the platform
        if sys.platform == 'win32':
            activate_cmd = 'venv\\Scripts\\activate'
        else:
            activate_cmd = 'source venv/bin/activate'
            
        print(f"[+] Virtual environment created. Activate with: {activate_cmd}")
    
    # Install dependencies
    run_command('pip install -e .', 'Installing dependencies')
    
    # Set up database
    setup_database(env_vars, 'development')
    
    # Create superuser if needed
    create_superuser = input("\nDo you want to create a superuser? [y/N]: ").lower() == 'y'
    if create_superuser:
        run_command('python manage.py createsuperuser', 'Creating superuser', exit_on_error=False)
    
    # Run development server
    port = DEPLOYMENT_MODES['development']['port']
    print(f"\n[+] Starting development server on port {port}...")
    print(f"[+] Access the application at http://localhost:{port}/")
    run_command(f'python manage.py runserver 0.0.0.0:{port}')


def deploy_production(env_vars):
    """Deploy in production mode."""
    # Install production dependencies
    run_command('pip install gunicorn', 'Installing Gunicorn')
    
    # Install dependencies
    run_command('pip install -e .', 'Installing dependencies')
    
    # Collect static files
    run_command('python manage.py collectstatic --noinput', 'Collecting static files')
    
    # Set up database
    setup_database(env_vars, 'production')
    
    # Create superuser if needed
    create_superuser = input("\nDo you want to create a superuser? [y/N]: ").lower() == 'y'
    if create_superuser:
        run_command('python manage.py createsuperuser', 'Creating superuser', exit_on_error=False)
    
    # Create Gunicorn configuration
    gunicorn_conf = f"""# Gunicorn configuration for Discuss
bind = "0.0.0.0:8000"
workers = 3
timeout = 120
accesslog = "gunicorn-access.log"
errorlog = "gunicorn-error.log"
capture_output = True
"""
    
    with open('gunicorn.conf.py', 'w') as f:
        f.write(gunicorn_conf)
    
    print("\n=== Production Deployment ===")
    print("1. Gunicorn configuration has been created.")
    print("2. To start the application with Gunicorn, run:")
    print("   gunicorn -c gunicorn.conf.py discuss.wsgi:application")
    print("\n3. For a proper production setup, configure Nginx with this location block:")
    print("""
server {
    listen 80;
    server_name %s;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias %s/static/;
    }

    location /media/ {
        alias %s/media/;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://localhost:8000;
    }
}
""" % (env_vars['ALLOWED_HOSTS'], os.path.abspath('static'), os.path.abspath('media')))
    
    print("\n4. Then secure with SSL using Let's Encrypt:")
    print("   sudo certbot --nginx -d example.com -d www.example.com")
    
    print("\n5. Consider creating a systemd service for automatic startup.")
    
    # Run the application with Gunicorn if requested
    run_now = input("\nDo you want to start the application with Gunicorn now? [y/N]: ").lower() == 'y'
    if run_now:
        run_command('gunicorn -c gunicorn.conf.py discuss.wsgi:application', 'Starting Gunicorn server')


def main():
    parser = argparse.ArgumentParser(description='Deploy Discuss platform')
    parser.add_argument('--production', action='store_true', help='Deploy in production mode')
    args = parser.parse_args()
    
    mode = 'production' if args.production else 'development'
    
    print("=" * 50)
    print(f"Discuss Platform Deployment - {mode.upper()} Mode")
    print("=" * 50)
    
    # Collect environment information
    env_vars = collect_environment_info(mode)
    
    # Create environment file
    create_env_file(env_vars)
    
    # Deploy based on mode
    if mode == 'development':
        deploy_development(env_vars)
    else:
        deploy_production(env_vars)


if __name__ == '__main__':
    main()