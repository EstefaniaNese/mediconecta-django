// Script específico para el dashboard del paciente
document.addEventListener('DOMContentLoaded', function() {
    initializePatientDashboard();
});

function initializePatientDashboard() {
    initializePatientForm();
    initializeReservationsTable();
    initializeNewReservationForm();
    initializeMedicalConditions();
}

function initializePatientForm() {
    const patientForm = document.querySelector('#editarPerfil form');
    if (!patientForm) return;
    
    // Validación en tiempo real
    const inputs = patientForm.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validatePatientField(this);
        });
        
        input.addEventListener('input', function() {
            clearFieldValidation(this);
        });
    });
    
    // Manejar envío del formulario
    patientForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validatePatientForm()) {
            showLoading('Guardando cambios...');
            
            // Simular envío
            setTimeout(() => {
                hideLoading();
                showSuccessMessage('Perfil actualizado correctamente');
                this.submit();
            }, 1500);
        }
    });
}

function initializeReservationsTable() {
    const table = document.querySelector('.table');
    if (!table) return;
    
    // Agregar funcionalidad a los botones de la tabla
    table.addEventListener('click', function(e) {
        const target = e.target.closest('button');
        if (!target) return;
        
        const action = target.title;
        const row = target.closest('tr');
        
        switch (action) {
            case 'Editar':
                editReservation(row);
                break;
            case 'Eliminar':
                deleteReservation(row);
                break;
        }
    });
}

function initializeNewReservationForm() {
    const reservationForm = document.querySelector('#reservasHistorial form');
    if (!reservationForm) return;
    
    reservationForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (validateReservationForm()) {
            showLoading('Procesando reserva...');
            
            // Simular envío
            setTimeout(() => {
                hideLoading();
                showSuccessMessage('Reserva creada correctamente');
                addReservationToTable(getFormData(this));
                this.reset();
            }, 1500);
        }
    });
}

function initializeMedicalConditions() {
    const checkboxes = document.querySelectorAll('.afeccion-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const detailInput = document.querySelector(`#detalle-${this.value}`);
            if (detailInput) {
                if (this.checked) {
                    detailInput.classList.remove('d-none');
                    detailInput.required = true;
                } else {
                    detailInput.classList.add('d-none');
                    detailInput.required = false;
                    detailInput.value = '';
                }
            }
        });
    });
}

function validatePatientForm() {
    const form = document.querySelector('#editarPerfil form');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validatePatientField(field)) {
            isValid = false;
        }
    });
    
    // Validar fecha de nacimiento
    const birthDate = form.querySelector('input[name="fechaNacimiento"]');
    if (birthDate && birthDate.value) {
        const birth = new Date(birthDate.value);
        const today = new Date();
        const age = today.getFullYear() - birth.getFullYear();
        
        if (age < 0 || age > 150) {
            showFieldError(birthDate, 'Fecha de nacimiento inválida');
            isValid = false;
        }
    }
    
    // Validar confirmación de contraseña
    const password = form.querySelector('input[name="contrasena"]');
    const confirmPassword = form.querySelector('input[name="confirmarContrasena"]');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
        showFieldError(confirmPassword, 'Las contraseñas no coinciden');
        isValid = false;
    }
    
    return isValid;
}

function validatePatientField(input) {
    const value = input.value.trim();
    const fieldName = input.name;
    
    // Campos requeridos
    if (input.required && !value) {
        showFieldError(input, `${getFieldLabel(input)} es requerido`);
        return false;
    }
    
    // Validaciones específicas
    switch (fieldName) {
        case 'nombre':
            if (value && value.length < 2) {
                showFieldError(input, 'El nombre debe tener al menos 2 caracteres');
                return false;
            }
            break;
            
        case 'email':
            if (value && !isValidEmail(value)) {
                showFieldError(input, 'Correo electrónico inválido');
                return false;
            }
            break;
            
        case 'contrasena':
            if (value && value.length < 6) {
                showFieldError(input, 'La contraseña debe tener al menos 6 caracteres');
                return false;
            }
            break;
    }
    
    showFieldSuccess(input);
    return true;
}

