from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
import psutil
from device_manager import DeviceManager
from cloud_client import CloudClient

# Configurar logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

# Inicializar componentes
device_manager = DeviceManager()
cloud_client = CloudClient()

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'POS Device Connector API',
        'version': '1.0.0',
        'environment': os.getenv('FLASK_ENV', 'development')
    })

@app.route('/health')
def health():
    """Health check para Dockploy y monitoreo"""
    try:
        # Verificar uso de recursos
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Verificar conexión con dispositivos
        printers_count = len(device_manager.get_printers())
        
        health_data = {
            'status': 'healthy',
            'timestamp': psutil.boot_time(),
            'resources': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': disk.percent,
                'available_memory_gb': memory.available / (1024**3)
            },
            'devices': {
                'printers_available': printers_count
            },
            'cloud_connection': cloud_client.connected
        }
        
        # Determinar estado basado en recursos
        if cpu_percent > 90 or memory.percent > 90:
            health_data['status'] = 'warning'
            return jsonify(health_data), 200
        
        return jsonify(health_data), 200
        
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503

@app.route('/metrics')
def metrics():
    """Métricas para monitoreo"""
    try:
        if not os.getenv('ENABLE_METRICS', 'false').lower() == 'true':
            return jsonify({'error': 'Metrics disabled'}), 404
        
        # Métricas Prometheus-style
        metrics_data = {
            'pos_device_connector_info': {
                'version': '1.0.0',
                'uptime': psutil.boot_time()
            },
            'pos_device_connector_resources': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent
            },
            'pos_device_connector_devices': {
                'printers_total': len(device_manager.get_printers()),
                'scales_total': len(device_manager.get_scales())
            },
            'pos_device_connector_requests': {
                'total': 0,  # Implementar contador si es necesario
                'errors': 0
            }
        }
        
        return jsonify(metrics_data), 200
        
    except Exception as e:
        logging.error(f"Metrics failed: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/devices/printers', methods=['GET'])
def get_printers():
    """Obtener lista de impresoras disponibles"""
    try:
        printers = device_manager.get_printers()
        return jsonify({
            'success': True,
            'printers': printers,
            'count': len(printers)
        })
    except Exception as e:
        logging.error(f"Error getting printers: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/devices/scales', methods=['GET'])
def get_scales():
    """Obtener lista de básculas disponibles"""
    try:
        scales = device_manager.get_scales()
        return jsonify({
            'success': True,
            'scales': scales,
            'count': len(scales)
        })
    except Exception as e:
        logging.error(f"Error getting scales: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/print', methods=['POST'])
def print_ticket():
    """Imprimir ticket en impresora específica"""
    try:
        data = request.json
        printer_name = data.get('printer_name')
        content = data.get('content')
        
        if not printer_name or not content:
            return jsonify({
                'success': False,
                'error': 'Se requiere printer_name y content'
            }), 400
        
        result = device_manager.print_ticket(printer_name, content)
        
        # Enviar confirmación al POS en la nube
        if cloud_client.connected:
            cloud_client.notify_print_completed(result)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        logging.error(f"Error printing ticket: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/scale/read', methods=['POST'])
def read_scale():
    """Leer peso de báscula específica"""
    try:
        data = request.json
        scale_port = data.get('scale_port')
        
        if not scale_port:
            return jsonify({
                'success': False,
                'error': 'Se requiere scale_port'
            }), 400
        
        weight = device_manager.read_scale(scale_port)
        
        # Enviar lectura al POS en la nube
        if cloud_client.connected:
            cloud_client.send_weight_reading(weight)
        
        return jsonify({
            'success': True,
            'weight': weight
        })
    except Exception as e:
        logging.error(f"Error reading scale: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/cloud/connect', methods=['POST'])
def connect_to_cloud():
    """Conectar con sistema POS en la nube"""
    try:
        data = request.json
        cloud_url = data.get('cloud_url') or os.getenv('CLOUD_URL')
        api_key = data.get('api_key') or os.getenv('API_KEY')
        
        if not cloud_url or not api_key:
            return jsonify({
                'success': False,
                'error': 'Se requiere cloud_url y api_key'
            }), 400
        
        result = cloud_client.connect(cloud_url, api_key)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        logging.error(f"Error connecting to cloud: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/cloud/status', methods=['GET'])
def cloud_status():
    """Verificar estado de conexión con nube"""
    return jsonify({
        'connected': cloud_client.connected,
        'cloud_url': cloud_client.cloud_url,
        'last_connection': getattr(cloud_client, 'last_connection', None)
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    
    if os.getenv('FLASK_ENV') == 'production':
        # En producción, Gunicorn se encargará de servir
        app.run(host='0.0.0.0', port=port, debug=debug)
    else:
        # En desarrollo, Flask directamente
        app.run(host='0.0.0.0', port=port, debug=debug)