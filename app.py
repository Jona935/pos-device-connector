from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
from device_manager import DeviceManager
from cloud_client import CloudClient

app = Flask(__name__)
CORS(app)

device_manager = DeviceManager()
cloud_client = CloudClient()

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'POS Device Connector API',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Health check básico"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time()
    })

@app.route('/devices/printers', methods=['GET'])
def get_printers():
    """Obtener lista de impresoras disponibles"""
    try:
        printers = device_manager.get_printers()
        return jsonify({
            'success': True,
            'printers': printers
        })
    except Exception as e:
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
            'scales': scales
        })
    except Exception as e:
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
        cloud_client.notify_print_completed(result)
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
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
        
        return jsonify({
            'success': True,
            'weight': weight
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/cloud/connect', methods=['POST'])
def connect_to_cloud():
    """Conectar con sistema POS en la nube"""
    try:
        data = request.json
        cloud_url = data.get('cloud_url')
        api_key = data.get('api_key')
        
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)