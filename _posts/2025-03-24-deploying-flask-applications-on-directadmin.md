---
tags: [scratchpad]
info: aberto.
date: 2025-03-24
type: post
layout: post
published: true
slug: deploying-flask-applications-on-directadmin
title: 'deploying Flask applications on DirectAdmin'
---
This guide provides a comprehensive workflow for deploying a Flask application on DirectAdmin using Nginx Unit, with an emphasis on security and production best practices.

## 1. Understanding Nginx Unit in DirectAdmin

DirectAdmin integrates Nginx Unit as a polyglot application server that supports multiple languages and their versions. According to the [DirectAdmin documentation](https://docs.directadmin.com/webservices/nginx_unit/), you can access Nginx Unit functionality through:

```
User level → Advanced Features → Nginx unit
```

## 2. Creating a Flask Application Structure

Let's create a production-ready Flask application structure:

```bash
mkdir -p /home/username/domains/example.com/public_html/flask_app
mkdir -p /home/username/domains/example.com/public_html/flask_app/app
mkdir -p /home/username/domains/example.com/public_html/flask_app/app/static
mkdir -p /home/username/domains/example.com/public_html/flask_app/app/templates
mkdir -p /home/username/domains/example.com/public_html/flask_app/app/models
mkdir -p /home/username/domains/example.com/public_html/flask_app/app/views
mkdir -p /home/username/domains/example.com/public_html/flask_app/logs
mkdir -p /home/username/domains/example.com/public_html/flask_app/instance
```

This structure follows Flask best practices with separation of concerns and a dedicated instance folder for configuration files that shouldn't be in version control.

## 3. Flask Application Files

### wsgi.py (Entry Point)
```python
import os
from app import create_app

# Load configuration based on environment
config_name = os.environ.get('FLASK_CONFIG', 'production')
application = create_app(config_name)

if __name__ == "__main__":
    application.run()
```

### app/__init__.py
```python
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load default configuration
    app.config.from_object('config.default')
    
    # Load environment specific configuration
    app.config.from_object(f'config.{config_name}')
    
    # Load instance configuration if it exists
    if os.path.exists(os.path.join(app.instance_path, 'config.py')):
        app.config.from_pyfile('config.py')
    
    # Set up logging
    if not app.debug and not app.testing:
        log_dir = os.path.join(os.path.dirname(app.instance_path), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = RotatingFileHandler(
            os.path.join(log_dir, 'flask_app.log'),
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Flask application startup')
    
    # Register blueprints
    from app.views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
```

### app/views/main.py
```python
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')
```

### config/default.py
```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
```

### requirements.txt
```
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
python-dotenv==1.0.0
```

## 4. Setting Up Python Virtual Environment

Create a virtual environment and install dependencies:

```bash
cd /home/username/domains/example.com/public_html/flask_app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
```

## 5. Environment Variables Management

For production environments, sensitive information should be managed securely. Create a `.env` file in the instance directory:

```bash
cd /home/username/domains/example.com/public_html/flask_app/instance
touch .env
chmod 600 .env  # Only owner can read/write
```

Add environment variables to `.env`:
```
FLASK_APP=wsgi.py
FLASK_CONFIG=production
SECRET_KEY=your-secure-secret-key
DATABASE_URL=mysql://user:password@localhost/dbname
```

Then create a custom `config.py` in the instance directory to load these variables:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
```

## 6. Security-Focused File Permissions

Setting proper permissions is crucial for security:

```bash
cd /home/username/domains/example.com/public_html
find flask_app -type d -exec chmod 755 {} \;  # Directories
find flask_app -type f -exec chmod 644 {} \;  # Regular files
chmod 755 flask_app/wsgi.py  # Application entry point
chmod 700 flask_app/instance  # Instance directory with sensitive configuration
chmod 700 flask_app/logs  # Log directory
```

## 7. Enabling Nginx Unit in DirectAdmin

If Nginx Unit isn't already enabled:

```bash
cd /usr/local/directadmin/custombuild
./build set unit yes
./build unit
```

## 8. Creating the Application in DirectAdmin UI

1. Log in to DirectAdmin with your username and password
2. Navigate to **Advanced Features → Nginx Unit** 
3. Click **Create Application**
4. Fill in the following details:
   - **Name**: `flask_app`
   - **Type**: `python 3.9` (or your Python version)
   - **Path**: `/home/username/domains/example.com/public_html/flask_app`
   - **Module**: `wsgi`
   - **Callable**: `application`
   - **Environment Variables**:
     - FLASK_CONFIG: `production`
     - FLASK_APP: `wsgi.py`
     - PYTHONPATH: `/home/username/domains/example.com/public_html/flask_app`
5. Click **Save**

## 9. Enhanced Security with Filesystem Isolation

Nginx Unit provides filesystem isolation via the `rootfs` option. This feature restricts your application's access to only the specified directory, enhancing security.

While the DirectAdmin UI may not expose all isolation options directly, you can update the configuration using the API. Here's an example of how to add filesystem isolation:

```bash
curl -X PUT --unix-socket /var/run/unit/control.sock \
  -d '{
    "isolation": {
      "rootfs": "/home/username/domains/example.com/public_html/flask_app",
      "namespaces": {
        "mount": true
      }
    }
  }' \
  http://localhost/config/applications/flask_app/
