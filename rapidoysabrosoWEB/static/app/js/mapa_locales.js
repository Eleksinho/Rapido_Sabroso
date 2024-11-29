// Esperamos que el contenido se cargue completamente
document.addEventListener('DOMContentLoaded', function() {
    // Crear el mapa y establecer su vista inicial
    var map = L.map('map').setView([0, 0], 13);  // Coords por defecto

    // Agregar capa de tiles (OpenStreetMap en este caso)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Verificar si el navegador soporta geolocalización
    if (navigator.geolocation) {
        // Obtener la posición actual del usuario
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
        
            map.setView([lat, lon], 13); // Actualiza la vista del mapa a la ubicación actual
        
            L.marker([lat, lon]).addTo(map)
                .bindPopup('Estás aquí')
                .openPopup();
        }, function(error) {
            alert("No se pudo obtener tu ubicación.");
        }, {
            enableHighAccuracy: true, // Intenta obtener la ubicación más precisa
            timeout: 10000, // Espera hasta 10 segundos para obtener la ubicación
            maximumAge: 0 // No usar ubicaciones almacenadas en caché
        });
    } else {
        alert("La geolocalización no es soportada por este navegador.");
    }
});

navigator.geolocation.getCurrentPosition(function(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;

    map.setView([lat, lon], 13); // Actualiza la vista del mapa a la ubicación actual

    L.marker([lat, lon]).addTo(map)
        .bindPopup('Estás aquí')
        .openPopup();
}, function(error) {
    alert("No se pudo obtener tu ubicación.");
}, {
    enableHighAccuracy: true, // Intenta obtener la ubicación más precisa
    timeout: 10000, // Espera hasta 10 segundos para obtener la ubicación
    maximumAge: 0 // No usar ubicaciones almacenadas en caché
});