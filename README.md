# Discuss - Social Community Platform

A dynamic Reddit-like social platform that enables community-driven content sharing and intelligent interaction through advanced social features.

## Key Features

- User authentication with AllAuth
- Community creation and management
- Post creation (text and link posts)
- Commenting with nested replies
- Advanced search functionality
- User profiles with reputation system
- Voting system for posts and comments
- Notification system for user interactions
- Private messaging between users
- Donation functionality

## Technologies

- Django web framework
- PostgreSQL database
- Responsive web design with Bootstrap 5
- AJAX-powered interactive features
- django-allauth for authentication
- django-mptt for nested comments
- django-taggit for tagging
- django-watson for search
- django-countries for location data
- django-postman for messaging
- django-payments for donations
- Sentry for error tracking

## Project Structure

The Discuss platform follows a modular architecture for maintainability and scalability:

### Core Application Structure

```
discuss/                # Main project settings
core/                   # Main application
├── management/         # Custom management commands
├── migrations/         # Database migrations
├── static/core/        # Static assets
│   ├── css/            # Stylesheets
│   │   ├── universal-adaptive.css   # Responsive styling
│   │   ├── reddit-comments.css      # Comment system styling
│   │   └── unified-theme.css        # Theme styling
│   └── js/             # JavaScript files
│       └── script.js    # Consolidated JavaScript functionality
├── templates/core/     # HTML templates organized by feature
│   ├── base.html       # Base template with common elements
│   ├── includes/       # Reusable template components
│   ├── community/      # Community-related templates
│   ├── posts/          # Post-related templates
│   ├── profile/        # User profile templates
│   └── messaging/      # Messaging system templates
├── templatetags/       # Custom template tags and filters
│   ├── core_tags.py    # Consolidated template tags and filters
│   └── dict_tags.py    # Dictionary-related template tags
├── views/              # Views organized by feature
│   ├── auth_views.py   # Authentication views
│   ├── auth_urls.py    # Authentication URLs
│   ├── community_views.py      # Community-related views
│   ├── messaging_views.py      # Messaging system views
│   ├── messaging_urls.py       # Messaging system URLs
│   ├── notification_views.py   # Notification system views
│   ├── payment_views.py        # Payment/donation views
│   ├── post_views.py           # Post-related views
│   ├── profile_views.py        # User profile views
│   ├── search_views.py         # Search functionality views
│   └── utils_views.py          # Utility views
├── admin.py            # Admin panel configuration
├── apps.py             # App configuration
├── context_processors.py # Template context processors
├── filters.py          # Filter classes for Django-filter
├── forms.py            # Form classes
├── models.py           # Database models
└── urls.py             # URL configuration
utils/                  # Utility scripts
├── check_comments.py   # Script to list posts with comments
├── migrate_data.py     # Database migration utility for SQLite to PostgreSQL
└── reset_sequences.py  # PostgreSQL sequence reset utility
```

### Code Organization Principles

1. **Template Organization**: All templates are located in `core/templates/core/` and organized by feature.
2. **CSS Consolidation**: Styles are consolidated into purpose-specific files to prevent duplication.
3. **JavaScript Consolidation**: Core functionality is in `script.js` with specialized functions as needed.
4. **Template Tags**: Consolidated in `core_tags.py` for better maintainability.
5. **View Organization**: Views are separated by feature in the `views/` directory.
6. **Utility Scripts**: Database and maintenance utilities are stored in the `utils/` directory.

### Utility Scripts

The `utils/` directory contains helpful scripts for database management, deployment, and maintenance:

1. **check_comments.py**: Lists all posts that have comments with their count
   ```
   python -c "import django; django.setup(); from utils import check_comments"
   ```

2. **migrate_data.py**: Migrates data from SQLite to PostgreSQL
   ```
   python utils/migrate_data.py
   ```

