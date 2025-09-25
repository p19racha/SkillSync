// Company Authentication JavaScript
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
    
    // Auto-dismiss success alerts after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            const alert = alertContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }
}

function setButtonLoading(buttonId, isLoading) {
    const button = document.getElementById(buttonId);
    const text = document.getElementById(buttonId.replace('Btn', 'BtnText'));
    const spinner = document.getElementById(buttonId.replace('Btn', 'Spinner'));
    
    if (isLoading) {
        button.disabled = true;
        text.style.display = 'none';
        spinner.classList.remove('d-none');
    } else {
        button.disabled = false;
        text.style.display = 'inline';
        spinner.classList.add('d-none');
    }
}

// Check if company is logged in
function checkCompanyAuth() {
    return fetch(`${API_BASE_URL}/profile`, {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            return data.company;
        }
        throw new Error('Not authenticated');
    });
}

// Redirect to login if not authenticated
function requireAuth() {
    checkCompanyAuth().catch(() => {
        window.location.href = '/company/login';
    });
}

// Company Login
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        setButtonLoading('loginBtn', true);
        
        const formData = new FormData(this);
        const loginData = {
            company_email: formData.get('company_email'),
            password: formData.get('password')
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(loginData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/company/dashboard';
                }, 1500);
            } else {
                showAlert(data.message || 'Login failed');
            }
        } catch (error) {
            showAlert('Network error. Please try again.');
        } finally {
            setButtonLoading('loginBtn', false);
        }
    });
}

// Company Registration
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        setButtonLoading('registerBtn', true);
        
        const formData = new FormData(this);
        const password = formData.get('password');
        const confirmPassword = formData.get('confirm_password');
        
        // Validate passwords match
        if (password !== confirmPassword) {
            showAlert('Passwords do not match');
            setButtonLoading('registerBtn', false);
            return;
        }
        
        const registerData = {
            company_name: formData.get('company_name'),
            company_email: formData.get('company_email'),
            company_website: formData.get('company_website'),
            company_description: formData.get('company_description'),
            password: password
        };
        
        try {
            const response = await fetch(`${API_BASE_URL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(registerData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('Registration successful! Please login.', 'success');
                setTimeout(() => {
                    window.location.href = '/company/login';
                }, 2000);
            } else {
                showAlert(data.message || 'Registration failed');
            }
        } catch (error) {
            showAlert('Network error. Please try again.');
        } finally {
            setButtonLoading('registerBtn', false);
        }
    });
}

// Logout functionality
document.addEventListener('DOMContentLoaded', function() {
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