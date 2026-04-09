const API_URL = 'https://secret-voter.onrender.com/api/';

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }

    console.log(`Calling API: ${endpoint}`);

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    // ONLY redirect if the error is 401 AND we aren't already on the login page/endpoints
    if (response.status === 401 && !endpoint.includes('accounts/')) {
        console.log("Unauthorized! Redirecting...");
        localStorage.clear();
        window.location.href = 'login.html';
        return;
    }

    return response;
}