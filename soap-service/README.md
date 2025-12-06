# Servicio SOAP de Gestión de Alumnos

Servicio SOAP para la gestión de alumnos - Universidad Autónoma Veracruzana

Parte del **Sistema de Integración Académica** (3 componentes: SOAP Service, REST Service, Frontend Web)

---

## 📋 Descripción

Servicio SOAP desarrollado con Python 3, Flask y Spyne que proporciona operaciones para:
- ✅ Registrar alumnos con validaciones
- 🔍 Consultar alumnos por matrícula
- 🗑️ Eliminar múltiples alumnos en transacción

---

## 🛠️ Tecnologías Utilizadas

- **Python**: 3.x
- **Flask**: 3.0.0 (Framework web)
- **Spyne**: 2.14.0 (SOAP)
- **MySQL**: Base de datos (Railway - compartida con REST)
- **mysql-connector-python**: 8.2.0
- **Flask-CORS**: CORS habilitado
- **lxml**: Validación XML

---

## 📦 Estructura del Proyecto

```
soap-service/
├── app.py                      # Aplicación principal Flask
├── soap_service.py             # Operaciones SOAP con Spyne
├── models.py                   # Modelo Alumno y operaciones CRUD
├── database.py                 # Gestión de conexiones MySQL
├── config.py                   # Configuración del servicio
├── requirements.txt            # Dependencias Python
├── sql/
│   └── crear_tabla_alumnos.sql # Script SQL
├── ejemplos-soap.md            # Ejemplos de peticiones XML
└── README.md                   # Este archivo
```

---

## 🗄️ Modelo de Datos

### Entidad: Alumno

| Campo           | Tipo         | Restricciones                    |
|-----------------|--------------|----------------------------------|
| id              | INT          | PK, Auto-increment               |
| matricula       | VARCHAR(20)  | UNIQUE, NOT NULL, 6-20 chars     |
| nombre          | VARCHAR(100) | NOT NULL, 2-100 chars            |
| apellido        | VARCHAR(100) | NOT NULL, 2-100 chars            |
| email           | VARCHAR(100) | UNIQUE, NOT NULL, formato válido |
| fecha_registro  | DATETIME     | DEFAULT CURRENT_TIMESTAMP        |

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes Python)
- MySQL 8.x (Railway ya configurado)
- Acceso a la base de datos compartida

### 1. Clonar o ubicarse en el directorio

```bash
cd soap-service
```

### 2. Crear entorno virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el script SQL

Ejecuta el script `sql/crear_tabla_alumnos.sql` en tu base de datos MySQL Railway.

```bash
mysql -h trolley.proxy.rlwy.net -P 34558 -u root -p railway < sql/crear_tabla_alumnos.sql
```

### 5. Verificar configuración

Edita `config.py` si necesitas cambiar alguna configuración (normalmente no es necesario).

### 6. Ejecutar el servicio

```bash
python app.py
```

### 7. Verificar que el servicio está corriendo

**Health check:**
```bash
curl http://localhost:5001/health
```

**Ver WSDL:**
```bash
curl http://localhost:5001/soap?wsdl
```

El servicio estará disponible en: **http://localhost:5001**

---

## 📡 Operaciones SOAP

### Base URL: `http://localhost:5001/soap`
### WSDL: `http://localhost:5001/soap?wsdl`
### Namespace: `http://uav.edu.mx/alumnos`

| Operación                      | Descripción                              |
|--------------------------------|------------------------------------------|
| `registrarAlumno`              | Registra un nuevo alumno                 |
| `consultarAlumnoPorMatricula`  | Consulta alumno por matrícula            |
| `eliminarAlumnos`              | Elimina múltiples alumnos (mínimo 2)     |

### Detalles de Operaciones

#### 1. registrarAlumno

**Parámetros:**
- `matricula` (string): Matrícula única, 6-20 caracteres alfanuméricos
- `nombre` (string): Nombre del alumno, 2-100 caracteres
- `apellido` (string): Apellido del alumno, 2-100 caracteres
- `email` (string): Email único, formato válido

**Retorna:** RespuestaRegistro con mensaje y datos del alumno creado

**Ejemplo XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:registrarAlumno>
            <alum:matricula>S20024583</alum:matricula>
            <alum:nombre>Carlos Alberto</alum:nombre>
            <alum:apellido>Ramírez Flores</alum:apellido>
            <alum:email>carlos.ramirez@uv.mx</alum:email>
        </alum:registrarAlumno>
    </soap:Body>
