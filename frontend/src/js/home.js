// Home page JavaScript
class HomePage {
    constructor() {
        this.user = null;
        this.recommendations = [];
        // Don't auto-initialize, let the script tag call init()
    }

    async init() {
        try {
            console.log('=== HOME PAGE INIT START ===');
            console.log('Current URL:', window.location.href);
            
            // Show loading state
            this.showLoading();

            // Check if user is logged in
            console.log('About to check auth status...');
            await this.checkAuthStatus();
            console.log('Auth check completed. User:', this.user);

            if (!this.user) {
                // Redirect to login if not authenticated
                console.log('No user found, redirecting to auth.html');
                console.log('Current location before redirect:', window.location.href);
                window.location.href = 'auth.html#login';
                return;
            }

            console.log('User is authenticated, showing home page content');
            console.log('User data:', this.user);

            // Hide loading and show content
            this.hideLoading();

            // Initialize page content
            this.setupEventListeners();
            this.displayUserInfo();
            this.checkProfileCompletion();
            
            console.log('=== HOME PAGE INIT COMPLETE ===');

        } catch (error) {
            console.error('Error initializing home page:', error);
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

    setupEventListeners() {
        // Profile button dropdown toggle
        const profileBtn = document.getElementById('profile-btn');
        const profileDropdown = document.getElementById('profile-dropdown');

        if (profileBtn && profileDropdown) {
            profileBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                profileDropdown.classList.toggle('hidden');
            });

            // Close dropdown when clicking outside
            document.addEventListener('click', () => {
                profileDropdown.classList.add('hidden');
            });
        }

        // Mobile menu toggle
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        const mobileMenu = document.getElementById('mobile-menu');

        if (mobileMenuBtn && mobileMenu) {
            mobileMenuBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                mobileMenu.classList.toggle('hidden');
                
                // Toggle hamburger icon
                const icon = mobileMenuBtn.querySelector('i');
                if (mobileMenu.classList.contains('hidden')) {
                    icon.className = 'fas fa-bars text-xl';
                } else {
                    icon.className = 'fas fa-times text-xl';
                }
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                const icon = mobileMenuBtn.querySelector('i');
                icon.className = 'fas fa-bars text-xl';
            });

