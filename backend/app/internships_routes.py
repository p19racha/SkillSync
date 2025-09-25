from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db
from app.models import Internship
from sqlalchemy.exc import IntegrityError
import re

# Create blueprint for internships
internships_bp = Blueprint('internships', __name__)


def validate_internship_data(data):
    """Validate internship data"""
    errors = []
    
    # Required fields
    required_fields = ['internship_title', 'industry_domain', 'education_level', 'location_type', 'duration']
    for field in required_fields:
        if not data.get(field) or not data.get(field).strip():
            errors.append(f'{field.replace("_", " ").title()} is required')
    
    # Validate education level
    valid_education_levels = ['High School', 'Undergraduate', 'Graduate', 'Postgraduate', 'PhD']
    if data.get('education_level') and data.get('education_level') not in valid_education_levels:
        errors.append('Invalid education level')
    
    # Validate location type
    valid_location_types = ['On-site', 'Remote', 'Hybrid']
    if data.get('location_type') and data.get('location_type') not in valid_location_types:
        errors.append('Invalid location type')
    
    # Validate minimum GPA if provided
    if data.get('minimum_gpa'):
        try:
            gpa = float(data.get('minimum_gpa'))
            if gpa < 0.0 or gpa > 10.0:  # Assuming 10.0 scale
                errors.append('Minimum GPA must be between 0.0 and 10.0')
        except (ValueError, TypeError):
            errors.append('Minimum GPA must be a valid number')
    
    # Validate fulltime_conversion
    if 'fulltime_conversion' in data:
        if not isinstance(data['fulltime_conversion'], bool):
            # Try to convert string values
            if str(data['fulltime_conversion']).lower() in ['true', '1', 'yes', 'on']:
                data['fulltime_conversion'] = True
            elif str(data['fulltime_conversion']).lower() in ['false', '0', 'no', 'off', '']:
                data['fulltime_conversion'] = False
            else:
                errors.append('Full-time conversion must be true or false')
    
    return errors


