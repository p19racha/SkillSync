from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
import re
from datetime import datetime
import os
from werkzeug.utils import secure_filename

# Create blueprint
main = Blueprint('main', __name__)

def validate_username(username):
    """Validate username format"""
    if len(username) < 3 or len(username) > 50:
        return False
    # Allow email addresses as usernames
    if not re.match(r"^[a-zA-Z0-9_.@]+$", username):
        return False
    return True

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False
    return True

@main.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'GET':
        return render_template('register.html')
    
    # Handle AJAX POST request
    if request.is_json:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Validation
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        if not validate_username(username):
            return jsonify({
                'success': False,
                'message': 'Username must be 3-20 characters and contain only letters, numbers, and underscores'
            }), 400
        
        if not validate_password(password):
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 409
        
        try:
            # Create new user
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            
            # Auto-login after registration
            login_user(user, remember=True)
            
            return jsonify({
                'success': True,
                'message': 'Registration successful! Welcome!',
                'user': user.to_dict(),
                'redirect': url_for('main.dashboard')
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': 'Registration failed. Please try again.'
            }), 500
    
    # Handle regular form submission
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if not username or not password:
        flash('Username and password are required', 'error')
        return redirect(url_for('main.register'))
    
    if not validate_username(username):
        flash('Username must be 3-20 characters and contain only letters, numbers, and underscores', 'error')
        return redirect(url_for('main.register'))
    
    if not validate_password(password):
        flash('Password must be at least 6 characters long', 'error')
        return redirect(url_for('main.register'))
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(url_for('main.register'))
    
    try:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user, remember=True)
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('main.dashboard'))
        
    except Exception as e:
        db.session.rollback()
        flash('Registration failed. Please try again.', 'error')
        return redirect(url_for('main.register'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'GET':
        return render_template('login.html')
    
    # Handle AJAX POST request
    if request.is_json:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400
        
        # Find user and verify password
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict(),
                'redirect': 'home.html'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
    
    # Handle regular form submission
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    
    if not username or not password:
        flash('Username and password are required', 'error')
        return redirect(url_for('main.login'))
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user, remember=True)
        flash('Login successful!', 'success')
        return redirect(url_for('main.dashboard'))
    else:
        flash('Invalid username or password', 'error')
        return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    """User dashboard - protected route"""
    return render_template('dashboard.html', user=current_user)

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    
    if request.is_json:
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('main.index'))

