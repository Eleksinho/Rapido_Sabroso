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

    carrusel.addEventListener("mouseenter", () => { isPaused = true; });
    carrusel.addEventListener("mouseleave", () => { isPaused = false; });
    requestAnimationFrame(scrollCarrusel);

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

    // Inicializar Fuse.js
    const productos = Array.from(document.querySelectorAll('.producto-card'));
    const productosData = productos.map(producto => ({
        elemento: producto,
        nombre: producto.querySelector('.producto-nombre').innerText.toLowerCase(),
        descripcion: producto.querySelector('.producto-descripcion').innerText.toLowerCase(),
        precio: parseFloat(producto.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0
    }));

    const options = {
        keys: ['nombre', 'descripcion'],
        threshold: 0.3,
        distance: 100,
        minMatchCharLength: 1,
        includeScore: true
    };

    const fuse = new Fuse(productosData, options);

    let timeoutFilter;

    const filtrarProductos = function() {
        clearTimeout(timeoutFilter);
        timeoutFilter = setTimeout(() => {
            const busqueda = document.getElementById('busqueda-producto').value.toLowerCase().trim();
            const precioMinimo = parseFloat(slider.noUiSlider.get()[0].replace(/\D/g, '')) || 0;
            const precioMaximo = parseFloat(slider.noUiSlider.get()[1].replace(/\D/g, '')) || Infinity;

            if (busqueda === '') {
                // Si el campo de búsqueda está vacío, mostrar todos los productos que cumplen con el filtro de precio
                productos.forEach(producto => {
                    const precioTexto = producto.querySelector('.producto-precio').innerText
                        .replace('$', '')
                        .replace(/\./g, '')
                        .replace(',', '.')
                        .trim();

                    const precioProducto = parseFloat(precioTexto) || 0;
                    const cumplePrecio = precioProducto >= precioMinimo && precioProducto <= precioMaximo;

                    producto.style.display = cumplePrecio ? '' : 'none';
                });
                return;
            }

            // Realiza la búsqueda con Fuse.js
            const resultados = fuse.search(busqueda);
            const resultadosNombres = new Set(resultados.map(resultado => resultado.item.nombre));

            productos.forEach(producto => {
                const nombreProducto = producto.querySelector('.producto-nombre').innerText.toLowerCase();
                const precioTexto = producto.querySelector('.producto-precio').innerText
                    .replace('$', '')
                    .replace(/\./g, '')
                    .replace(',', '.')
                    .trim();

                const precioProducto = parseFloat(precioTexto) || 0;
                const cumplePrecio = precioProducto >= precioMinimo && precioProducto <= precioMaximo;

                producto.style.display = (resultadosNombres.has(nombreProducto) && cumplePrecio) ? '' : 'none';
            });
        }, 300);
    };

    document.getElementById('busqueda-producto').addEventListener('input', debounce(filtrarProductos, 300));

    slider.noUiSlider.on('update', debounce(function(values, handle) {
        if (handle === 0) {
            document.getElementById('precio-minimo').innerText = values[0];
        } else {
            document.getElementById('precio-maximo').innerText = values[1];
        }
        filtrarProductos(); 
    }, 300));

   
});
function ordenarProductos(orden) {
    const productosContainer = document.getElementById('productos-container');
    const productos = Array.from(productosContainer.querySelectorAll('.producto-card'));

    productos.sort((a, b) => {
        const precioA = parseFloat(a.querySelector('.producto-precio').innerText.replace(/[^\d.-]/g, '')) || 0;
        const precioB = parseFloat(b.querySelector('.producto-precio').innerText.replace(/[^\d.-]/g, '')) || 0;

        // Ordena según el parámetro 'orden'
        return orden === 'asc' ? precioA - precioB : precioB - precioA;
    });

    // Después de ordenar, reordena los elementos en el contenedor
    productos.forEach(producto => productosContainer.appendChild(producto));
}
function ordenarProductos(orden) {
    const productosContainer = document.getElementById('productos-container');
    const productos = Array.from(productosContainer.querySelectorAll('.producto-card'));

    productos.sort((a, b) => {
        const precioA = parseFloat(a.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0;
        const precioB = parseFloat(b.querySelector('.producto-precio').innerText.replace(/\D/g, '')) || 0;

        return orden === 'asc' ? precioA - precioB : precioB - precioA;
    });

    productosContainer.innerHTML = '';
    productos.forEach(producto => {
        productosContainer.appendChild(producto);
    });
}
// Botones para ordenar
document.getElementById("sortAscBtn").addEventListener('click', function() {
    ordenarProductos('asc');
});

document.getElementById("sortDescBtn").addEventListener('click', function() {
    ordenarProductos('desc');
});
