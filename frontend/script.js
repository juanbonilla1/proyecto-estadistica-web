const API_BASE = 'http://localhost:5000/api';

// Función para cargar datos
async function cargarDatos() {
    const input = document.getElementById('datosInput');
    const infoBox = document.getElementById('datosInfo');
    
    const datosTexto = input.value.trim();
    if (!datosTexto) {
        mostrarError(infoBox, 'Por favor, ingrese algunos datos');
        return;
    }

    // Procesar entrada (acepta comas, espacios, o ambos)
    const datosArray = datosTexto.split(/[\s,]+/).filter(val => val !== '');
    const datosNumeros = datosArray.map(num => parseFloat(num));

    // Validar que todos sean números
    if (datosNumeros.some(isNaN)) {
        mostrarError(infoBox, 'Por favor, ingrese solo números válidos');
        return;
    }

    try {
        mostrarCargando(infoBox, 'Cargando datos...');
        
        const response = await fetch(`${API_BASE}/cargar-datos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ datos: datosNumeros })
        });

        const resultado = await response.json();

        if (response.ok) {
            mostrarExito(infoBox, `✅ ${resultado.mensaje}. Se cargaron ${resultado.cantidad} datos.`);
        } else {
            mostrarError(infoBox, `Error: ${resultado.error}`);
        }
    } catch (error) {
        mostrarError(infoBox, 'Error de conexión con el servidor');
    }
}

// Función para obtener todas las estadísticas
async function obtenerEstadisticas() {
    try {
        const response = await fetch(`${API_BASE}/estadisticas-completas`);
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultados(resultado);
        } else {
            alert(`Error: ${resultado.error}`);
        }
    } catch (error) {
        alert('Error de conexión con el servidor');
    }
}

// Función para obtener tendencia central
async function obtenerTendenciaCentral() {
    try {
        const response = await fetch(`${API_BASE}/tendencia-central`);
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultados(resultado);
        } else {
            alert(`Error: ${resultado.error}`);
        }
    } catch (error) {
        alert('Error de conexión con el servidor');
    }
}

// Función para obtener medidas de dispersión
async function obtenerDispersion() {
    try {
        const response = await fetch(`${API_BASE}/dispersion`);
        const resultado = await response.json();
        
        if (response.ok) {
            mostrarResultados(resultado);
        } else {
            alert(`Error: ${resultado.error}`);
        }
    } catch (error) {
        alert('Error de conexión con el servidor');
    }
}

// Función para generar gráficos
async function generarGrafico(tipo) {
    const imagen = document.getElementById('graficoImagen');
    const container = document.getElementById('graficoContainer');
    
    try {
        imagen.style.display = 'none';
        mostrarCargando(container, 'Generando gráfico...');
        
        const response = await fetch(`${API_BASE}/grafico/${tipo}`);
        const resultado = await response.json();
        
        if (response.ok) {
            imagen.src = resultado.imagen;
            imagen.style.display = 'block';
            container.innerHTML = '';
            container.appendChild(imagen);
        } else {
            mostrarError(container, `Error: ${resultado.error}`);
        }
    } catch (error) {
        mostrarError(container, 'Error de conexión con el servidor');
    }
}

// Función para mostrar resultados
function mostrarResultados(datos) {
    const container = document.getElementById('resultados');
    
    const cards = Object.entries(datos).map(([clave, valor]) => {
        const nombreFormateado = formatearNombre(clave);
        return `
            <div class="stat-card">
                <h3>${nombreFormateado}</h3>
                <div class="stat-value">${typeof valor === 'number' ? valor.toFixed(4) : valor}</div>
            </div>
        `;
    }).join('');

    container.innerHTML = cards;
}

// Funciones auxiliares para mostrar mensajes
function mostrarError(elemento, mensaje) {
    elemento.innerHTML = `<span class="error">❌ ${mensaje}</span>`;
    elemento.className = 'info-box error';
}

function mostrarExito(elemento, mensaje) {
    elemento.innerHTML = `<span class="success">${mensaje}</span>`;
    elemento.className = 'info-box success';
}

function mostrarCargando(elemento, mensaje) {
    elemento.innerHTML = `<span>⏳ ${mensaje}</span>`;
    elemento.className = 'info-box loading';
}

function formatearNombre(texto) {
    return texto
        .split('_')
        .map(palabra => palabra.charAt(0).toUpperCase() + palabra.slice(1))
        .join(' ');
}

// Event listeners para mejor UX
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('datosInput');
    
    // Ejemplo de datos pre-cargados
    textarea.placeholder = 'Ejemplo: 12.5, 15.2, 18.7, 22.1, 14.8, 19.3, 16.4, 20.9, 13.6, 17.8';
    
    // Permitir Enter para cargar datos
    textarea.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            cargarDatos();
        }
    });
});