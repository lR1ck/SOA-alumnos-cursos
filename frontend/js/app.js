/**
 * Sistema Académico UAV - Frontend JavaScript
 * Universidad Autónoma Veracruzana
 *
 * Consume servicios SOAP (Alumnos) y REST (Cursos)
 */

// ============================================
// Configuración
// ============================================

const CONFIG = {
    SOAP_URL: 'http://localhost:5001/soap',
    REST_URL: 'http://localhost:10000/api/cursos',
    SOAP_NAMESPACE: 'http://uav.edu.mx/alumnos'
};

// ============================================
// Utilidades
// ============================================

/**
 * Muestra u oculta el overlay de carga
 */
function toggleLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    if (show) {
        overlay.classList.remove('hidden');
    } else {
        overlay.classList.add('hidden');
    }
}

/**
 * Muestra un mensaje de resultado en un contenedor
 */
function mostrarResultado(containerId, tipo, titulo, contenido) {
    const container = document.getElementById(containerId);
    container.className = `resultado show ${tipo}`;

    let html = `<h4>${titulo}</h4>`;
    if (typeof contenido === 'string') {
        html += `<p>${contenido}</p>`;
    } else if (Array.isArray(contenido)) {
        html += '<ul>';
        contenido.forEach(item => {
            html += `<li>${item}</li>`;
        });
        html += '</ul>';
    } else {
        html += contenido;
    }

    container.innerHTML = html;
}

/**
 * Limpia un formulario
 */
function limpiarFormulario(formId) {
    document.getElementById(formId).reset();
}

/**
 * Escapa caracteres especiales para XML
 */
function escapeXml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&apos;');
}

// ============================================
// Funciones SOAP (Alumnos)
// ============================================

/**
 * Construye el envelope SOAP para registrar alumno
 */
function buildRegistrarAlumnoXML(matricula, nombre, apellido, email) {
    return `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="${CONFIG.SOAP_NAMESPACE}">
    <soap:Body>
        <alum:registrarAlumno>
            <alum:matricula>${escapeXml(matricula)}</alum:matricula>
            <alum:nombre>${escapeXml(nombre)}</alum:nombre>
            <alum:apellido>${escapeXml(apellido)}</alum:apellido>
            <alum:email>${escapeXml(email)}</alum:email>
        </alum:registrarAlumno>
    </soap:Body>
</soap:Envelope>`;
}

/**
 * Construye el envelope SOAP para consultar alumno
 */
function buildConsultarAlumnoXML(matricula) {
    return `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="${CONFIG.SOAP_NAMESPACE}">
    <soap:Body>
        <alum:consultarAlumnoPorMatricula>
            <alum:matricula>${escapeXml(matricula)}</alum:matricula>
        </alum:consultarAlumnoPorMatricula>
    </soap:Body>
</soap:Envelope>`;
}

/**
 * Construye el envelope SOAP para eliminar alumnos
 */
function buildEliminarAlumnosXML(matriculas) {
    let matriculasXML = matriculas
        .map(m => `            <alum:lista_matriculas>${escapeXml(m)}</alum:lista_matriculas>`)
        .join('\n');

    return `<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="${CONFIG.SOAP_NAMESPACE}">
    <soap:Body>
        <alum:eliminarAlumnos>
${matriculasXML}
        </alum:eliminarAlumnos>
    </soap:Body>
</soap:Envelope>`;
}

/**
 * Envía una petición SOAP
 */
async function enviarPeticionSOAP(xmlBody) {
    const response = await fetch(CONFIG.SOAP_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/xml; charset=utf-8'
        },
        body: xmlBody
    });

    const xmlText = await response.text();
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, 'text/xml');

    // Verificar si hay un Fault SOAP
    const fault = xmlDoc.querySelector('Fault, soap\\:Fault, soap11env\\:Fault');
    if (fault) {
        const faultString = fault.querySelector('faultstring')?.textContent || 'Error desconocido';
        throw new Error(faultString);
    }

    return xmlDoc;
}

/**
 * Extrae el valor de un elemento XML por nombre local
 */