```

Using `namespaces.mount` set to `true` enhances security by using `pivot_root` instead of `chroot`, preventing common chroot escape techniques.

## 10. Creating Route in DirectAdmin UI

1. From the Nginx Unit page, click **Create Route**
2. Fill in the following details:
   - **Domain**: `example.com`
   - **Application**: `flask_app`
   - **Add Static Files Route**: Check this option
   - **Static Files Path**: `/home/username/domains/example.com/public_html/flask_app/app/static`
   - **Static Files URI**: `/static/*`
3. Click **Save**

## 11. Understanding Nginx Unit Configuration JSON

DirectAdmin generates Nginx Unit configuration in JSON format. Here's what a complete configuration might look like:

```json
{
  "listeners": {
    "*:80": {
      "pass": "routes"
    }
  },
  "routes": [
    {
      "match": {
        "uri": "/static/*"
      },
      "action": {
        "share": "/home/username/domains/example.com/public_html/flask_app/app/static$uri"
      }
    },
    {
      "action": {
        "pass": "applications/flask_app"
      }
    }
  ],
  "applications": {
    "flask_app": {
      "type": "python 3.9",
      "path": "/home/username/domains/example.com/public_html/flask_app",
      "module": "wsgi",
      "callable": "application",
      "environment": {
        "FLASK_CONFIG": "production",
        "FLASK_APP": "wsgi.py",
        "PYTHONPATH": "/home/username/domains/example.com/public_html/flask_app"
      },
      "isolation": {
        "rootfs": "/home/username/domains/example.com/public_html/flask_app",
        "namespaces": {
          "mount": true
        }
      }
    }
  }
}
```

## 12. Configuring Logging

Nginx Unit logs application errors to its own log file:

```bash
tail -f /var/log/unit/unit.log
```

For Flask application-specific logs, check:

```bash
tail -f /home/username/domains/example.com/public_html/flask_app/logs/flask_app.log
```

## 13. Testing Your Deployment

Access your application by visiting your domain in a web browser:
```
http://example.com/
```

## 14. Production Security Best Practices

1. **Use HTTPS**: Configure LetsEncrypt SSL certificates through DirectAdmin.

2. **Web Application Firewall**: Consider adding ModSecurity or similar WAF.

3. **Content Security Policy**: Add appropriate headers:
   ```python
   @app.after_request
   def add_security_headers(response):
       response.headers['Content-Security-Policy'] = "default-src 'self'"
       response.headers['X-Content-Type-Options'] = 'nosniff'
       response.headers['X-Frame-Options'] = 'SAMEORIGIN'
       response.headers['X-XSS-Protection'] = '1; mode=block'
       return response
   ```

4. **Rate Limiting**: Implement rate limiting for API endpoints.

5. **CSRF Protection**: Ensure Flask-WTF CSRF protection is enabled:
   ```python
   from flask_wtf.csrf import CSRFProtect
   csrf = CSRFProtect(app)
   ```

6. **Dependency Scanning**: Regularly scan dependencies for vulnerabilities:
   ```bash
   pip install safety
   safety check -r requirements.txt
   ```

## 15. Troubleshooting Guide

### 404 Not Found Errors
- **Check if routes were created properly** in DirectAdmin UI
- **Verify Nginx Unit configuration** using:
  ```bash
  curl --unix-socket /var/run/unit/control.sock http://localhost/config/
  ```

### 500 Internal Server Error
- **Check application logs**:
  ```bash
  tail -f /home/username/domains/example.com/public_html/flask_app/logs/flask_app.log
  ```
- **Check Nginx Unit logs**:
  ```bash
  tail -f /var/log/unit/unit.log
  ```

### Permission Issues
- **Verify file ownership**:
  ```bash
  ls -la /home/username/domains/example.com/public_html/flask_app
  ```
- **Check if Nginx Unit can access your application files**:
  ```bash
  sudo -u www-data test -r /home/username/domains/example.com/public_html/flask_app/wsgi.py && echo "Readable" || echo "Not readable"
  ```

### Environment Variables Not Available
- **Verify environment variables in configuration**:
  ```bash
  curl --unix-socket /var/run/unit/control.sock http://localhost/config/applications/flask_app/environment
  ```
- **Check if `.env` file is being loaded properly** in your application

## 16. Updating Your Application

To update your Flask application:

1. Deploy new code to your application directory
2. Update dependencies if needed:
   ```bash
   cd /home/username/domains/example.com/public_html/flask_app
   source venv/bin/activate
   pip install -r requirements.txt
   deactivate
   ```
3. Reload the application configuration if necessary:
   ```bash
   curl -X PUT --unix-socket /var/run/unit/control.sock -d '{}' http://localhost/config/applications/flask_app
   ```

## 17. Monitoring Your Application

For production deployments, consider setting up monitoring:

1. **Application Monitoring**: Integrate with Flask-Monitoring-Dashboard or similar
2. **Performance Monitoring**: Consider New Relic or Datadog
3. **Error Tracking**: Integrate with Sentry for automatic error reporting:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration

   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[FlaskIntegration()]
   )
   ```