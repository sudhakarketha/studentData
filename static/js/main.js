// Main JavaScript file for Student Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Attendance status change confirmation
    const statusForms = document.querySelectorAll('form[action^="/update_status/"]');
    
    statusForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const statusInput = this.querySelector('input[name="status"]');
            if (statusInput.value === 'absent') {
                if (!confirm('Are you sure you want to mark this student as absent? An SMS notification will be sent to their contact number.')) {
                    e.preventDefault();
                }
            }
        });
    });

    // Student deletion confirmation
    const deleteLinks = document.querySelectorAll('a[href^="/delete_student/"]');
    
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this student? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Search form enhancements
    const searchForm = document.querySelector('form[action="/search"]');
    const searchInput = document.querySelector('input[name="query"]');
    
    if (searchForm && searchInput) {
        // Clear search when X is clicked
        const clearSearchBtn = document.createElement('button');
        clearSearchBtn.type = 'button';
        clearSearchBtn.className = 'btn btn-sm btn-outline-secondary';
        clearSearchBtn.innerHTML = '<i class="fas fa-times"></i>';
        clearSearchBtn.style.display = 'none';
        clearSearchBtn.style.position = 'absolute';
        clearSearchBtn.style.right = '10px';
        clearSearchBtn.style.top = '50%';
        clearSearchBtn.style.transform = 'translateY(-50%)';
        
        searchInput.parentNode.style.position = 'relative';
        searchInput.parentNode.appendChild(clearSearchBtn);
        
        searchInput.addEventListener('input', function() {
            clearSearchBtn.style.display = this.value ? 'block' : 'none';
        });
        
        clearSearchBtn.addEventListener('click', function() {
            searchInput.value = '';
            this.style.display = 'none';
            searchForm.submit();
        });
        
        // Show clear button if search has value on page load
        if (searchInput.value) {
            clearSearchBtn.style.display = 'block';
        }
    }

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            // Remove non-numeric characters
            let value = this.value.replace(/\D/g, '');
            
            // Format the number as needed
            if (value.length > 0) {
                if (value.length <= 3) {
                    this.value = value;
                } else if (value.length <= 6) {
                    this.value = value.slice(0, 3) + '-' + value.slice(3);
                } else {
                    this.value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 10);
                }
            }
        });
    });
});