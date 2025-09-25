// Internship Form JavaScript
const API_BASE_URL = 'http://localhost:5001/api/company';

// Utility Functions
function showAlert(message, type = 'danger') {
    const alertContainer = document.getElementById('alert-container');
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    alertContainer.innerHTML = alertHtml;
    
    // Auto-dismiss success alerts
    if (type === 'success') {
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }
    
    // Scroll to top to show alert
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function setButtonLoading(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    const text = document.getElementById(buttonId.replace('Btn', 'BtnText'));
    const spinner = document.getElementById(buttonId.replace('Btn', 'Spinner'));
    
    if (isLoading) {
        button.disabled = true;
        if (text) text.style.display = 'none';
        if (spinner) spinner.classList.remove('d-none');
    } else {
        button.disabled = false;
        if (text) text.style.display = 'inline';
        if (spinner) spinner.classList.add('d-none');
    }
}

// Check authentication
async function checkAuth() {
    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (!data.success) {
            window.location.href = '/company/login';
        }
    } catch (error) {
        console.error('Auth check error:', error);
        window.location.href = '/company/login';
    }
}

// Add Internship Form
if (document.getElementById('addInternshipForm')) {
    document.getElementById('addInternshipForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        setButtonLoading('submitBtn', true);
        
        const formData = new FormData(this);
        
        const internshipData = {
            internship_title: formData.get('internship_title'),
            industry_domain: formData.get('industry_domain'),
            location_type: formData.get('location_type'),
            education_level: formData.get('education_level'),
            duration: formData.get('duration'),
            minimum_gpa: formData.get('minimum_gpa'),
            stipend: formData.get('stipend'),
            fulltime_conversion: formData.has('fulltime_conversion'),
            required_skills: formData.get('required_skills'),
            job_description: formData.get('job_description'),
            past_intern_records: formData.get('past_intern_records')
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/internships`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(internshipData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('Internship created successfully!', 'success');
                setTimeout(() => {
                    window.location.href = '/company/dashboard';
                }, 2000);
            } else {
                showAlert(data.message || 'Failed to create internship');
            }
        } catch (error) {
            console.error('Error creating internship:', error);
            showAlert('Network error. Please try again.');
        } finally {
            setButtonLoading('submitBtn', false);
        }
    });
}

// Edit Internship Form (if on edit page)
if (window.location.pathname.includes('edit-internship')) {
    const urlParams = new URLSearchParams(window.location.search);
    const internshipId = urlParams.get('id');
    
    if (internshipId) {
        loadInternshipData(internshipId);
    } else {
        showAlert('No internship ID provided');
        setTimeout(() => {
            window.location.href = '/company/dashboard';
        }, 3000);
    }
}

// Load existing internship data for editing
async function loadInternshipData(internshipId) {
    try {
        const response = await fetch(`${API_BASE_URL}/internships/${internshipId}`, {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.success) {
            populateForm(data.internship);
        } else {
            showAlert(data.message || 'Failed to load internship data');
            setTimeout(() => {
                window.location.href = '/company/dashboard';
            }, 3000);
        }
    } catch (error) {
        console.error('Error loading internship:', error);
        showAlert('Error loading internship data');
    }
}

// Populate form with existing data
function populateForm(internship) {
    const form = document.getElementById('editInternshipForm') || document.getElementById('addInternshipForm');
    if (!form) return;
    
    // Fill form fields
    const fields = [
        'internship_title', 'industry_domain', 'location_type',
        'education_level', 'duration', 'minimum_gpa', 'stipend',
        'required_skills', 'job_description', 'past_intern_records'
    ];
    
    fields.forEach(field => {
        const element = form.querySelector(`[name="${field}"]`);
        if (element && internship[field] !== undefined && internship[field] !== null) {
            element.value = internship[field];
        }
    });
    
    // Handle checkbox
    const fulltimeCheckbox = form.querySelector('[name="fulltime_conversion"]');
    if (fulltimeCheckbox) {
        fulltimeCheckbox.checked = internship.fulltime_conversion;
    }
    
    // Update form submission for edit
    setupEditForm(internship.internship_id);
}

// Setup edit form submission
function setupEditForm(internshipId) {
    const form = document.getElementById('editInternshipForm');
    if (!form) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        setButtonLoading('updateBtn', true);
        
        const formData = new FormData(this);
        
        const internshipData = {
            internship_title: formData.get('internship_title'),
            industry_domain: formData.get('industry_domain'),
            location_type: formData.get('location_type'),
            education_level: formData.get('education_level'),
            duration: formData.get('duration'),
            minimum_gpa: formData.get('minimum_gpa'),
            stipend: formData.get('stipend'),
            fulltime_conversion: formData.has('fulltime_conversion'),
            required_skills: formData.get('required_skills'),
            job_description: formData.get('job_description'),
            past_intern_records: formData.get('past_intern_records')
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/internships/${internshipId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(internshipData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('Internship updated successfully!', 'success');
                setTimeout(() => {
                    window.location.href = '/company/dashboard';
                }, 2000);
            } else {
                showAlert(data.message || 'Failed to update internship');
            }
        } catch (error) {
            console.error('Error updating internship:', error);
            showAlert('Network error. Please try again.');
        } finally {
            setButtonLoading('updateBtn', false);
        }
    });
}

// Logout functionality
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication on page load
    checkAuth();
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function() {
            try {
                await fetch(`${API_BASE_URL}/logout`, {
                    method: 'POST',
                    credentials: 'include'
                });
                window.location.href = '/company/login';
            } catch (error) {
                console.error('Logout error:', error);
                window.location.href = '/company/login';
            }
        });
    }
});