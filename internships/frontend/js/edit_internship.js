// Edit Internship JavaScript
class EditInternship {
    constructor() {
        this.form = document.getElementById('editInternshipForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.submitText = document.getElementById('submitText');
        this.submitSpinner = document.getElementById('submitSpinner');
        this.errorContainer = document.getElementById('errorContainer');
        this.errorList = document.getElementById('errorList');
        this.loadingState = document.getElementById('loadingState');
        this.errorState = document.getElementById('errorState');
        this.editForm = document.getElementById('editForm');
        
        this.internshipId = null;
        this.originalData = null;
        
        this.init();
    }

    init() {
        this.getInternshipIdFromUrl();
        if (this.internshipId) {
            this.loadInternship();
        } else {
            this.showError('No internship ID provided');
        }
    }

    getInternshipIdFromUrl() {
        const urlParams = new URLSearchParams(window.location.search);
        this.internshipId = urlParams.get('id');
    }

    async loadInternship() {
        this.showLoading();
        
        try {
            const response = await fetch(`http://localhost:5001/api/internships/${this.internshipId}`, {
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.originalData = data.internship;
                this.populateForm(data.internship);
                this.showEditForm();
                this.bindEvents();
            } else {
                this.showError(data.message || 'Failed to load internship');
            }
        } catch (error) {
            console.error('Error loading internship:', error);
            this.showError('Network error. Please check your connection.');
        }
    }

    populateForm(internship) {
        // Populate form fields
        document.getElementById('internship_id').value = internship.internship_id;
        document.getElementById('internship_title').value = internship.internship_title || '';
        document.getElementById('industry_domain').value = internship.industry_domain || '';
        document.getElementById('required_skills').value = internship.required_skills || '';
        document.getElementById('education_level').value = internship.education_level || '';
        document.getElementById('minimum_gpa').value = internship.minimum_gpa || '';
        document.getElementById('location_type').value = internship.location_type || '';
        document.getElementById('duration').value = internship.duration || '';
        document.getElementById('stipend').value = internship.stipend || '';
        document.getElementById('fulltime_conversion').checked = internship.fulltime_conversion || false;
        document.getElementById('description').value = internship.description || '';
        document.getElementById('past_intern_records').value = internship.past_intern_records || '';
    }

    bindEvents() {
        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleSubmit();
        });

        // Cancel button
        document.getElementById('cancelBtn').addEventListener('click', () => {
            this.handleCancel();
        });

        // Real-time validation
        const requiredFields = ['internship_title', 'industry_domain', 'location_type', 'education_level', 'duration'];
        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('blur', () => this.validateField(field));
                field.addEventListener('input', () => this.clearFieldError(field));
            }
        });

        // GPA validation
        const gpaField = document.getElementById('minimum_gpa');
        if (gpaField) {
            gpaField.addEventListener('input', () => this.validateGPA(gpaField));
        }
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.getAttribute('name') || field.id;
        
        // Clear previous error
        this.clearFieldError(field);
        
        // Check if required field is empty
        if (field.hasAttribute('required') && !value) {
            this.setFieldError(field, `${this.getFieldDisplayName(fieldName)} is required`);
            return false;
        }
        
        // Specific validations
        switch (fieldName) {
            case 'internship_title':
                if (value && value.length < 3) {
                    this.setFieldError(field, 'Internship title must be at least 3 characters');
                    return false;
                }
                break;
                
            case 'industry_domain':
                if (value && value.length < 2) {
                    this.setFieldError(field, 'Industry domain must be at least 2 characters');
                    return false;
                }
                break;
                
            case 'duration':
                if (value && value.length < 2) {
                    this.setFieldError(field, 'Duration must be specified');
                    return false;
                }
                break;
        }
        
        return true;
    }

    validateGPA(field) {
        const value = parseFloat(field.value);
        
        this.clearFieldError(field);
        
        if (field.value && (isNaN(value) || value < 0 || value > 10)) {
            this.setFieldError(field, 'GPA must be between 0.0 and 10.0');
            return false;
        }
        
        return true;
    }

    setFieldError(field, message) {
        field.classList.add('border-red-500', 'focus:ring-red-500');
        field.classList.remove('border-gray-300', 'focus:ring-primary');
        
        // Add error message below field
        let errorMsg = field.parentNode.querySelector('.error-message');
        if (!errorMsg) {
            errorMsg = document.createElement('p');
            errorMsg.className = 'error-message text-red-600 text-sm mt-1';
            field.parentNode.appendChild(errorMsg);
        }
        errorMsg.textContent = message;
    }

    clearFieldError(field) {
        field.classList.remove('border-red-500', 'focus:ring-red-500');
        field.classList.add('border-gray-300', 'focus:ring-primary');
        
        // Remove error message
        const errorMsg = field.parentNode.querySelector('.error-message');
        if (errorMsg) {
            errorMsg.remove();
        }
    }

    validateForm() {
        let isValid = true;
        const errors = [];
        
        // Get form data
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData.entries());
        
        // Required field validation
        const requiredFields = {
            'internship_title': 'Internship Title',
            'industry_domain': 'Industry Domain',
            'location_type': 'Location Type',
            'education_level': 'Education Level',
            'duration': 'Duration'
        };
        
        Object.entries(requiredFields).forEach(([field, displayName]) => {
            if (!data[field] || !data[field].trim()) {
                errors.push(`${displayName} is required`);
                isValid = false;
                
                const fieldElement = document.getElementById(field);
                if (fieldElement) {
                    this.setFieldError(fieldElement, `${displayName} is required`);
                }
            }
        });
        
        // GPA validation
        if (data.minimum_gpa) {
            const gpa = parseFloat(data.minimum_gpa);
            if (isNaN(gpa) || gpa < 0 || gpa > 10) {
                errors.push('Minimum GPA must be between 0.0 and 10.0');
                isValid = false;
                
                const gpaField = document.getElementById('minimum_gpa');
                if (gpaField) {
                    this.setFieldError(gpaField, 'GPA must be between 0.0 and 10.0');
                }
            }
        }
        
        // Length validations
        if (data.internship_title && data.internship_title.length < 3) {
            errors.push('Internship title must be at least 3 characters');
            isValid = false;
        }
        
        if (data.industry_domain && data.industry_domain.length < 2) {
            errors.push('Industry domain must be at least 2 characters');
            isValid = false;
        }
        
        // Show errors if any
        if (errors.length > 0) {
            this.showErrors(errors);
        } else {
            this.hideErrors();
        }
        
        return isValid;
    }

    async handleSubmit() {
        // Clear previous errors
        this.hideErrors();
        
        // Validate form
        if (!this.validateForm()) {
            return;
        }
        
        // Show loading state
        this.setLoading(true);
        
        try {
            // Collect form data
            const formData = new FormData(this.form);
            const data = {
                internship_title: formData.get('internship_title').trim(),
                industry_domain: formData.get('industry_domain').trim(),
                required_skills: formData.get('required_skills').trim(),
                education_level: formData.get('education_level'),
                minimum_gpa: formData.get('minimum_gpa') ? parseFloat(formData.get('minimum_gpa')) : null,
                location_type: formData.get('location_type'),
                duration: formData.get('duration').trim(),
                stipend: formData.get('stipend').trim(),
                fulltime_conversion: formData.has('fulltime_conversion'),
                description: formData.get('description').trim(),
                past_intern_records: formData.get('past_intern_records').trim()
            };
            
            // Send API request
            const response = await fetch(`http://localhost:5001/api/internships/${this.internshipId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message
                this.showSuccess();
                
                // Update original data
                this.originalData = result.internship;
                
                // Redirect after a delay
                setTimeout(() => {
                    window.location.href = 'internships_list.html';
                }, 2000);
                
            } else {
                // Handle validation errors from server
                if (result.errors && Array.isArray(result.errors)) {
                    this.showErrors(result.errors);
                } else {
                    this.showErrors([result.message || 'Failed to update internship']);
                }
            }
            
        } catch (error) {
            console.error('Error updating internship:', error);
            this.showErrors(['Network error. Please check your connection and try again.']);
        } finally {
            this.setLoading(false);
        }
    }

    handleCancel() {
        if (this.hasUnsavedChanges()) {
            if (confirm('You have unsaved changes. Are you sure you want to cancel?')) {
                this.goBack();
            }
        } else {
            this.goBack();
        }
    }

    hasUnsavedChanges() {
        if (!this.originalData) return false;
        
        const currentData = {
            internship_title: document.getElementById('internship_title').value.trim(),
            industry_domain: document.getElementById('industry_domain').value.trim(),
            required_skills: document.getElementById('required_skills').value.trim(),
            education_level: document.getElementById('education_level').value,
            minimum_gpa: document.getElementById('minimum_gpa').value ? parseFloat(document.getElementById('minimum_gpa').value) : null,
            location_type: document.getElementById('location_type').value,
            duration: document.getElementById('duration').value.trim(),
            stipend: document.getElementById('stipend').value.trim(),
            fulltime_conversion: document.getElementById('fulltime_conversion').checked,
            description: document.getElementById('description').value.trim(),
            past_intern_records: document.getElementById('past_intern_records').value.trim()
        };
        
        // Compare with original data
        const fieldsToCompare = Object.keys(currentData);
        return fieldsToCompare.some(field => {
            const currentValue = currentData[field];
            const originalValue = this.originalData[field];
            
            // Handle null/empty string comparison
            if ((currentValue === null || currentValue === '') && (originalValue === null || originalValue === '')) {
                return false;
            }
            
            return currentValue !== originalValue;
        });
    }

    goBack() {
        // Try to go back in history, or redirect to internships list
        if (document.referrer && document.referrer.includes(window.location.origin)) {
            window.history.back();
        } else {
            window.location.href = 'internships_list.html';
        }
    }

    showLoading() {
        this.loadingState.classList.remove('hidden');
        this.errorState.classList.add('hidden');
        this.editForm.classList.add('hidden');
    }

    showEditForm() {
        this.loadingState.classList.add('hidden');
        this.errorState.classList.add('hidden');
        this.editForm.classList.remove('hidden');
    }

    showError(message) {
        this.loadingState.classList.add('hidden');
        this.editForm.classList.add('hidden');
        this.errorState.classList.remove('hidden');
        document.getElementById('errorMessage').textContent = message;
    }

    setLoading(loading) {
        this.submitBtn.disabled = loading;
        
        if (loading) {
            this.submitText.textContent = 'Updating...';
            this.submitSpinner.classList.remove('hidden');
            this.submitBtn.classList.add('opacity-75');
        } else {
            this.submitText.textContent = 'Update Internship';
            this.submitSpinner.classList.add('hidden');
            this.submitBtn.classList.remove('opacity-75');
        }
    }

    showErrors(errors) {
        this.errorList.innerHTML = '';
        errors.forEach(error => {
            const li = document.createElement('li');
            li.textContent = error;
            this.errorList.appendChild(li);
        });
        this.errorContainer.classList.remove('hidden');
        
        // Scroll to top to show errors
        this.errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    hideErrors() {
        this.errorContainer.classList.add('hidden');
        this.errorList.innerHTML = '';
    }

    showSuccess() {
        const toast = document.getElementById('successToast');
        toast.classList.remove('hidden');
        
        setTimeout(() => {
            toast.classList.add('hidden');
        }, 5000);
    }

    getFieldDisplayName(fieldName) {
        const fieldNames = {
            'internship_title': 'Internship Title',
            'industry_domain': 'Industry Domain',
            'required_skills': 'Required Skills',
            'education_level': 'Education Level',
            'minimum_gpa': 'Minimum GPA',
            'location_type': 'Location Type',
            'duration': 'Duration',
            'stipend': 'Stipend',
            'fulltime_conversion': 'Full-time Conversion',
            'description': 'Description',
            'past_intern_records': 'Past Intern Records'
        };
        
        return fieldNames[fieldName] || fieldName.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
}

// Initialize when DOM loads
document.addEventListener('DOMContentLoaded', () => {
    new EditInternship();
});