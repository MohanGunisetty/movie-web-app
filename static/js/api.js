const API_URL = '/api';

const api = {
    // Helper for authenticated requests
    async fetch(endpoint, options = {}) {
        const token = localStorage.getItem('token');
        const headers = {
            'Content-Type': 'application/json',
            ...(options.headers || {})
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // HandleFormData
        if (options.body instanceof FormData) {
            delete headers['Content-Type'];
        }

        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Token expired or invalid
            this.logout();
            window.location.href = '/static/login.html';
            return;
        }

        return response;
    },

    setToken(token) {
        localStorage.setItem('token', token);
    },

    getToken() {
        return localStorage.getItem('token');
    },

    parseJwt(token) {
        try {
            return JSON.parse(atob(token.split('.')[1]));
        } catch (e) {
            return null;
        }
    },

    getUserRole() {
        const token = this.getToken();
        if (!token) return null;
        const payload = this.parseJwt(token);
        return payload ? payload.role : null;
    },

    isLoggedIn() {
        return !!this.getToken();
    },

    logout() {
        localStorage.removeItem('token');
        window.location.href = '/static/index.html';
    }
};

// UI Helpers
function updateNav() {
    const navLinks = document.getElementById('nav-links');
    if (!navLinks) return;

    if (api.isLoggedIn()) {
        const role = api.getUserRole();
        let html = `
            <a href="/static/index.html">Browse</a>
            <a href="/static/profile.html">Profile</a>
        `;
        if (role === 'ADMIN') {
            html += `<a href="/static/admin/dashboard.html">Admin Panel</a>`;
        }
        html += `<a href="#" onclick="api.logout()">Logout</a>`;
        navLinks.innerHTML = html;
    } else {
        navLinks.innerHTML = `
            <a href="/static/login.html">Login</a>
            <a href="/static/register.html" class="btn btn-secondary" style="padding: 8px 16px; margin-left: 20px;">Sign Up</a>
        `;
    }
}

document.addEventListener('DOMContentLoaded', updateNav);
