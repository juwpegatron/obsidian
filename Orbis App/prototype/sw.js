/* Orbis service worker.
 * Strategy:
 *   - Navigations and HTML: network-first (fresh content, cache as fallback).
 *   - Static assets: cache-first (fast, offline-capable).
 */

const CACHE = 'orbis-cache-v1';

const PRECACHE = [
  '/',
  '/index.html',
  '/app.html',
  '/manifest.webmanifest',
  '/icons/orbit.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

function isHtmlRequest(request) {
  if (request.mode === 'navigate') {
    return true;
  }
  const accept = request.headers.get('accept') || '';
  return accept.indexOf('text/html') !== -1;
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') {
    return;
  }

  // Never intercept the API: always go to the network.
  const url = new URL(request.url);
  if (url.pathname.indexOf('/api/') === 0) {
    return;
  }

  if (isHtmlRequest(request)) {
    // Network-first for navigations and HTML documents.
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE)
            .then((cache) => cache.put(request, copy))
            .catch(() => {});
          return response;
        })
        .catch(() => caches.match(request).then((cached) => {
          return cached || caches.match('/app.html');
        }))
    );
    return;
  }

  // Cache-first for everything else (static assets).
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) {
        return cached;
      }
      return fetch(request).then((response) => {
        if (response && response.ok && url.origin === self.location.origin) {
          const copy = response.clone();
          caches.open(CACHE)
            .then((cache) => cache.put(request, copy))
            .catch(() => {});
        }
        return response;
      });
    })
  );
});
