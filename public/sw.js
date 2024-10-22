// public/sw.js
const AUTH_HEADER = 'Basic ' + btoa('username:password'); // Replace with your auth credentials

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    const request = event.request;

    // Check if request already has auth headers
    if (request.headers.has('Authorization')) {
        return;
    }

    // Clone the request to modify headers
    const modifiedRequest = new Request(request.url, {
        method: request.method,
        headers: {
            ...Object.fromEntries(request.headers),
            'Authorization': AUTH_HEADER
        },
        mode: request.mode,
        credentials: request.credentials,
        redirect: request.redirect
    });

    event.respondWith(
        fetch(modifiedRequest)
            .then(response => {
                // Check if response indicates auth failure
                if (response.status === 401) {
                    // You could handle auth failure here
                    console.error('Authentication failed');
                }
                return response;
            })
            .catch(error => {
                console.error('Fetch error:', error);
                throw error;
            })
    );
});