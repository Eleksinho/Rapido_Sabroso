// Función para convertir el precio a un número flotante
function convertirPrecio(precio) {
    // Eliminar símbolos de dólar, comas y convertir a número flotante
    return parseFloat(precio.replace('$', '').replace(/\./g, '').replace(',', ''));
}

document.addEventListener('DOMContentLoaded', function () {
    // Obtener los datos del historial de precios desde el contexto
    const fechas = JSON.parse(document.getElementById('fechas-data').textContent);
    const precios = JSON.parse(document.getElementById('precios-data').textContent);

    // Convertir precios a float utilizando la función convertirPrecio
    const preciosFloat = precios.map(convertirPrecio);

    // Crear gráfico
    const ctx = document.getElementById('historial-precios-chart').getContext('2d');
    const historialChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: fechas,
            datasets: [{
                label: 'Historial de precios',
                data: preciosFloat,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Precio ($)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Fecha'
                    }
                }
            }
        }
    });
});