function getXmlValue(doc, localName) {
    // Buscar con diferentes variantes de namespace
    const selectors = [
        localName,
        `tns\\:${localName}`,
        `*|${localName}`
    ];

    for (const selector of selectors) {
        const element = doc.querySelector(selector);
        if (element) {
            return element.textContent;
        }
    }

    // Buscar por nombre local directamente
    const elements = doc.getElementsByTagName('*');
    for (const el of elements) {
        if (el.localName === localName) {
            return el.textContent;
        }
    }

    return null;
}

/**
 * Extrae datos de un alumno del XML
 */
function extraerAlumnoDeXML(doc) {
    return {
        id: getXmlValue(doc, 'id'),
        matricula: getXmlValue(doc, 'matricula'),
        nombre: getXmlValue(doc, 'nombre'),
        apellido: getXmlValue(doc, 'apellido'),
        email: getXmlValue(doc, 'email'),
        fechaRegistro: getXmlValue(doc, 'fecha_registro')
    };
}

// ============================================
// Handlers de Formularios - Alumnos (SOAP)
// ============================================

/**
 * Registrar un nuevo alumno
 */
async function registrarAlumno(event) {
    event.preventDefault();

    const matricula = document.getElementById('alumno-matricula').value.trim();
    const nombre = document.getElementById('alumno-nombre').value.trim();
    const apellido = document.getElementById('alumno-apellido').value.trim();
    const email = document.getElementById('alumno-email').value.trim();

    toggleLoading(true);

    try {
        const xmlBody = buildRegistrarAlumnoXML(matricula, nombre, apellido, email);
        const xmlDoc = await enviarPeticionSOAP(xmlBody);

        const mensaje = getXmlValue(xmlDoc, 'mensaje') || 'Alumno registrado exitosamente';
        const alumno = extraerAlumnoDeXML(xmlDoc);

        const contenido = `
            <p>${mensaje}</p>
            <p><strong>ID:</strong> ${alumno.id}</p>
            <p><strong>Matrícula:</strong> ${alumno.matricula}</p>
            <p><strong>Nombre:</strong> ${alumno.nombre} ${alumno.apellido}</p>
            <p><strong>Email:</strong> ${alumno.email}</p>
        `;

        mostrarResultado('resultado-registrar-alumno', 'success', 'Registro Exitoso', contenido);
        limpiarFormulario('form-registrar-alumno');

    } catch (error) {
        mostrarResultado('resultado-registrar-alumno', 'error', 'Error', error.message);
    } finally {
        toggleLoading(false);
    }
}

/**
 * Consultar un alumno por matrícula
 */
async function consultarAlumno(event) {
    event.preventDefault();

    const matricula = document.getElementById('consulta-matricula').value.trim();

    toggleLoading(true);

    try {
        const xmlBody = buildConsultarAlumnoXML(matricula);
        const xmlDoc = await enviarPeticionSOAP(xmlBody);

        const alumno = extraerAlumnoDeXML(xmlDoc);

        const contenido = `
            <p><strong>ID:</strong> ${alumno.id}</p>
            <p><strong>Matrícula:</strong> ${alumno.matricula}</p>
            <p><strong>Nombre:</strong> ${alumno.nombre}</p>
            <p><strong>Apellido:</strong> ${alumno.apellido}</p>
            <p><strong>Email:</strong> ${alumno.email}</p>
            <p><strong>Fecha de Registro:</strong> ${alumno.fechaRegistro || 'N/A'}</p>
        `;

        mostrarResultado('resultado-consultar-alumno', 'success', 'Alumno Encontrado', contenido);

    } catch (error) {
        mostrarResultado('resultado-consultar-alumno', 'error', 'Error', error.message);
    } finally {
        toggleLoading(false);
    }
}

/**
 * Eliminar múltiples alumnos
 */
