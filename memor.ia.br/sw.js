// Service Worker for memor.ia.br
const CACHE_NAME = 'memor-cache-v2.0';
const API_BASE_URL = 'https://arcreformas.com.br/api/tasks/';

// App shell files to cache on install
const SHELL = [
  '/',
  '/index.php',
  '/manifest.json',
  '/favicon.svg',
  '/icon-192.png',
  '/icon-512.png',
  '/sw.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching App Shell');
        return cache.addAll(SHELL);
      })
      .catch(err => console.error('SW install failed:', err))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(keys.map(key => {
        if (key !== CACHE_NAME) {
          console.log('Service Worker: Clearing old cache', key);
          return caches.delete(key);
        }
      }));
    })
  );
  return self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // For API GET requests to our task boards, use stale-while-revalidate
  if (e.request.method === 'GET' && e.request.url.startsWith(API_BASE_URL)) {
    e.respondWith(
      caches.open(CACHE_NAME).then(cache => {
        return cache.match(e.request).then(cachedResponse => {
          const fetchPromise = fetch(e.request).then(networkResponse => {
            if (networkResponse.ok) {
              cache.put(e.request, networkResponse.clone());
            }
            return networkResponse;
          });
          // Return cached response immediately if available, otherwise wait for network
          return cachedResponse || fetchPromise;
        });
      })
    );
    return;
  }

  // For other GET requests (app shell), use network-first, fallback to cache
  if (e.request.method === 'GET') {
      e.respondWith(
          fetch(e.request)
              .then(networkResponse => {
                  // If fetch is successful, update the cache
                  if (networkResponse.ok) {
                      return caches.open(CACHE_NAME).then(cache => {
                          cache.put(e.request, networkResponse.clone());
                          return networkResponse;
                      });
                  }
                  // If network fails, try to serve from cache
                  return caches.match(e.request).then(cachedResponse => {
                      return cachedResponse || new Response('<!doctype html><meta charset="utf-8"><title>Offline</title><h1>You are Offline</h1><p>This page could not be loaded. Please check your network connection.</p>', { headers: {'Content-Type':'text/html; charset=utf-8'} });
                  });
              })
      );
  }
});
