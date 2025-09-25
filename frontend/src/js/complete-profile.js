// Complete Profile page JavaScript
class CompleteProfilePage {
    constructor() {
        this.user = null;
        this.uploadedFiles = [];
        this.isEditMode = false; // Track if we're editing an existing profile
        this.init();
    }

    async init() {
        try {
            console.log('=== COMPLETE PROFILE PAGE INIT START ===');
            
            // Show loading state
            this.showLoading();

            // Check if user is logged in
            await this.checkAuthStatus();

            if (!this.user) {
                // Redirect to login if not authenticated
                console.log('No user found, redirecting to auth.html');
                window.location.href = 'auth.html#login';
                return;
            }

            console.log('User authenticated, initializing complete profile page');

            // Hide loading and show content
            this.hideLoading();

            // Set up event listeners
            this.setupEventListeners();
            
            // Display user info
            this.displayUserInfo();
            
            // Try to load existing profile
            await this.loadExistingProfile();
            
            console.log('=== COMPLETE PROFILE PAGE INIT COMPLETE ===');

        } catch (error) {
            console.error('Error initializing complete profile page:', error);
            this.hideLoading();
            this.showError('Failed to load page. Please try again.');
        }
    }

    async checkAuthStatus() {
        try {
            console.log('Checking authentication status...');
            // Use dynamic backend URL based on current host
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            const backendUrl = `http://${backendHost}:5001/api/check-auth`;
            console.log('Auth check URL:', backendUrl);
            
            const response = await fetch(backendUrl, {
                method: 'GET',
                credentials: 'include'
            });

            console.log('Auth check response status:', response.status);
            const data = await response.json();
            console.log('Auth check response data:', data);

            if (data.authenticated && data.user) {
                this.user = data.user;
                console.log('User authenticated:', this.user);
            } else {
                this.user = null;
                console.log('User not authenticated');
            }
        } catch (error) {
            console.error('Auth check failed:', error);
            this.user = null;
        }
    }

    async loadExistingProfile() {
        try {
            console.log('Loading existing profile...');
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            const backendUrl = `http://${backendHost}:5001/api/complete-profile`;
            console.log('Fetching from:', backendUrl);
            
            const response = await fetch(backendUrl, {
                method: 'GET',
                credentials: 'include'
            });

            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('Load profile response:', data);

            if (response.ok && data.success && data.profile) {
                console.log('Found existing profile, entering edit mode');
                console.log('Profile data:', data.profile);
                
                this.populateForm(data.profile);
                this.isEditMode = true;
                this.updateFormForEditMode();
                
                console.log('Edit mode setup complete');
            } else if (response.status === 404) {
                console.log('No existing profile found - staying in create mode');
                this.isEditMode = false;
            } else {
                console.log('Unexpected response:', data);
                this.isEditMode = false;
            }
        } catch (error) {
            console.error('Error loading existing profile:', error);
            this.isEditMode = false;
        }
    }

    updateFormForEditMode() {
        console.log('Updating form for edit mode...');
        
        // Update page title in header
        const headerTitle = document.querySelector('h1');
        if (headerTitle) {
            headerTitle.textContent = 'Edit Your Profile';
        }
        
        // Update form title
        const title = document.querySelector('h2');
        if (title) {
            title.textContent = 'Edit Complete Profile';
            console.log('Updated form title to edit mode');
        } else {
            console.error('Could not find h2 element for title');
        }

        // Update submit button text
        const submitButton = document.getElementById('submit-btn');
        if (submitButton) {
            submitButton.textContent = 'Update Profile';
            console.log('Updated submit button text to edit mode');
        } else {
            console.error('Could not find submit button');
        }
    }

    populateForm(profile) {
        try {
            console.log('Populating form with profile data:', profile);
            
            // Personal Information
            console.log('Setting personal information...');
            this.setFieldValue('aadhar_id', profile.aadhar_id);
            this.setFieldValue('name', profile.name);
            this.setFieldValue('dob', profile.dob);
            this.setFieldValue('state', profile.state);
            this.setFieldValue('city', profile.city);
            this.setFieldValue('pincode', profile.pincode);

            // Education
            console.log('Setting education information...');
            this.setFieldValue('education_level', profile.education_level);
            this.setFieldValue('degree', profile.degree);
            this.setFieldValue('year_of_study', profile.year_of_study);
            this.setFieldValue('gpa_percentage', profile.gpa_percentage);

            // Skills and Courses
            console.log('Setting skills and courses...');
            this.setFieldValue('relevant_courses', profile.relevant_courses);
            this.setFieldValue('technical_skills', profile.technical_skills);
            this.setFieldValue('soft_skills', profile.soft_skills);

            // Experience
            console.log('Setting experience information...');
            this.setFieldValue('previous_internships', profile.previous_internships);
            this.setFieldValue('projects', profile.projects);
            this.setFieldValue('hackathons_competitions', profile.hackathons_competitions);
            this.setFieldValue('research_experience', profile.research_experience);

            // Preferences
            console.log('Setting preferences...');
            this.setFieldValue('internship_type_preference', profile.internship_type_preference);
            this.setFieldValue('duration_preference', profile.duration_preference);
            this.setFieldValue('stipend_expectation', profile.stipend_expectation);
            this.setFieldValue('preferred_industry', profile.preferred_industry);

            // Handle certifications
            if (profile.certifications) {
                try {
                    const certs = JSON.parse(profile.certifications);
                    if (certs.length > 0) {
                        console.log('Displaying existing certifications:', certs);
                        this.displayExistingCertifications(certs);
                    }
                } catch (e) {
                    console.error('Error parsing certifications:', e);
                }
            }

            console.log('Form population completed successfully');

        } catch (error) {
            console.error('Error populating form:', error);
        }
    }

