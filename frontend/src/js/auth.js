// Tab switching logic and hash navigation
const loginTab = document.getElementById('login-tab');
const registerTab = document.getElementById('register-tab');
const loginFormContainer = document.getElementById('login-form');
const registerFormContainer = document.getElementById('register-form');

console.log('Auth.js loaded');
console.log('Elements found:', { loginTab, registerTab, loginFormContainer, registerFormContainer });

function showLoginTab() {
	if (loginTab && registerTab && loginFormContainer && registerFormContainer) {
		loginTab.classList.add('active-tab');
		loginTab.classList.remove('inactive-tab');
		registerTab.classList.remove('active-tab');
		registerTab.classList.add('inactive-tab');
		loginFormContainer.classList.remove('hidden');
		registerFormContainer.classList.add('hidden');
	}
}
function showRegisterTab() {
	if (loginTab && registerTab && loginFormContainer && registerFormContainer) {
		registerTab.classList.add('active-tab');
		registerTab.classList.remove('inactive-tab');
		loginTab.classList.remove('active-tab');
		loginTab.classList.add('inactive-tab');
		registerFormContainer.classList.remove('hidden');
		loginFormContainer.classList.add('hidden');
	}
}

if (loginTab && registerTab && loginFormContainer && registerFormContainer) {
	loginTab.onclick = showLoginTab;
	registerTab.onclick = showRegisterTab;
	// On page load, check hash for navigation
	if (window.location.hash === '#register') {
		showRegisterTab();
	} else {
		showLoginTab();
	}
} else {
	console.error('Some required elements not found for tab switching');
}

// Registration AJAX
const registerForm = registerFormContainer ? registerFormContainer.querySelector('form') : null;
console.log('Register form found:', registerForm);

if (registerForm) {
	registerForm.onsubmit = async (e) => {
		console.log('Registration form submitted');
		e.preventDefault();
		
		const emailField = document.getElementById('register-email');
		const passwordField = document.getElementById('register-password');
		const confirmPasswordField = document.getElementById('confirm-password');
		
		console.log('Form fields:', { emailField, passwordField, confirmPasswordField });
		
		const email = emailField ? emailField.value : '';
		const password = passwordField ? passwordField.value : '';
		const confirmPassword = confirmPasswordField ? confirmPasswordField.value : '';
		const registerBtn = registerForm.querySelector('button[type="submit"]');
		
		console.log('Form values:', { email, password, confirmPassword });
		
		if (!email || !password) {
			alert('Please fill in all required fields.');
			return;
		}
		
		if (password !== confirmPassword) {
			alert('Passwords do not match.');
			return;
		}
		
		registerBtn.disabled = true;
		registerBtn.textContent = 'Registering...';
		
		try {
			console.log('Sending registration request...');
			// Use dynamic backend URL based on current host
			const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
			const backendUrl = `http://${backendHost}:5001/register`;
			console.log('Registration URL:', backendUrl);
			
			const res = await fetch(backendUrl, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ username: email, password })
			});
			
			console.log('Response status:', res.status);
			const data = await res.json();
			console.log('Response data:', data);
			
			if (res.ok) {
				alert(data.message || 'Registration successful!');
				showLoginTab();
			} else {
				alert(data.message || 'Registration failed.');
			}
		} catch (err) {
			console.error('Registration error:', err);
			alert('Registration failed. Please check your connection.');
		}
		
		registerBtn.disabled = false;
		registerBtn.textContent = 'Create Account';
	};
} else {
	console.error('Register form not found');
}

// Login AJAX
const loginForm = loginFormContainer ? loginFormContainer.querySelector('form') : null;
console.log('Login form found:', loginForm);

if (loginForm) {
	loginForm.onsubmit = async (e) => {
		console.log('Login form submitted');
		e.preventDefault();
		
		const emailField = document.getElementById('login-email');
		const passwordField = document.getElementById('login-password');
		
		console.log('Login form fields:', { emailField, passwordField });
		
		const email = emailField ? emailField.value : '';
		const password = passwordField ? passwordField.value : '';
		const loginBtn = loginForm.querySelector('button[type="submit"]');
		
		console.log('Login form values:', { email, password });
		
		if (!email || !password) {
			alert('Please fill in all fields.');
			return;
		}
		
		loginBtn.disabled = true;
		loginBtn.textContent = 'Signing in...';
		
		try {
			console.log('Sending login request...');
			// Use dynamic backend URL based on current host
			const backendHost = window.location.hostname === '127.0.0.1' ? '127.0.0.1' : 'localhost';
			const backendUrl = `http://${backendHost}:5001/login`;
			console.log('Backend URL:', backendUrl);
			
			const res = await fetch(backendUrl, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				credentials: 'include',
				body: JSON.stringify({ username: email, password })
			});
			
			console.log('Login response status:', res.status);
			const data = await res.json();
			console.log('Login response data:', data);
			
			if (res.ok) {
				console.log('Login successful, redirecting to home...');
				// Direct redirect without delay
				window.location.href = 'home.html';
			} else {
				console.log('Login failed:', data);
				alert(data.message || 'Login failed.');
			}
		} catch (err) {
			console.error('Login error:', err);
			alert('Login failed. Please check your connection.');
		}
		
		loginBtn.disabled = false;
		loginBtn.textContent = 'Sign In';
	};
} else {
	console.error('Login form not found');
}