3. **reset_sequences.py**: Resets PostgreSQL sequences after data migration or manual edits
   ```
   python utils/reset_sequences.py
   ```

4. **deploy.py**: Automated deployment script with interactive setup
   ```
   # For development deployment
   python utils/deploy.py
   
   # For production deployment
   python utils/deploy.py --production
   ```

5. **update.py**: Automated update script for code and database
   ```
   # Basic update
   python utils/update.py
   
   # Update with database backup
   python utils/update.py --backup
   
   # Update and restart server
   python utils/update.py --restart
   
   # Full update with backup and restart
   python utils/update.py --backup --restart
   ```

6. **clean_profiles.py**: Utility to clean up Silk profiling files
   ```
   python utils/clean_profiles.py
   ```

## Development Environment Setup

### Automated Setup (Recommended)

1. Clone the repository:
   ```
   git clone https://codeberg.org/Adamcatholic/Ds.git
   cd Ds
   ```

2. Run the automated deployment script:
   ```
   python utils/deploy.py
   ```
   
   This script will:
   - Prompt for database configuration
   - Create a virtual environment if needed
   - Install all dependencies
   - Set up the database
   - Configure environment variables
   - Offer to create a superuser
   - Start the development server

### Manual Setup

If you prefer to set up manually:

1. Clone the repository:
   ```
   git clone https://codeberg.org/Adamcatholic/Ds.git
   cd Ds
   ```

2. Install required Python packages:
   ```
   pip install -e .
   ```

3. Set up environment variables (create a .env file or export in your shell):
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/discuss
   DJANGO_SECRET_KEY=your_secret_key
   DEBUG=True
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver 0.0.0.0:8000
   ```

## Deployment Guide

### Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- SSH access
- Domain name (optional but recommended)
- Knowledge of Linux, Nginx, PostgreSQL

### Automated Production Deployment (Recommended)

1. Update your system packages and install required software:
   ```
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv git nginx postgresql postgresql-contrib
   ```

2. Clone the repository:
   ```
   git clone https://codeberg.org/Adamcatholic/Ds.git /home/discuss/app
   cd /home/discuss/app
   ```

3. Run the automated deployment script in production mode:
   ```
   python utils/deploy.py --production
   ```
   
   This script will:
   - Guide you through database configuration
   - Help set up secure credentials
   - Generate or prompt for a secure Django secret key
   - Set up Sentry error tracking (optional)
   - Install all dependencies
   - Create Gunicorn configuration
   - Provide Nginx configuration instructions
   - Offer to create a superuser
   
4. Follow the script's instructions for completing the Nginx setup and enabling SSL with Let's Encrypt.

### Manual Production Deployment

If you prefer to deploy manually or need more control over the setup process:

#### 1. Server Setup

1. Update your system packages and install required software:
   ```
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip python3-venv git nginx postgresql postgresql-contrib
   ```

2. Create a dedicated user for the application:
   ```
   sudo adduser discuss
   sudo usermod -aG sudo discuss
   ```

#### 2. Database Setup

1. Create a PostgreSQL database and user:
   ```
   sudo -u postgres psql
   CREATE DATABASE discuss;
   CREATE USER discussuser WITH PASSWORD 'secure_password';
   ALTER ROLE discussuser SET client_encoding TO 'utf8';
   ALTER ROLE discussuser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE discussuser SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE discuss TO discussuser;
   \q
   ```

2. Update your environment variables with the database connection information.

#### 3. Application Setup

1. Clone the repository:
   ```
   git clone https://codeberg.org/Adamcatholic/Ds.git /home/discuss/app
   cd /home/discuss/app
   ```

2. Set up a Python virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -e .
   pip install gunicorn
   ```

4. Create an environment file (.env) with required settings:
   ```
   DEBUG=False
   DJANGO_SECRET_KEY=your_secure_secret_key
   DATABASE_URL=postgresql://discussuser:secure_password@localhost:5432/discuss
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   SENTRY_DSN=your_sentry_dsn_if_using
   ```