</soap:Envelope>
```

#### 2. consultarAlumnoPorMatricula

**Parámetros:**
- `matricula` (string): Matrícula del alumno a consultar

**Retorna:** AlumnoSOAP con todos los datos del alumno

**Ejemplo XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:consultarAlumnoPorMatricula>
            <alum:matricula>S20014578</alum:matricula>
        </alum:consultarAlumnoPorMatricula>
    </soap:Body>
</soap:Envelope>
```

#### 3. eliminarAlumnos

**Parámetros:**
- `lista_matriculas` (array): Array de matrículas (mínimo 2)

**Proceso:**
1. Verifica que se proporcionen al menos 2 matrículas
2. Consulta que TODOS los alumnos existan
3. Elimina en transacción (todo o nada)

**Retorna:** RespuestaEliminacion con mensaje, cantidad y lista de alumnos eliminados

**Ejemplo XML:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:eliminarAlumnos>
            <alum:lista_matriculas>S20014580</alum:lista_matriculas>
            <alum:lista_matriculas>S20014581</alum:lista_matriculas>
        </alum:eliminarAlumnos>
    </soap:Body>
</soap:Envelope>
```

---

## 🧪 Pruebas

Ver archivo `ejemplos-soap.md` para ejemplos detallados de todas las operaciones con XML.

### Probar con cURL

```bash
# Registrar alumno
curl -X POST http://localhost:5001/soap \
  -H "Content-Type: text/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:registrarAlumno>
            <alum:matricula>S20024583</alum:matricula>
            <alum:nombre>Carlos Alberto</alum:nombre>
            <alum:apellido>Ramírez Flores</alum:apellido>
            <alum:email>carlos.ramirez@uv.mx</alum:email>
        </alum:registrarAlumno>
    </soap:Body>
</soap:Envelope>'
```

### Probar con Python (zeep)

```python
from zeep import Client

# Crear cliente SOAP
wsdl = 'http://localhost:5001/soap?wsdl'
client = Client(wsdl)

# Registrar alumno
resultado = client.service.registrarAlumno(
    matricula='S20024584',
    nombre='Elena',
    apellido='Vargas Silva',
    email='elena.vargas@uv.mx'
)
print(resultado)

# Consultar alumno
alumno = client.service.consultarAlumnoPorMatricula('S20024584')
print(f"Alumno: {alumno.nombre} {alumno.apellido}")

# Eliminar alumnos
resultado = client.service.eliminarAlumnos(['S20014580', 'S20014581'])
print(f"Eliminados: {resultado.cantidad_eliminados}")
```

---

## ✅ Validaciones Implementadas

### Campo: matricula
- ❌ No puede estar vacía
- ❌ Mínimo 6 caracteres
- ❌ Máximo 20 caracteres
- ❌ Solo caracteres alfanuméricos
- ❌ Debe ser única

### Campo: nombre/apellido
- ❌ No puede estar vacío
- ❌ Mínimo 2 caracteres
- ❌ Máximo 100 caracteres

### Campo: email
- ❌ No puede estar vacío
- ❌ Formato de email válido
- ❌ Máximo 100 caracteres
- ❌ Debe ser único

### Operación: eliminarAlumnos
- ❌ Mínimo 2 matrículas requeridas
- ❌ Todos los alumnos deben existir
- ✅ Transacción: todo o nada

---

## 🚨 Manejo de Errores SOAP

Todos los errores se devuelven como SOAP Fault:

### Client.ValidationError
```xml
<soap11env:Fault>
    <faultcode>Client.ValidationError</faultcode>
    <faultstring>Ya existe un alumno con la matrícula: S20024583</faultstring>
</soap11env:Fault>
```

### Client.NotFound
```xml
<soap11env:Fault>
    <faultcode>Client.NotFound</faultcode>
    <faultstring>No se encontró un alumno con la matrícula: S99999999</faultstring>
</soap11env:Fault>
```

### Server
```xml
<soap11env:Fault>
    <faultcode>Server</faultcode>
    <faultstring>Error interno del servidor: [detalle del error]</faultstring>
</soap11env:Fault>
```

---

## 🔧 Configuración

### config.py

```python
# Puerto del servidor
PORT = 5001

# Base de datos MySQL Railway (compartida con REST)
DB_CONFIG = {
    'host': 'trolley.proxy.rlwy.net',
    'port': 34558,
    'user': 'root',
    'password': '...',
    'database': 'railway'
}

