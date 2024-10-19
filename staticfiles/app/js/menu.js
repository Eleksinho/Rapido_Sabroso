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

document.getElementById('sortAscBtn').addEventListener('click', function() {
    sortProducts(true); // Ordenar de menor a mayor
});

document.getElementById('sortDescBtn').addEventListener('click', function() {
    sortProducts(false); // Ordenar de mayor a menor
});

function sortProducts(isAscending) {
    const productosContainer = document.getElementById('productos-container');
    const productos = Array.from(productosContainer.getElementsByClassName('producto-card'));

    // Ordenar los productos según el precio
    productos.sort((a, b) => {
        let precioA = parseFloat(a.querySelector('.producto-precio').innerText.replace('$', '').replace('.', '').replace(',', '.').trim());
        let precioB = parseFloat(b.querySelector('.producto-precio').innerText.replace('$', '').replace('.', '').replace(',', '.').trim());
        return isAscending ? precioA - precioB : precioB - precioA; // Ordenar según la dirección
    });

    // Limpiar el contenedor y agregar los productos ordenados
    productosContainer.innerHTML = ''; // Limpiar el contenedor
    productos.forEach(producto => {
        productosContainer.appendChild(producto); // Agregar cada producto ordenado
    });

    // Opcional: Reestablecer el filtrado
    filtrarProductos();
}

function actualizarPrecioMinimo(valor) {
    document.getElementById("precio-minimo").innerText = valor.toLocaleString();
    ajustarCubos(valor, 'min');
}

function actualizarPrecioMaximo(valor) {
    document.getElementById("precio-maximo").innerText = valor.toLocaleString();
    ajustarCubos(valor, 'max');
}

function ajustarCubos(valor, tipo) {
    let porcentaje = (valor / 50000) * 100; // Convertir a porcentaje basado en el rango de 0 a 50000
    if (tipo === 'min') {
        document.querySelectorAll(".cube")[0].querySelectorAll(".a, .b, .c, .d").forEach(c => c.style.width = porcentaje + "%");
    } else {
        document.querySelectorAll(".cube")[1].querySelectorAll(".a, .b, .c, .d").forEach(c => c.style.width = porcentaje + "%");
    }
}