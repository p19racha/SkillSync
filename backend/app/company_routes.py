from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import Company, Internship
import re

company_bp = Blueprint('company', __name__, url_prefix='/api/company')

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_company_data(data, is_registration=False):
    """Validate company registration/login data"""
    errors = []
    
    if is_registration:
        # Company name validation
        if not data.get('company_name') or len(data['company_name'].strip()) < 2:
            errors.append('Company name must be at least 2 characters long')
        
        # Website validation (optional)
        website = data.get('company_website', '').strip()
        if website and not (website.startswith('http://') or website.startswith('https://')):
            data['company_website'] = 'https://' + website
    
    # Email validation
    email = data.get('company_email', '').strip().lower()
    if not email or not validate_email(email):
        errors.append('Please provide a valid email address')
    else:
        data['company_email'] = email
    
    # Password validation
    password = data.get('password', '')
    if not password or len(password) < 6:
        errors.append('Password must be at least 6 characters long')
    
    return errors

@company_bp.route('/register', methods=['POST'])
def register():
    """Register a new company"""
    try:
        data = request.get_json()
        
        # Validate input data
        errors = validate_company_data(data, is_registration=True)
        if errors:
            return jsonify({'success': False, 'message': '. '.join(errors)}), 400
        
        # Check if company already exists
        existing_company = Company.query.filter_by(company_email=data['company_email']).first()
        if existing_company:
            return jsonify({'success': False, 'message': 'Company with this email already exists'}), 400
        
        # Create new company
        new_company = Company(
            company_name=data['company_name'].strip(),
            company_email=data['company_email'],
            password=data['password'],
            company_website=data.get('company_website', '').strip(),
            company_description=data.get('company_description', '').strip()
        )
        
        db.session.add(new_company)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Company registered successfully',
            'company': new_company.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Registration failed: {str(e)}'}), 500

@company_bp.route('/login', methods=['POST'])
def login():
    """Login company"""
    try:
        data = request.get_json()
        
        # Validate input data
        errors = validate_company_data(data)
        if errors:
            return jsonify({'success': False, 'message': '. '.join(errors)}), 400
        
        # Find company
        company = Company.query.filter_by(company_email=data['company_email']).first()
        
        if company and company.check_password(data['password']):
            # Store company session
            session['company_id'] = company.company_id
            session['company_logged_in'] = True
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'company': company.to_dict()
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'Login failed: {str(e)}'}), 500

@company_bp.route('/logout', methods=['POST'])
def logout():
    """Logout company"""
    session.pop('company_id', None)
    session.pop('company_logged_in', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@company_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get company profile"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    company = Company.query.get(session['company_id'])
    if not company:
        return jsonify({'success': False, 'message': 'Company not found'}), 404
    
    return jsonify({'success': True, 'company': company.to_dict()}), 200

@company_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update company profile"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        company = Company.query.get(session['company_id'])
        if not company:
            return jsonify({'success': False, 'message': 'Company not found'}), 404
        
        data = request.get_json()
        
        # Update company fields
        if 'company_name' in data:
            if len(data['company_name'].strip()) < 2:
                return jsonify({'success': False, 'message': 'Company name must be at least 2 characters long'}), 400
            company.company_name = data['company_name'].strip()
        
        if 'company_website' in data:
            website = data['company_website'].strip()
            if website and not (website.startswith('http://') or website.startswith('https://')):
                website = 'https://' + website
            company.company_website = website
        
        if 'company_description' in data:
            company.company_description = data['company_description'].strip()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'company': company.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Update failed: {str(e)}'}), 500

# Internship Management Routes
@company_bp.route('/internships', methods=['GET'])
def get_company_internships():
    """Get all internships for the logged-in company"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        internships = Internship.query.filter_by(company_id=session['company_id']).all()
        return jsonify({
            'success': True,
            'internships': [internship.to_dict() for internship in internships]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to fetch internships: {str(e)}'}), 500

@company_bp.route('/internships', methods=['POST'])
def create_internship():
    """Create a new internship"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'internship_title', 'industry_domain', 'location_type',
            'education_level', 'duration', 'job_description'
        ]
        
        errors = []
        for field in required_fields:
            if not data.get(field) or not data[field].strip():
                errors.append(f'{field.replace("_", " ").title()} is required')
        
        # Validate location_type
        valid_location_types = ['Remote', 'On-site', 'Hybrid']
        if data.get('location_type') not in valid_location_types:
            errors.append('Location type must be Remote, On-site, or Hybrid')
        
        # Validate minimum_gpa if provided
        if data.get('minimum_gpa'):
            try:
                gpa = float(data['minimum_gpa'])
                if gpa < 0 or gpa > 4.0:
                    errors.append('Minimum GPA must be between 0 and 4.0')
            except ValueError:
                errors.append('Minimum GPA must be a valid number')
        
        if errors:
            return jsonify({'success': False, 'message': '. '.join(errors)}), 400
        
        # Create new internship
        new_internship = Internship(
            company_id=session['company_id'],
            internship_title=data['internship_title'].strip(),
            industry_domain=data['industry_domain'].strip(),
            location_type=data['location_type'],
            education_level=data['education_level'].strip(),
            duration=data['duration'].strip(),
            minimum_gpa=float(data['minimum_gpa']) if data.get('minimum_gpa') else None,
            stipend=data.get('stipend', '').strip(),
            fulltime_conversion=data.get('fulltime_conversion', False),
            required_skills=data.get('required_skills', '').strip(),
            job_description=data['job_description'].strip(),
            past_intern_records=data.get('past_intern_records', '').strip()
        )
        
        db.session.add(new_internship)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Internship created successfully',
            'internship': new_internship.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to create internship: {str(e)}'}), 500

