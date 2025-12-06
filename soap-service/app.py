"""
Aplicación principal del servicio SOAP
Universidad Autónoma Veracruzana - Gestión de Alumnos
"""

import logging
from flask import Flask
from flask_cors import CORS
from spyne.server.wsgi import WsgiApplication
from soap_service import soap_app
from database import init_connection_pool, check_connection
from config import Config

# Configurar logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)

# Habilitar CORS para permitir peticiones desde el frontend
CORS(app, resources={
    r"/soap*": {"origins": Config.CORS_ORIGINS}
})

# Crear aplicación WSGI de Spyne
wsgi_app = WsgiApplication(soap_app)

# Ruta para el servicio SOAP
@app.route('/soap', methods=['POST', 'GET'])
def soap_service():
    """
    Endpoint del servicio SOAP
    GET: Devuelve el WSDL
    POST: Procesa peticiones SOAP
    """
    return wsgi_app

# Ruta de salud del servicio
@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servicio"""
    try:
        db_status = check_connection()
        if db_status:
            return {
                'status': 'healthy',
                'service': 'SOAP Alumnos Service',
                'database': 'connected',
                'port': Config.PORT
            }, 200
        else:
            return {
                'status': 'unhealthy',
                'service': 'SOAP Alumnos Service',
                'database': 'disconnected',
                'port': Config.PORT
            }, 503
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            'status': 'error',
            'message': str(e)
        }, 500

# Ruta principal
@app.route('/', methods=['GET'])
def index():
    """Página de información del servicio"""
    return {
        'service': 'SOAP Alumnos Service',
        'version': '1.0',
        'universidad': 'Universidad Autónoma Veracruzana',
        'endpoints': {
            'soap': '/soap',
            'wsdl': '/soap?wsdl',
            'health': '/health'
        },
        'operaciones': [
            'registrarAlumno(matricula, nombre, apellido, email)',
            'consultarAlumnoPorMatricula(matricula)',
            'eliminarAlumnos(lista_matriculas)'
        ]
    }, 200

def main():
    """Función principal para iniciar el servicio"""
    logger.info("=" * 60)
    logger.info("Iniciando servicio SOAP - Gestión de Alumnos")
    logger.info("Universidad Autónoma Veracruzana")
    logger.info("=" * 60)

    # Inicializar pool de conexiones
    logger.info("Inicializando conexión a base de datos...")
    if init_connection_pool():
        logger.info("✓ Conexión a base de datos establecida")
    else:
        logger.error("✗ Error al conectar con la base de datos")
        logger.error("Verifica la configuración en config.py")
        return

    # Verificar conexión
    if check_connection():
        logger.info("✓ Verificación de conexión exitosa")
    else:
        logger.error("✗ Error al verificar la conexión")
        return

    # Información del servicio
    logger.info(f"Puerto: {Config.PORT}")
    logger.info(f"Namespace: {Config.SOAP_NAMESPACE}")
    logger.info(f"WSDL disponible en: http://localhost:{Config.PORT}/soap?wsdl")
    logger.info(f"Endpoint SOAP: http://localhost:{Config.PORT}/soap")
    logger.info(f"Health check: http://localhost:{Config.PORT}/health")

    logger.info("=" * 60)
    logger.info("Servicio SOAP iniciado correctamente")
    logger.info("Presiona Ctrl+C para detener el servicio")
    logger.info("=" * 60)

    # Iniciar servidor Flask
    try:
        app.run(
            host=Config.HOST,
            port=Config.PORT,
            debug=Config.DEBUG
        )
    except KeyboardInterrupt:
        logger.info("\nDeteniendo servicio SOAP...")
    except Exception as e:
        logger.error(f"Error al iniciar el servidor: {e}")

if __name__ == '__main__':
    main()
