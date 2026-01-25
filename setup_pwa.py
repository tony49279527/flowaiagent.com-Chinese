import os
import re
import json
from PIL import Image

BASE_DIR = r'c:\Users\sales-Tony\.gemini\antigravity\playground\vector-apogee'
FAVICON = os.path.join(BASE_DIR, 'favicon.png')
MANIFEST_FILE = os.path.join(BASE_DIR, 'manifest.json')
SW_FILE = os.path.join(BASE_DIR, 'sw.js')

def generate_icons():
    print("Generating PWA icons...")
    if not os.path.exists(FAVICON):
        print("Error: favicon.png not found!")
        return
        
    try:
        with Image.open(FAVICON) as img:
            # icon-192.png
            img.resize((192, 192), Image.Resampling.LANCZOS).save(os.path.join(BASE_DIR, 'icon-192.png'))
            # icon-512.png
            img.resize((512, 512), Image.Resampling.LANCZOS).save(os.path.join(BASE_DIR, 'icon-512.png'))
        print("Icons generated: icon-192.png, icon-512.png")
    except Exception as e:
        print(f"Failed to generate icons: {e}")

def create_manifest():
    print("Creating manifest.json...")
    manifest = {
        "name": "FlowAI Agent",
        "short_name": "FlowAI",
        "start_url": "index.html",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#667eea",
        "icons": [
            {
                "src": "icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    with open(MANIFEST_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

def create_service_worker():
    print("Creating sw.js...")
    sw_content = """
const CACHE_NAME = 'flowai-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/index.html',
    '/styles.css',
    '/script.js',
    '/mobile-menu.js',
    '/favicon.png',
    '/icon-192.png'
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
"""
    with open(SW_FILE, 'w', encoding='utf-8') as f:
        f.write(sw_content)

def inject_pwa_meta():
    print("Injecting PWA meta tags and script...")
    updated_files = 0
    pwa_head = """    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#667eea">
    <link rel="apple-touch-icon" href="icon-192.png">"""
    
    pwa_script = """    <script>
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('sw.js')
                    .then(reg => console.log('SW registered'))
                    .catch(err => console.log('SW failed', err));
            });
        }
    </script>"""

    for filename in os.listdir(BASE_DIR):
        if filename.endswith('.html'):
            file_path = os.path.join(BASE_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # Inject Head Meta
            if 'manifest.json' not in content:
                # Insert before </head>
                if '</head>' in content:
                    new_content = new_content.replace('</head>', pwa_head + '\n</head>')
            
            # Inject Script
            if 'serviceWorker.register' not in content:
                # Insert before </body>
                if '</body>' in content:
                    new_content = new_content.replace('</body>', pwa_script + '\n</body>')
            
            if content != new_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files += 1
                print(f"Updated {filename}")

    print(f"HTML injection complete. {updated_files} files updated.")

if __name__ == "__main__":
    generate_icons()
    create_manifest()
    create_service_worker()
    inject_pwa_meta()