@main.route('/api/user')
@login_required
def api_user():
    """Get current user info (API endpoint)"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    })

@main.route('/api/check-auth')
def check_auth():
    """Check if user is authenticated"""
    return jsonify({
        'authenticated': current_user.is_authenticated,
        'user': current_user.to_dict() if current_user.is_authenticated else None
    })

@main.route('/api/complete-profile', methods=['GET'])
@login_required
def get_complete_profile():
    """Get the complete profile for the current user"""
    try:
        return jsonify({
            'success': True,
            'profile': current_user.to_dict(),
            'completion_percentage': current_user.get_profile_completion_percentage()
        }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving profile: {str(e)}'
        }), 500

@main.route('/api/complete-profile', methods=['POST', 'PUT'])
@login_required
def complete_profile():
    """Handle POST and PUT requests to update user profile"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        print(f"Received data: {data}")  # Debug logging
        
        # Get current user
        user = current_user
        
        # Handle date of birth and calculate age first
        dob_str = data.get('dob')
        if dob_str:
            try:
                user.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                user.set_age_from_dob()  # Auto-calculate age
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Update profile fields - ensuring all are strings or proper types
        if 'aadhar_id' in data:
            user.aadhar_id = str(data.get('aadhar_id', ''))
        if 'name' in data:
            user.name = str(data.get('name', ''))
        if 'state' in data:
            user.state = str(data.get('state', ''))
        if 'city' in data:
            user.city = str(data.get('city', ''))
        if 'pincode' in data:
            user.pincode = str(data.get('pincode', ''))
        
        # Education fields
        if 'education_level' in data:
            user.education_level = str(data.get('education_level', ''))
        if 'degree' in data:
            user.degree = str(data.get('degree', ''))
        if 'year_of_study' in data:
            user.year_of_study = str(data.get('year_of_study', ''))
        
        # Handle GPA as float
        if 'gpa_percentage' in data:
            try:
                user.gpa_percentage = float(data.get('gpa_percentage', 0))
            except (ValueError, TypeError):
                return jsonify({'success': False, 'message': 'Invalid GPA/Percentage format'}), 400
        
        # Skills and courses - ensure they are strings
        if 'relevant_courses' in data:
            user.relevant_courses = str(data.get('relevant_courses', ''))
        if 'technical_skills' in data:
            user.technical_skills = str(data.get('technical_skills', ''))
        if 'soft_skills' in data:
            user.soft_skills = str(data.get('soft_skills', ''))
        
        # Experience - ensure they are strings
        if 'previous_internships' in data:
            user.previous_internships = str(data.get('previous_internships', ''))
        if 'projects' in data:
            user.projects = str(data.get('projects', ''))
        if 'hackathons_competitions' in data:
            user.hackathons_competitions = str(data.get('hackathons_competitions', ''))
        if 'research_experience' in data:
            user.research_experience = str(data.get('research_experience', ''))
        
        # Preferences - ensure they are strings
        if 'internship_type_preference' in data:
            user.internship_type_preference = str(data.get('internship_type_preference', ''))
        if 'duration_preference' in data:
            user.duration_preference = str(data.get('duration_preference', ''))
        if 'stipend_expectation' in data:
            user.stipend_expectation = str(data.get('stipend_expectation', ''))
        if 'preferred_industry' in data:
            user.preferred_industry = str(data.get('preferred_industry', ''))
        
        # Handle certifications (this will be updated when file upload is implemented)
        if 'certifications' in data:
            user.certifications = str(data.get('certifications', ''))
        
        # Update profile timestamp
        user.profile_updated_at = datetime.utcnow()
        
        print(f"User object before save: {user.__dict__}")  # Debug logging
        
        # Save to database
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'profile': user.to_dict(),
            'completion_percentage': user.get_profile_completion_percentage()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in complete_profile route: {e}")  # Debug logging
        return jsonify({
            'success': False,
            'message': f'Error updating profile: {str(e)}'
        }), 500

