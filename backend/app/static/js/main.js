// Main JavaScript file for Flask MySQL Login System

// Common utility functions
function showMessage(message, type = 'success') {
    // Create a Bootstrap alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main content
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv && alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function showError(message) {
    showMessage(message, 'danger');
}

function showSuccess(message) {
    showMessage(message, 'success');
}

// Form validation utilities
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validatePassword(password) {
    // At least 6 characters
    return password.length >= 6;
}

function validateUsername(username) {
    // At least 3 characters, alphanumeric and underscore only
    const usernameRegex = /^[a-zA-Z0-9_]{3,}$/;
    return usernameRegex.test(username);
}

// Loading state management
function setFormLoading(form, isLoading) {
    const submitBtn = form.querySelector('button[type="submit"]');
    const inputs = form.querySelectorAll('input');
    
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        inputs.forEach(input => input.disabled = true);
    } else {
        submitBtn.disabled = false;
        submitBtn.innerHTML = submitBtn.dataset.originalText || 'Submit';
        inputs.forEach(input => input.disabled = false);
    }
}

// Initialize common functionality when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Store original button text for loading states
    document.querySelectorAll('button[type="submit"]').forEach(btn => {
        btn.dataset.originalText = btn.innerHTML;
    });
    
    // Auto-dismiss flash messages after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            if (alert.classList.contains('show')) {
                alert.remove();
            }
        });
    }, 5000);
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Export functions for use in other modules
window.AppUtils = {
    showMessage,
    showError,
    showSuccess,
    validateEmail,
    validatePassword,
    validateUsername,
    setFormLoading
};