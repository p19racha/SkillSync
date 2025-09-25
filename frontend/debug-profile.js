// Debug script for complete profile edit functionality
console.log('=== DEBUG SCRIPT LOADED ===');

// Wait for page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, starting debug checks...');
    
    // Check if form exists
    const form = document.getElementById('complete-profile-form');
    console.log('Form found:', !!form);
    
    // Check if CompleteProfilePage class is loaded
    console.log('CompleteProfilePage available:', typeof CompleteProfilePage !== 'undefined');
    
    // Test authentication manually
    setTimeout(async () => {
        try {
            console.log('Testing authentication...');
            const response = await fetch('http://127.0.0.1:5001/api/check-auth', {
                credentials: 'include'
            });
            console.log('Auth response status:', response.status);
            const data = await response.json();
            console.log('Auth response data:', data);
            
            if (data.authenticated) {
                console.log('User is authenticated, testing profile retrieval...');
                
                const profileResponse = await fetch('http://127.0.0.1:5001/api/complete-profile', {
                    credentials: 'include'
                });
                console.log('Profile response status:', profileResponse.status);
                const profileData = await profileResponse.json();
                console.log('Profile response data:', profileData);
                
                if (profileResponse.status === 200 && profileData.success) {
                    console.log('Profile found! Should be in edit mode.');
                    console.log('Testing form field population...');
                    
                    // Test setting a field manually
                    const nameField = document.getElementById('name');
                    if (nameField) {
                        nameField.value = profileData.profile.name;
                        console.log('Manually set name field to:', profileData.profile.name);
                    } else {
                        console.error('Name field not found!');
                    }
                    
                    // Check all form fields
                    const fields = ['aadhar_id', 'name', 'dob', 'state', 'city', 'pincode'];
                    fields.forEach(fieldName => {
                        const field = document.getElementById(fieldName);
                        console.log(`Field ${fieldName}:`, field ? 'found' : 'NOT FOUND', field ? field.value : 'n/a');
                    });
                    
                } else if (profileResponse.status === 404) {
                    console.log('No profile found - should be in create mode.');
                } else {
                    console.error('Unexpected profile response:', profileData);
                }
            } else {
                console.log('User not authenticated');
            }
        } catch (error) {
            console.error('Debug test error:', error);
        }
    }, 2000); // Wait 2 seconds for page to initialize
});