async function eliminarAlumnos(event) {
    event.preventDefault();

    const inputs = document.querySelectorAll('#matriculas-container input[name="matricula[]"]');
    const matriculas = Array.from(inputs)
        .map(input => input.value.trim())
        .filter(m => m !== '');

    if (matriculas.length < 2) {
        mostrarResultado('resultado-eliminar-alumnos', 'error', 'Error',
            'Debe proporcionar al menos 2 matrículas para eliminar');
        return;
    }

    // Confirmar eliminación
    const confirmar = confirm(`¿Está seguro de eliminar ${matriculas.length} alumnos?\n\nMatrículas: ${matriculas.join(', ')}`);
    if (!confirmar) return;

    toggleLoading(true);

    try {
        const xmlBody = buildEliminarAlumnosXML(matriculas);
        const xmlDoc = await enviarPeticionSOAP(xmlBody);

        const mensaje = getXmlValue(xmlDoc, 'mensaje') || 'Alumnos eliminados exitosamente';
        const cantidad = getXmlValue(xmlDoc, 'cantidad_eliminados') || matriculas.length;

        // Extraer lista de alumnos eliminados
        const alumnosElements = xmlDoc.querySelectorAll('AlumnoSOAP, tns\\:AlumnoSOAP');
        const alumnosInfo = [];

        alumnosElements.forEach(alumnoEl => {
            const matriculaEl = alumnoEl.querySelector('matricula, tns\\:matricula');
            const nombreEl = alumnoEl.querySelector('nombre, tns\\:nombre');
            const apellidoEl = alumnoEl.querySelector('apellido, tns\\:apellido');

            if (matriculaEl) {
                alumnosInfo.push(`${matriculaEl.textContent} - ${nombreEl?.textContent || ''} ${apellidoEl?.textContent || ''}`);
            }
        });

        const contenido = `
            <p>${mensaje}</p>
            <p><strong>Cantidad eliminados:</strong> ${cantidad}</p>
            ${alumnosInfo.length > 0 ? '<p><strong>Alumnos eliminados:</strong></p><ul>' + alumnosInfo.map(a => `<li>${a}</li>`).join('') + '</ul>' : ''}
        `;

        mostrarResultado('resultado-eliminar-alumnos', 'success', 'Eliminación Exitosa', contenido);
        resetearFormularioMatriculas();

    } catch (error) {
        mostrarResultado('resultado-eliminar-alumnos', 'error', 'Error', error.message);
    } finally {
        toggleLoading(false);
    }
}

/**
 * Agrega un nuevo input de matrícula
 */
function agregarMatricula() {
    const container = document.getElementById('matriculas-container');
    const count = container.querySelectorAll('.matricula-input').length + 1;

    const div = document.createElement('div');
    div.className = 'form-group matricula-input';
    div.innerHTML = `
        <label>Matrícula ${count}</label>
        <input type="text" name="matricula[]" placeholder="Ej: S2002458${count}" required>
        <button type="button" class="btn-remove" onclick="removerMatricula(this)" title="Eliminar">&times;</button>
    `;

    container.appendChild(div);
}

/**
 * Remueve un input de matrícula
 */
function removerMatricula(button) {
    const container = document.getElementById('matriculas-container');
    if (container.querySelectorAll('.matricula-input').length > 2) {
        button.parentElement.remove();
        actualizarNumerosMatricula();
    } else {
        alert('Debe mantener al menos 2 matrículas');
    }
}

/**
 * Actualiza los números de las matrículas
 */
function actualizarNumerosMatricula() {
    const inputs = document.querySelectorAll('#matriculas-container .matricula-input');
    inputs.forEach((div, index) => {
        const label = div.querySelector('label');
        if (label) {
            label.textContent = `Matrícula ${index + 1}`;
        }
    });
}

/**
 * Resetea el formulario de matrículas a su estado original
 */
function resetearFormularioMatriculas() {
    const container = document.getElementById('matriculas-container');
    container.innerHTML = `
        <div class="form-group matricula-input">
            <label>Matrícula 1</label>
            <input type="text" name="matricula[]" placeholder="Ej: S20024583" required>
        </div>
        <div class="form-group matricula-input">
            <label>Matrícula 2</label>
            <input type="text" name="matricula[]" placeholder="Ej: S20024584" required>
        </div>
    `;
}

// ============================================
// Funciones REST (Cursos)
// ============================================

/**
 * Registrar un nuevo curso
 */