function validateReservationForm() {
    const form = document.querySelector('#reservasHistorial form');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!validateReservationField(field)) {
            isValid = false;
        }
    });
    
    // Validar que la fecha no sea en el pasado
    const fecha = form.querySelector('input[type="date"]');
    if (fecha && fecha.value) {
        const selectedDate = new Date(fecha.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            showFieldError(fecha, 'No puedes reservar para fechas pasadas');
            isValid = false;
        }
    }
    
    return isValid;
}

function validateReservationField(input) {
    const value = input.value.trim();
    
    if (input.required && !value) {
        showFieldError(input, `${getFieldLabel(input)} es requerido`);
        return false;
    }
    
    showFieldSuccess(input);
    return true;
}

function editReservation(row) {
    const fecha = row.cells[0].textContent;
    const hora = row.cells[1].textContent;
    const especialista = row.cells[2].textContent;
    
    // Llenar el formulario con los datos existentes
    const form = document.querySelector('#reservasHistorial form');
    const fechaInput = form.querySelector('input[type="date"]');
    const horaInput = form.querySelector('input[type="time"]');
    const especialistaSelect = form.querySelector('select');
    
    if (fechaInput) fechaInput.value = convertDateFormat(fecha);
    if (horaInput) horaInput.value = hora;
    if (especialistaSelect) especialistaSelect.value = especialista;
    
    // Scroll al formulario
    form.scrollIntoView({ behavior: 'smooth' });
    
    showInfoMessage('Datos cargados para edición');
}

function deleteReservation(row) {
    const fecha = row.cells[0].textContent;
    const especialista = row.cells[2].textContent;
    
    const message = `¿Estás seguro de que quieres cancelar la cita con ${especialista} del ${fecha}?`;
    
    if (confirm(message)) {
        showLoading('Cancelando cita...');
        
        setTimeout(() => {
            hideLoading();
            row.remove();
            showSuccessMessage('Cita cancelada correctamente');
        }, 1000);
    }
}

function addReservationToTable(formData) {
    const table = document.querySelector('#reservasHistorial .table tbody');
    if (!table) return;
    
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${formatDate(formData.fecha)}</td>
        <td>${formData.hora}</td>
        <td>${formData.especialista}</td>
        <td>Pendiente</td>
        <td>
            <button class="btn btn-sm btn-success" title="Editar">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-sm btn-danger" title="Eliminar">
                <i class="fas fa-trash-alt"></i>
            </button>
        </td>
    `;
    
    table.appendChild(newRow);
}

function getFormData(form) {
    const formData = {};
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        formData[input.name || input.id] = input.value;
    });
    
    return formData;
}

function getFieldLabel(input) {
    const label = input.closest('.mb-3').querySelector('label');
    return label ? label.textContent.replace('*', '').trim() : 'Este campo';
}

function showFieldError(input, message) {
    clearFieldValidation(input);
    
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
    clearFieldValidation(input);
    input.classList.add('is-valid');
    input.classList.remove('is-invalid');
}

function clearFieldValidation(input) {
    input.classList.remove('is-valid', 'is-invalid');
    
    const feedback = input.parentNode.querySelector('.invalid-feedback');
    if (feedback && feedback.classList.contains('d-block')) {
        feedback.remove();
    }
}

function showLoading(message = 'Procesando...') {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${message}`;
        submitBtn.dataset.originalText = originalText;
    }
}

function hideLoading() {
    const submitBtn = document.querySelector('button[type="submit"]');
    if (submitBtn && submitBtn.dataset.originalText) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = submitBtn.dataset.originalText;
        delete submitBtn.dataset.originalText;
    }
}

function showSuccessMessage(message) {
    if (window.Mediconecta) {
        window.Mediconecta.showAlert(message, 'success');
    }
}

function showInfoMessage(message) {
    if (window.Mediconecta) {
        window.Mediconecta.showAlert(message, 'info');
    }
}

function showErrorMessage(message) {
    if (window.Mediconecta) {
        window.Mediconecta.showAlert(message, 'danger');
    }
}

function convertDateFormat(dateString) {
    // Convertir de dd/mm/yyyy a yyyy-mm-dd
    const parts = dateString.split('/');
    if (parts.length === 3) {
        return `${parts[2]}-${parts[1].padStart(2, '0')}-${parts[0].padStart(2, '0')}`;
    }
    return dateString;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Exportar funciones para uso global
window.PatientDashboard = {
    validatePatientForm,
    validateReservationForm,
    editReservation,
    deleteReservation,
    addReservationToTable
};
