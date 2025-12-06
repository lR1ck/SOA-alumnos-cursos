"""
Módulo de gestión de base de datos
Manejo de conexiones y transacciones con MySQL
"""

import mysql.connector
from mysql.connector import Error, pooling
import logging
from config import Config

# Configurar logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Pool de conexiones
connection_pool = None

def init_connection_pool():
    """Inicializa el pool de conexiones a MySQL"""
    global connection_pool

    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="soap_pool",
            pool_size=5,
            pool_reset_session=True,
            **Config.DB_CONFIG
        )
        logger.info("Pool de conexiones MySQL inicializado correctamente")
        return True
    except Error as e:
        logger.error(f"Error al crear pool de conexiones: {e}")
        return False

def get_connection():
    """
    Obtiene una conexión del pool

    Returns:
        Connection o None si hay error
    """
    global connection_pool

    if connection_pool is None:
        init_connection_pool()

    try:
        connection = connection_pool.get_connection()
        return connection
    except Error as e:
        logger.error(f"Error al obtener conexión del pool: {e}")
        return None

def execute_query(query, params=None, fetch=True):
    """
    Ejecuta una consulta SELECT

    Args:
        query: Consulta SQL
        params: Parámetros de la consulta
        fetch: Si es True, devuelve resultados; si es False, solo ejecuta

    Returns:
        Lista de resultados o None si hay error
    """
    connection = get_connection()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())

        if fetch:
            results = cursor.fetchall()
            logger.debug(f"Consulta ejecutada: {cursor.rowcount} filas obtenidas")
            return results
        else:
            connection.commit()
            logger.debug(f"Consulta ejecutada: {cursor.rowcount} filas afectadas")
            return cursor.rowcount

    except Error as e:
        logger.error(f"Error ejecutando consulta: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def execute_insert(query, params=None):
    """
    Ejecuta una consulta INSERT

    Args:
        query: Consulta SQL INSERT
        params: Parámetros de la consulta

    Returns:
        ID del registro insertado o None si hay error
    """
    connection = get_connection()
    if not connection:
        return None

    cursor = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()

        last_id = cursor.lastrowid
        logger.info(f"Registro insertado con ID: {last_id}")
        return last_id

    except Error as e:
        connection.rollback()
        logger.error(f"Error ejecutando INSERT: {e}")
        logger.error(f"Query: {query}")
        logger.error(f"Params: {params}")
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def execute_transaction(operations):
    """
    Ejecuta múltiples operaciones en una transacción

    Args:
        operations: Lista de tuplas (query, params)

    Returns:
        True si todas las operaciones se ejecutaron correctamente, False si hubo error
    """
    connection = get_connection()
    if not connection:
        return False

    cursor = None
    try:
        cursor = connection.cursor()

        # Ejecutar todas las operaciones
        for query, params in operations:
            cursor.execute(query, params or ())
            logger.debug(f"Operación ejecutada: {cursor.rowcount} filas afectadas")

        # Confirmar transacción
        connection.commit()
        logger.info(f"Transacción completada exitosamente: {len(operations)} operaciones")
        return True

    except Error as e:
        # Revertir en caso de error
        connection.rollback()
        logger.error(f"Error en transacción, rollback ejecutado: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def check_connection():
    """
    Verifica la conexión a la base de datos

    Returns:
        True si la conexión es exitosa, False en caso contrario
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            logger.info("Conexión a base de datos verificada correctamente")
            return True
        except Error as e:
            logger.error(f"Error verificando conexión: {e}")
            return False
    return False
