"""
Servicio SOAP para gestión de alumnos
Implementación de operaciones SOAP con Spyne
"""

import logging
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Array, Fault
from spyne.protocol.soap import Soap11
from spyne.model.complex import ComplexModel
from models import Alumno
from config import Config

logger = logging.getLogger(__name__)

# Definir tipos complejos para SOAP

class AlumnoSOAP(ComplexModel):
    """Modelo SOAP para representar un Alumno"""
    __namespace__ = Config.SOAP_NAMESPACE

    id = Integer
    matricula = Unicode
    nombre = Unicode
    apellido = Unicode
    email = Unicode
    fecha_registro = Unicode

class RespuestaRegistro(ComplexModel):
    """Modelo SOAP para respuesta de registro"""
    __namespace__ = Config.SOAP_NAMESPACE

    mensaje = Unicode
    alumno = AlumnoSOAP

class RespuestaEliminacion(ComplexModel):
    """Modelo SOAP para respuesta de eliminación"""
    __namespace__ = Config.SOAP_NAMESPACE

    mensaje = Unicode
    cantidad_eliminados = Integer
    alumnos = Array(AlumnoSOAP)

# Servicio SOAP

class AlumnoService(ServiceBase):
    """
    Servicio SOAP para gestión de alumnos
    Universidad Autónoma Veracruzana
    """

    @rpc(Unicode, Unicode, Unicode, Unicode, _returns=RespuestaRegistro)
    def registrarAlumno(ctx, matricula, nombre, apellido, email):
        """
        Registra un nuevo alumno en el sistema

        Args:
            matricula: Matrícula única del alumno (6-20 caracteres alfanuméricos)
            nombre: Nombre del alumno (2-100 caracteres)
            apellido: Apellido del alumno (2-100 caracteres)
            email: Email único del alumno (formato válido)

        Returns:
            RespuestaRegistro con confirmación y datos del alumno creado

        Raises:
            Fault: Si hay errores de validación o el alumno ya existe
        """
        logger.info(f"SOAP: registrarAlumno - Matrícula: {matricula}, Email: {email}")

        try:
            # Crear alumno (incluye todas las validaciones)
            alumno = Alumno.crear(matricula, nombre, apellido, email)

            if not alumno:
                logger.error("Error al crear alumno en base de datos")
                raise Fault(
                    faultcode="Server",
                    faultstring="Error al crear el alumno en la base de datos"
                )

            # Construir respuesta SOAP
            alumno_soap = AlumnoSOAP()
            alumno_soap.id = alumno.id
            alumno_soap.matricula = alumno.matricula
            alumno_soap.nombre = alumno.nombre
            alumno_soap.apellido = alumno.apellido
            alumno_soap.email = alumno.email
            alumno_soap.fecha_registro = alumno.fecha_registro.isoformat() if alumno.fecha_registro else None

            respuesta = RespuestaRegistro()
            respuesta.mensaje = f"Alumno registrado exitosamente con matrícula {alumno.matricula}"
            respuesta.alumno = alumno_soap

            logger.info(f"SOAP: Alumno registrado exitosamente - ID: {alumno.id}")
            return respuesta

        except ValueError as e:
            # Error de validación
            logger.warning(f"SOAP: Error de validación - {str(e)}")
            raise Fault(
                faultcode="Client.ValidationError",
                faultstring=str(e)
            )
        except Exception as e:
            # Error inesperado
            logger.error(f"SOAP: Error inesperado - {str(e)}")
            raise Fault(
                faultcode="Server",
                faultstring=f"Error interno del servidor: {str(e)}"
            )

    @rpc(Unicode, _returns=AlumnoSOAP)
    def consultarAlumnoPorMatricula(ctx, matricula):
        """
        Consulta un alumno por su matrícula

        Args:
            matricula: Matrícula del alumno a consultar

        Returns:
            AlumnoSOAP con los datos completos del alumno

        Raises:
            Fault: Si el alumno no existe
        """
        logger.info(f"SOAP: consultarAlumnoPorMatricula - Matrícula: {matricula}")

        try:
            # Buscar alumno por matrícula
            alumno = Alumno.buscar_por_matricula(matricula)

            if not alumno:
                logger.warning(f"SOAP: Alumno no encontrado - Matrícula: {matricula}")
                raise Fault(
                    faultcode="Client.NotFound",
                    faultstring=f"No se encontró un alumno con la matrícula: {matricula}"
                )

            # Construir respuesta SOAP
            alumno_soap = AlumnoSOAP()
            alumno_soap.id = alumno.id
            alumno_soap.matricula = alumno.matricula
            alumno_soap.nombre = alumno.nombre
            alumno_soap.apellido = alumno.apellido
            alumno_soap.email = alumno.email
            alumno_soap.fecha_registro = alumno.fecha_registro.isoformat() if alumno.fecha_registro else None

            logger.info(f"SOAP: Alumno encontrado - ID: {alumno.id}")
            return alumno_soap

        except Fault:
            # Re-lanzar Faults SOAP
            raise
        except Exception as e:
            # Error inesperado
            logger.error(f"SOAP: Error inesperado - {str(e)}")
            raise Fault(
                faultcode="Server",
                faultstring=f"Error interno del servidor: {str(e)}"
            )

    @rpc(Array(Unicode), _returns=RespuestaEliminacion)
    def eliminarAlumnos(ctx, lista_matriculas):
        """
        Elimina múltiples alumnos por sus matrículas

        Este método realiza las siguientes validaciones:
        1. Verifica que se proporcionen al menos 2 matrículas
        2. Consulta que TODOS los alumnos existan antes de eliminar
        3. Elimina todos en una transacción (todo o nada)

        Args:
            lista_matriculas: Array de matrículas a eliminar (mínimo 2)

        Returns:
            RespuestaEliminacion con confirmación y lista de alumnos eliminados

        Raises:
            Fault: Si hay errores de validación o algún alumno no existe
        """
        logger.info(f"SOAP: eliminarAlumnos - Cantidad: {len(lista_matriculas) if lista_matriculas else 0}")

        try:
            # Validar que se proporcione lista de matrículas
            if not lista_matriculas:
                raise ValueError("Debe proporcionar una lista de matrículas")

            # Eliminar alumnos (incluye todas las validaciones y transacción)
            alumnos_eliminados = Alumno.eliminar_multiples(lista_matriculas)

            # Construir respuesta SOAP
            alumnos_soap = []
            for alumno in alumnos_eliminados:
                alumno_soap = AlumnoSOAP()
                alumno_soap.id = alumno.id
                alumno_soap.matricula = alumno.matricula
                alumno_soap.nombre = alumno.nombre
                alumno_soap.apellido = alumno.apellido
                alumno_soap.email = alumno.email
                alumno_soap.fecha_registro = alumno.fecha_registro.isoformat() if alumno.fecha_registro else None
                alumnos_soap.append(alumno_soap)

            respuesta = RespuestaEliminacion()
            respuesta.mensaje = f"Se eliminaron exitosamente {len(alumnos_eliminados)} alumnos"
            respuesta.cantidad_eliminados = len(alumnos_eliminados)
            respuesta.alumnos = alumnos_soap

            logger.info(f"SOAP: Eliminación exitosa de {len(alumnos_eliminados)} alumnos")
            return respuesta

        except ValueError as e:
            # Error de validación
            logger.warning(f"SOAP: Error de validación - {str(e)}")
            raise Fault(
                faultcode="Client.ValidationError",
                faultstring=str(e)
            )
        except Exception as e:
            # Error inesperado
            logger.error(f"SOAP: Error inesperado - {str(e)}")
            raise Fault(
                faultcode="Server",
                faultstring=f"Error al eliminar alumnos: {str(e)}"
            )

# Crear aplicación SOAP
soap_app = Application(
    [AlumnoService],
    tns=Config.SOAP_NAMESPACE,
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
