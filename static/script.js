/* ========================================
   SMART FEE MANAGEMENT SYSTEM - MAIN SCRIPT
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // LOGIN PAGE
    // ========================================
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn.disabled) {
                e.preventDefault();
                return;
            }
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
        });
    }
    
    // ========================================
    // SIGNUP PAGE
    // ========================================
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (confirmPassword) {
            confirmPassword.addEventListener('keyup', function() {
                if (password.value !== this.value) {
                    this.setCustomValidity('Passwords do not match');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        signupForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn.disabled) {
                e.preventDefault();
                return;
            }
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating account...';
        });
    }
    
    // ========================================
    // ADMIN DASHBOARD
    // ========================================
    
    // Tab switching
    window.showTab = function(tabName) {
        document.querySelectorAll('.tab').forEach(tab => {
            tab.classList.remove('active');
        });
        const selectedTab = document.getElementById(tabName);
        if (selectedTab) selectedTab.classList.add('active');
    };
    
    // ---------------- MODAL FUNCTIONS ----------------
    window.showAddStudent = function() {
        const modal = document.getElementById('studentModal');
        if (modal) modal.style.display = 'block';
    };
    
    window.showAddCourse = function() {
        const modal = document.getElementById('courseModal');
        if (modal) modal.style.display = 'block';
    };
    
    window.showAddPayment = function() {
        const modal = document.getElementById('paymentModal');
        if (modal) {
            const dateInput = modal.querySelector('input[type="date"]');
            if (dateInput) dateInput.value = new Date().toISOString().split('T')[0];
            modal.style.display = 'block';
        }
    };
    
    window.showAddInstallment = function() {
        const modal = document.getElementById('installmentModal');
        if (modal) {
            const dateInput = modal.querySelector('input[type="date"]');
            if (dateInput) {
                const today = new Date();
                today.setDate(today.getDate() + 30);
                dateInput.value = today.toISOString().split('T')[0];
            }
            modal.style.display = 'block';
        }
    };
    
    window.closeModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
            const form = modal.querySelector('form');
            if (form) form.reset();
        }
    };
    
    // Close modal when clicking outside
    window.onclick = function(event) {
        if (event.target.classList.contains('modal')) {
            event.target.style.display = 'none';
            const form = event.target.querySelector('form');
            if (form) form.reset();
        }
    };
    
    // Close modal with ESC key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(modal => {
                if (modal.style.display === 'block') {
                    modal.style.display = 'none';
                    const form = modal.querySelector('form');
                    if (form) form.reset();
                }
            });
        }
    });
    
    // ---------------- BUTTON DISABLE WHILE SUBMIT ----------------
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const btn = this.querySelector('button[type="submit"]');
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            }
        });
    });
    
    // Show students tab by default on admin dashboard
    if (document.querySelector('.admin-dashboard')) {
        showTab('students');
    }
});