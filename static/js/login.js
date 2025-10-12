// Script específico para la página de login
document.addEventListener('DOMContentLoaded', function() {
    initializeLoginForm();
});

function initializeLoginForm() {
    const loginForm = document.querySelector('form');
    const emailInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    
    if (!loginForm) return;
    
    // Validación en tiempo real del nombre de usuario
    if (emailInput) {
        emailInput.addEventListener('blur', function() {
            validateUsername(this);
        });
        
        emailInput.addEventListener('input', function() {
            clearValidation(this);
        });
    }
    
    // Validación en tiempo real de la contraseña
    if (passwordInput) {
        passwordInput.addEventListener('blur', function() {
            validatePassword(this);
        });
        
        passwordInput.addEventListener('input', function() {
            clearValidation(this);
        });
    }
    
    // Manejar envío del formulario
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateLoginForm()) {
            // Mostrar loading
            showLoading();
            
            // Simular envío (en producción esto se manejará por Django)
            setTimeout(() => {
                hideLoading();
                // El formulario se enviará normalmente
                this.submit();
            }, 1000);
        }
    });
}

function validateLoginForm() {
    const emailInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    
    let isValid = true;
    
    // Validar nombre de usuario
    if (!validateUsername(emailInput)) {
        isValid = false;
    }
    
    // Validar contraseña
    if (!validatePassword(passwordInput)) {
        isValid = false;
    }
    
    return isValid;
}

function validateUsername(input) {
    const username = input.value.trim();
    
    if (!username) {
        showFieldError(input, 'El nombre de usuario es requerido');
        return false;
    }
    
    showFieldSuccess(input);
    return true;
}

function validatePassword(input) {
    const password = input.value;
    
    if (!password) {
        showFieldError(input, 'La contraseña es requerida');
        return false;
    }
    
    if (password.length < 6) {
        showFieldError(input, 'La contraseña debe tener al menos 6 caracteres');
        return false;
    }
    
    showFieldSuccess(input);
    return true;
}

function showFieldError(input, message) {
    clearValidation(input);
    
    input.classList.add('is-invalid');
    input.classList.remove('is-valid');
    
    const feedback = input.parentNode.querySelector('.invalid-feedback');
    if (feedback) {
        feedback.textContent = message;
    } else {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback d-block';
        errorDiv.textContent = message;
        input.parentNode.appendChild(errorDiv);
    }
}

function showFieldSuccess(input) {
    clearValidation(input);
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
}

function clearValidation(input) {
    input.classList.remove('is-valid', 'is-invalid');
    
    const feedback = input.parentNode.querySelector('.invalid-feedback');
    if (feedback && feedback.classList.contains('d-block')) {
        feedback.remove();
    }
}

function showLoading() {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Iniciando sesión...';
    }
}

function hideLoading() {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Iniciar sesión';
    }
}

// Función para manejar errores del servidor
function handleServerErrors(errors) {
    Object.keys(errors).forEach(field => {
        const input = document.querySelector(`[name="${field}"]`);
        if (input) {
            showFieldError(input, errors[field][0]);
        }
    });
}

// Función para mostrar mensaje de éxito
function showSuccessMessage(message) {
    if (window.Mediconecta) {
        window.Mediconecta.showAlert(message, 'success');
    }
}

// Función para mostrar mensaje de error
function showErrorMessage(message) {
    if (window.Mediconecta) {
        window.Mediconecta.showAlert(message, 'danger');
    }
}

// Exportar funciones para uso global
window.LoginForm = {
    validateLoginForm,
    validateUsername,
    validatePassword,
    handleServerErrors,
    showSuccessMessage,
    showErrorMessage
};