    setFieldValue(fieldName, value) {
        if (value === null || value === undefined || value === '') {
            console.log(`Skipping empty value for field: ${fieldName}`);
            return;
        }
        
        // Try to find the field by id first
        let field = document.getElementById(fieldName);
        
        // If not found by id, try to find by name attribute
        if (!field) {
            field = document.querySelector(`[name="${fieldName}"]`);
        }
        
        // If still not found, try input/select/textarea with the name
        if (!field) {
            field = document.querySelector(`input[name="${fieldName}"], select[name="${fieldName}"], textarea[name="${fieldName}"]`);
        }
        
        if (field) {
            field.value = value;
            console.log(`Set ${fieldName} = ${value}`);
            
            // Trigger change event to ensure any listeners are notified
            field.dispatchEvent(new Event('change', { bubbles: true }));
        } else {
            console.error(`Could not find field: ${fieldName}`);
        }
    }

    displayExistingCertifications(certifications) {
        const uploadedFilesDiv = document.getElementById('uploaded-files');
        const fileListDiv = document.getElementById('file-list');
        
        if (uploadedFilesDiv && fileListDiv) {
            uploadedFilesDiv.classList.remove('hidden');
            fileListDiv.innerHTML = '';
            
            certifications.forEach((certPath, index) => {
                const fileName = certPath.split('/').pop();
                const fileDiv = document.createElement('div');
                fileDiv.className = 'flex items-center justify-between bg-gray-50 px-3 py-2 rounded-md';
                fileDiv.innerHTML = `
                    <span class="text-sm text-gray-700">${fileName}</span>
                    <span class="text-xs text-gray-500">Existing file</span>
                `;
                fileListDiv.appendChild(fileDiv);
            });
        }
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('complete-profile-form');
        if (form) {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        }

        // File upload handling
        const fileInput = document.getElementById('certifications');
        if (fileInput) {
            fileInput.addEventListener('change', this.handleFileSelection.bind(this));
        }

        // Drag and drop for file upload
        const dropZone = fileInput?.closest('.border-dashed');
        if (dropZone) {
            dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
            dropZone.addEventListener('drop', this.handleFileDrop.bind(this));
        }
    }

    handleFileSelection(event) {
        const files = Array.from(event.target.files);
        this.displaySelectedFiles(files);
    }

    handleDragOver(event) {
        event.preventDefault();
        event.currentTarget.classList.add('border-primary', 'bg-blue-50');
    }

    handleFileDrop(event) {
        event.preventDefault();
        event.currentTarget.classList.remove('border-primary', 'bg-blue-50');
        
        const files = Array.from(event.dataTransfer.files);
        const fileInput = document.getElementById('certifications');
        
        // Update the file input
        const dt = new DataTransfer();
        files.forEach(file => dt.items.add(file));
        fileInput.files = dt.files;
        
        this.displaySelectedFiles(files);
    }

    displaySelectedFiles(files) {
        const uploadedFilesDiv = document.getElementById('uploaded-files');
        const fileListDiv = document.getElementById('file-list');
        
        if (files.length > 0) {
            uploadedFilesDiv.classList.remove('hidden');
            fileListDiv.innerHTML = '';
            
            files.forEach((file, index) => {
                const fileDiv = document.createElement('div');
                fileDiv.className = 'flex items-center justify-between bg-gray-50 px-3 py-2 rounded-md';
                fileDiv.innerHTML = `
                    <span class="text-sm text-gray-700">${file.name}</span>
                    <button type="button" onclick="this.parentElement.remove()" class="text-red-500 hover:text-red-700">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                `;
                fileListDiv.appendChild(fileDiv);
            });
        } else {
            uploadedFilesDiv.classList.add('hidden');
        }
    }

