// Authentication JavaScript for Flask MySQL Login System

document.addEventListener('DOMContentLoaded', function() {
    // Get forms
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    // Login form handler
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const username = formData.get('username');
            const password = formData.get('password');
            
            // Basic validation
            if (!username || !password) {
                AppUtils.showError('Please fill in all fields');
                return;
            }
            
            try {
                AppUtils.setFormLoading(this, true);
                
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    AppUtils.showSuccess(data.message);
                    // Redirect to dashboard after short delay
                    setTimeout(() => {
                        window.location.href = data.redirect_url || '/dashboard';
                    }, 1000);
                } else {
                    AppUtils.showError(data.message || 'Login failed');
                }
                
            } catch (error) {
                console.error('Login error:', error);
                AppUtils.showError('An error occurred during login. Please try again.');
            } finally {
                AppUtils.setFormLoading(this, false);
            }
        });
    }
    
    // Register form handler
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const username = formData.get('username');
            const password = formData.get('password');
            const confirmPassword = formData.get('confirm_password');
            
            // Validation
            if (!username || !password || !confirmPassword) {
                AppUtils.showError('Please fill in all fields');
                return;
            }
            
            if (!AppUtils.validateUsername(username)) {
                AppUtils.showError('Username must be at least 3 characters and contain only letters, numbers, and underscores');
                return;
            }
            
            if (!AppUtils.validatePassword(password)) {
                AppUtils.showError('Password must be at least 6 characters long');
                return;
            }
            
            if (password !== confirmPassword) {
                AppUtils.showError('Passwords do not match');
                return;
            }
            
            try {
                AppUtils.setFormLoading(this, true);
                
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    AppUtils.showSuccess(data.message);
                    // Redirect to login after short delay
                    setTimeout(() => {
                        window.location.href = data.redirect_url || '/login';
                    }, 1500);
                } else {
                    AppUtils.showError(data.message || 'Registration failed');
                }
                
            } catch (error) {
                console.error('Registration error:', error);
                AppUtils.showError('An error occurred during registration. Please try again.');
            } finally {
                AppUtils.setFormLoading(this, false);
            }
        });
    }
    
    // Real-time validation for registration form
    if (registerForm) {
        const usernameInput = registerForm.querySelector('input[name="username"]');
        const passwordInput = registerForm.querySelector('input[name="password"]');
        const confirmPasswordInput = registerForm.querySelector('input[name="confirm_password"]');
        
        // Username validation
        if (usernameInput) {
            usernameInput.addEventListener('blur', function() {
                const feedback = this.parentNode.querySelector('.invalid-feedback') || 
                               this.parentNode.querySelector('.valid-feedback');
                
                if (this.value && !AppUtils.validateUsername(this.value)) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                    if (!feedback) {
                        const feedbackDiv = document.createElement('div');
                        feedbackDiv.className = 'invalid-feedback';
                        feedbackDiv.textContent = 'Username must be at least 3 characters and contain only letters, numbers, and underscores';
                        this.parentNode.appendChild(feedbackDiv);
                    }
                } else if (this.value) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                    if (feedback) feedback.remove();
                }
            });
        }
        
        // Password validation
        if (passwordInput) {
            passwordInput.addEventListener('blur', function() {
                const feedback = this.parentNode.querySelector('.invalid-feedback') || 
                               this.parentNode.querySelector('.valid-feedback');
                
                if (this.value && !AppUtils.validatePassword(this.value)) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                    if (!feedback) {
                        const feedbackDiv = document.createElement('div');
                        feedbackDiv.className = 'invalid-feedback';
                        feedbackDiv.textContent = 'Password must be at least 6 characters long';
                        this.parentNode.appendChild(feedbackDiv);
                    }
                } else if (this.value) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                    if (feedback) feedback.remove();
                }
            });
        }
        
        // Confirm password validation
        if (confirmPasswordInput && passwordInput) {
            confirmPasswordInput.addEventListener('blur', function() {
                const feedback = this.parentNode.querySelector('.invalid-feedback') || 
                               this.parentNode.querySelector('.valid-feedback');
                
                if (this.value && this.value !== passwordInput.value) {
                    this.classList.add('is-invalid');
                    this.classList.remove('is-valid');
                    if (!feedback) {
                        const feedbackDiv = document.createElement('div');
                        feedbackDiv.className = 'invalid-feedback';
                        feedbackDiv.textContent = 'Passwords do not match';
                        this.parentNode.appendChild(feedbackDiv);
                    }
                } else if (this.value) {
                    this.classList.add('is-valid');
                    this.classList.remove('is-invalid');
                    if (feedback) feedback.remove();
                }
            });
        }
    }
    
    // Show/hide password functionality
    document.querySelectorAll('.password-toggle').forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.parentNode.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });
});