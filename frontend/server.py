from flask import Flask, render_template, send_from_directory, request
import os

app = Flask(__name__)

# Get the frontend directory path
frontend_dir = os.path.dirname(os.path.abspath(__file__))

# Student Portal routes
@app.route('/')
def index():
    """Student homepage"""
    return send_from_directory(os.path.join(frontend_dir, 'public'), 'index.html')

@app.route('/home')
@app.route('/home.html')
def home():
    return send_from_directory(os.path.join(frontend_dir, 'public'), 'home.html')

@app.route('/auth')
@app.route('/auth.html')
def auth():
    return send_from_directory(os.path.join(frontend_dir, 'public'), 'auth.html')

@app.route('/complete-profile')
@app.route('/complete-profile.html')
def complete_profile():
    return send_from_directory(os.path.join(frontend_dir, 'public'), 'complete-profile.html')

# Alternative route for index.html
@app.route('/index.html')
def index_html():
    return send_from_directory(os.path.join(frontend_dir, 'public'), 'index.html')

# Company routes
@app.route('/company/')
def company_index():
    """Company homepage"""
    return send_from_directory(frontend_dir, 'company/index.html')

@app.route('/company/login')
def company_login():
    return send_from_directory(frontend_dir, 'company/login.html')

@app.route('/company/register')
def company_register():
    return send_from_directory(frontend_dir, 'company/register.html')

@app.route('/company/dashboard')
def company_dashboard():
    return send_from_directory(frontend_dir, 'company/dashboard.html')

@app.route('/company/add-internship')
def add_internship():
    return send_from_directory(frontend_dir, 'company/add-internship.html')

@app.route('/company/edit-internship')
def edit_internship():
    return send_from_directory(frontend_dir, 'company/edit-internship.html')

# Static files for student portal
@app.route('/src/<path:filename>')
def src_files(filename):
    return send_from_directory(os.path.join(frontend_dir, 'src'), filename)

@app.route('/styles/<path:filename>')
def styles(filename):
    return send_from_directory(os.path.join(frontend_dir, 'src', 'styles'), filename)

# Static files for company portal
@app.route('/company/js/<path:filename>')
def company_js(filename):
    return send_from_directory(os.path.join(frontend_dir, 'company', 'js'), filename)

@app.route('/company/css/<path:filename>')
def company_css(filename):
    return send_from_directory(os.path.join(frontend_dir, 'company', 'css'), filename)

# Debug route to check file paths
@app.route('/debug')
def debug():
    return f"""
    Frontend dir: {frontend_dir}<br>
    Public dir exists: {os.path.exists(os.path.join(frontend_dir, 'public'))}<br>
    Files in public: {os.listdir(os.path.join(frontend_dir, 'public')) if os.path.exists(os.path.join(frontend_dir, 'public')) else 'Not found'}<br>
    """

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=8080)