            // Close mobile menu when window is resized to desktop size
            window.addEventListener('resize', () => {
                if (window.innerWidth >= 768) { // md breakpoint
                    mobileMenu.classList.add('hidden');
                    const icon = mobileMenuBtn.querySelector('i');
                    icon.className = 'fas fa-bars text-xl';
                }
            });
        }

        // Logout button
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', this.handleLogout.bind(this));
        }

        // Complete profile button
        const completeProfileBtn = document.getElementById('complete-profile-btn');
        if (completeProfileBtn) {
            completeProfileBtn.addEventListener('click', this.handleCompleteProfile.bind(this));
        }

        // Refresh recommendations button
        const refreshBtn = document.getElementById('refresh-recommendations');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshRecommendations());
        }


    }

    displayUserInfo() {
        const usernameElement = document.getElementById('username');
        const userWelcome = document.getElementById('user-welcome');

        if (this.user && usernameElement && userWelcome) {
            usernameElement.textContent = this.user.username;
            userWelcome.classList.remove('hidden');
        }
    }

    async checkProfileCompletion() {
        try {
            console.log('Checking profile completion...');
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            const backendUrl = `http://${backendHost}:5001/api/complete-profile`;
            
            const response = await fetch(backendUrl, {
                method: 'GET',
                credentials: 'include'
            });

            console.log('Profile check response status:', response.status);
            
            if (response.ok) {
                const data = await response.json();
                console.log('Profile check response data:', data);
                
                const completionPercentage = data.completion_percentage || 0;
                const isProfileComplete = data.profile && data.profile.is_profile_complete;
                
                // Update progress bar and status
                this.updateProfileProgress(completionPercentage, isProfileComplete);
                
                // Show progress card if profile is started (> 0%) or not complete (< 100%)
                if (completionPercentage < 100) {
                    this.showCompleteProfilePrompt();
                }
                
                if (completionPercentage >= 80) {
                    console.log('Profile is substantially complete, also showing recommendations');
                    this.showRecommendations();
                } else if (completionPercentage === 0) {
                    console.log('Profile not started, showing initial prompt');
                } else {
                    console.log(`Profile ${completionPercentage}% complete, showing progress`);
                }
            } else {
                console.log('Profile data not available, showing prompt');
                this.updateProfileProgress(0, false);
                this.showCompleteProfilePrompt();
            }
        } catch (error) {
            console.error('Error checking profile completion:', error);
            this.updateProfileProgress(0, false);
            this.showCompleteProfilePrompt();
        }
    }

    updateProfileProgress(percentage, isComplete) {
        const progressBar = document.getElementById('progress-bar');
        const completionPercentageElement = document.getElementById('completion-percentage');
        const profileStatusText = document.getElementById('profile-status-text');
        const completeProfileBtnText = document.getElementById('complete-profile-btn-text');
        const completeProfileCard = document.getElementById('complete-profile-card');
        
        // Update progress bar width
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
            
            // Change color based on completion
            if (percentage >= 80) {
                progressBar.className = 'bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-300';
            } else if (percentage >= 50) {
                progressBar.className = 'bg-gradient-to-r from-yellow-500 to-orange-500 h-2 rounded-full transition-all duration-300';
            } else {
                progressBar.className = 'bg-gradient-to-r from-red-500 to-red-600 h-2 rounded-full transition-all duration-300';
            }
        }
        
        // Update percentage text
        if (completionPercentageElement) {
            completionPercentageElement.textContent = `${percentage}%`;
        }
        
        // Update status text and button based on completion
        if (profileStatusText && completeProfileBtnText) {
            if (percentage === 0) {
                profileStatusText.textContent = "Get started by completing your profile to unlock personalized internship recommendations.";
                completeProfileBtnText.textContent = "Start Profile";
            } else if (percentage < 50) {
                profileStatusText.textContent = "You're just getting started! Complete more fields to improve your recommendations.";
                completeProfileBtnText.textContent = "Continue Profile";
            } else if (percentage < 80) {
                profileStatusText.textContent = "Great progress! Add a few more details to get the best internship matches.";
                completeProfileBtnText.textContent = "Finish Profile";
            } else if (percentage < 100) {
                profileStatusText.textContent = "Almost there! Complete the remaining fields for optimal recommendations.";
                completeProfileBtnText.textContent = "Complete Profile";
            } else {
                profileStatusText.textContent = "Excellent! Your profile is complete. You can still edit or update your information.";
                completeProfileBtnText.textContent = "Edit Profile";
            }
        }
        
        // Update card border color based on progress
        if (completeProfileCard) {
            if (percentage >= 80) {
                completeProfileCard.className = 'bg-white rounded-lg shadow-md p-6 mb-8 border-l-4 border-green-400 hidden';
            } else if (percentage >= 50) {
                completeProfileCard.className = 'bg-white rounded-lg shadow-md p-6 mb-8 border-l-4 border-yellow-400 hidden';
            } else {
                completeProfileCard.className = 'bg-white rounded-lg shadow-md p-6 mb-8 border-l-4 border-red-400 hidden';
            }
        }
    }

    showCompleteProfilePrompt() {
        const completeProfileCard = document.getElementById('complete-profile-card');
        const recommendationsSection = document.getElementById('recommendations-section');

        if (completeProfileCard) {
            completeProfileCard.classList.remove('hidden');
        }
        if (recommendationsSection) {
            recommendationsSection.classList.add('hidden');
        }
    }

    showRecommendations() {
        const recommendationsSection = document.getElementById('recommendations-section');

        // Don't hide the profile card anymore - keep it visible
        if (recommendationsSection) {
            recommendationsSection.classList.remove('hidden');
        }

        // Load recommendations
        this.loadRecommendations();
    }

    async loadRecommendations() {
        try {
            console.log('Loading AI-powered recommendations...');
            
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            
            // First, try to get existing recommendations
            let backendUrl = `http://${backendHost}:5001/api/get_recommendations`;
            let response = await fetch(backendUrl, {
                method: 'GET',
                credentials: 'include'
            });

            let data;
            
            if (response.ok) {
                data = await response.json();
                console.log('Existing recommendations found:', data);
            } else {
                // No existing recommendations, generate new ones
                console.log('No existing recommendations, generating new ones...');
                
                backendUrl = `http://${backendHost}:5001/api/generate_recommendations`;
                response = await fetch(backendUrl, {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ force_refresh: false })
                });

                if (response.ok) {
                    data = await response.json();
                    console.log('New recommendations generated:', data);
                } else {
                    throw new Error('Failed to generate recommendations');
                }
            }

            if (data.success && data.detailed_internships && data.detailed_internships.length > 0) {
                this.recommendations = data.detailed_internships.map(internship => ({
                    id: internship.internship_id,
                    title: internship.internship_title,
                    company: internship.company_name,
                    location: `${internship.location_type}`,
                    duration: internship.duration || '3-6 months',
                    stipend: internship.stipend || 'Negotiable',
                    skills: internship.required_skills ? internship.required_skills.split(',').map(s => s.trim()).slice(0, 3) : ['Various Skills'],
                    description: internship.job_description,
                    industry: internship.industry_domain
                }));
                
                console.log('Processed recommendations:', this.recommendations);
                this.renderRecommendations();
            } else {
                console.log('No recommendations available, using fallback');
                this.recommendations = this.getPlaceholderRecommendations();
                this.renderRecommendations();
            }
        } catch (error) {
            console.error('Error loading recommendations:', error);
            // Fallback to placeholder data if API fails
            console.log('Using placeholder recommendations due to error');
            this.recommendations = this.getPlaceholderRecommendations();
            this.renderRecommendations();
        }
    }

    getPlaceholderRecommendations() {
        return [
            {
                id: 1,
                title: 'Software Development Intern',
                company: 'TechCorp Solutions',
                location: 'Bangalore, India',
                duration: '3 months',
                stipend: '₹15,000/month',
                skills: ['React', 'Node.js', 'JavaScript']
            },
            {
                id: 2,
                title: 'Data Science Intern',
                company: 'DataMinds Analytics',
                location: 'Mumbai, India',
                duration: '6 months',
                stipend: '₹20,000/month',
                skills: ['Python', 'Machine Learning', 'SQL']
            },
            {
                id: 3,
                title: 'UI/UX Design Intern',
                company: 'Creative Studios',
                location: 'Delhi, India',
                duration: '4 months',
                stipend: '₹12,000/month',
                skills: ['Figma', 'Adobe XD', 'Prototyping']
            },
            {
                id: 4,
                title: 'Marketing Intern',
                company: 'Growth Partners',
                location: 'Pune, India',
                duration: '3 months',
                stipend: '₹10,000/month',
                skills: ['Digital Marketing', 'Content Writing', 'SEO']
            },
            {
                id: 5,
                title: 'Backend Developer Intern',
                company: 'CloudTech Systems',
                location: 'Hyderabad, India',
                duration: '5 months',
                stipend: '₹18,000/month',
                skills: ['Java', 'Spring Boot', 'AWS']
            }
        ];
    }

    renderRecommendations() {
        const grid = document.getElementById('recommendations-grid');
        const noRecommendations = document.getElementById('no-recommendations');

        if (!grid) return;

        if (this.recommendations.length === 0) {
            this.showNoRecommendations();
            return;
        }

        // Hide no recommendations message
        if (noRecommendations) {
            noRecommendations.classList.add('hidden');
        }

        // Clear existing content
        grid.innerHTML = '';

        // Render recommendation cards
        this.recommendations.forEach(recommendation => {
            const card = this.createRecommendationCard(recommendation);
            grid.appendChild(card);
        });
    }

    createRecommendationCard(recommendation) {
        const card = document.createElement('div');
        card.className = 'bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow border border-gray-200';

        card.innerHTML = `
            <div class="flex justify-between items-start mb-4">
                <h3 class="text-lg font-semibold text-gray-900 line-clamp-2">${recommendation.title}</h3>
                <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">${recommendation.duration}</span>
            </div>
            
            <div class="space-y-2 mb-4">
                <p class="text-gray-600 font-medium">${recommendation.company}</p>
                <p class="text-sm text-gray-500 flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    ${recommendation.location}
                </p>
                <p class="text-sm text-gray-500 flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
                    </svg>
                    ${recommendation.stipend}
                </p>
            </div>
            
            <div class="mb-4">
                <div class="flex flex-wrap gap-2">
                    ${recommendation.skills.map(skill => 
                        `<span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">${skill}</span>`
                    ).join('')}
                </div>
            </div>
            
            <button class="w-full bg-primary text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors font-medium" onclick="window.viewInternship(${recommendation.id})">
                View Details
            </button>
        `;

        return card;
    }

    showNoRecommendations() {
        const grid = document.getElementById('recommendations-grid');
        const noRecommendations = document.getElementById('no-recommendations');

        if (grid) {
            grid.innerHTML = '';
        }
        if (noRecommendations) {
            noRecommendations.classList.remove('hidden');
        }
    }

    async handleLogout() {
        try {
            // Use dynamic backend URL based on current host
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            const backendUrl = `http://${backendHost}:5001/logout`;
            console.log('Logout URL:', backendUrl);
            
            const response = await fetch(backendUrl, {
                method: 'POST',
                credentials: 'include'
            });

            if (response.ok) {
                window.location.href = 'auth.html#login';
            } else {
                throw new Error('Logout failed');
            }
        } catch (error) {
            console.error('Logout error:', error);
            // Force redirect even if logout request fails
            window.location.href = 'auth.html#login';
        }
    }

    handleCompleteProfile() {
        // Redirect to profile completion page
        console.log('Redirecting to complete profile page...');
        window.location.href = 'complete-profile.html';
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

    async refreshRecommendations() {
        try {
            console.log('Refreshing recommendations with force refresh...');
            
            const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
            const backendUrl = `http://${backendHost}:5001/api/generate_recommendations`;
            
            const response = await fetch(backendUrl, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ force_refresh: true })
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Force refreshed recommendations:', data);
                
                if (data.success && data.detailed_internships) {
                    this.recommendations = data.detailed_internships.map(internship => ({
                        id: internship.internship_id,
                        title: internship.internship_title,
                        company: internship.company_name,
                        location: internship.location_type,
                        duration: internship.duration || '3-6 months',
                        stipend: internship.stipend || 'Negotiable',
                        skills: internship.required_skills ? internship.required_skills.split(',').map(s => s.trim()).slice(0, 3) : ['Various Skills'],
                        description: internship.job_description,
                        industry: internship.industry_domain
                    }));
                    
                    this.renderRecommendations();
                    this.showSuccessMessage('Recommendations updated successfully!');
                } else {
                    throw new Error('Failed to refresh recommendations');
                }
            } else {
                throw new Error('Failed to refresh recommendations');
            }
        } catch (error) {
            console.error('Error refreshing recommendations:', error);
            this.showError('Failed to refresh recommendations. Please try again.');
        }
    }

    showSuccessMessage(message) {
        // Create a success notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-md shadow-lg z-50';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.parentElement.removeChild(notification);
            }
        }, 3000);
    }

    showError(message) {
        // Create an error notification
        const notification = document.createElement('div');
        notification.className = 'fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-md shadow-lg z-50';
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.parentElement.removeChild(notification);
            }
        }, 5000);
    }
}

// Global functions
window.viewInternship = function(id) {
    // TODO: Implement internship detail view
    alert(`View internship details for ID: ${id}`);
};

// Initialize the home page when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HomePage();
});
