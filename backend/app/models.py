from app import db, bcrypt
from flask_login import UserMixin
from datetime import datetime
import string
import random

class User(UserMixin, db.Model):
    """Unified User model combining authentication and profile data"""
    __tablename__ = 'users'
    
    # Use 6-character random string as primary key
    user_id = db.Column(db.String(6), primary_key=True)
    
    # Authentication fields
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Profile fields (from CompleteProfile) - all optional except aadhar_id
    aadhar_id = db.Column(db.String(12), unique=True, nullable=True, index=True)
    
    # Personal Information
    name = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    state = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    pincode = db.Column(db.String(6), nullable=True)
    
    # Education
    education_level = db.Column(db.String(50), nullable=True)
    degree = db.Column(db.String(100), nullable=True)
    year_of_study = db.Column(db.String(20), nullable=True)
    gpa_percentage = db.Column(db.Float, nullable=True)
    
    # Skills and Courses
    relevant_courses = db.Column(db.Text, nullable=True)
    technical_skills = db.Column(db.Text, nullable=True)
    soft_skills = db.Column(db.Text, nullable=True)
    
    # Certifications (file paths)
    certifications = db.Column(db.Text, nullable=True)
    
    # Experience
    previous_internships = db.Column(db.Text, nullable=True)
    projects = db.Column(db.Text, nullable=True)
    hackathons_competitions = db.Column(db.Text, nullable=True)
    research_experience = db.Column(db.Text, nullable=True)
    
    # Preferences
    internship_type_preference = db.Column(db.String(20), nullable=True)
    duration_preference = db.Column(db.String(50), nullable=True)
    stipend_expectation = db.Column(db.String(50), nullable=True)
    preferred_industry = db.Column(db.Text, nullable=True)
    
    # AI/ML Fields for recommendation engine
    vision_extracted_data = db.Column(db.Text, nullable=True)  # JSON string of vision-extracted info
    vision_vector_data = db.Column(db.Text, nullable=True)     # JSON string of processed vectors/embeddings
    recommendation_list = db.Column(db.Text, nullable=True)    # JSON string of recommended internship IDs
    recommendations_updated_at = db.Column(db.DateTime, nullable=True)
    vision_processed_at = db.Column(db.DateTime, nullable=True) # When documents were last processed
    
    # Profile completion tracking
    profile_updated_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self, username, password):
        """Initialize user with username, hashed password, and generated user_id"""
        self.user_id = self.generate_user_id()
        self.username = username
        self.set_password(password)
    
    @staticmethod
    def generate_user_id():
        """Generate a random 6-character alphanumeric user ID"""
        characters = string.ascii_letters + string.digits
        while True:
            user_id = ''.join(random.choices(characters, k=6))
            # Check if this ID already exists
            if not User.query.filter_by(user_id=user_id).first():
                return user_id
    
    def get_id(self):
        """Return the user_id for Flask-Login"""
        return self.user_id
    
    def set_password(self, password):
        """Hash and set password using Flask-Bcrypt"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return bcrypt.check_password_hash(self.password, password)
    
    def calculate_age(self):
        """Calculate age from date of birth"""
        if self.dob:
            today = datetime.now().date()
            age = today.year - self.dob.year
            if today < self.dob.replace(year=today.year):
                age -= 1
            return age
        return 0
    
    def set_age_from_dob(self):
        """Set the age field based on date of birth"""
        if self.dob:
            self.age = self.calculate_age()
    
    def get_profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        # Define all profile fields that count towards completion
        profile_fields = [
            'name', 'dob', 'aadhar_id', 'state', 'city', 'pincode',
            'education_level', 'degree', 'year_of_study', 'gpa_percentage',
            'technical_skills', 'soft_skills', 'internship_type_preference',
            'duration_preference', 'preferred_industry'
        ]
        
        completed_fields = 0
        for field in profile_fields:
            value = getattr(self, field, None)
            if value is not None and str(value).strip():
                completed_fields += 1
        
        return round((completed_fields / len(profile_fields)) * 100, 1)
    
    def is_profile_complete(self):
        """Check if profile has minimum required fields"""
        required_fields = ['name', 'dob', 'aadhar_id', 'education_level', 'degree']
        for field in required_fields:
            if not getattr(self, field, None):
                return False
        return True
    
    def to_dict(self):
        """Convert user object to dictionary for JSON responses"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'profile_completion': self.get_profile_completion_percentage(),
            'is_profile_complete': self.is_profile_complete(),
            # Profile data
            'aadhar_id': self.aadhar_id,
            'name': self.name,
            'dob': self.dob.isoformat() if self.dob else None,
            'age': self.age,
            'state': self.state,
            'city': self.city,
            'pincode': self.pincode,
            'education_level': self.education_level,
            'degree': self.degree,
            'year_of_study': self.year_of_study,
            'gpa_percentage': self.gpa_percentage,
            'relevant_courses': self.relevant_courses,
            'technical_skills': self.technical_skills,
            'soft_skills': self.soft_skills,
            'certifications': self.certifications,
            'previous_internships': self.previous_internships,
            'projects': self.projects,
            'hackathons_competitions': self.hackathons_competitions,
            'research_experience': self.research_experience,
            'internship_type_preference': self.internship_type_preference,
            'duration_preference': self.duration_preference,
            'stipend_expectation': self.stipend_expectation,
            'preferred_industry': self.preferred_industry,
            'vision_extracted_data': self.vision_extracted_data,
            'vision_vector_data': self.vision_vector_data,
            'recommendation_list': self.recommendation_list,
            'recommendations_updated_at': self.recommendations_updated_at.isoformat() if self.recommendations_updated_at else None,
            'vision_processed_at': self.vision_processed_at.isoformat() if self.vision_processed_at else None,
            'profile_updated_at': self.profile_updated_at.isoformat() if self.profile_updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username} ({self.user_id})>'


