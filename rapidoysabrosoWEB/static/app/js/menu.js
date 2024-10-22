document.addEventListener("DOMContentLoaded", function() {
    const carrusel = document.getElementById("marcaCarrusel");
    const carruselInner = carrusel.querySelector(".marca-cards-inner");
    let scrollAmount = 0;
    const scrollStep = 0.2;
    let isPaused = false;

    function scrollCarrusel() {
        const maxScroll = carruselInner.scrollWidth - carrusel.clientWidth;

        if (!isPaused) {
            if (scrollAmount < maxScroll) {
                scrollAmount += scrollStep;
                carrusel.scrollLeft = scrollAmount;
            } else {
                scrollAmount = 0;
                carrusel.scrollLeft = scrollAmount;
            }
        }
        requestAnimationFrame(scrollCarrusel);
    }

    carrusel.addEventListener("mouseenter", function() {
        isPaused = true;
    });

    carrusel.addEventListener("mouseleave", function() {
        isPaused = false;
    });

    requestAnimationFrame(scrollCarrusel);
});

// Configuración del slider de rango de precios
var slider = document.getElementById('rango-precio');

noUiSlider.create(slider, {
    start: [0, 50000],
    connect: true,
    range: {
        'min': 0,
        'max': 50000
    },
    step: 1000,
    tooltips: [true, true],
    format: {
        to: (value) => value.toLocaleString(),
        from: (value) => Number(value.replace(',', ''))
    }
});

// Función debounce
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Función para filtrar productos por nombre y precio
const filtrarProductos = function() {
    const busqueda = document.getElementById('busqueda-producto').value.toLowerCase();
    const precioMinimo = parseFloat(slider.noUiSlider.get()[0].replace(/\D/g, '')) || 0;
    const precioMaximo = parseFloat(slider.noUiSlider.get()[1].replace(/\D/g, '')) || Infinity;
    const productos = document.querySelectorAll('.producto-card');

    const productosFiltrados = Array.from(productos).filter(producto => {
        const nombreProducto = producto.querySelector('.producto-nombre').innerText.toLowerCase();
        const precioTexto = producto.querySelector('.producto-precio').innerText
                            .replace('$', '').replace(/\./g, '').replace(',', '.').trim();
        const precioProducto = parseFloat(precioTexto) || 0;
        const cumpleBusqueda = nombreProducto.includes(busqueda);
        const cumplePrecio = precioProducto >= precioMinimo && precioProducto <= precioMaximo;
        return cumpleBusqueda && cumplePrecio;
    });

    const productosContainer = document.getElementById('productos-container');
    productosContainer.innerHTML = ''; // Limpiar el contenedor

    // Crear una nueva fila para los productos filtrados
    const fila = document.createElement('div');
    fila.className = 'row'; // Aseguramos que la estructura de fila se mantenga

    productosFiltrados.forEach(producto => {
        fila.appendChild(producto.parentElement); // Agregar la columna dentro de la fila
    });

    productosContainer.appendChild(fila); // Insertar la fila en el contenedor
};

// Evento para el campo de búsqueda con debounce aplicado
document.getElementById('busqueda-producto').addEventListener('input', debounce(filtrarProductos, 300));

// Personalizar los tooltips del slider
slider.noUiSlider.on('update', function(values, handle) {
    if (handle === 0) {
        document.getElementById('precio-minimo').innerText = values[0];
    } else {
        document.getElementById('precio-maximo').innerText = values[1];
    }
    filtrarProductos(); // Llama a la función filtradora
});

// Función para ordenar productos por precio
function ordenarProductos(orden) {
    const productosContainer = document.getElementById('productos-container');
    const productos = Array.from(productosContainer.querySelectorAll('.producto-card'));

    productos.sort((a, b) => {
        const precioA = parseFloat(a.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0;
        const precioB = parseFloat(b.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0;

        return orden === 'asc' ? precioA - precioB : precioB - precioA;
    });

    productosContainer.innerHTML = ''; // Limpiar el contenedor

    // Crear un nuevo contenedor de fila (row)
    const fila = document.createElement('div');
    fila.className = 'row'; // Clase de Bootstrap

    productos.forEach(producto => {
        fila.appendChild(producto.parentElement);  // Agregar la columna con la tarjeta dentro de la fila
    });

    productosContainer.appendChild(fila);
} 