// Add Internship JavaScript
class AddInternship {
    constructor() {
        this.form = document.getElementById('addInternshipForm');
        this.submitBtn = document.getElementById('submitBtn');
        this.submitText = document.getElementById('submitText');
        this.submitSpinner = document.getElementById('submitSpinner');
        this.errorContainer = document.getElementById('errorContainer');
        this.errorList = document.getElementById('errorList');
        
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupValidation();
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

    setupValidation() {
        // Add validation styling for required fields
        const requiredFields = document.querySelectorAll('input[required], select[required]');
        requiredFields.forEach(field => {
            const label = document.querySelector(`label[for="${field.id}"]`);
            if (label && !label.querySelector('.text-red-500')) {
                label.innerHTML = label.innerHTML; // Ensure asterisk is visible
            }
        });
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
            const response = await fetch('http://localhost:5001/api/internships', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(data)
            });
            
            // Check if response is ok
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Try to parse JSON response
            let result;
            try {
                result = await response.json();
            } catch (parseError) {
                console.error('Failed to parse response as JSON:', parseError);
                throw new Error('Invalid response from server. Please try again.');
            }
            
            if (result.success) {
                // Show success message
                this.showSuccess();
                
                // Reset form after a delay
                setTimeout(() => {
                    this.resetForm();
                    // Optionally redirect to internships list
                    // window.location.href = 'internships_list.html';
                }, 2000);
                
            } else {
                // Handle validation errors from server
                if (result.errors && Array.isArray(result.errors)) {
                    this.showErrors(result.errors);
                } else {
                    this.showErrors([result.message || 'Failed to create internship']);
                }
            }
            
        } catch (error) {
            console.error('Error creating internship:', error);
            this.showErrors(['Network error. Please check your connection and try again.']);
        } finally {
            this.setLoading(false);
        }
    }

    handleCancel() {
        if (this.isFormDirty()) {
            if (confirm('You have unsaved changes. Are you sure you want to cancel?')) {
                this.goBack();
            }
        } else {
            this.goBack();
        }
    }

    goBack() {
        // Try to go back in history, or redirect to internships list
        if (document.referrer && document.referrer.includes(window.location.origin)) {
            window.history.back();
        } else {
            window.location.href = 'internships_list.html';
        }
    }

    isFormDirty() {
        const formData = new FormData(this.form);
        for (let [key, value] of formData.entries()) {
            if (value && value.trim()) {
                return true;
            }
        }
        return false;
    }

    resetForm() {
        this.form.reset();
        this.hideErrors();
        
        // Clear all field errors
        const errorMessages = document.querySelectorAll('.error-message');
        errorMessages.forEach(msg => msg.remove());
        
        // Reset field styling
        const fields = this.form.querySelectorAll('input, select, textarea');
        fields.forEach(field => {
            field.classList.remove('border-red-500', 'focus:ring-red-500');
            field.classList.add('border-gray-300', 'focus:ring-primary');
        });
    }

    setLoading(loading) {
        this.submitBtn.disabled = loading;
        
        if (loading) {
            this.submitText.textContent = 'Creating...';
            this.submitSpinner.classList.remove('hidden');
            this.submitBtn.classList.add('opacity-75');
        } else {
            this.submitText.textContent = 'Add Internship';
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
    new AddInternship();
});