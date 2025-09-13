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
          return cachedResponse || fetchPromise;
        });
      })
    );
    return;
  }

  // For other GET requests (app shell), use a robust network-falling-back-to-cache strategy
  if (e.request.method === 'GET') {
    e.respondWith(
      caches.open(CACHE_NAME).then(cache => {
        return fetch(e.request)
          .then(networkResponse => {
            // If we get a good response, cache it and return it
            if (networkResponse.ok) {
              cache.put(e.request, networkResponse.clone());
            }
            return networkResponse;
          })
          .catch(() => {
            // If the network fails entirely, immediately try the cache
            return cache.match(e.request).then(cachedResponse => {
              // If we have a cached response, serve it, otherwise show offline page
              return cachedResponse || new Response('<!doctype html><meta charset="utf-8"><title>Offline</title><h1>You are Offline</h1><p>This page could not be loaded. Please check your network connection.</p>', { headers: {'Content-Type':'text/html; charset=utf-8'} });
            });
          });
      })
    );
  }
});