# SOAP
SOAP_NAMESPACE = 'http://uav.edu.mx/alumnos'

# CORS - Frontend
CORS_ORIGINS = ['http://localhost:3000']
```

---

## 🌐 CORS

CORS está habilitado para permitir peticiones desde:
- `http://localhost:3000` (Frontend web)

---

## 📊 Logging

El servicio registra logs informativos de todas las operaciones:

```
2025-12-05 19:30:00 - __main__ - INFO - ====================================
2025-12-05 19:30:00 - __main__ - INFO - Iniciando servicio SOAP - Gestión de Alumnos
2025-12-05 19:30:00 - __main__ - INFO - ✓ Conexión a base de datos establecida
2025-12-05 19:30:00 - __main__ - INFO - Puerto: 5001
2025-12-05 19:30:00 - __main__ - INFO - WSDL disponible en: http://localhost:5001/soap?wsdl
2025-12-05 19:30:15 - soap_service - INFO - SOAP: registrarAlumno - Matrícula: S20024583
2025-12-05 19:30:15 - models - INFO - Alumno creado exitosamente - ID: 6, Matrícula: S20024583
```

---

## 🔗 Integración con Otros Componentes

Este servicio SOAP forma parte de un sistema más grande:

1. **SOAP Service (Python)** - Puerto 5001 ← **Este proyecto**
   - Gestión de alumnos
   - Endpoints SOAP

2. **REST Service (Java)** - Puerto 10000
   - Gestión de cursos
   - Endpoints REST

3. **Frontend Web (HTML/JS)** - Puerto 3000
   - Interfaz unificada
   - Consume ambos servicios

**Base de datos compartida**: MySQL Railway

---

## 🔍 Endpoints Auxiliares

### Health Check
```bash
GET http://localhost:5001/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "SOAP Alumnos Service",
  "database": "connected",
  "port": 5001
}
```

### Información del Servicio
```bash
GET http://localhost:5001/
```

**Respuesta:**
```json
{
  "service": "SOAP Alumnos Service",
  "version": "1.0",
  "universidad": "Universidad Autónoma Veracruzana",
  "endpoints": {
    "soap": "/soap",
    "wsdl": "/soap?wsdl",
    "health": "/health"
  },
  "operaciones": [
    "registrarAlumno(matricula, nombre, apellido, email)",
    "consultarAlumnoPorMatricula(matricula)",
    "eliminarAlumnos(lista_matriculas)"
  ]
}
```

---

## 👥 Autor

**Universidad Autónoma Veracruzana**
Asignatura: Diseño y Práctica
Proyecto: Sistema de Integración Académica

---

## 📄 Licencia

Este proyecto es de uso académico para la Universidad Autónoma Veracruzana.

---

## 📞 Soporte

Para dudas o problemas:
1. Revisa los logs en consola
2. Verifica la conexión a MySQL Railway
3. Consulta el archivo `ejemplos-soap.md`
4. Verifica el WSDL en `/soap?wsdl`
5. Usa el endpoint `/health` para diagnóstico

---

## 🎯 Próximos Pasos

- [x] Implementar servicio REST (Java) para cursos
- [x] Implementar servicio SOAP (Python) para alumnos
- [ ] Desarrollar frontend web con HTML/JS
- [ ] Integrar ambos servicios en el frontend
- [ ] Añadir autenticación
- [ ] Implementar tests unitarios

---

## 🛠️ Desarrollo

### Estructura de Base de Datos

**Pool de Conexiones:** 5 conexiones máximo
**Transacciones:** Manejadas manualmente para `eliminarAlumnos`
**Validaciones:** En modelo antes de insertar/actualizar

### Arquitectura SOAP

- **Framework SOAP:** Spyne 2.14.0
- **Protocolo:** SOAP 1.1
- **Validación XML:** lxml
- **Formato:** XML estándar
- **WSDL:** Auto-generado

---

## 📝 Notas Importantes

1. **Puerto 5001**: Asegúrate de que el puerto esté disponible
2. **Base de datos compartida**: Usa la misma BD que el servicio REST
3. **Transacciones**: `eliminarAlumnos` usa transacciones para garantizar consistencia
4. **WSDL dinámico**: El WSDL se genera automáticamente
5. **CORS**: Necesario para el frontend web
6. **Logs**: Todos los errores y operaciones se registran
7. **Validaciones**: Realizadas en el modelo antes de operaciones de BD
