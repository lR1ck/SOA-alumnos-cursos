# Ejemplos de Peticiones SOAP - Gestión de Alumnos

Servicio SOAP para la gestión de alumnos - Universidad Autónoma Veracruzana

**Endpoint SOAP**: `http://localhost:5001/soap`
**WSDL**: `http://localhost:5001/soap?wsdl`
**Namespace**: `http://uav.edu.mx/alumnos`

---

## Herramientas para Probar

### 1. cURL (Línea de comandos)
```bash
curl -X POST http://localhost:5001/soap \
  -H "Content-Type: text/xml; charset=utf-8" \
  -H "SOAPAction: registrarAlumno" \
  -d @request.xml
```

### 2. SoapUI
- Importar WSDL: `http://localhost:5001/soap?wsdl`
- Crear peticiones automáticamente

### 3. Postman
- New Request → Body → raw → XML
- Headers: `Content-Type: text/xml; charset=utf-8`

---

## 1. registrarAlumno

Registra un nuevo alumno en el sistema.

### Petición XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="http://uav.edu.mx/alumnos">
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

### Respuesta Exitosa (200 OK)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://uav.edu.mx/alumnos">
    <soap11env:Body>
        <tns:registrarAlumnoResponse>
            <tns:registrarAlumnoResult>
                <tns:mensaje>Alumno registrado exitosamente con matrícula S20024583</tns:mensaje>
                <tns:alumno>
                    <tns:id>6</tns:id>
                    <tns:matricula>S20024583</tns:matricula>
                    <tns:nombre>Carlos Alberto</tns:nombre>
                    <tns:apellido>Ramírez Flores</tns:apellido>
                    <tns:email>carlos.ramirez@uv.mx</tns:email>
                    <tns:fecha_registro>2025-12-05T19:30:00</tns:fecha_registro>
                </tns:alumno>
            </tns:registrarAlumnoResult>
        </tns:registrarAlumnoResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

### Error - Matrícula Duplicada (500 SOAP Fault)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap11env:Body>
        <soap11env:Fault>
            <faultcode>Client.ValidationError</faultcode>
            <faultstring>Ya existe un alumno con la matrícula: S20024583</faultstring>
        </soap11env:Fault>
    </soap11env:Body>
</soap11env:Envelope>
```

### Comando cURL - Registrar Alumno

```bash
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

---

## 2. consultarAlumnoPorMatricula

Consulta los datos de un alumno por su matrícula.

### Petición XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:consultarAlumnoPorMatricula>
            <alum:matricula>S20014578</alum:matricula>
        </alum:consultarAlumnoPorMatricula>
    </soap:Body>
</soap:Envelope>
```

### Respuesta Exitosa (200 OK)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://uav.edu.mx/alumnos">
    <soap11env:Body>
        <tns:consultarAlumnoPorMatriculaResponse>
            <tns:consultarAlumnoPorMatriculaResult>
                <tns:id>1</tns:id>
                <tns:matricula>S20014578</tns:matricula>
                <tns:nombre>Juan Carlos</tns:nombre>
                <tns:apellido>García López</tns:apellido>
                <tns:email>juan.garcia@uv.mx</tns:email>
                <tns:fecha_registro>2025-12-05T18:00:00</tns:fecha_registro>
            </tns:consultarAlumnoPorMatriculaResult>
        </tns:consultarAlumnoPorMatriculaResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

### Error - Alumno No Encontrado (500 SOAP Fault)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap11env:Body>
        <soap11env:Fault>
            <faultcode>Client.NotFound</faultcode>
            <faultstring>No se encontró un alumno con la matrícula: S99999999</faultstring>
        </soap11env:Fault>
    </soap11env:Body>
</soap11env:Envelope>
```

### Comando cURL - Consultar Alumno

```bash
curl -X POST http://localhost:5001/soap \
  -H "Content-Type: text/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:consultarAlumnoPorMatricula>
            <alum:matricula>S20014578</alum:matricula>
        </alum:consultarAlumnoPorMatricula>
    </soap:Body>
</soap:Envelope>'
```

---

## 3. eliminarAlumnos

Elimina múltiples alumnos en una transacción (mínimo 2).

### Petición XML - 2 Alumnos

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:eliminarAlumnos>
            <alum:lista_matriculas>S20014580</alum:lista_matriculas>
            <alum:lista_matriculas>S20014581</alum:lista_matriculas>
        </alum:eliminarAlumnos>
    </soap:Body>
</soap:Envelope>
```

### Petición XML - 3 Alumnos

```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:eliminarAlumnos>
            <alum:lista_matriculas>S20014578</alum:lista_matriculas>
            <alum:lista_matriculas>S20014579</alum:lista_matriculas>
            <alum:lista_matriculas>S20014582</alum:lista_matriculas>
        </alum:eliminarAlumnos>
    </soap:Body>
