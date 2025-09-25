// Company Dashboard JavaScript
const API_BASE_URL = 'http://localhost:5001/api/company';

let currentCompany = null;

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

// Check authentication and load company data
async function loadCompanyData() {
    try {
        const response = await fetch(`${API_BASE_URL}/profile`, {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentCompany = data.company;
            updateCompanyInfo();
            loadInternships();
        } else {
            window.location.href = '/company/login';
        }
    } catch (error) {
        console.error('Error loading company data:', error);
        window.location.href = '/company/login';
    }
}

// Update company information in the UI
function updateCompanyInfo() {
    if (!currentCompany) return;
    
    // Update navbar
    const companyName = document.getElementById('companyName');
    if (companyName) {
        companyName.textContent = `Welcome, ${currentCompany.company_name}!`;
    }
    
    // Update profile section
    const profileSection = document.getElementById('profileSection');
    if (profileSection) {
        profileSection.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <p><strong>Company Name:</strong> ${currentCompany.company_name}</p>
                    <p><strong>Email:</strong> ${currentCompany.company_email}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>Website:</strong> ${currentCompany.company_website ? `<a href="${currentCompany.company_website}" target="_blank">${currentCompany.company_website}</a>` : 'Not provided'}</p>
                    <p><strong>Total Internships:</strong> ${currentCompany.total_internships || 0}</p>
                </div>
            </div>
            ${currentCompany.company_description ? `
                <div class="row mt-2">
                    <div class="col-12">
                        <p><strong>Description:</strong></p>
                        <p class="text-muted">${currentCompany.company_description}</p>
                    </div>
                </div>
            ` : ''}
        `;
    }
}

// Load company internships
async function loadInternships() {
    const container = document.getElementById('internshipsContainer');
    
    try {
        const response = await fetch(`${API_BASE_URL}/internships`, {
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.internships.length === 0) {
                container.innerHTML = `
                    <div class="text-center py-4">
                        <h5 class="text-muted">No internships posted yet</h5>
                        <p class="text-muted">Start by creating your first internship posting!</p>
                        <a href="/company/add-internship" class="btn btn-primary">Add Your First Internship</a>
                    </div>
                `;
            } else {
                displayInternships(data.internships);
            }
        } else {
            container.innerHTML = `
                <div class="alert alert-warning" role="alert">
                    Failed to load internships: ${data.message}
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading internships:', error);
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                Error loading internships. Please refresh the page.
            </div>
        `;
    }
}

// Display internships in the UI
function displayInternships(internships) {
    const container = document.getElementById('internshipsContainer');
    
    const internshipsHtml = internships.map(internship => `
        <div class="card mb-3">
            <div class="card-body">
                <div class="row">
                    <div class="col-md-8">
                        <h5 class="card-title">${internship.internship_title}</h5>
                        <p class="card-text">
                            <span class="badge bg-primary me-2">${internship.industry_domain}</span>
                            <span class="badge bg-info me-2">${internship.location_type}</span>
                            <span class="badge bg-secondary me-2">${internship.duration}</span>
                            ${internship.stipend ? `<span class="badge bg-success">${internship.stipend}</span>` : ''}
                        </p>
                        <p class="card-text text-muted">
                            <strong>Education:</strong> ${internship.education_level} | 
                            <strong>Created:</strong> ${new Date(internship.created_at).toLocaleDateString()}
                            ${!internship.is_active ? ' | <span class="text-danger">Inactive</span>' : ''}
                        </p>
                    </div>
                    <div class="col-md-4 text-md-end">
                        <div class="btn-group" role="group">
                            <button class="btn btn-outline-primary btn-sm" onclick="viewInternship(${internship.internship_id})">
                                View
                            </button>
                            <button class="btn btn-outline-secondary btn-sm" onclick="editInternship(${internship.internship_id})">
                                Edit
                            </button>
                            <button class="btn btn-outline-danger btn-sm" onclick="deleteInternship(${internship.internship_id})">
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = internshipsHtml;
}

// View internship details
function viewInternship(internshipId) {
    // You can implement a modal or redirect to a detail page
    console.log('View internship:', internshipId);
}

// Edit internship
function editInternship(internshipId) {
    window.location.href = `/company/edit-internship?id=${internshipId}`;
}

// Delete internship
async function deleteInternship(internshipId) {
    if (!confirm('Are you sure you want to delete this internship? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/internships/${internshipId}`, {
            method: 'DELETE',
            credentials: 'include'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('Internship deleted successfully!', 'success');
            loadInternships(); // Reload the list
        } else {
            showAlert(data.message || 'Failed to delete internship');
        }
    } catch (error) {
        console.error('Error deleting internship:', error);
        showAlert('Error deleting internship. Please try again.');
    }
}

// Edit profile modal
document.addEventListener('DOMContentLoaded', function() {
    const editProfileBtn = document.getElementById('editProfileBtn');
    const saveProfileBtn = document.getElementById('saveProfileBtn');
    const editProfileModal = new bootstrap.Modal(document.getElementById('editProfileModal'));
    
    // Open edit profile modal
    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function() {
            if (currentCompany) {
                document.getElementById('edit_company_name').value = currentCompany.company_name;
                document.getElementById('edit_company_website').value = currentCompany.company_website || '';
                document.getElementById('edit_company_description').value = currentCompany.company_description || '';
                editProfileModal.show();
            }
        });
    }
    
    // Save profile changes
    if (saveProfileBtn) {
        saveProfileBtn.addEventListener('click', async function() {
            const updateData = {
                company_name: document.getElementById('edit_company_name').value,
                company_website: document.getElementById('edit_company_website').value,
                company_description: document.getElementById('edit_company_description').value
            };
            
            try {
                const response = await fetch(`${API_BASE_URL}/profile`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                    body: JSON.stringify(updateData)
                });
                
                const data = await response.json();
                
                if (data.success) {
                    currentCompany = data.company;
                    updateCompanyInfo();
                    editProfileModal.hide();
                    showAlert('Profile updated successfully!', 'success');
                } else {
                    showAlert(data.message || 'Failed to update profile');
                }
            } catch (error) {
                console.error('Error updating profile:', error);
                showAlert('Error updating profile. Please try again.');
            }
        });
    }
    
    // Logout functionality
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
    
    // Load company data on page load
    loadCompanyData();
});