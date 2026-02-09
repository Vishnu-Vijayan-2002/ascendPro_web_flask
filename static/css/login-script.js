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

// Form validation and animation
const loginForm = document.querySelector('.login-form');
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

// Form submission handler (example)
loginForm.addEventListener('submit', function(e) {
    // Uncomment to prevent actual submission for demo
    // e.preventDefault();
    
    const submitBtn = document.querySelector('.btn-login');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<span>Logging in...</span>';
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