async function registrarCurso(event) {
    event.preventDefault();

    const curso = {
        nombre: document.getElementById('curso-nombre').value.trim(),
        descripcion: document.getElementById('curso-descripcion').value.trim(),
        fechaInicio: document.getElementById('curso-fecha').value,
        creditos: parseInt(document.getElementById('curso-creditos').value)
    };

    toggleLoading(true);

    try {
        const response = await fetch(CONFIG.REST_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(curso)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.mensaje || data.error || 'Error al registrar el curso');
        }

        const contenido = `
            <p>Curso registrado exitosamente</p>
            <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Nombre:</strong> ${data.nombre}</p>
            <p><strong>Descripción:</strong> ${data.descripcion || 'N/A'}</p>
            <p><strong>Fecha de Inicio:</strong> ${data.fechaInicio}</p>
            <p><strong>Créditos:</strong> ${data.creditos}</p>
            <p><strong>Estado:</strong> ${data.activo ? 'Activo' : 'Inactivo'}</p>
        `;

        mostrarResultado('resultado-registrar-curso', 'success', 'Registro Exitoso', contenido);
        limpiarFormulario('form-registrar-curso');

    } catch (error) {
        mostrarResultado('resultado-registrar-curso', 'error', 'Error', error.message);
    } finally {
        toggleLoading(false);
    }
}

/**
 * Buscar cursos
 */
async function buscarCurso(event) {
    event.preventDefault();

    const tipoBusqueda = document.querySelector('input[name="tipo-busqueda"]:checked').value;
    let url = `${CONFIG.REST_URL}/buscar?`;

    if (tipoBusqueda === 'nombre') {
        const nombre = document.getElementById('busqueda-nombre').value.trim();
        if (!nombre) {
            mostrarResultado('resultado-buscar-curso', 'error', 'Error', 'Ingrese un nombre para buscar');
            return;
        }
        url += `nombre=${encodeURIComponent(nombre)}`;
    } else {
        const fecha = document.getElementById('busqueda-fecha').value;
        if (!fecha) {
            mostrarResultado('resultado-buscar-curso', 'error', 'Error', 'Seleccione una fecha para buscar');
            return;
        }
        url += `fecha=${fecha}`;
    }

    toggleLoading(true);

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.mensaje || data.error || 'No se encontraron cursos');
        }

        // Asegurar que data sea un array
        const cursos = Array.isArray(data) ? data : [data];

        if (cursos.length === 0) {
            throw new Error('No se encontraron cursos con ese criterio');
        }

        mostrarResultado('resultado-buscar-curso', 'success', 'Búsqueda Exitosa',
            `Se encontraron ${cursos.length} curso(s)`);

        mostrarTablaCursos(cursos);

    } catch (error) {
        mostrarResultado('resultado-buscar-curso', 'error', 'Error', error.message);
        document.getElementById('card-resultados-cursos').style.display = 'none';
    } finally {
        toggleLoading(false);
    }
}

/**
 * Muestra la tabla de cursos encontrados
 */
