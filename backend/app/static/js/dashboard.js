// Dashboard JavaScript for Flask MySQL Login System

document.addEventListener('DOMContentLoaded', function() {
    // Profile update functionality
    const profileForm = document.getElementById('profileForm');
    const changePasswordForm = document.getElementById('changePasswordForm');
    
    // Profile update handler
    if (profileForm) {
        profileForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const username = formData.get('username');
            
            // Basic validation
            if (!username) {
                AppUtils.showError('Username is required');
                return;
            }
            
            if (!AppUtils.validateUsername(username)) {
                AppUtils.showError('Username must be at least 3 characters and contain only letters, numbers, and underscores');
                return;
            }
            
            try {
                AppUtils.setFormLoading(this, true);
                
                const response = await fetch('/dashboard/profile', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        username: username
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    AppUtils.showSuccess(data.message);
                    // Update the displayed username in the navbar if it exists
                    const navUsername = document.querySelector('.navbar .username');
                    if (navUsername) {
                        navUsername.textContent = username;
                    }
                } else {
                    AppUtils.showError(data.message || 'Profile update failed');
                }
                
            } catch (error) {
                console.error('Profile update error:', error);
                AppUtils.showError('An error occurred while updating profile. Please try again.');
            } finally {
                AppUtils.setFormLoading(this, false);
            }
        });
    }
    
    // Change password handler
    if (changePasswordForm) {
        changePasswordForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const currentPassword = formData.get('current_password');
            const newPassword = formData.get('new_password');
            const confirmPassword = formData.get('confirm_password');
            
            // Validation
            if (!currentPassword || !newPassword || !confirmPassword) {
                AppUtils.showError('Please fill in all fields');
                return;
            }
            
            if (!AppUtils.validatePassword(newPassword)) {
                AppUtils.showError('New password must be at least 6 characters long');
                return;
            }
            
            if (newPassword !== confirmPassword) {
                AppUtils.showError('New passwords do not match');
                return;
            }
            
            if (currentPassword === newPassword) {
                AppUtils.showError('New password must be different from current password');
                return;
            }
            
            try {
                AppUtils.setFormLoading(this, true);
                
                const response = await fetch('/dashboard/change-password', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: JSON.stringify({
                        current_password: currentPassword,
                        new_password: newPassword
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    AppUtils.showSuccess(data.message);
                    // Clear the form
                    this.reset();
                } else {
                    AppUtils.showError(data.message || 'Password change failed');
                }
                
            } catch (error) {
                console.error('Password change error:', error);
                AppUtils.showError('An error occurred while changing password. Please try again.');
            } finally {
                AppUtils.setFormLoading(this, false);
            }
        });
    }
    
    // Logout confirmation
    const logoutLinks = document.querySelectorAll('a[href="/logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('Are you sure you want to logout?')) {
                window.location.href = '/logout';
            }
        });
    });
    
    // Auto-refresh user statistics if present
    const refreshStatsBtn = document.getElementById('refreshStats');
    if (refreshStatsBtn) {
        refreshStatsBtn.addEventListener('click', async function() {
            try {
                this.disabled = true;
                this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Refreshing...';
                
                const response = await fetch('/dashboard/stats', {
                    method: 'GET',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Update stats on the page
                    if (data.stats) {
                        Object.keys(data.stats).forEach(key => {
                            const element = document.getElementById(`stat-${key}`);
                            if (element) {
                                element.textContent = data.stats[key];
                            }
                        });
                    }
                    AppUtils.showSuccess('Statistics refreshed successfully');
                } else {
                    AppUtils.showError('Failed to refresh statistics');
                }
                
            } catch (error) {
                console.error('Stats refresh error:', error);
                AppUtils.showError('An error occurred while refreshing statistics.');
            } finally {
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Refresh Stats';
            }
        });
    }
    
    // Dark mode toggle (if implemented)
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
            darkModeToggle.checked = savedTheme === 'dark';
        }
        
        darkModeToggle.addEventListener('change', function() {
            const theme = this.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        });
    }
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});