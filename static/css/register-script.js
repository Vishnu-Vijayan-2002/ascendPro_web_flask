// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.textContent = '🙈';
    } else {
        passwordInput.type = 'password';
        toggleIcon.textContent = '👁️';
    }
}

// Password strength checker
const passwordInput = document.getElementById('password');
const strengthFill = document.getElementById('strengthFill');
const strengthText = document.getElementById('strengthText');

passwordInput.addEventListener('input', function() {
    const password = this.value;
    const strength = calculatePasswordStrength(password);
    
    // Update strength bar
    strengthFill.style.width = strength.percentage + '%';
    strengthFill.style.backgroundColor = strength.color;
    strengthText.textContent = strength.text;
    strengthText.style.color = strength.color;
});

function calculatePasswordStrength(password) {
    let score = 0;
    
    if (password.length === 0) {
        return { percentage: 0, color: '#cbd5e1', text: 'Enter password' };
    }
    
    // Length check
    if (password.length >= 8) score += 25;
    if (password.length >= 12) score += 15;
    
    // Character variety checks
    if (/[a-z]/.test(password)) score += 15; // lowercase
    if (/[A-Z]/.test(password)) score += 15; // uppercase
    if (/[0-9]/.test(password)) score += 15; // numbers
    if (/[^a-zA-Z0-9]/.test(password)) score += 15; // special characters
    
    // Determine strength level
    let strength = { percentage: score, color: '', text: '' };
    
    if (score <= 30) {
        strength.color = '#ef4444';
        strength.text = 'Weak password';
    } else if (score <= 60) {
        strength.color = '#f59e0b';
        strength.text = 'Fair password';
    } else if (score <= 80) {
        strength.color = '#3b82f6';
        strength.text = 'Good password';
    } else {
        strength.color = '#10b981';
        strength.text = 'Strong password';
    }
    
    return strength;
}

// Form validation and animation
const registerForm = document.querySelector('.register-form');
const inputs = document.querySelectorAll('.input-wrapper input');

// Add focus animation to inputs
inputs.forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'scale(1.02)';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'scale(1)';
    });
});

// Email validation
const emailInput = document.getElementById('email');
emailInput.addEventListener('blur', function() {
    const email = this.value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (email && !emailRegex.test(email)) {
        this.style.borderColor = '#ef4444';
        this.setCustomValidity('Please enter a valid email address');
    } else {
        this.style.borderColor = '#e2e8f0';
        this.setCustomValidity('');
    }
});

// Form submission handler
registerForm.addEventListener('submit', function(e) {
    // Uncomment to prevent actual submission for demo
    // e.preventDefault();
    
    const submitBtn = document.querySelector('.btn-register');
    const originalText = submitBtn.innerHTML;
    
    // Validate role selection
    const roleSelected = document.querySelector('input[name="role"]:checked');
    if (!roleSelected) {
        e.preventDefault();
        alert('Please select your role');
        return;
    }
    
    // Validate terms checkbox
    const termsChecked = document.querySelector('input[name="terms"]:checked');
    if (!termsChecked) {
        e.preventDefault();
        alert('Please agree to the Terms of Service and Privacy Policy');
        return;
    }
    
    // Show loading state
    submitBtn.innerHTML = '<span>Creating account...</span>';
    submitBtn.disabled = true;
    submitBtn.style.opacity = '0.7';
    
    // Simulate API call (remove in production)
    setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
    }, 2000);
});

// Add shake animation on invalid input
inputs.forEach(input => {
    input.addEventListener('invalid', function(e) {
        e.preventDefault();
        this.parentElement.classList.add('shake');
        this.style.borderColor = '#ef4444';
        
        setTimeout(() => {
            this.parentElement.classList.remove('shake');
        }, 500);
    });
    
    input.addEventListener('input', function() {
        if (this.validity.valid) {
            this.style.borderColor = '#e2e8f0';
        }
    });
});

// Role card animation
const roleCards = document.querySelectorAll('.role-card');
roleCards.forEach(card => {
    card.addEventListener('click', function() {
        roleCards.forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
    });
});

// Add shake animation CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .shake {
        animation: shake 0.5s;
    }
`;
document.head.appendChild(style);