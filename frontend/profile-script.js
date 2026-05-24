// ============================================================================
// PUBLIC PROFILE PAGE SCRIPT
// ============================================================================

const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    loadPublicProfile();
});

async function loadPublicProfile() {
    // Get username from URL
    const urlParts = window.location.pathname.split('/');
    const username = urlParts[urlParts.length - 1];

    if (!username) {
        showError('No username provided');
        return;
    }

    const profileContent = document.getElementById('profileContent');
    const profileError = document.getElementById('profileError');

    try {
        const response = await fetch(`${API_URL}/u/${username}`);

        if (!response.ok) {
            throw new Error('User not found');
        }

        const profile = await response.json();

        // Format last updated date
        const lastUpdated = new Date(profile.updated_at).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        // Build profile HTML
        const formattedInstructions = profile.instructions || 'Available for contact';

        profileContent.innerHTML = `
            <div class="profile-display">
                <h1>📱 ${profile.username}</h1>
                
                <div class="instructions-box">
                    <div class="instructions-text">${escapeHtml(formattedInstructions)}</div>
                </div>

                <div class="action-buttons">
                    <a href="tel:${profile.phone}" class="btn-call">📞 Call Now</a>
                    <a href="https://wa.me/${profile.whatsapp.replace(/\D/g, '')}" 
                       target="_blank" rel="noopener noreferrer" class="btn-whatsapp">💬 WhatsApp</a>
                </div>

                <p class="last-updated">Last updated: ${lastUpdated}</p>
            </div>
        `;

        profileError.style.display = 'none';
    } catch (error) {
        showError(error.message);
    }
}

function showError(message) {
    const profileContent = document.getElementById('profileContent');
    const profileError = document.getElementById('profileError');

    profileContent.innerHTML = '';
    profileError.textContent = message;
    profileError.style.display = 'block';
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
