// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',
    '../static/css/material-dashboard-rtl.css',
    '../static/css/material-dashboard.css.map',
    '../static/css/material-dashboard.min.css',
    '../static/img/apple-icon.png',
    '../static/img/favicon.png',
    '../static/css/material-dashboard.css',
    '../static/demo/demo.css',
    '../static/img/sidebar-1.jpg',
    '../static/img/sidebar-2.jpg',
    '../static/img/sidebar-3.jpg',
    '../static/img/sidebar-4.jpg',
    '../static/js/core/jquery.min.js',
    '../static/js/core/popper.min.js',
    '../static/js/core/bootstrap-material-design.min.js',
    '../static/js/plugins/perfect-scrollbar.jquery.min.js',
    '../static/js/plugins/moment.min.js',
    '../static/js/plugins/sweetalert2.js',
    '../static/js/plugins/jquery.validate.min.js', 
    '../static/js/plugins/jquery.bootstrap-wizard.js', 
    '../static/js/plugins/bootstrap-selectpicker.js ', 
    '../static/js/plugins/bootstrap-datetimepicker.min.js',
    '../static/js/plugins/jquery.dataTables.min.js ' ,
    '../static/js/plugins/bootstrap-tagsinput.js ' ,
    '../static/js/plugins/jasny-bootstrap.min.js ' ,
    '../static/js/plugins/fullcalendar.min.js ' ,
    '../static/js/plugins/jquery-jvectormap.js ' ,
    '../static/js/plugins/nouislider.min.js ' ,
    '../static/js/plugins/arrive.min.js ',
    '../static/js/plugins/chartist.min.js ',
    '../static/js/plugins/bootstrap-notify.js ',
    '../static/js/material-dashboard.js',
    '../static/demo/demo.js',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
// self.addEventListener("fetch", event => {
//     event.respondWith(
//         caches.match(event.request)
//             .then(response => {
//                 return response || fetch(event.request);
//             })
//             .catch(() => {
//                 return caches.match('/offline/');
//             })
//     )
// });

self.addEventListener("fetch", function(event) {
    event.respondWith(
        fetch(event.request)
        .then(function(response) {
            return caches.open(staticCacheName)
            .then(function(c) {
                c.put(event.request.url, response.clone())
                return response;
            })
        })
        .catch(function(e) {
            return caches.match(event.request);
        })
    )
});