</soap:Envelope>
```

### Respuesta Exitosa (200 OK)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:tns="http://uav.edu.mx/alumnos">
    <soap11env:Body>
        <tns:eliminarAlumnosResponse>
            <tns:eliminarAlumnosResult>
                <tns:mensaje>Se eliminaron exitosamente 2 alumnos</tns:mensaje>
                <tns:cantidad_eliminados>2</tns:cantidad_eliminados>
                <tns:alumnos>
                    <tns:AlumnoSOAP>
                        <tns:id>3</tns:id>
                        <tns:matricula>S20014580</tns:matricula>
                        <tns:nombre>Pedro Antonio</tns:nombre>
                        <tns:apellido>Martínez Sánchez</tns:apellido>
                        <tns:email>pedro.martinez@uv.mx</tns:email>
                        <tns:fecha_registro>2025-12-05T18:00:00</tns:fecha_registro>
                    </tns:AlumnoSOAP>
                    <tns:AlumnoSOAP>
                        <tns:id>4</tns:id>
                        <tns:matricula>S20014581</tns:matricula>
                        <tns:nombre>Ana Laura</tns:nombre>
                        <tns:apellido>Hernández Gómez</tns:apellido>
                        <tns:email>ana.hernandez@uv.mx</tns:email>
                        <tns:fecha_registro>2025-12-05T18:00:00</tns:fecha_registro>
                    </tns:AlumnoSOAP>
                </tns:alumnos>
            </tns:eliminarAlumnosResult>
        </tns:eliminarAlumnosResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

### Error - Menos de 2 Matrículas (500 SOAP Fault)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap11env:Body>
        <soap11env:Fault>
            <faultcode>Client.ValidationError</faultcode>
            <faultstring>Debe proporcionar al menos 2 matrículas para eliminar</faultstring>
        </soap11env:Fault>
    </soap11env:Body>
</soap11env:Envelope>
```

### Error - Alumno No Existe (500 SOAP Fault)

```xml
<?xml version='1.0' encoding='UTF-8'?>
<soap11env:Envelope
    xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/">
    <soap11env:Body>
        <soap11env:Fault>
            <faultcode>Client.ValidationError</faultcode>
            <faultstring>No existe un alumno con la matrícula: S99999999</faultstring>
        </soap11env:Fault>
    </soap11env:Body>
</soap11env:Envelope>
```

### Comando cURL - Eliminar Alumnos

```bash
curl -X POST http://localhost:5001/soap \
  -H "Content-Type: text/xml; charset=utf-8" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:alum="http://uav.edu.mx/alumnos">
    <soap:Body>
        <alum:eliminarAlumnos>
            <alum:lista_matriculas>S20014580</alum:lista_matriculas>
            <alum:lista_matriculas>S20014581</alum:lista_matriculas>
        </alum:eliminarAlumnos>
    </soap:Body>
</soap:Envelope>'
```

---

## Validaciones Implementadas

### registrarAlumno
- ✅ Matrícula: 6-20 caracteres alfanuméricos, única
- ✅ Nombre: 2-100 caracteres, obligatorio
- ✅ Apellido: 2-100 caracteres, obligatorio
- ✅ Email: formato válido, único, máximo 100 caracteres

### consultarAlumnoPorMatricula
- ✅ El alumno debe existir en la base de datos

### eliminarAlumnos
- ✅ Mínimo 2 matrículas requeridas
- ✅ Todos los alumnos deben existir antes de eliminar
- ✅ Eliminación en transacción (todo o nada)

---

## Códigos de Error SOAP

| Código | Descripción |
|--------|-------------|
| `Client.ValidationError` | Error de validación de datos |
| `Client.NotFound` | Recurso no encontrado |
| `Server` | Error interno del servidor |

---

## Probar con Python (requests + zeep)

### Instalar zeep
```bash
pip install zeep
```

### Script de prueba

```python
from zeep import Client

# Crear cliente SOAP
wsdl = 'http://localhost:5001/soap?wsdl'
client = Client(wsdl)

# 1. Registrar alumno
resultado = client.service.registrarAlumno(
    matricula='S20024584',
    nombre='Elena',
    apellido='Vargas Silva',
    email='elena.vargas@uv.mx'
)
print(resultado)

# 2. Consultar alumno
alumno = client.service.consultarAlumnoPorMatricula('S20024584')
print(f"Alumno: {alumno.nombre} {alumno.apellido}")

# 3. Eliminar alumnos
resultado = client.service.eliminarAlumnos(['S20014580', 'S20014581'])
print(f"Eliminados: {resultado.cantidad_eliminados}")
```

---

## Notas Importantes

1. **WSDL**: El WSDL se genera automáticamente en `/soap?wsdl`
2. **Namespace**: Todas las peticiones deben usar el namespace `http://uav.edu.mx/alumnos`
3. **Transacciones**: La operación `eliminarAlumnos` usa transacciones - si falla uno, se revierten todos
4. **CORS**: Habilitado para `http://localhost:3000` (frontend)
5. **Logs**: Todas las operaciones se registran en la consola del servidor
6. **Puerto**: El servicio corre en el puerto `5001`

---

## Verificar el Servicio

### 1. Ver WSDL
```bash
curl http://localhost:5001/soap?wsdl
```

### 2. Health Check
```bash
curl http://localhost:5001/health
```

### 3. Info del Servicio
```bash
curl http://localhost:5001/
```