function mostrarTablaCursos(cursos) {
    const card = document.getElementById('card-resultados-cursos');
    const tbody = document.getElementById('cursos-tbody');

    tbody.innerHTML = '';

    cursos.forEach(curso => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${curso.id}</td>
            <td>${curso.nombre}</td>
            <td>${curso.descripcion || '-'}</td>
            <td>${curso.fechaInicio}</td>
            <td>${curso.creditos}</td>
            <td class="${curso.activo ? 'estado-activo' : 'estado-inactivo'}">
                ${curso.activo ? 'Activo' : 'Inactivo'}
            </td>
            <td>
                <button class="btn btn-outline btn-sm" onclick="editarCurso(${curso.id})">
                    Editar
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    card.style.display = 'block';

    // Guardar cursos en memoria para edición
    window.cursosEncontrados = cursos;
}

/**
 * Prepara el formulario de edición con los datos del curso
 */
function editarCurso(id) {
    const curso = window.cursosEncontrados?.find(c => c.id === id);
    if (!curso) {
        alert('Curso no encontrado');
        return;
    }

    document.getElementById('editar-curso-id').value = curso.id;
    document.getElementById('editar-nombre').value = curso.nombre;
    document.getElementById('editar-descripcion').value = curso.descripcion || '';
    document.getElementById('editar-fecha').value = curso.fechaInicio;
    document.getElementById('editar-creditos').value = curso.creditos;
    document.getElementById('editar-activo').value = curso.activo.toString();

    document.getElementById('card-editar-curso').style.display = 'block';
    document.getElementById('card-editar-curso').scrollIntoView({ behavior: 'smooth' });

    // Limpiar resultado anterior
    const resultado = document.getElementById('resultado-editar-curso');
    resultado.className = 'resultado';
}

/**
 * Guardar cambios del curso
 */
async function guardarCambiosCurso(event) {
    event.preventDefault();

    const id = document.getElementById('editar-curso-id').value;
    const curso = {
        nombre: document.getElementById('editar-nombre').value.trim(),
        descripcion: document.getElementById('editar-descripcion').value.trim(),
        fechaInicio: document.getElementById('editar-fecha').value,
        creditos: parseInt(document.getElementById('editar-creditos').value),
        activo: document.getElementById('editar-activo').value === 'true'
    };

    toggleLoading(true);

    try {
        const response = await fetch(`${CONFIG.REST_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(curso)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.mensaje || data.error || 'Error al actualizar el curso');
        }

        const contenido = `
            <p>Curso actualizado exitosamente</p>
            <p><strong>ID:</strong> ${data.id}</p>
            <p><strong>Nombre:</strong> ${data.nombre}</p>
            <p><strong>Estado:</strong> ${data.activo ? 'Activo' : 'Inactivo'}</p>
        `;

        mostrarResultado('resultado-editar-curso', 'success', 'Actualización Exitosa', contenido);

        // Actualizar la tabla si está visible
        if (window.cursosEncontrados) {
            const index = window.cursosEncontrados.findIndex(c => c.id === parseInt(id));
            if (index !== -1) {
                window.cursosEncontrados[index] = data;
                mostrarTablaCursos(window.cursosEncontrados);
            }
        }

    } catch (error) {
        mostrarResultado('resultado-editar-curso', 'error', 'Error', error.message);
    } finally {
        toggleLoading(false);
    }
}

/**
 * Cancela la edición del curso
 */
function cancelarEdicion() {
    document.getElementById('card-editar-curso').style.display = 'none';
    const resultado = document.getElementById('resultado-editar-curso');
    resultado.className = 'resultado';
}

// ============================================
// Navegación por Tabs
// ============================================

function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabId = button.dataset.tab;

            // Desactivar todos los tabs
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Activar el tab seleccionado
            button.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// ============================================
// Toggle de campos de búsqueda
// ============================================

function initBusquedaToggle() {
    const radios = document.querySelectorAll('input[name="tipo-busqueda"]');
    const nombreGroup = document.getElementById('busqueda-nombre-group');
    const fechaGroup = document.getElementById('busqueda-fecha-group');

    radios.forEach(radio => {
        radio.addEventListener('change', () => {
            if (radio.value === 'nombre') {
                nombreGroup.classList.remove('hidden');
                fechaGroup.classList.add('hidden');
                document.getElementById('busqueda-nombre').required = true;
                document.getElementById('busqueda-fecha').required = false;
            } else {
                nombreGroup.classList.add('hidden');
                fechaGroup.classList.remove('hidden');
                document.getElementById('busqueda-nombre').required = false;
                document.getElementById('busqueda-fecha').required = true;
            }
        });
    });
}

// ============================================
// Inicialización
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar navegación
    initTabs();
    initBusquedaToggle();

    // Establecer fecha mínima para cursos (hoy)
    const hoy = new Date().toISOString().split('T')[0];
    document.getElementById('curso-fecha').min = hoy;
    document.getElementById('editar-fecha').min = hoy;

    // Event listeners - Alumnos (SOAP)
    document.getElementById('form-registrar-alumno').addEventListener('submit', registrarAlumno);
    document.getElementById('form-consultar-alumno').addEventListener('submit', consultarAlumno);
    document.getElementById('form-eliminar-alumnos').addEventListener('submit', eliminarAlumnos);
    document.getElementById('btn-agregar-matricula').addEventListener('click', agregarMatricula);

    // Event listeners - Cursos (REST)
    document.getElementById('form-registrar-curso').addEventListener('submit', registrarCurso);
    document.getElementById('form-buscar-curso').addEventListener('submit', buscarCurso);
    document.getElementById('form-editar-curso').addEventListener('submit', guardarCambiosCurso);
    document.getElementById('btn-cancelar-edicion').addEventListener('click', cancelarEdicion);

    console.log('Sistema Académico UAV - Frontend inicializado');
    console.log(`SOAP Service: ${CONFIG.SOAP_URL}`);
    console.log(`REST Service: ${CONFIG.REST_URL}`);
});
