// public/sw.js
// Store the authorization header value
let storedAuthHeader = null;

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    const request = event.request;

    // If this request has an Authorization header, store it for future use
    if (request.headers.has('Authorization')) {
        storedAuthHeader = request.headers.get('Authorization');
        return;
    }

    // If we have a stored Authorization header, add it to the request
    if (storedAuthHeader) {
        // Clone the request to modify headers
        const modifiedRequest = new Request(request.url, {
            method: request.method,
            headers: {
                ...Object.fromEntries(request.headers),
                'Authorization': storedAuthHeader
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
                        // Clear stored header if authentication fails
                        storedAuthHeader = null;
                        console.error('Authentication failed');
                    }
                    return response;
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                    throw error;
                })
        );
    }
});