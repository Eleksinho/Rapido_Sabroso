document.addEventListener("DOMContentLoaded", function() {
    const carrusel = document.getElementById("marcaCarrusel");
    const carruselInner = carrusel.querySelector(".marca-cards-inner");  // Asegúrate de que esta clase sea correcta
    let scrollAmount = 0;
    const scrollStep = 0.2;  // Disminuye este valor para hacerlo más lento
    let isPaused = false;  // Bandera para pausar el movimiento

    function scrollCarrusel() {
        const maxScroll = carruselInner.scrollWidth - carrusel.clientWidth;

        if (!isPaused) {  // Solo mueve el carrusel si no está pausado
            if (scrollAmount < maxScroll) {
                scrollAmount += scrollStep;
                carrusel.scrollLeft = scrollAmount;
            } else {
                // Vuelve al principio cuando llega al final
                scrollAmount = 0;
                carrusel.scrollLeft = scrollAmount;
            }
        }

        // Solicita el siguiente cuadro de animación
        requestAnimationFrame(scrollCarrusel);
    }

    // Pausar el carrusel al pasar el mouse
    carrusel.addEventListener("mouseenter", function() {
        isPaused = true;
    });

    // Reanudar el carrusel al quitar el mouse
    carrusel.addEventListener("mouseleave", function() {
        isPaused = false;
    });

    // Comienza la animación
    requestAnimationFrame(scrollCarrusel);
});

var slider = document.getElementById('rango-precio');

noUiSlider.create(slider, {
    start: [0, 50000], // Rango inicial
    connect: true,
    range: {
        'min': 0,
        'max': 50000
    },
    step: 1000,
    tooltips: [true, true], // Activar tooltips para ambos valores
    format: {
        to: (value) => value.toLocaleString(),
        from: (value) => Number(value.replace(',', ''))
    }
});

// Función debounce
// Reutiliza la función debounce
function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Función para buscar productos por nombre y filtrar por precio
const filtrarProductos = function() {
    // Obtener el valor de búsqueda
    const busqueda = document.getElementById('busqueda-producto').value.toLowerCase();
    
    // Obtener valores del slider transformados a número
    const precioMinimo = parseFloat(slider.noUiSlider.get()[0].replace(/\D/g, '')) || 0;
    const precioMaximo = parseFloat(slider.noUiSlider.get()[1].replace(/\D/g, '')) || Infinity;

    // Seleccionar todos los productos
    const productos = document.querySelectorAll('.producto-card');

    productos.forEach(producto => {
        // Obtener el nombre del producto y hacerlo minúsculas para la comparación
        const nombreProducto = producto.querySelector('.producto-nombre').innerText.toLowerCase();
        
        // Obtener el precio del producto, remover símbolo $ y puntos/comas
        const precioTexto = producto.querySelector('.producto-precio').innerText
                            .replace('$', '')        // Eliminar el símbolo $
                            .replace(/\./g, '')      // Eliminar puntos (separadores de miles)
                            .replace(',', '.')       // Reemplazar comas por puntos si son decimales
                            .trim();                 // Remover espacios adicionales
        
        const precioProducto = parseFloat(precioTexto) || 0;

        // Comprobar si el producto cumple con la búsqueda por nombre y está dentro del rango de precios
        const cumpleBusqueda = nombreProducto.includes(busqueda);
        const cumplePrecio = precioProducto >= precioMinimo && precioProducto <= precioMaximo;

        // Mostrar u ocultar el producto basado en ambos filtros
        if (cumpleBusqueda && cumplePrecio) {
            producto.style.display = ''; // Mostrar el producto
        } else {
            producto.style.display = 'none'; // Ocultar el producto
        }
    });
};

// Evento para el campo de búsqueda con debounce aplicado
document.getElementById('busqueda-producto').addEventListener('input', debounce(filtrarProductos, 300));

// Personalizar los tooltips del slider
slider.noUiSlider.on('update', function(values, handle) {
    if (handle === 0) {
        document.getElementById('precio-minimo').innerText = values[0]; // Tooltip de precio mínimo
    } else {
        document.getElementById('precio-maximo').innerText = values[1]; // Tooltip de precio máximo
    }
    filtrarProductos(); // Llama a la función filtradora
});


// Evento para el campo de búsqueda
document.getElementById('busqueda-producto').addEventListener('input', filtrarProductos);

function ordenarProductos(orden) {
    const productosContainer = document.getElementById('productos-container');
    const productos = Array.from(productosContainer.querySelectorAll('.producto-card'));

    // Ordenar productos basado en el precio
    productos.sort((a, b) => {
        const precioA = parseFloat(a.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0;
        const precioB = parseFloat(b.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0;

        return orden === 'asc' ? precioA - precioB : precioB - precioA; // Ascendente o descendente
    });

    // Limpiar el contenedor de productos
    productosContainer.innerHTML = '';

    // Añadir los productos ordenados de nuevo al contenedor
    productos.forEach(producto => {
        productosContainer.appendChild(producto);
    });
}
