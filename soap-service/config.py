"""
Configuración del servicio SOAP - Gestión de Alumnos
Universidad Autónoma Veracruzana
"""

import os

class Config:
    """Configuración de la aplicación"""

    # Configuración del servidor
    HOST = '0.0.0.0'
    PORT = 5001
    DEBUG = True

    # Configuración de MySQL Railway (misma BD que el servicio REST)
    DB_CONFIG = {
        'host': 'trolley.proxy.rlwy.net',
        'port': 34558,
        'user': 'root',
        'password': 'jMLMOhCURJQHHQmPclBxQahvwOjMMkTu',
        'database': 'railway',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci',
        'autocommit': False,  # Para manejar transacciones manualmente
        'raise_on_warnings': True
    }

    # Configuración SOAP
    SOAP_NAMESPACE = 'http://uav.edu.mx/alumnos'
    SOAP_SERVICE_NAME = 'AlumnoService'

    # CORS - Permitir peticiones desde el frontend
    CORS_ORIGINS = ['http://localhost:3000']

    # Validaciones
    MATRICULA_MIN_LENGTH = 6
    MATRICULA_MAX_LENGTH = 20
    NOMBRE_MIN_LENGTH = 2
    NOMBRE_MAX_LENGTH = 100
    MIN_ALUMNOS_ELIMINAR = 2

    # Logging
    LOG_LEVEL = 'INFO'
