
const CACHE_NAME = 'flowai-v1';
const ASSETS_TO_CACHE = [
    './',
    './index.html',
    './styles.css',
    './script.js',
    './mobile-menu.js',
    './favicon.png',
    './icon-192.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request).then((fetchRes) => {
                return caches.open(CACHE_NAME).then((cache) => {
                    // Cache regular requests, but be careful with API calls or non-GET
                    if (event.request.method === 'GET') {
                        cache.put(event.request, fetchRes.clone());
                    }
                    return fetchRes;
                });
            });
        })
    );
});
