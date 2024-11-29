// Acceso a Mapbox con tu token de API
mapboxgl.accessToken = 'pk.eyJ1IjoiZ29kbGlzYSIsImEiOiJjbTQxenp5enoyb3FhMmpxMnRqaDRjdnU4In0.wWcDCZMMKGiHqm0OZIrWCw';

// Crear el mapa de Mapbox
var map = new mapboxgl.Map({
    container: 'map',  // El contenedor donde se mostrará el mapa
    style: 'mapbox://styles/mapbox/streets-v11', // Estilo de mapa
    zoom: 14  // Zoom por defecto, se ajustará según la ubicación
});

// Función para calcular la distancia entre dos puntos (en kilómetros) usando la fórmula de Haversine
function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radio de la Tierra en km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distancia en km
}

// Función para encontrar el local más cercano
function encontrarLocalMasCercano(locales, latUsuario, lonUsuario) {
    let localMasCercano = null;
    let distanciaMinima = Infinity;

    locales.forEach(function(local) {
        // Calcular la distancia entre el local y la ubicación del usuario
        const distancia = calcularDistancia(latUsuario, lonUsuario, local.lat, local.lon);
        
        // Verificar si este local es el más cercano
        if (distancia < distanciaMinima) {
            distanciaMinima = distancia;
            localMasCercano = local;
        }
    });

    return localMasCercano;
}

// Función para trazar la ruta utilizando Mapbox Directions API
function trazarRuta(lat1, lon1, lat2, lon2) {
    var url = `https://api.mapbox.com/directions/v5/mapbox/driving/${lon1},${lat1};${lon2},${lat2}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`;
    
    // Hacer la solicitud a la API de Directions
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.routes.length > 0) {
                const route = data.routes[0].geometry; // Obtener la geometría de la ruta
                map.addLayer({
                    "id": "route",
                    "type": "line",
                    "source": {
                        "type": "geojson",
                        "data": {
                            "type": "Feature",
                            "geometry": route
                        }
                    },
                    "paint": {
                        "line-color": "#3887be",
                        "line-width": 5
                    }
                });
            }
        })
        .catch(error => {
            console.error("Error al trazar la ruta:", error);
        });
}

// Obtener la ubicación actual del usuario
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;

            // Establecer la vista del mapa en la ubicación del usuario
            map.setCenter([lon, lat]);

            // Agregar un marcador en la ubicación actual
            new mapboxgl.Marker()
                .setLngLat([lon, lat])
                .setPopup(new mapboxgl.Popup().setHTML("<h3>Estás aquí</h3>"))
                .addTo(map);

            // Suposición de que los datos de los locales se pasan desde el backend en JSON
            var locales = JSON.parse(localesData);  // `localesData` será un objeto JSON pasado desde el servidor
            agregarLocales(locales, lat, lon);  // Agregar los marcadores de los locales y encontrar el más cercano
        }, function(error) {
            alert("No se pudo obtener la ubicación.");
        });
    } else {
        alert("La geolocalización no es soportada por este navegador.");
    }
}

// Función para agregar marcadores para cada local
function agregarLocales(locales, latUsuario, lonUsuario) {
    let localMasCercano = encontrarLocalMasCercano(locales, latUsuario, lonUsuario);

    locales.forEach(function(local) {
        const isMasCercano = local === localMasCercano;

        // Agregar el marcador en el mapa
        let marker = new mapboxgl.Marker()
            .setLngLat([local.lon, local.lat]);

        // Si es el local más cercano, añadir una etiqueta especial
        if (isMasCercano) {
            marker.setPopup(new mapboxgl.Popup().setHTML(
                `<h3>LOCAL MÁS CERCANO</h3><p>${local.name}</p><p>${local.address}</p>`
            ));
            
            // Trazar la ruta hacia el local más cercano
            trazarRuta(latUsuario, lonUsuario, local.lat, local.lon);
        } else {
            marker.setPopup(new mapboxgl.Popup().setHTML(
                `<h3>${local.name}</h3><p>${local.address}</p>`
            ));
        }

        marker.addTo(map);
    });
}

// Cuando se carga el mapa, obtener la ubicación actual y agregar los locales
map.on('load', function() {
    getLocation();  // Llamar a la función para obtener la ubicación del usuario
});