# Error handlers
@main.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized access"""
    if request.is_json:
        return jsonify({
            'success': False,
            'message': 'Please log in to access this resource'
        }), 401
    return redirect(url_for('main.login'))

@main.route('/api/upload-certification', methods=['POST'])
@login_required
def upload_certification():
    """Handle certification file uploads"""
    try:
        if 'certification' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400
        
        file = request.files['certification']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Check file extension
        allowed_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                'success': False,
                'message': 'File type not allowed'
            }), 400
        
        # Create user-specific uploads directory
        user_upload_dir = os.path.join('uploads', 'certifications', current_user.user_id)
        os.makedirs(user_upload_dir, exist_ok=True)
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        # Add timestamp to avoid naming conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
        
        file_path = os.path.join(user_upload_dir, filename)
        file.save(file_path)
        
        # Automatically process documents after upload
        try:
            processing_result = process_user_documents_automatically(current_user.user_id)
            return jsonify({
                'success': True,
                'message': 'File uploaded and processed successfully',
                'file_path': file_path,
                'filename': filename,
                'processing_result': processing_result
            })
        except Exception as process_error:
            # File upload succeeded but processing failed - that's okay
            print(f"Document processing failed: {process_error}")
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully (processing will occur in background)',
                'file_path': file_path,
                'filename': filename,
                'processing_status': 'deferred'
            })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Upload failed: {str(e)}'
        }), 500

def process_user_documents_automatically(user_id):
    """Automatically process uploaded documents for a user"""
    try:
        # Import the Engine with fallback
        try:
            import sys
            import os
            engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Engine')
            if engine_path not in sys.path:
                sys.path.append(engine_path)
            
            from main import RecommendationOrchestrator
        except ImportError as e:
            print(f"Engine import failed: {e}")
            return {'success': False, 'message': 'AI processing temporarily unavailable'}
        from datetime import datetime
        import json
        
        # Get uploaded file paths for user
        upload_dir = os.path.join('uploads', 'certifications', user_id)
        
        if not os.path.exists(upload_dir):
            return {'success': False, 'message': 'No documents to process'}
        
        # Get all files in user's upload directory
        file_paths = []
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_paths.append(os.path.abspath(file_path))
        
        if not file_paths:
            return {'success': False, 'message': 'No documents found'}
        
        # Initialize the recommendation orchestrator
        orchestrator = RecommendationOrchestrator()
        
        # Process documents
        result = orchestrator.process_uploaded_documents(user_id, file_paths)
        
        # Check if processing was successful (at least one successful extraction)
        processing_summary = result.get('processing_summary', {})
        successful_extractions = processing_summary.get('successful_extractions', 0)
        
        if successful_extractions > 0:
            # Update user's vision fields
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                user.vision_extracted_data = json.dumps(result)
                
                # Create vector data from combined results
                vector_data = {
                    'processed_files': len(file_paths),
                    'successful_extractions': successful_extractions,
                    'failed_extractions': processing_summary.get('failed_extractions', 0),
                    'skills_extracted': result.get('combined_skills', []),
                    'technologies_extracted': result.get('combined_technologies', []),
                    'processing_timestamp': datetime.utcnow().isoformat()
                }
                user.vision_vector_data = json.dumps(vector_data)
                user.vision_processed_at = datetime.utcnow()
                
                db.session.commit()
                
                return {
                    'success': True,
                    'message': f'Documents processed successfully ({successful_extractions}/{len(file_paths)} files)',
                    'extracted_data': result,
                    'vector_data': vector_data
                }
        
        return {'success': False, 'message': 'Document processing failed'}
        
    except Exception as e:
        print(f"Automatic document processing failed: {e}")
        return {'success': False, 'message': str(e)}

@main.route('/api/process_documents', methods=['POST'])
@login_required
def process_documents():
    """Process uploaded documents using AI vision"""
    try:
        # Import the Engine with fallback
        try:
            import sys
            import os
            engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Engine')
            if engine_path not in sys.path:
                sys.path.append(engine_path)
            
            from main import RecommendationOrchestrator
        except ImportError as e:
            print(f"Engine import failed: {e}")
            return jsonify({
                'success': False,
                'message': 'AI processing service temporarily unavailable'
            }), 503
        
        # Get uploaded file paths for current user
        user_id = current_user.user_id
        upload_dir = os.path.join('uploads', 'certifications', user_id)
        
        if not os.path.exists(upload_dir):
            return jsonify({
                'success': False,
                'message': 'No uploaded documents found'
            }), 404
        
        # Get all files in user's upload directory
        file_paths = []
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_paths.append(file_path)
        
        if not file_paths:
            return jsonify({
                'success': False,
                'message': 'No documents to process'
            }), 400
        
        # Initialize the recommendation orchestrator
        orchestrator = RecommendationOrchestrator()
        
        # Process documents
        result = orchestrator.process_uploaded_documents(user_id, file_paths)
        
        if result.get('success', False):
            # Update user's vision_extracted_data field
            import json
            current_user.vision_extracted_data = json.dumps(result['extracted_data'])
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Documents processed successfully',
                'extracted_data': result['extracted_data']
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('error', 'Document processing failed')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Document processing failed: {str(e)}'
        }), 500

@main.route('/api/generate_recommendations', methods=['POST'])
@login_required
def generate_recommendations():
    """Generate personalized internship recommendations"""
    try:
        # Import the Engine with fallback
        try:
            import sys
            import os
            engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Engine')
            if engine_path not in sys.path:
                sys.path.append(engine_path)
            
            from main import RecommendationOrchestrator
        except ImportError as e:
            print(f"Engine import failed: {e}")
            return jsonify({
                'success': False,
                'message': 'Recommendation engine temporarily unavailable'
            }), 503
        from app.models import Internship
        
        # Get user data
        user_data = current_user.to_dict()
        
        # Get all active internships
        internships = Internship.query.filter_by(is_active=True).all()
        internships_data = [internship.to_dict() for internship in internships]
        
        if not internships_data:
            return jsonify({
                'success': False,
                'message': 'No internships available for recommendations'
            }), 404
        
        # Initialize orchestrator and generate recommendations
        orchestrator = RecommendationOrchestrator()
        
        # Check for force refresh parameter
        force_refresh = request.get_json().get('force_refresh', False) if request.is_json else False
        
        result = orchestrator.generate_user_recommendations(
            user_data, 
            internships_data,
            force_refresh=force_refresh
        )
        
        if result['recommendations']:
            # Update user's recommendation_list in database
            import json
            current_user.recommendation_list = json.dumps(result['recommendations'])
            current_user.recommendations_updated_at = datetime.utcnow()
            db.session.commit()
            
            # Get detailed internship data for the recommendations
            recommended_internships = []
            for internship_id in result['recommendations']:
                internship = Internship.query.get(internship_id)
                if internship:
                    recommended_internships.append(internship.to_dict())
            
            return jsonify({
                'success': True,
                'recommendations': result['recommendations'],
                'detailed_internships': recommended_internships,
                'metadata': {
                    'source': result['source'],
                    'processing_time': result['processing_time'],
                    'profile_completion': result.get('user_profile_completion', 0),
                    'confidence': result.get('recommendation_confidence', 0)
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Unable to generate recommendations',
                'error': result.get('error', 'Unknown error')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Recommendation generation failed: {str(e)}'
        }), 500

@main.route('/api/get_recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """Get current user's recommendations"""
    try:
        import json
        from app.models import Internship
        
        if not current_user.recommendation_list:
            return jsonify({
                'success': False,
                'message': 'No recommendations available. Generate recommendations first.'
            }), 404
        
        # Parse recommendation list
        recommendation_ids = json.loads(current_user.recommendation_list)
        
        # Get detailed internship data
        recommended_internships = []
        for internship_id in recommendation_ids:
            internship = Internship.query.get(internship_id)
            if internship and internship.is_active:
                recommended_internships.append(internship.to_dict())
        
        return jsonify({
            'success': True,
            'recommendations': recommendation_ids,
            'detailed_internships': recommended_internships,
            'updated_at': current_user.recommendations_updated_at.isoformat() if current_user.recommendations_updated_at else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to retrieve recommendations: {str(e)}'
        }), 500

@main.route('/api/system_health', methods=['GET'])
def system_health():
    """Check system health for recommendation engine"""
    try:
        # Import the Engine with fallback
        try:
            import sys
            import os
            engine_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Engine')
            if engine_path not in sys.path:
                sys.path.append(engine_path)
            
            from main import RecommendationOrchestrator
        except ImportError as e:
            print(f"Engine import failed: {e}")
            return jsonify({
                'success': True,
                'health': {'status': 'engine_unavailable', 'message': 'AI engine temporarily unavailable'}
            })
        
        orchestrator = RecommendationOrchestrator()
        health = orchestrator.get_system_health()
        
        return jsonify({
            'success': True,
            'health': health
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Health check failed: {str(e)}'
        }), 500

@main.errorhandler(404)
def not_found(error):
    """Handle page not found"""
    if request.is_json:
        return jsonify({
            'success': False,
            'message': 'Resource not found'
        }), 404
    return render_template('404.html'), 404