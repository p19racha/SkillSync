from app import create_app, db
from app.models import User

app = create_app()

@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print("Database tables created successfully!")

@app.cli.command()
def create_admin():
    """Create an admin user."""
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    if User.query.filter_by(username=username).first():
        print(f"User {username} already exists!")
        return
    
    admin_user = User(username=username)
    admin_user.set_password(password)
    
    db.session.add(admin_user)
    db.session.commit()
    
    print(f"Admin user {username} created successfully!")

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database initialized!")
    
    app.run(debug=True, host='0.0.0.0', port=5001)