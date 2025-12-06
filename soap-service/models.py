"""
Modelo de datos Alumno
Operaciones CRUD para la tabla alumnos
"""

import re
import logging
from datetime import datetime
from database import execute_query, execute_insert, execute_transaction
from config import Config

logger = logging.getLogger(__name__)

class Alumno:
    """Clase que representa a un alumno"""

    def __init__(self, id=None, matricula=None, nombre=None, apellido=None,
                 email=None, fecha_registro=None):
        self.id = id
        self.matricula = matricula
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.fecha_registro = fecha_registro

    @staticmethod
    def validar_matricula(matricula):
        """
        Valida el formato de la matrícula

        Args:
            matricula: Matrícula a validar

        Returns:
            (bool, str): (Es válida, Mensaje de error)
        """
        if not matricula or not isinstance(matricula, str):
            return False, "La matrícula es obligatoria"

        matricula = matricula.strip()

        if len(matricula) < Config.MATRICULA_MIN_LENGTH:
            return False, f"La matrícula debe tener al menos {Config.MATRICULA_MIN_LENGTH} caracteres"

        if len(matricula) > Config.MATRICULA_MAX_LENGTH:
            return False, f"La matrícula no puede exceder {Config.MATRICULA_MAX_LENGTH} caracteres"

        if not re.match(r'^[a-zA-Z0-9]+$', matricula):
            return False, "La matrícula solo puede contener letras y números"

        return True, ""

    @staticmethod
    def validar_email(email):
        """
        Valida el formato del email

        Args:
            email: Email a validar

        Returns:
            (bool, str): (Es válido, Mensaje de error)
        """
        if not email or not isinstance(email, str):
            return False, "El email es obligatorio"

        email = email.strip()

        # Expresión regular para validar email
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron, email):
            return False, "El formato del email es inválido"

        if len(email) > 100:
            return False, "El email no puede exceder 100 caracteres"

        return True, ""

    @staticmethod
    def validar_nombre(nombre, campo="nombre"):
        """
        Valida el formato del nombre o apellido

        Args:
            nombre: Nombre a validar
            campo: Nombre del campo (para mensajes de error)

        Returns:
            (bool, str): (Es válido, Mensaje de error)
        """
        if not nombre or not isinstance(nombre, str):
            return False, f"El {campo} es obligatorio"

        nombre = nombre.strip()

        if len(nombre) < Config.NOMBRE_MIN_LENGTH:
            return False, f"El {campo} debe tener al menos {Config.NOMBRE_MIN_LENGTH} caracteres"

        if len(nombre) > Config.NOMBRE_MAX_LENGTH:
            return False, f"El {campo} no puede exceder {Config.NOMBRE_MAX_LENGTH} caracteres"

        return True, ""

    @staticmethod
    def crear(matricula, nombre, apellido, email):
        """
        Crea un nuevo alumno en la base de datos

        Args:
            matricula: Matrícula del alumno
            nombre: Nombre del alumno
            apellido: Apellido del alumno
            email: Email del alumno

        Returns:
            Alumno creado o None si hay error
        """
        # Validaciones
        es_valida, error = Alumno.validar_matricula(matricula)
        if not es_valida:
            logger.error(f"Validación fallida - Matrícula: {error}")
            raise ValueError(error)

        es_valido, error = Alumno.validar_nombre(nombre, "nombre")
        if not es_valido:
            logger.error(f"Validación fallida - Nombre: {error}")
            raise ValueError(error)

        es_valido, error = Alumno.validar_nombre(apellido, "apellido")
        if not es_valido:
            logger.error(f"Validación fallida - Apellido: {error}")
            raise ValueError(error)

        es_valido, error = Alumno.validar_email(email)
        if not es_valido:
            logger.error(f"Validación fallida - Email: {error}")
            raise ValueError(error)

        # Verificar que no exista la matrícula
        if Alumno.buscar_por_matricula(matricula.strip()):
            error = f"Ya existe un alumno con la matrícula: {matricula}"
            logger.error(error)
            raise ValueError(error)

        # Verificar que no exista el email
        query = "SELECT id FROM alumnos WHERE email = %s"
        resultado = execute_query(query, (email.strip(),))
        if resultado:
            error = f"Ya existe un alumno con el email: {email}"
            logger.error(error)
            raise ValueError(error)

        # Insertar alumno
        query = """
            INSERT INTO alumnos (matricula, nombre, apellido, email)
            VALUES (%s, %s, %s, %s)
        """
        params = (matricula.strip(), nombre.strip(), apellido.strip(), email.strip())

        alumno_id = execute_insert(query, params)

        if alumno_id:
            logger.info(f"Alumno creado exitosamente - ID: {alumno_id}, Matrícula: {matricula}")
            return Alumno.buscar_por_id(alumno_id)

        return None

    @staticmethod
    def buscar_por_id(alumno_id):
        """
        Busca un alumno por su ID

        Args:
            alumno_id: ID del alumno

        Returns:
            Alumno o None si no existe
        """
        query = "SELECT * FROM alumnos WHERE id = %s"
        resultados = execute_query(query, (alumno_id,))

        if resultados and len(resultados) > 0:
            row = resultados[0]
            return Alumno(
                id=row['id'],
                matricula=row['matricula'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                fecha_registro=row['fecha_registro']
            )

        return None

    @staticmethod
    def buscar_por_matricula(matricula):
        """
        Busca un alumno por su matrícula

        Args:
            matricula: Matrícula del alumno

        Returns:
            Alumno o None si no existe
        """
        query = "SELECT * FROM alumnos WHERE matricula = %s"
        resultados = execute_query(query, (matricula.strip(),))

        if resultados and len(resultados) > 0:
            row = resultados[0]
            logger.info(f"Alumno encontrado - Matrícula: {matricula}")
            return Alumno(
                id=row['id'],
                matricula=row['matricula'],
                nombre=row['nombre'],
                apellido=row['apellido'],
                email=row['email'],
                fecha_registro=row['fecha_registro']
            )

        logger.warning(f"Alumno no encontrado - Matrícula: {matricula}")
        return None

    @staticmethod
    def eliminar_multiples(matriculas):
        """
        Elimina múltiples alumnos por sus matrículas en una transacción

        Args:
            matriculas: Lista de matrículas a eliminar

        Returns:
            Lista de alumnos eliminados o None si hay error
        """
        # Validar cantidad mínima
        if len(matriculas) < Config.MIN_ALUMNOS_ELIMINAR:
            error = f"Debe proporcionar al menos {Config.MIN_ALUMNOS_ELIMINAR} matrículas para eliminar"
            logger.error(error)
            raise ValueError(error)

        # Verificar que todos los alumnos existan
        alumnos = []
        for matricula in matriculas:
            alumno = Alumno.buscar_por_matricula(matricula.strip())
            if not alumno:
                error = f"No existe un alumno con la matrícula: {matricula}"
                logger.error(error)
                raise ValueError(error)
            alumnos.append(alumno)

        logger.info(f"Todos los alumnos existen, procediendo con eliminación de {len(alumnos)} registros")

        # Preparar operaciones de eliminación
        operations = []
        for matricula in matriculas:
            query = "DELETE FROM alumnos WHERE matricula = %s"
            operations.append((query, (matricula.strip(),)))

        # Ejecutar transacción
        exito = execute_transaction(operations)

        if exito:
            logger.info(f"Eliminación exitosa de {len(alumnos)} alumnos")
            return alumnos
        else:
            error = "Error al eliminar los alumnos, transacción revertida"
            logger.error(error)
            raise Exception(error)

    def to_dict(self):
        """
        Convierte el objeto Alumno a diccionario

        Returns:
            Diccionario con los datos del alumno
        """
        return {
            'id': self.id,
            'matricula': self.matricula,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None
        }

    def __repr__(self):
        return f"Alumno(id={self.id}, matricula='{self.matricula}', nombre='{self.nombre}', apellido='{self.apellido}')"