@company_bp.route('/internships/<int:internship_id>', methods=['GET'])
def get_internship(internship_id):
    """Get a specific internship"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    internship = Internship.query.filter_by(
        internship_id=internship_id,
        company_id=session['company_id']
    ).first()
    
    if not internship:
        return jsonify({'success': False, 'message': 'Internship not found'}), 404
    
    return jsonify({
        'success': True,
        'internship': internship.to_dict()
    }), 200

@company_bp.route('/internships/<int:internship_id>', methods=['PUT'])
def update_internship(internship_id):
    """Update an existing internship"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        internship = Internship.query.filter_by(
            internship_id=internship_id,
            company_id=session['company_id']
        ).first()
        
        if not internship:
            return jsonify({'success': False, 'message': 'Internship not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided
        updateable_fields = [
            'internship_title', 'industry_domain', 'location_type',
            'education_level', 'duration', 'stipend', 'required_skills',
            'job_description', 'past_intern_records', 'is_active'
        ]
        
        for field in updateable_fields:
            if field in data:
                if field == 'location_type' and data[field] not in ['Remote', 'On-site', 'Hybrid']:
                    return jsonify({'success': False, 'message': 'Invalid location type'}), 400
                
                if field == 'minimum_gpa' and data[field]:
                    try:
                        gpa = float(data[field])
                        if gpa < 0 or gpa > 4.0:
                            return jsonify({'success': False, 'message': 'GPA must be between 0 and 4.0'}), 400
                        setattr(internship, field, gpa)
                    except ValueError:
                        return jsonify({'success': False, 'message': 'Invalid GPA value'}), 400
                else:
                    setattr(internship, field, data[field])
        
        # Handle special fields
        if 'minimum_gpa' in data:
            if data['minimum_gpa']:
                try:
                    internship.minimum_gpa = float(data['minimum_gpa'])
                except ValueError:
                    return jsonify({'success': False, 'message': 'Invalid GPA value'}), 400
            else:
                internship.minimum_gpa = None
        
        if 'fulltime_conversion' in data:
            internship.fulltime_conversion = bool(data['fulltime_conversion'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Internship updated successfully',
            'internship': internship.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to update internship: {str(e)}'}), 500

@company_bp.route('/internships/<int:internship_id>', methods=['DELETE'])
def delete_internship(internship_id):
    """Delete an internship"""
    if 'company_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        internship = Internship.query.filter_by(
            internship_id=internship_id,
            company_id=session['company_id']
        ).first()
        
        if not internship:
            return jsonify({'success': False, 'message': 'Internship not found'}), 404
        
        db.session.delete(internship)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Internship deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Failed to delete internship: {str(e)}'}), 500