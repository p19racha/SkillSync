# Flask MySQL Login System

A complete Flask-based authentication system with MySQL database integration, featuring a modern Bootstrap frontend and AJAX-powered user interactions.

## Features

- **User Authentication**: Secure registration and login system
- **Password Security**: Bcrypt password hashing for enhanced security
- **Session Management**: Flask-Login for user session handling
- **MySQL Integration**: Full MySQL database support with SQLAlchemy ORM
- **Responsive UI**: Modern Bootstrap 5 interface with custom styling
- **AJAX Forms**: Seamless form submissions without page reloads
- **Real-time Validation**: Client-side form validation with instant feedback
- **Dashboard**: Protected user dashboard with profile management
- **Error Handling**: Comprehensive error handling and user feedback

## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt
- **Database**: MySQL
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Styling**: Custom CSS with modern design principles

## Prerequisites

- Python 3.7+
- MySQL Server 5.7+
- pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-engine
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**:
   ```sql
   CREATE DATABASE login_system;
   CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
   GRANT ALL PRIVILEGES ON login_system.* TO 'myuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

5. **Initialize the database**:
   ```bash
   python run.py init-db
   ```

## Configuration

The application uses the following MySQL configuration:
- **Host**: localhost:3306
- **Database**: login_system
- **Username**: myuser
- **Password**: mypassword

To modify these settings, update the `SQLALCHEMY_DATABASE_URI` in `app/__init__.py`.

## Running the Application

1. **Start the Flask development server**:
   ```bash
   python run.py
   ```

2. **Access the application**:
   Open your web browser and navigate to `http://localhost:5000`

## Project Structure

```
ai-engine/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes.py            # Application routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Custom styles
│   │   └── js/
│   │       ├── main.js      # Common utilities
│   │       ├── auth.js      # Authentication logic
│   │       └── dashboard.js # Dashboard functionality
│   └── templates/
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── login.html       # Login form
│       ├── register.html    # Registration form
│       ├── dashboard.html   # User dashboard
│       └── 404.html         # Error page
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## API Endpoints

### Authentication Routes
- `GET /` - Home page
- `GET /login` - Login form
- `POST /login` - Process login (JSON)
- `GET /register` - Registration form  
- `POST /register` - Process registration (JSON)
- `GET /logout` - Logout user
- `GET /dashboard` - User dashboard (protected)

### Features

#### User Registration
- Username validation (3+ characters, alphanumeric + underscore)
- Password strength requirements (6+ characters)
- Duplicate username prevention
- Real-time form validation

#### User Login
- Secure password verification
- Session management
- Remember user state
- Automatic redirects

#### Dashboard
- Welcome message with username
- User profile information
- Logout functionality
- Future: Profile editing, password change

#### Security Features
- Password hashing with Bcrypt
- CSRF protection
- Session management
- Input validation and sanitization

## Development

### Adding New Features

1. **Database Models**: Add new models in `app/models.py`
2. **Routes**: Add new routes in `app/routes.py`
3. **Templates**: Create new templates in `app/templates/`
4. **Static Files**: Add CSS/JS in `app/static/`

### Customization

- **Styling**: Modify `app/static/css/style.css`
- **JavaScript**: Update files in `app/static/js/`
- **Database**: Change connection string in `app/__init__.py`
- **Templates**: Customize HTML in `app/templates/`

## CLI Commands

The application includes helpful CLI commands:

```bash
# Initialize database tables
python run.py init-db

# Create an admin user
python run.py create-admin
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in the configuration
2. Use a production WSGI server (e.g., Gunicorn)
3. Configure proper MySQL credentials
4. Set up SSL/HTTPS
5. Configure environment variables
6. Set up proper logging

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**:
   - Verify MySQL server is running
   - Check database credentials
   - Ensure database exists

2. **Import Errors**:
   - Verify virtual environment is activated
   - Install all requirements: `pip install -r requirements.txt`

3. **Template Not Found**:
   - Check file paths in `app/templates/`
   - Verify template inheritance

4. **Static Files Not Loading**:
   - Check file paths in `app/static/`
   - Verify Flask static configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code documentation
3. Create an issue in the repository
