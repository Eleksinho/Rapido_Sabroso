// Función para convertir el precio a un número flotante
function convertirPrecio(precio) {
    return parseFloat(precio.replace('$', '').replace(/\./g, '').replace(',', ''));
}

// Obtener los datos del gráfico desde los elementos del DOM
const fechas = JSON.parse(document.getElementById('fechas-data').textContent);
const precios = JSON.parse(document.getElementById('precios-data').textContent);

// Convertir precios a números flotantes
const preciosFloat = precios.map(precio => precio); // Aquí ya vienen como float
// Crear dimensiones y márgenes del gráfico
const margin = { top: 20, right: 30, bottom: 30, left: 40 };
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// Crear el SVG y añadir un grupo con márgenes
const svg = d3.select("#historial-precios-chart")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Escalas
const x = d3.scaleBand()
    .domain(fechas)
    .range([0, width])
    .padding(0.1);

const y = d3.scaleLinear()
    .domain([0, d3.max(preciosFloat)]) // Asegúrate de establecer el dominio basado en los precios
    .nice()
    .range([height, 0]);

// Ejes
svg.append("g")
    .attr("class", "x-axis")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x));

svg.append("g")
    .attr("class", "y-axis")
    .call(d3.axisLeft(y));

// Línea
const line = d3.line()
    .x((d, i) => x(fechas[i]) + x.bandwidth() / 2) // Usa la posición de la banda
    .y(d => y(d));

// Añadir la línea al gráfico
svg.append("path")
    .datum(preciosFloat)
    .attr("fill", "none")
    .attr("stroke", "rgba(75, 192, 192, 1)")
    .attr("stroke-width", 2)
    .attr("d", line);

// Añadir el área bajo la línea
svg.append("path")
    .datum(preciosFloat)
    .attr("fill", "rgba(75, 192, 192, 0.2)")
    .attr("d", d3.area()
        .x((d, i) => x(fechas[i]) + x.bandwidth() / 2)
        .y0(height)
        .y1(d => y(d))
    );
