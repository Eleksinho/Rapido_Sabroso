document.addEventListener("DOMContentLoaded", function() {
    const carrusel = document.getElementById("marcaCarrusel");
    const carruselInner = carrusel.querySelector("div");  // El contenedor interno
    let scrollAmount = 0;
    const scrollStep = 0.5;  // Pequeño desplazamiento en cada paso
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