5. Run migrations and collect static files:
   ```
   python manage.py migrate
   python manage.py collectstatic
   ```

6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

#### 4. Web Server Configuration

1. Create a systemd service file for Gunicorn:
   ```
   sudo nano /etc/systemd/system/gunicorn_discuss.service
   ```

   Add the following content:
   ```
   [Unit]
   Description=Gunicorn daemon for Discuss
   After=network.target

   [Service]
   User=discuss
   Group=www-data
   WorkingDirectory=/home/discuss/app
   ExecStart=/home/discuss/app/venv/bin/gunicorn \
             --access-logfile - \
             --workers 3 \
             --bind unix:/home/discuss/app/discuss.sock \
             discuss.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the Gunicorn service:
   ```
   sudo systemctl enable gunicorn_discuss
   sudo systemctl start gunicorn_discuss
   ```

3. Configure Nginx:
   ```
   sudo nano /etc/nginx/sites-available/discuss
   ```

   Add the following configuration:
   ```
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /home/discuss/app;
       }

       location /media/ {
           root /home/discuss/app;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/home/discuss/app/discuss.sock;
       }
   }
   ```

4. Enable the site and restart Nginx:
   ```
   sudo ln -s /etc/nginx/sites-available/discuss /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

5. Set up SSL with Let's Encrypt:
   ```
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

### Maintenance and Updates

#### Automated Updates (Recommended)

To update your application with the latest code:

1. Navigate to your application directory:
   ```
   cd /home/discuss/app
   source venv/bin/activate
   ```

2. Run the automated update script:
   ```
   # Basic update
   python utils/update.py
   
   # Update with database backup
   python utils/update.py --backup
   
   # Update and restart server
   python utils/update.py --restart
   ```

#### Manual Maintenance

1. Set up automatic database backups:
   ```
   cd /home/discuss
   mkdir backups
   nano backup.sh
   ```

   Add the following script:
   ```bash
   #!/bin/bash
   DATE=$(date +%Y-%m-%d)
   PGPASSWORD=secure_password pg_dump -h localhost -U discussuser discuss > /home/discuss/backups/discuss_$DATE.sql
   ```

   Make it executable and set up a cron job:
   ```
   chmod +x backup.sh
   crontab -e
   ```

   Add the line to run daily at 2 AM:
   ```
   0 2 * * * /home/discuss/backup.sh
   ```

2. Monitor logs:
   ```
   sudo journalctl -u gunicorn_discuss
   sudo tail -f /var/log/nginx/access.log
   sudo tail -f /var/log/nginx/error.log
   ```

3. Update application manually:
   ```
   cd /home/discuss/app
   source venv/bin/activate
   git pull
   pip install -e .
   python manage.py migrate
   python manage.py collectstatic
   sudo systemctl restart gunicorn_discuss
   ```

## Security Considerations

1. Always use environment variables for sensitive information
2. Keep your server and packages updated
3. Use HTTPS in production
4. Implement IP rate limiting for login attempts
5. Maintain regular database backups

## Contributing

Contributions to Discuss are welcome! Please follow these guidelines:

### Development Conventions

1. **Template Tags**: Add new template tags to `core_tags.py` rather than creating new tag files.

2. **Templates**: Place all templates in the appropriate feature directory under `core/templates/core/`. 
   Use includes for reusable components.

3. **CSS/JS**: Consolidate CSS and JS files based on functionality. Don't create new files for small features;
   instead, add to the appropriate existing file.

4. **Views**: Organize views by feature in separate files within the `views/` directory.

5. **Code Style**:
   - Follow PEP 8 for Python code
   - Use 4 spaces for indentation
   - Use meaningful variable and function names
   - Include docstrings for all functions, classes, and modules
   - Add comments for complex logic

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Known Issues

1. There is an issue with URL reversing in the messaging system that needs to be fixed.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