@internships_bp.route('/api/internships', methods=['POST'])
@login_required
def create_internship():
    """Create a new internship"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validate input data
        errors = validate_internship_data(data)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation errors',
                'errors': errors
            }), 400
        
        # Create new internship
        internship = Internship(
            internship_title=data.get('internship_title', '').strip(),
            industry_domain=data.get('industry_domain', '').strip(),
            required_skills=data.get('required_skills', '').strip(),
            education_level=data.get('education_level'),
            minimum_gpa=float(data.get('minimum_gpa')) if data.get('minimum_gpa') else None,
            location_type=data.get('location_type'),
            duration=data.get('duration', '').strip(),
            stipend=data.get('stipend', '').strip(),
            fulltime_conversion=data.get('fulltime_conversion', False),
            description=data.get('description', '').strip(),
            past_intern_records=data.get('past_intern_records', '').strip()
        )
        
        db.session.add(internship)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Internship created successfully',
            'internship': internship.to_dict()
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Database error: Internship could not be created',
            'error': str(e)
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error creating internship: {str(e)}'
        }), 500


@internships_bp.route('/api/internships', methods=['GET'])
def get_all_internships():
    """Fetch all internships"""
    try:
        # Get query parameters for filtering/pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        industry = request.args.get('industry', '')
        location_type = request.args.get('location_type', '')
        education_level = request.args.get('education_level', '')
        
        # Build query with filters
        query = Internship.query
        
        if industry:
            query = query.filter(Internship.industry_domain.ilike(f'%{industry}%'))
        
        if location_type:
            query = query.filter(Internship.location_type == location_type)
            
        if education_level:
            query = query.filter(Internship.education_level == education_level)
        
        # Order by creation date (newest first)
        query = query.order_by(Internship.created_at.desc())
        
        # Paginate results
        internships_paginated = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        internships_list = [internship.to_dict() for internship in internships_paginated.items]
        
        return jsonify({
            'success': True,
            'internships': internships_list,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': internships_paginated.total,
                'pages': internships_paginated.pages,
                'has_next': internships_paginated.has_next,
                'has_prev': internships_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching internships: {str(e)}'
        }), 500


@internships_bp.route('/api/internships/<int:internship_id>', methods=['GET'])
def get_internship_by_id(internship_id):
    """Fetch a specific internship by ID"""
    try:
        internship = Internship.query.get(internship_id)
        
        if not internship:
            return jsonify({
                'success': False,
                'message': 'Internship not found'
            }), 404
        
        return jsonify({
            'success': True,
            'internship': internship.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching internship: {str(e)}'
        }), 500


@internships_bp.route('/api/internships/<int:internship_id>', methods=['PUT'])
@login_required
def update_internship(internship_id):
    """Update an existing internship"""
    try:
        internship = Internship.query.get(internship_id)
        
        if not internship:
            return jsonify({
                'success': False,
                'message': 'Internship not found'
            }), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validate input data
        errors = validate_internship_data(data)
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation errors',
                'errors': errors
            }), 400
        
        # Update internship fields
        internship.internship_title = data.get('internship_title', internship.internship_title).strip()
        internship.industry_domain = data.get('industry_domain', internship.industry_domain).strip()
        internship.required_skills = data.get('required_skills', internship.required_skills).strip()
        internship.education_level = data.get('education_level', internship.education_level)
        internship.minimum_gpa = float(data.get('minimum_gpa')) if data.get('minimum_gpa') else internship.minimum_gpa
        internship.location_type = data.get('location_type', internship.location_type)
        internship.duration = data.get('duration', internship.duration).strip()
        internship.stipend = data.get('stipend', internship.stipend).strip() if data.get('stipend') else internship.stipend
        internship.fulltime_conversion = data.get('fulltime_conversion', internship.fulltime_conversion)
        internship.description = data.get('description', internship.description).strip() if data.get('description') else internship.description
        internship.past_intern_records = data.get('past_intern_records', internship.past_intern_records).strip() if data.get('past_intern_records') else internship.past_intern_records
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Internship updated successfully',
            'internship': internship.to_dict()
        }), 200
        
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Database error: Internship could not be updated',
            'error': str(e)
        }), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error updating internship: {str(e)}'
        }), 500


@internships_bp.route('/api/internships/<int:internship_id>', methods=['DELETE'])
@login_required
def delete_internship(internship_id):
    """Delete an internship"""
    try:
        internship = Internship.query.get(internship_id)
        
        if not internship:
            return jsonify({
                'success': False,
                'message': 'Internship not found'
            }), 404
        
        # Store internship data for response
        internship_data = internship.to_dict()
        
        db.session.delete(internship)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Internship deleted successfully',
            'deleted_internship': internship_data
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting internship: {str(e)}'
        }), 500


# Additional utility routes

@internships_bp.route('/api/internships/filters', methods=['GET'])
def get_filter_options():
    """Get available filter options for internships"""
    try:
        # Get unique values for filtering
        industries = db.session.query(Internship.industry_domain).distinct().all()
        education_levels = db.session.query(Internship.education_level).distinct().all()
        location_types = ['On-site', 'Remote', 'Hybrid']  # From enum
        
        return jsonify({
            'success': True,
            'filters': {
                'industries': [industry[0] for industry in industries if industry[0]],
                'education_levels': [level[0] for level in education_levels if level[0]],
                'location_types': location_types
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching filter options: {str(e)}'
        }), 500


@internships_bp.route('/api/internships/search', methods=['GET'])
def search_internships():
    """Search internships by keyword"""
    try:
        keyword = request.args.get('q', '').strip()
        
        if not keyword:
            return jsonify({
                'success': False,
                'message': 'Search keyword is required'
            }), 400
        
        # Search in title, industry, skills, and description
        internships = Internship.query.filter(
            db.or_(
                Internship.internship_title.ilike(f'%{keyword}%'),
                Internship.industry_domain.ilike(f'%{keyword}%'),
                Internship.required_skills.ilike(f'%{keyword}%'),
                Internship.description.ilike(f'%{keyword}%')
            )
        ).order_by(Internship.created_at.desc()).all()
        
        internships_list = [internship.to_dict() for internship in internships]
        
        return jsonify({
            'success': True,
            'internships': internships_list,
            'search_term': keyword,
            'count': len(internships_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error searching internships: {str(e)}'
        }), 500