    async handleFormSubmit(event) {
        event.preventDefault();
        
        console.log('Form submission started. Edit mode:', this.isEditMode);
        
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = this.isEditMode ? 'Updating...' : 'Saving...';
        
        try {
            console.log('Submitting complete profile form...');
            
            const form = event.target;
            const formData = new FormData(form);
            
            // Handle file uploads first if there are any
            const fileInput = document.getElementById('certifications');
            let certificationsData = '';
            
            if (fileInput && fileInput.files && fileInput.files.length > 0) {
                console.log('Processing certificate files...');
                certificationsData = await this.handleCertificationUploads(fileInput.files);
            }
            
            // Convert FormData to JSON object (excluding files)
            const profileData = {};
            for (let [key, value] of formData.entries()) {
                // Skip file inputs, handle them separately
                if (key !== 'certifications') {
                    profileData[key] = value;
                }
            }
            
            // Add processed certifications data
            if (certificationsData) {
                profileData.certifications = certificationsData;
            }
            
            // Log form data for debugging
            console.log('Profile data being submitted:', profileData);
            
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            const backendUrl = `http://${backendHost}:5001/api/complete-profile`;
            const method = this.isEditMode ? 'PUT' : 'POST';
            console.log(`Submitting to: ${backendUrl} with method: ${method}`);
            
            const response = await fetch(backendUrl, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(profileData)
            });
            
            console.log('Response status:', response.status);
            const data = await response.json();
            console.log('Response data:', data);
            
            if (response.ok && data.success) {
                const message = `Profile ${this.isEditMode ? 'updated' : 'created'} successfully!`;
                console.log(message);
                this.showSuccess(message);
                
                // If we were in create mode and successfully created, switch to edit mode
                if (!this.isEditMode) {
                    this.isEditMode = true;
                    this.updateFormForEditMode();
                }
                
                // Redirect to home page after a short delay
                setTimeout(() => {
                    window.location.href = 'home.html';
                }, 2000);
            } else {
                const errorMessage = data.message || `Failed to ${this.isEditMode ? 'update' : 'save'} profile. Please try again.`;
                console.error('Server error:', errorMessage);
                this.showError(errorMessage);
            }
            
        } catch (error) {
            console.error('Error submitting form:', error);
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = this.isEditMode ? 'Update Profile' : 'Save Profile';
        }
    }

    displayUserInfo() {
        if (this.user) {
            const welcomeSpan = document.getElementById('user-welcome');
            const usernameSpan = document.getElementById('username');
            
            if (welcomeSpan && usernameSpan) {
                usernameSpan.textContent = this.user.username;
                welcomeSpan.classList.remove('hidden');
            }
        }
    }

    showLoading() {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.remove('hidden');
        }
    }

    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.add('hidden');
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    async handleCertificationUploads(files) {
        console.log('Uploading certification files:', files.length);
        
        try {
            const uploadPromises = [];
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                console.log(`Uploading file ${i + 1}: ${file.name}`);
                
                const formData = new FormData();
                formData.append('certification', file);
                
                const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
                const uploadUrl = `http://${backendHost}:5001/api/upload-certification`;
                
                const uploadPromise = fetch(uploadUrl, {
                    method: 'POST',
                    credentials: 'include',
                    body: formData
                }).then(response => response.json());
                
                uploadPromises.push(uploadPromise);
            }
            
            const uploadResults = await Promise.all(uploadPromises);
            const uploadedPaths = uploadResults
                .filter(result => result.success)
                .map(result => result.file_path);
            
            console.log('Upload results:', uploadResults);
            
            // Check for automatic processing results
            const processedFiles = uploadResults.filter(result => 
                result.processing_result && result.processing_result.success
            );
            
            if (processedFiles.length > 0) {
                this.showProcessingSuccess(`${processedFiles.length} document(s) uploaded and automatically analyzed with AI!`);
            } else {
                const deferredFiles = uploadResults.filter(result => 
                    result.processing_status === 'deferred'
                );
                if (deferredFiles.length > 0) {
                    this.showInfo(`${deferredFiles.length} document(s) uploaded. AI analysis will be performed automatically.`);
                }
            }
            
            // Return as JSON string for storage
            return JSON.stringify(uploadedPaths);
            
        } catch (error) {
            console.error('Error uploading certifications:', error);
            throw new Error('Failed to upload certification files');
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 z-50 p-4 rounded-md shadow-lg max-w-sm ${
            type === 'success' ? 'bg-green-500 text-white' : 
            type === 'error' ? 'bg-red-500 text-white' : 
            'bg-blue-500 text-white'
        }`;
        
        notification.innerHTML = `
            <div class="flex items-center">
                <span class="flex-1">${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-200">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    showProcessingSuccess(message) {
        this.showNotification(message, 'success');
    }

    showInfo(message) {
        this.showNotification(message, 'info');
    }
}

// Initialize the complete profile page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing CompleteProfilePage...');
    window.completeProfilePage = new CompleteProfilePage();
});