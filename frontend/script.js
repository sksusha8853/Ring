// ============================================================================
// CONFIGURATION
// ============================================================================

const API_URL = 'http://localhost:8000';
let currentToken = null;
let currentUser = null;

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    // Load token from localStorage
    const token = localStorage.getItem('token');
    if (token) {
        currentToken = token;
        showDashboard();
    } else {
        showAuth();
    }

    // Setup logout button
    document.getElementById('navLogout').addEventListener('click', logout);
});

// ============================================================================
// TAB SWITCHING
// ============================================================================

function switchTab(tab) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));

    // Show selected tab
    document.getElementById(tab + 'Tab').classList.add('active');
    event.target.classList.add('active');

    // Clear error messages
    document.getElementById(tab + 'Error').innerHTML = '';
    document.getElementById(tab + 'Error').classList.remove('show');
}

// ============================================================================
// AUTHENTICATION HANDLERS
// ============================================================================

async function handleLogin(event) {
    event.preventDefault();

    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const errorDiv = document.getElementById('loginError');

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Login failed');
        }

        // Store token and user data
        currentToken = data.access_token;
        currentUser = data.user;
        localStorage.setItem('token', currentToken);
        localStorage.setItem('user', JSON.stringify(currentUser));

        // Show dashboard
        showDashboard();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
}

async function handleSignup(event) {
    event.preventDefault();

    const username = document.getElementById('signupUsername').value;
    const password = document.getElementById('signupPassword').value;
    const phone = document.getElementById('signupPhone').value;
    const whatsapp = document.getElementById('signupWhatsapp').value;
    const instructions = document.getElementById('signupInstructions').value;
    const errorDiv = document.getElementById('signupError');

    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username,
                password,
                phone,
                whatsapp,
                instructions
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Signup failed');
        }

        // Store token and user data
        currentToken = data.access_token;
        currentUser = data.user;
        localStorage.setItem('token', currentToken);
        localStorage.setItem('user', JSON.stringify(currentUser));

        // Show dashboard
        showDashboard();
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.classList.add('show');
    }
}

function logout() {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    showAuth();
}

// ============================================================================
// UI DISPLAY FUNCTIONS
// ============================================================================

function showAuth() {
    document.getElementById('authSection').style.display = 'block';
    document.getElementById('dashboardSection').style.display = 'none';
    document.getElementById('navLogout').style.display = 'none';

    // Clear forms
    document.getElementById('loginForm').reset();
    document.getElementById('signupForm').reset();
    switchTab('login');
}

function showDashboard() {
    document.getElementById('authSection').style.display = 'none';
    document.getElementById('dashboardSection').style.display = 'block';
    document.getElementById('navLogout').style.display = 'block';

    loadUserProfile();
    loadAnalytics();
}

// ============================================================================
// PROFILE MANAGEMENT
// ============================================================================

async function loadUserProfile() {
    if (!currentToken) return;

    try {
        const response = await fetch(`${API_URL}/me`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                logout();
                return;
            }
            throw new Error('Failed to load profile');
        }

        const user = await response.json();
        currentUser = user;

        // Update dashboard display
        document.getElementById('dashboardUsername').textContent = user.username;
        document.getElementById('profileUsername').textContent = user.username;
        document.getElementById('profilePhone').textContent = user.phone;
        document.getElementById('profileWhatsapp').textContent = user.whatsapp;
        document.getElementById('profileInstructions').textContent = user.instructions || '(No instructions set)';
        document.getElementById('profileUrl').value = user.profile_url;

        // Pre-fill update form
        document.getElementById('updatePhone').placeholder = user.phone;
        document.getElementById('updateWhatsapp').placeholder = user.whatsapp;
        document.getElementById('updateInstructions').placeholder = user.instructions || '(No instructions)';
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

async function handleUpdate(event) {
    event.preventDefault();

    const phone = document.getElementById('updatePhone').value;
    const whatsapp = document.getElementById('updateWhatsapp').value;
    const instructions = document.getElementById('updateInstructions').value;
    const errorDiv = document.getElementById('updateError');

    if (!phone && !whatsapp && !instructions) {
        errorDiv.textContent = 'Please update at least one field';
        errorDiv.classList.add('show');
        return;
    }

    try {
        const updateData = {};
        if (phone) updateData.phone = phone;
        if (whatsapp) updateData.whatsapp = whatsapp;
        if (instructions) updateData.instructions = instructions;

        const response = await fetch(`${API_URL}/me`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify(updateData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'Update failed');
        }

        // Update current user
        currentUser = data;

        // Reload profile
        loadUserProfile();

        // Clear form and show success
        errorDiv.textContent = 'Profile updated successfully!';
        errorDiv.style.backgroundColor = '#d4edda';
        errorDiv.style.color = '#155724';
        errorDiv.style.borderColor = '#c3e6cb';
        errorDiv.classList.add('show');

        // Clear form
        document.getElementById('updateForm').reset();

        // Hide message after 3 seconds
        setTimeout(() => {
            errorDiv.classList.remove('show');
        }, 3000);
    } catch (error) {
        errorDiv.textContent = error.message;
        errorDiv.style.backgroundColor = '#f8d7da';
        errorDiv.style.color = '#721c24';
        errorDiv.style.borderColor = '#f5c6cb';
        errorDiv.classList.add('show');
    }
}

function copyProfileLink() {
    const profileUrl = document.getElementById('profileUrl');
    profileUrl.select();
    document.execCommand('copy');

    // Show feedback
    const btn = event.target;
    const originalText = btn.textContent;
    btn.textContent = '✓ Copied!';
    setTimeout(() => {
        btn.textContent = originalText;
    }, 2000);
}

// ============================================================================
// QR CODE FUNCTIONS
// ============================================================================

async function generateQRCode() {
    if (!currentUser) return;

    const qrContainer = document.getElementById('qrContainer');
    qrContainer.innerHTML = '<div class="loading">Generating QR code...</div>';

    try {
        const response = await fetch(`${API_URL}/qr/${currentUser.username}`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });

        if (!response.ok) {
            throw new Error('Failed to generate QR code');
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);

        // Store for download
        window.qrCodeUrl = url;

        // Display QR code
        const img = document.createElement('img');
        img.src = url;
        img.alt = 'QR Code';
        qrContainer.innerHTML = '';
        qrContainer.appendChild(img);

        // Show download button
        document.getElementById('downloadQRBtn').style.display = 'block';
    } catch (error) {
        qrContainer.innerHTML = `<div class="error-message show">${error.message}</div>`;
    }
}

function downloadQRCode() {
    if (!window.qrCodeUrl) return;

    const link = document.createElement('a');
    link.href = window.qrCodeUrl;
    link.download = `${currentUser.username}_qr.png`;
    link.click();
}

// ============================================================================
// ANALYTICS (BONUS FEATURE)
// ============================================================================

async function loadAnalytics() {
    if (!currentToken || !currentUser) return;

    const analyticsContainer = document.getElementById('analyticsContainer');

    try {
        const response = await fetch(`${API_URL}/analytics/visits`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });

        if (!response.ok) {
            analyticsContainer.innerHTML = '<p>Analytics data not available</p>';
            return;
        }

        const analytics = await response.json();

        analyticsContainer.innerHTML = `
            <p><strong>Total Profile Views:</strong> ${analytics.total_visits}</p>
            <p><strong>Views (Last 30 Days):</strong> ${analytics.visits_last_30_days}</p>
        `;
    } catch (error) {
        console.error('Error loading analytics:', error);
        analyticsContainer.innerHTML = '<p>Error loading analytics</p>';
    }
}
