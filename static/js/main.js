// Scripts principales de Mediconecta
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Función para scroll suave
    initializeSmoothScroll();
    
    // Función para manejar formularios
    initializeForms();
    
    // Función para animaciones
    initializeAnimations();
    
    // Nueva función para ajustar la altura del footer
    adjustFooterVisibility();
    
    // Reajustar cuando se redimensiona la ventana o cambia el zoom
    window.addEventListener('resize', adjustFooterVisibility);
    window.addEventListener('orientationchange', adjustFooterVisibility);
});

// Función para scroll suave
function initializeSmoothScroll() {
    // Manejar enlaces de scroll suave
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Función para inicializar formularios
function initializeForms() {
    // Validación en tiempo real
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });

        // Limpiar validación al escribir
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

// Función para inicializar animaciones
function initializeAnimations() {
    // Intersection Observer para animaciones al hacer scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observar elementos con clase 'animate-on-scroll'
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

// Función para mostrar alertas personalizadas
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remover después del tiempo especificado
    if (duration > 0) {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, duration);
    }
}

// Función para validar formularios médicos
function validateMedicalForm(formData) {
    const errors = [];
    
    // Validar campos requeridos
    if (!formData.nombre || formData.nombre.trim().length < 2) {
        errors.push('El nombre debe tener al menos 2 caracteres');
    }
    
    if (!formData.email || !isValidEmail(formData.email)) {
        errors.push('Debe proporcionar un correo electrónico válido');
    }
    
    if (formData.telefono && !isValidPhone(formData.telefono)) {
        errors.push('Debe proporcionar un teléfono válido');
    }
    
    return {
        isValid: errors.length === 0,
        errors: errors
    };
}

// Función para validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Función para validar teléfono
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Función para formatear fecha
function formatDate(date, format = 'dd/mm/yyyy') {
    const d = new Date(date);
    const day = d.getDate().toString().padStart(2, '0');
    const month = (d.getMonth() + 1).toString().padStart(2, '0');
    const year = d.getFullYear();
    
    switch (format) {
        case 'dd/mm/yyyy':
            return `${day}/${month}/${year}`;
        case 'yyyy-mm-dd':
            return `${year}-${month}-${day}`;
        default:
            return d.toLocaleDateString();
    }
}

// Función para formatear hora
function formatTime(time, format = '24h') {
    const [hours, minutes] = time.split(':');
    const h = parseInt(hours);
    const m = minutes;
    
    if (format === '12h') {
        const period = h >= 12 ? 'PM' : 'AM';
        const displayHour = h > 12 ? h - 12 : (h === 0 ? 12 : h);
        return `${displayHour}:${m} ${period}`;
    }
    
    return `${h.toString().padStart(2, '0')}:${m}`;
}

// Función para confirmar acciones
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Función para cargar datos dinámicamente
function loadData(url, container, options = {}) {
    const { method = 'GET', data = null, headers = {} } = options;
    
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            ...headers
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .then(data => {
        if (container) {
            container.innerHTML = data.html || data.message || 'Datos cargados';
        }
        if (data.success && data.message) {
            showAlert(data.message, 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Error al cargar los datos', 'danger');
    });
}

// Función para obtener cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Exportar funciones para uso global
window.Mediconecta = {
    showAlert,
    validateMedicalForm,
    formatDate,
    formatTime,
    confirmAction,
    loadData,
    isValidEmail,
    isValidPhone
};

// Función para ajustar la visibilidad del footer dinámicamente
function adjustFooterVisibility() {
    const body = document.body;
    const main = document.querySelector('main');
    const footer = document.querySelector('footer');
    const navbar = document.querySelector('.navbar');
    
    if (!main || !footer || !navbar) return;
    
    // Calcular alturas reales
    const windowHeight = window.innerHeight;
    const navbarHeight = navbar.offsetHeight;
    const footerHeight = footer.offsetHeight;
    
    // Calcular la altura mínima que debe tener el main
    const minMainHeight = windowHeight - navbarHeight - footerHeight;
    
    // Aplicar la altura mínima
    main.style.minHeight = `${minMainHeight}px`;
    
    // Para páginas con .force-footer-visible, asegurar que ocupen toda la altura
    const forceFooterContainer = document.querySelector('.force-footer-visible');
    if (forceFooterContainer) {
        forceFooterContainer.style.minHeight = `${windowHeight}px`;
        
        // Ajustar el contenido para que esté centrado
        const contentWrapper = forceFooterContainer.querySelector('.content-wrapper');
        if (contentWrapper) {
            const availableHeight = windowHeight - navbarHeight - footerHeight;
            contentWrapper.style.minHeight = `${availableHeight}px`;
        }
    }
    
    console.log('Footer visibility adjusted:', {
        windowHeight,
        navbarHeight,
        footerHeight,
        minMainHeight
    });
}