class Company(UserMixin, db.Model):
    """Company model for posting internships"""
    __tablename__ = 'companies'
    
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(200), nullable=False)
    company_email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    company_website = db.Column(db.String(200))
    company_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationship to internships
    internships = db.relationship('Internship', backref='company', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, company_name, company_email, password, company_website=None, company_description=None):
        """Initialize company with required details"""
        self.company_name = company_name
        self.company_email = company_email
        self.company_website = company_website
        self.company_description = company_description
        self.set_password(password)
    
    def set_password(self, password):
        """Hash and set password using Flask-Bcrypt"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches stored hash"""
        return bcrypt.check_password_hash(self.password, password)
    
    def get_id(self):
        """Return the company_id for Flask-Login"""
        return str(self.company_id)
    
    def to_dict(self):
        """Convert company object to dictionary for JSON responses"""
        return {
            'company_id': self.company_id,
            'company_name': self.company_name,
            'company_email': self.company_email,
            'company_website': self.company_website,
            'company_description': self.company_description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'total_internships': len(self.internships)
        }
    
    def __repr__(self):
        return f'<Company {self.company_name}>'



class Internship(db.Model):
    """Internship model for managing internship opportunities"""
    __tablename__ = 'internships'
    
    internship_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    
    # Basic Information
    internship_title = db.Column(db.String(200), nullable=False)
    industry_domain = db.Column(db.String(100), nullable=False)
    location_type = db.Column(db.Enum('Remote', 'On-site', 'Hybrid', name='location_type'), nullable=False)
    
    # Requirements
    education_level = db.Column(db.String(50), nullable=False)  # High School, Undergraduate, Graduate, etc.
    duration = db.Column(db.String(50), nullable=False)  # e.g., "3 months", "6 months"
    minimum_gpa = db.Column(db.Numeric(3, 2))  # DECIMAL(3,2) for GPA like 3.75
    stipend = db.Column(db.String(100))  # e.g., "10,000 INR/month", "Unpaid"
    fulltime_conversion = db.Column(db.Boolean, default=False)
    required_skills = db.Column(db.Text)  # Store as comma-separated or JSON
    
    # Descriptions
    job_description = db.Column(db.Text, nullable=False)
    past_intern_records = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert internship object to dictionary"""
        return {
            'internship_id': self.internship_id,
            'company_id': self.company_id,
            'company_name': self.company.company_name if self.company else None,
            'internship_title': self.internship_title,
            'industry_domain': self.industry_domain,
            'location_type': self.location_type,
            'education_level': self.education_level,
            'duration': self.duration,
            'minimum_gpa': float(self.minimum_gpa) if self.minimum_gpa else None,
            'stipend': self.stipend,
            'fulltime_conversion': self.fulltime_conversion,
            'required_skills': self.required_skills,
            'job_description': self.job_description,
            'past_intern_records': self.past_intern_records,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Internship {self.internship_title} - {self.company.company_name if self.company else "No Company"}>'